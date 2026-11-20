param(
    [Parameter(Mandatory=$true)][ValidateSet('chatgpt','claude')][string]$App,
    [string]$Text = 'TEST'
)
$ErrorActionPreference='Stop'
[Console]::OutputEncoding=[System.Text.Encoding]::UTF8
Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes
Add-Type -AssemblyName System.Windows.Forms
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class MK {
  [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr hWnd);
  [DllImport("user32.dll")] public static extern bool BringWindowToTop(IntPtr hWnd);
  [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
  [DllImport("user32.dll")] public static extern void keybd_event(byte bVk, byte bScan, uint dwFlags, UIntPtr dwExtraInfo);
  [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr hWnd, out RECT lpRect);
  [StructLayout(LayoutKind.Sequential)] public struct RECT { public int Left; public int Top; public int Right; public int Bottom; }
}
"@
$AE=[System.Windows.Automation.AutomationElement]
$TS=[System.Windows.Automation.TreeScope]
function Find-Win([string]$app){
    $procName=if($app -eq 'chatgpt'){'ChatGPT'}else{'claude'}
    $winTitle=if($app -eq 'chatgpt'){'ChatGPT'}else{'Claude'}
    $root=$AE::RootElement
    foreach($k in $root.FindAll($TS::Children,[System.Windows.Automation.Condition]::TrueCondition)){
        if($k.Current.Name -ne $winTitle){continue}
        $p=Get-Process -Id $k.Current.ProcessId -ErrorAction SilentlyContinue
        if($p -and $p.ProcessName -eq $procName){return $k}
    }
    return $null
}
$win=Find-Win $App
if(-not $win){Write-Output "ERROR: no window";exit 3}
$hwnd=[IntPtr]$win.Current.NativeWindowHandle
$rect=New-Object MK+RECT
[MK]::GetWindowRect($hwnd,[ref]$rect)|Out-Null
Write-Output ("WIN RECT: L=" + $rect.Left + " T=" + $rect.Top + " R=" + $rect.Right + " B=" + $rect.Bottom)

if($rect.Left -lt -100 -or $rect.Top -lt -100){ Write-Output "GHI CHU: cua so dang nam lech ngoai man hinh, se dua ve 0,0"; }

[MK]::ShowWindow($hwnd,9)|Out-Null
[MK]::keybd_event(0x12,0,0,[UIntPtr]::Zero); [MK]::keybd_event(0x12,0,2,[UIntPtr]::Zero)
Start-Sleep -Milliseconds 150
[MK]::BringWindowToTop($hwnd)|Out-Null
[MK]::SetForegroundWindow($hwnd)|Out-Null
Start-Sleep -Milliseconds 800
Write-Output ("FOCUS ok: " + ([MK]::GetForegroundWindow() -eq $hwnd))

$c=New-Object System.Windows.Automation.PropertyCondition($AE::ControlTypeProperty,[System.Windows.Automation.ControlType]::Edit)
$composer=$null
foreach($e in $win.FindAll($TS::Descendants,$c)){ if(-not $e.Current.IsOffscreen){$composer=$e} }
if(-not $composer){Write-Output "ERROR: no composer";exit 6}

$composer.SetFocus()
Start-Sleep -Milliseconds 400
[System.Windows.Forms.SendKeys]::SendWait('^a')
Start-Sleep -Milliseconds 200
[System.Windows.Forms.SendKeys]::SendWait('{DEL}')
Start-Sleep -Milliseconds 400
$vp=$composer.GetCurrentPattern([System.Windows.Automation.ValuePattern]::Pattern)
Write-Output ("SAU XOA: '" + $vp.Current.Value + "'")

Set-Clipboard -Value $Text
Start-Sleep -Milliseconds 400
[System.Windows.Forms.SendKeys]::SendWait('^v')
Start-Sleep -Milliseconds 1500
Write-Output ("SAU DAN: '" + $vp.Current.Value + "'")

$bc=New-Object System.Windows.Automation.PropertyCondition($AE::ControlTypeProperty,[System.Windows.Automation.ControlType]::Button)
foreach($b in $win.FindAll($TS::Descendants,$bc)){
    if($b.Current.IsOffscreen){continue}
    $n=$b.Current.Name
    if($n -match '^Gửi'){ Write-Output ("NUT: '" + $n + "' enabled=" + $b.Current.IsEnabled) }
}
