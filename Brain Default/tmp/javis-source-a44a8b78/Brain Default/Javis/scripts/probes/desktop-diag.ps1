param([ValidateSet('chatgpt','claude')][string]$App='chatgpt',[string]$Text='hi')
$ErrorActionPreference='Stop'
[Console]::OutputEncoding=[System.Text.Encoding]::UTF8
Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes
Add-Type -AssemblyName System.Windows.Forms
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class D1 {
  [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr hWnd);
  [DllImport("user32.dll")] public static extern bool BringWindowToTop(IntPtr hWnd);
  [DllImport("user32.dll")] public static extern void keybd_event(byte bVk, byte bScan, uint dwFlags, UIntPtr dwExtraInfo);
  [DllImport("user32.dll")] public static extern bool SetCursorPos(int X, int Y);
  [DllImport("user32.dll")] public static extern void mouse_event(uint dwFlags, uint dx, uint dy, uint dwData, UIntPtr dwExtraInfo);
  [DllImport("user32.dll")] public static extern bool MoveWindow(IntPtr hWnd, int X, int Y, int nWidth, int nHeight, bool bRepaint);
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
[D1]::MoveWindow($hwnd,80,60,1150,880,$true)|Out-Null
Start-Sleep -Milliseconds 800
[D1]::keybd_event(0x12,0,0,[UIntPtr]::Zero); [D1]::keybd_event(0x12,0,2,[UIntPtr]::Zero)
Start-Sleep -Milliseconds 200
[D1]::BringWindowToTop($hwnd)|Out-Null
[D1]::SetForegroundWindow($hwnd)|Out-Null
Start-Sleep -Milliseconds 900
$fg=[D1]::GetForegroundWindow()
Write-Output ("FOCUS: " + ($fg -eq $hwnd))
if($fg -ne $hwnd){ Write-Output "  foreground thuc te: " + ((Get-Process -Id ([D1]::GetForegroundWindow()) -ErrorAction SilentlyContinue).ProcessName); exit 4 }

$c=New-Object System.Windows.Automation.PropertyCondition($AE::ControlTypeProperty,[System.Windows.Automation.ControlType]::Edit)
$composer=$null
foreach($e in $win.FindAll($TS::Descendants,$c)){ if(-not $e.Current.IsOffscreen){$composer=$e} }
$r=$composer.Current.BoundingRectangle
$cx=[int]($r.X+80); $cy=[int]($r.Y+$r.Height/2)
Write-Output ("composer tai " + $cx + "," + $cy)
[D1]::SetCursorPos($cx,$cy)|Out-Null
Start-Sleep -Milliseconds 300
[D1]::mouse_event(0x0002,0,0,0,[UIntPtr]::Zero); Start-Sleep -Milliseconds 100; [D1]::mouse_event(0x0004,0,0,0,[UIntPtr]::Zero)
Start-Sleep -Milliseconds 800
$vp=$composer.GetCurrentPattern([System.Windows.Automation.ValuePattern]::Pattern)
Write-Output ("truoc khi go: '" + $vp.Current.Value + "'")
[System.Windows.Forms.SendKeys]::SendWait('^a')
Start-Sleep -Milliseconds 200
[System.Windows.Forms.SendKeys]::SendWait('{DEL}')
Start-Sleep -Milliseconds 500
Write-Output ("sau khi xoa: '" + $vp.Current.Value + "'")
[System.Windows.Forms.SendKeys]::SendWait($Text)
Start-Sleep -Milliseconds 1500
Write-Output ("sau khi go: '" + $vp.Current.Value + "'")

$bc=New-Object System.Windows.Automation.PropertyCondition($AE::ControlTypeProperty,[System.Windows.Automation.ControlType]::Button)
foreach($b in $win.FindAll($TS::Descendants,$bc)){
  if($b.Current.IsOffscreen){continue}
  $n=$b.Current.Name
  if($n -match '^Gửi' -or $n -match '^Send' -or $n -match 'Dừng'){ Write-Output ("NUT '" + $n + "' enabled=" + $b.Current.IsEnabled) }
}
