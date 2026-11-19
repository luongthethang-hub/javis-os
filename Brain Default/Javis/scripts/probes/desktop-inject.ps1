param([ValidateSet('chatgpt','claude')][string]$App='chatgpt',[string]$Text='')
$ErrorActionPreference='Stop'
[Console]::OutputEncoding=[System.Text.Encoding]::UTF8
Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes
Add-Type -AssemblyName System.Windows.Forms
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class Fg {
  [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr hWnd);
  [DllImport("user32.dll")] public static extern bool BringWindowToTop(IntPtr hWnd);
  [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
  [DllImport("user32.dll")] public static extern int GetWindowTextLength(IntPtr hWnd);
  [DllImport("user32.dll")] public static extern uint GetWindowThreadProcessId(IntPtr hWnd, out uint pid);
  [DllImport("user32.dll")] public static extern bool AttachThreadInput(uint idAttach, uint idAttachTo, bool fAttach);
  [DllImport("kernel32.dll")] public static extern uint GetCurrentThreadId();
}
"@
$procName = if ($App -eq 'chatgpt') { 'ChatGPT' } else { 'claude' }
$winTitle = if ($App -eq 'chatgpt') { 'ChatGPT' } else { 'Claude' }
$root=[System.Windows.Automation.AutomationElement]::RootElement
$kids=$root.FindAll([System.Windows.Automation.TreeScope]::Children,[System.Windows.Automation.Condition]::TrueCondition)
$target=$null
foreach($k in $kids){ if($k.Current.Name -ne $winTitle){continue}; $p=Get-Process -Id $k.Current.ProcessId -ErrorAction SilentlyContinue; if($p -and $p.ProcessName -eq $procName){$target=$k;break} }
if(-not $target){Write-Output "ERROR: no window";exit 3}
$hwnd=[IntPtr]$target.Current.NativeWindowHandle
Write-Output ("hwnd=" + $hwnd)

# foreground truoc khi lam
$fg=[Fg]::GetForegroundWindow()
$fgPid=0; [Fg]::GetWindowThreadProcessId($fg,[ref]$fgPid)|Out-Null
$fgName=(Get-Process -Id $fgPid -ErrorAction SilentlyContinue).ProcessName
Write-Output ("foreground truoc: pid=$fgPid ($fgName)")

# ep len truoc bang AttachThreadInput
$myTid=[Fg]::GetCurrentThreadId()
$fgTid=0; [Fg]::GetWindowThreadProcessId($fg,[ref]$fgTid)|Out-Null
[Fg]::AttachThreadInput($myTid,$fgTid,$true)|Out-Null
[Fg]::ShowWindow($hwnd,9)|Out-Null
[Fg]::BringWindowToTop($hwnd)|Out-Null
[Fg]::SetForegroundWindow($hwnd)|Out-Null
[Fg]::AttachThreadInput($myTid,$fgTid,$false)|Out-Null
Start-Sleep -Milliseconds 700

$fg2=[Fg]::GetForegroundWindow()
Write-Output ("foreground sau: " + $fg2 + " == target? " + ($fg2 -eq $hwnd))

$editCond=New-Object System.Windows.Automation.PropertyCondition([System.Windows.Automation.AutomationElement]::ControlTypeProperty,[System.Windows.Automation.ControlType]::Edit)
$edits=$target.FindAll([System.Windows.Automation.TreeScope]::Descendants,$editCond)
$composer=$null
foreach($e in $edits){ if(-not $e.Current.IsOffscreen){$composer=$e} }
if(-not $composer){Write-Output "ERROR: khong thay o soan";exit 4}

if($Text -ne ''){
  $vp=$composer.GetCurrentPattern([System.Windows.Automation.ValuePattern]::Pattern)
  $vp.SetValue($Text)
  Start-Sleep -Milliseconds 500
  Write-Output ("o soan sau khi dat: '" + $vp.Current.Value + "'")
}
$composer.SetFocus()
Start-Sleep -Milliseconds 500
[System.Windows.Forms.SendKeys]::SendWait('{ENTER}')
Start-Sleep -Milliseconds 1500
$vp2=$composer.GetCurrentPattern([System.Windows.Automation.ValuePattern]::Pattern)
Write-Output ("o soan sau Enter: '" + $vp2.Current.Value + "'")
