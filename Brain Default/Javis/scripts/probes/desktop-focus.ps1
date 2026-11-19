param([ValidateSet('chatgpt','claude','chrome')][string]$App='chatgpt')
$ErrorActionPreference='Stop'
[Console]::OutputEncoding=[System.Text.Encoding]::UTF8
Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class Fg2 {
  [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr hWnd);
  [DllImport("user32.dll")] public static extern bool BringWindowToTop(IntPtr hWnd);
  [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
  [DllImport("user32.dll")] public static extern uint GetWindowThreadProcessId(IntPtr hWnd, out uint pid);
  [DllImport("user32.dll")] public static extern void keybd_event(byte bVk, byte bScan, uint dwFlags, UIntPtr dwExtraInfo);
  [DllImport("user32.dll")] public static extern bool IsIconic(IntPtr hWnd);
  [DllImport("user32.dll")] public static extern bool IsWindowVisible(IntPtr hWnd);
}
"@
$procName = if ($App -eq 'chatgpt') { 'ChatGPT' } elseif ($App -eq 'claude') { 'claude' } else { 'chrome' }
$winTitle = if ($App -eq 'chatgpt') { 'ChatGPT' } elseif ($App -eq 'claude') { 'Claude' } else { 'Javis OS' }
$root=[System.Windows.Automation.AutomationElement]::RootElement
$kids=$root.FindAll([System.Windows.Automation.TreeScope]::Children,[System.Windows.Automation.Condition]::TrueCondition)
$target=$null
foreach($k in $kids){ if($k.Current.Name -ne $winTitle){continue}; $p=Get-Process -Id $k.Current.ProcessId -ErrorAction SilentlyContinue; if($p -and $p.ProcessName -eq $procName){$target=$k;break} }
if(-not $target){Write-Output "ERROR: no window";exit 3}
$hwnd=[IntPtr]$target.Current.NativeWindowHandle
Write-Output ("target hwnd=$hwnd visible=" + [Fg2]::IsWindowVisible($hwnd) + " iconic=" + [Fg2]::IsIconic($hwnd))
$fg=[Fg2]::GetForegroundWindow()
$pid1=0;[Fg2]::GetWindowThreadProcessId($fg,[ref]$pid1)|Out-Null
Write-Output ("foreground truoc: " + $fg + " pid=$pid1 " + (Get-Process -Id $pid1 -ErrorAction SilentlyContinue).ProcessName)

if([Fg2]::IsIconic($hwnd)){ [Fg2]::ShowWindow($hwnd,9)|Out-Null; Start-Sleep -Milliseconds 500 }

# Trick: nhan ALT de mo khoa SetForegroundWindow
[Fg2]::keybd_event(0x12,0,0,[UIntPtr]::Zero)
[Fg2]::keybd_event(0x12,0,2,[UIntPtr]::Zero)
Start-Sleep -Milliseconds 120
[Fg2]::BringWindowToTop($hwnd)|Out-Null
$ok=[Fg2]::SetForegroundWindow($hwnd)
Start-Sleep -Milliseconds 700
$fg2=[Fg2]::GetForegroundWindow()
Write-Output ("SetForegroundWindow tra ve: $ok | foreground sau: " + $fg2 + " | dung target? " + ($fg2 -eq $hwnd))
