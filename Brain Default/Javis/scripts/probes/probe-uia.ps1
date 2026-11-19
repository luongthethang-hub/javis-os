param(
    [ValidateSet('chatgpt','claude')][string]$App = 'chatgpt',
    [string]$Text = '',
    [switch]$Send,
    [switch]$Read
)
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class Win32 {
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr hWnd);
  [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
}
"@

$procName = if ($App -eq 'chatgpt') { 'ChatGPT' } else { 'claude' }
$root = [System.Windows.Automation.AutomationElement]::RootElement
$kids = $root.FindAll([System.Windows.Automation.TreeScope]::Children, [System.Windows.Automation.Condition]::TrueCondition)
$target = $null
foreach ($k in $kids) {
    $p = Get-Process -Id $k.Current.ProcessId -ErrorAction SilentlyContinue
    if ($p -and $p.ProcessName -eq $procName -and $k.Current.Name) {
        if ($App -eq 'chatgpt' -and $k.Current.Name -eq 'ChatGPT') { $target = $k; break }
        if ($App -eq 'claude' -and $k.Current.Name -eq 'Claude') { $target = $k; break }
    }
}
if (-not $target) { Write-Output "ERROR: khong tim thay cua so $App"; exit 3 }
Write-Output ("WINDOW: " + $target.Current.Name + " pid=" + $target.Current.ProcessId + " class=" + $target.Current.ClassName)

$hwnd = [IntPtr]$target.Current.NativeWindowHandle
[Win32]::ShowWindow($hwnd, 9) | Out-Null
[Win32]::SetForegroundWindow($hwnd) | Out-Null
Start-Sleep -Milliseconds 400

$editCond = New-Object System.Windows.Automation.PropertyCondition([System.Windows.Automation.AutomationElement]::ControlTypeProperty, [System.Windows.Automation.ControlType]::Edit)
$edits = $target.FindAll([System.Windows.Automation.TreeScope]::Descendants, $editCond)
Write-Output ("EDITS: " + $edits.Count)
$composer = $null
foreach ($e in $edits) {
    Write-Output ("  EDIT name='" + $e.Current.Name + "' class=" + $e.Current.ClassName + " offscreen=" + $e.Current.IsOffscreen)
    if (-not $e.Current.IsOffscreen) { $composer = $e }
}
if ($composer -and $Text -ne '') {
    try {
        $vp = $composer.GetCurrentPattern([System.Windows.Automation.ValuePattern]::Pattern)
        $vp.SetValue($Text)
        Write-Output "SETVALUE: ok"
    } catch {
        Write-Output ("SETVALUE FAIL: " + $_.Exception.Message)
    }
}
if ($Send -and $composer) {
    $composer.SetFocus()
    Start-Sleep -Milliseconds 250
    [System.Windows.Forms.SendKeys]::SendWait('{ENTER}')
    Write-Output "SENT: enter"
}
