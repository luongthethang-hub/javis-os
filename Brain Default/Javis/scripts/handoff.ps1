param(
    [Parameter(Mandatory=$true)][ValidateSet('chatgpt','claude')][string]$App,
    [string]$Text = '',
    [string]$PromptFile = '',
    [int]$WaitSeconds = 180,
    [int]$X = 60,
    [int]$Y = 40,
    [switch]$NoSend
)
$ErrorActionPreference='Stop'
[Console]::OutputEncoding=[System.Text.Encoding]::UTF8
Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes
Add-Type -AssemblyName System.Windows.Forms
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class HV2 {
  [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr hWnd);
  [DllImport("user32.dll")] public static extern bool BringWindowToTop(IntPtr hWnd);
  [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
  [DllImport("user32.dll")] public static extern bool MoveWindow(IntPtr hWnd, int X, int Y, int nWidth, int nHeight, bool bRepaint);
  [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr hWnd, out RECT lpRect);
  [DllImport("user32.dll")] public static extern void keybd_event(byte bVk, byte bScan, uint dwFlags, UIntPtr dwExtraInfo);
  [DllImport("user32.dll")] public static extern bool SetCursorPos(int X, int Y);
  [DllImport("user32.dll")] public static extern void mouse_event(uint dwFlags, uint dx, uint dy, uint dwData, UIntPtr dwExtraInfo);
  [StructLayout(LayoutKind.Sequential)] public struct RECT { public int Left; public int Top; public int Right; public int Bottom; }
}
"@
$AE=[System.Windows.Automation.AutomationElement]
$TS=[System.Windows.Automation.TreeScope]

function Find-Win([string]$app){
    $procName=if($app -eq 'chatgpt'){'ChatGPT'}else{'claude'}
    $winTitle=if($app -eq 'chatgpt'){'ChatGPT'}else{'Claude'}
    foreach($k in $AE::RootElement.FindAll($TS::Children,[System.Windows.Automation.Condition]::TrueCondition)){
        if($k.Current.Name -ne $winTitle){continue}
        $p=Get-Process -Id $k.Current.ProcessId -ErrorAction SilentlyContinue
        if($p -and $p.ProcessName -eq $procName){return $k}
    }
    return $null
}
function Get-Composer($win){
    $c=New-Object System.Windows.Automation.PropertyCondition($AE::ControlTypeProperty,[System.Windows.Automation.ControlType]::Edit)
    $best=$null
    foreach($e in $win.FindAll($TS::Descendants,$c)){ if(-not $e.Current.IsOffscreen){$best=$e} }
    return $best
}
function Get-SendButton($win){
    $c=New-Object System.Windows.Automation.PropertyCondition($AE::ControlTypeProperty,[System.Windows.Automation.ControlType]::Button)
    foreach($b in $win.FindAll($TS::Descendants,$c)){
        if($b.Current.IsOffscreen){continue}
        $n=$b.Current.Name
        if($n -eq 'Gửi' -or $n -eq 'Gửi tin nhắn' -or $n -eq 'Send'){return $b}
    }
    return $null
}
function Get-Transcript($win){
    $c=New-Object System.Windows.Automation.PropertyCondition($AE::ControlTypeProperty,[System.Windows.Automation.ControlType]::Document)
    $best='';$bestLen=-1
    foreach($d in $win.FindAll($TS::Descendants,$c)){
        try{
            $tp=$d.GetCurrentPattern([System.Windows.Automation.TextPattern]::Pattern)
            $t=$tp.DocumentRange.GetText(-1)
            if($t.Length -gt $bestLen){$bestLen=$t.Length;$best=$t}
        }catch{}
    }
    return $best
}
function Click-At([int]$x,[int]$y){
    [HV2]::SetCursorPos($x,$y)|Out-Null
    Start-Sleep -Milliseconds 250
    [HV2]::mouse_event(0x0002,0,0,0,[UIntPtr]::Zero)
    Start-Sleep -Milliseconds 90
    [HV2]::mouse_event(0x0004,0,0,0,[UIntPtr]::Zero)
    Start-Sleep -Milliseconds 400
}

$win=Find-Win $App
if(-not $win){ Write-Output "ERROR: khong tim thay cua so $App"; exit 3 }
$hwnd=[IntPtr]$win.Current.NativeWindowHandle

$rect=New-Object HV2+RECT
[HV2]::GetWindowRect($hwnd,[ref]$rect)|Out-Null
if($rect.Left -lt 0 -or $rect.Top -lt 0 -or $rect.Right -gt 1920 -or $rect.Bottom -gt 1080){
    [HV2]::MoveWindow($hwnd,$X,$Y,1180,900,$true)|Out-Null
    Start-Sleep -Milliseconds 900
    Write-Output ("CHUYEN CUA SO VE " + $X + "," + $Y)
}
[HV2]::ShowWindow($hwnd,9)|Out-Null
[HV2]::keybd_event(0x12,0,0,[UIntPtr]::Zero); [HV2]::keybd_event(0x12,0,2,[UIntPtr]::Zero)
Start-Sleep -Milliseconds 150
[HV2]::BringWindowToTop($hwnd)|Out-Null
[HV2]::SetForegroundWindow($hwnd)|Out-Null
Start-Sleep -Milliseconds 800
if([HV2]::GetForegroundWindow() -ne $hwnd){ Write-Output "ERROR: khong dua duoc cua so len truoc mat"; exit 4 }
Write-Output "FOCUS: ok ($App)"

$body=$Text
if($PromptFile -ne '' -and (Test-Path $PromptFile)){ $body=[System.IO.File]::ReadAllText($PromptFile) }
if([string]::IsNullOrWhiteSpace($body)){ Write-Output "ERROR: khong co noi dung"; exit 5 }
$body=$body.Trim()

$composer=Get-Composer $win
if(-not $composer){ Write-Output "ERROR: khong thay o soan"; exit 6 }
$cr=$composer.Current.BoundingRectangle
$cx=[int]($cr.X + 60)
$cy=[int]($cr.Y + $cr.Height/2)

$vp=$composer.GetCurrentPattern([System.Windows.Automation.ValuePattern]::Pattern)
$norm = { param($s) if($null -eq $s){return ''} return ($s -replace '\s+','') }
$bodyNorm = & $norm $body
$done=$false
for($attempt=1; $attempt -le 3; $attempt++){
    Click-At $cx $cy
    $composer.SetFocus()
    Start-Sleep -Milliseconds 350
    [System.Windows.Forms.SendKeys]::SendWait('^a')
    Start-Sleep -Milliseconds 250
    Set-Clipboard -Value $body
    Start-Sleep -Milliseconds 250
    [System.Windows.Forms.SendKeys]::SendWait('^v')
    Start-Sleep -Milliseconds 1800
    $now=& $norm $vp.Current.Value
    Write-Output ("  lan " + $attempt + ": o soan " + $now.Length + "/" + $bodyNorm.Length)
    if($now -eq $bodyNorm){ $done=$true; break }
}
if(-not $done){
    $vp.SetValue($body)
    Start-Sleep -Milliseconds 1000
    $composer.SetFocus()
    Start-Sleep -Milliseconds 200
    [System.Windows.Forms.SendKeys]::SendWait(' ')
    Start-Sleep -Milliseconds 150
    [System.Windows.Forms.SendKeys]::SendWait('{BACKSPACE}')
    Start-Sleep -Milliseconds 700
    if((& $norm $vp.Current.Value) -eq $bodyNorm){ $done=$true; Write-Output "  dat bang SetValue + phim" }
}
if(-not $done){
    # mot so o soan tu dinh dang lai (danh so, xuong dong) nen so ky tu lech vai chuc;
    # chap nhan khi >=95% va duoi noi dung khop, de khong gui lan voi noi dung cu
    $nowNorm=& $norm $vp.Current.Value
    $tailLen=[Math]::Min(40,$bodyNorm.Length)
    $tail=$bodyNorm.Substring($bodyNorm.Length-$tailLen)
    if($nowNorm.Length -ge [int]($bodyNorm.Length*0.95) -and $nowNorm.EndsWith($tail)){
        $done=$true
        Write-Output ("  chap nhan: o soan " + $nowNorm.Length + "/" + $bodyNorm.Length + " (dinh dang lai)")
    }
}
if(-not $done){ Write-Output ("ERROR: khong dat duoc noi dung, o soan hien tai: '" + $vp.Current.Value.Trim() + "'"); exit 7 }

$before=Get-Transcript $win
Write-Output ("TRANSCRIPT TRUOC: " + $before.Length)

if($NoSend){ Write-Output "STOP: da dat noi dung, khong gui"; exit 0 }

$sent=$false
for($t=1; $t -le 8; $t++){
    $btn=Get-SendButton $win
    if($btn -and $btn.Current.IsEnabled){
        try{
            $btn.GetCurrentPattern([System.Windows.Automation.InvokePattern]::Pattern).Invoke()
            $sent=$true; Write-Output "GUI: bam nut Gui"; break
        }catch{}
    }
    Start-Sleep -Milliseconds 500
}
if(-not $sent){
    # thu bam chuot that vao nut Gui
    $btn=Get-SendButton $win
    if($btn){
        $br=$btn.Current.BoundingRectangle
        $bx=[int]($br.X + $br.Width/2); $by=[int]($br.Y + $br.Height/2)
        Click-At $bx $by
        Write-Output ("GUI: bam chuot vao nut tai " + $bx + "," + $by)
        Start-Sleep -Milliseconds 2500
        if($vp.Current.Value.Trim().Length -lt 5){ $sent=$true }
    }
}
if(-not $sent){
    $composer.SetFocus()
    Start-Sleep -Milliseconds 300
    [System.Windows.Forms.SendKeys]::SendWait('{ENTER}')
    Write-Output "GUI: bang Enter"
}
Start-Sleep -Milliseconds 2500
$left=$vp.Current.Value.Trim()
if($left.Length -ge 5){
    Write-Output ("CANH BAO: o soan con " + $left.Length + " ky tu, thu Enter lan 2")
    $composer.SetFocus()
    Start-Sleep -Milliseconds 300
    [System.Windows.Forms.SendKeys]::SendWait('{ENTER}')
    Start-Sleep -Milliseconds 3000
    $left=$vp.Current.Value.Trim()
}
if($left.Length -ge 5){ Write-Output ("ERROR: tin nhan chua gui duoc, o soan con '" + $left + "'"); exit 10 }
Write-Output "GUI: da gui (o soan da trong)"

$deadline=(Get-Date).AddSeconds($WaitSeconds)
$lastLen=-1;$stable=0
while((Get-Date) -lt $deadline){
    Start-Sleep -Seconds 6
    $now=Get-Transcript $win
    if($now.Length -eq $lastLen){$stable++}else{$stable=0;$lastLen=$now.Length}
    Write-Output ("  ... " + $now.Length + " ky tu (on dinh=" + $stable + ")")
    if($stable -ge 3 -and $now.Length -gt ($before.Length+30)){break}
}
$final=Get-Transcript $win
$key=$body; if($key.Length -gt 40){$key=$key.Substring(0,40)}
$idx=$final.LastIndexOf($key)
if($idx -ge 0){ $answer=$final.Substring($idx+$key.Length) } else { $answer=$final.Substring($before.Length) }
$answer=$answer.Trim()
if($answer.Length -gt 9000){$answer=$answer.Substring($answer.Length-9000)}
$outFile=Join-Path $PSScriptRoot ("handoff-$App-last.txt")
[System.IO.File]::WriteAllText($outFile,$answer,(New-Object System.Text.UTF8Encoding($false)))
Write-Output "----- TRA LOI ($App) -----"
Write-Output $answer
Write-Output "----- HET -----"
