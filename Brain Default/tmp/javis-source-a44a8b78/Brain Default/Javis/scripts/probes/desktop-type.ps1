param([ValidateSet('chatgpt','claude')][string]$App='chatgpt',[string]$Text='abc')
$ErrorActionPreference='Stop'
[Console]::OutputEncoding=[System.Text.Encoding]::UTF8
Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes
Add-Type -AssemblyName System.Windows.Forms
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class T10 {
  [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr hWnd);
  [DllImport("user32.dll")] public static extern bool BringWindowToTop(IntPtr hWnd);
  [DllImport("user32.dll")] public static extern void keybd_event(byte bVk, byte bScan, uint dwFlags, UIntPtr dwExtraInfo);
  [DllImport("user32.dll")] public static extern bool SetCursorPos(int X, int Y);
  [DllImport("user32.dll")] public static extern void mouse_event(uint dwFlags, uint dx, uint dy, uint dwData, UIntPtr dwExtraInfo);
}
"@
$AE=[System.Windows.Automation.AutomationElement]
$TS=[System.Windows.Automation.TreeScope]
$procName=if($App -eq 'chatgpt'){'ChatGPT'}else{'claude'}
$winTitle=if($App -eq 'chatgpt'){'ChatGPT'}else{'Claude'}
$win=$null
foreach($k in $AE::RootElement.FindAll($TS::Children,[System.Windows.Automation.Condition]::TrueCondition)){
  if($k.Current.Name -ne $winTitle){continue}
  $p=Get-Process -Id $k.Current.ProcessId -ErrorAction SilentlyContinue
  if($p -and $p.ProcessName -eq $procName){$win=$k;break}
}
if(-not $win){Write-Output "ERROR: no window";exit 3}
$hwnd=[IntPtr]$win.Current.NativeWindowHandle
[T10]::keybd_event(0x12,0,0,[UIntPtr]::Zero); [T10]::keybd_event(0x12,0,2,[UIntPtr]::Zero)
Start-Sleep -Milliseconds 150
[T10]::BringWindowToTop($hwnd)|Out-Null
[T10]::SetForegroundWindow($hwnd)|Out-Null
Start-Sleep -Milliseconds 700
Write-Output ("FOCUS: " + ([T10]::GetForegroundWindow() -eq $hwnd))

$c=New-Object System.Windows.Automation.PropertyCondition($AE::ControlTypeProperty,[System.Windows.Automation.ControlType]::Edit)
$composer=$null
foreach($e in $win.FindAll($TS::Descendants,$c)){ if(-not $e.Current.IsOffscreen){$composer=$e} }
$r=$composer.Current.BoundingRectangle
$cx=[int]($r.X+60); $cy=[int]($r.Y+$r.Height/2)
[T10]::SetCursorPos($cx,$cy)|Out-Null
Start-Sleep -Milliseconds 250
[T10]::mouse_event(0x0002,0,0,0,[UIntPtr]::Zero); Start-Sleep -Milliseconds 90; [T10]::mouse_event(0x0004,0,0,0,[UIntPtr]::Zero)
Start-Sleep -Milliseconds 500
$composer.SetFocus()
Start-Sleep -Milliseconds 300
$vp=$composer.GetCurrentPattern([System.Windows.Automation.ValuePattern]::Pattern)
$vp.SetValue('')
Start-Sleep -Milliseconds 600
Write-Output ("SAU CLEAR: '" + $vp.Current.Value + "'")

$sw=[System.Diagnostics.Stopwatch]::StartNew()
[System.Windows.Forms.SendKeys]::SendWait($Text)
$sw.Stop()
Start-Sleep -Milliseconds 1200
Write-Output ("GO PHIM (" + $sw.ElapsedMilliseconds + "ms): '" + $vp.Current.Value + "'")

$bc=New-Object System.Windows.Automation.PropertyCondition($AE::ControlTypeProperty,[System.Windows.Automation.ControlType]::Button)
foreach($b in $win.FindAll($TS::Descendants,$bc)){
  if($b.Current.IsOffscreen){continue}
  $n=$b.Current.Name
  if($n -match '^Gửi' -or $n -match '^Send' -or $n -match 'Dừng'){ Write-Output ("NUT '" + $n + "' enabled=" + $b.Current.IsEnabled) }
}
