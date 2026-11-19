param(
    [Parameter(Mandatory=$true)][ValidateSet('chatgpt','claude')][string]$App,
    [string]$Text = 'TEST-CLICK-PASTE-20261119'
)
$ErrorActionPreference='Stop'
[Console]::OutputEncoding=[System.Text.Encoding]::UTF8
Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes
Add-Type -AssemblyName System.Windows.Forms
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class M {
  [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr hWnd);
  [DllImport("user32.dll")] public static extern bool BringWindowToTop(IntPtr hWnd);
  [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
  [DllImport("user32.dll")] public static extern void keybd_event(byte bVk, byte bScan, uint dwFlags, UIntPtr dwExtraInfo);
  [DllImport("user32.dll")] public static extern bool SetCursorPos(int X, int Y);
  [DllImport("user32.dll")] public static extern void mouse_event(uint dwFlags, uint dx, uint dy, uint dwData, UIntPtr dwExtraInfo);
}
"@
$AE=[System.Windows.Automation.AutomationElement]
$TS=[System.Windows.Automation.TreeScope]
function Get-AppWindow([string]$app){
    $procName=if($app -eq 'chatgpt'){'ChatGPT'}else{'claude'}
    $winTitle=if($app -eq 'chatgpt'){'ChatGPT'}else{'Claude'}
    $root=$AE::RootElement
    $kids=$root.FindAll($TS::Children,[System.Windows.Automation.Condition]::TrueCondition)
    foreach($k in $kids){ if($k.Current.Name -ne $winTitle){continue}; $p=Get-Process -Id $k.Current.ProcessId -ErrorAction SilentlyContinue; if($p -and $p.ProcessName -eq $procName){return $k} }
    return $null
}
$win=Get-AppWindow $App
if(-not $win){Write-Output "ERROR: no window";exit 3}
$hwnd=[IntPtr]$win.Current.NativeWindowHandle
[M]::ShowWindow($hwnd,9)|Out-Null
[M]::keybd_event(0x12,0,0,[UIntPtr]::Zero); [M]::keybd_event(0x12,0,2,[UIntPtr]::Zero)
Start-Sleep -Milliseconds 120
[M]::BringWindowToTop($hwnd)|Out-Null
[M]::SetForegroundWindow($hwnd)|Out-Null
Start-Sleep -Milliseconds 700
Write-Output ("FOCUS: " + ([M]::GetForegroundWindow() -eq $hwnd))

$c=New-Object System.Windows.Automation.PropertyCondition($AE::ControlTypeProperty,[System.Windows.Automation.ControlType]::Edit)
$edits=$win.FindAll($TS::Descendants,$c)
$composer=$null
foreach($e in $edits){ if(-not $e.Current.IsOffscreen){$composer=$e} }
if(-not $composer){Write-Output "ERROR: no composer";exit 6}
$r=$composer.Current.BoundingRectangle
Write-Output ("composer rect: " + $r.X + "," + $r.Y + " " + $r.Width + "x" + $r.Height)
$cx=[int]($r.X + $r.Width/2); $cy=[int]($r.Y + $r.Height/2)
[M]::SetCursorPos($cx,$cy)|Out-Null
Start-Sleep -Milliseconds 300
[M]::mouse_event(0x0002,0,0,0,[UIntPtr]::Zero)  # left down
Start-Sleep -Milliseconds 80
[M]::mouse_event(0x0004,0,0,0,[UIntPtr]::Zero)  # left up
Start-Sleep -Milliseconds 600
Write-Output "CLICK: da click vao o soan"

$composer.SetFocus()
Start-Sleep -Milliseconds 300

Set-Clipboard -Value $Text
Start-Sleep -Milliseconds 400
[System.Windows.Forms.SendKeys]::SendWait('^v')
Start-Sleep -Milliseconds 1200

$vp=$composer.GetCurrentPattern([System.Windows.Automation.ValuePattern]::Pattern)
Write-Output ("O SOAN: '" + $vp.Current.Value + "'")

$bc=New-Object System.Windows.Automation.PropertyCondition($AE::ControlTypeProperty,[System.Windows.Automation.ControlType]::Button)
$btns=$win.FindAll($TS::Descendants,$bc)
foreach($b in $btns){ $n=$b.Current.Name; if($b.Current.IsOffscreen){continue}; if($n -match '^Gửi'){ Write-Output ("NUT: '" + $n + "' enabled=" + $b.Current.IsEnabled) } }
