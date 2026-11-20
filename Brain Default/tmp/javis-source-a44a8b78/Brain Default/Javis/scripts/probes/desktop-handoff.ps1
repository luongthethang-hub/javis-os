param(
    [ValidateSet('chatgpt','claude')][string]$App = 'chatgpt',
    [string]$Text = '',
    [switch]$Send,
    [switch]$DoNotFocus
)
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes
Add-Type -AssemblyName System.Windows.Forms
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class Win32F {
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr hWnd);
  [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
}
"@

$procName = if ($App -eq 'chatgpt') { 'ChatGPT' } else { 'claude' }
$winTitle = if ($App -eq 'chatgpt') { 'ChatGPT' } else { 'Claude' }

$root = [System.Windows.Automation.AutomationElement]::RootElement
$kids = $root.FindAll([System.Windows.Automation.TreeScope]::Children, [System.Windows.Automation.Condition]::TrueCondition)
$target = $null
foreach ($k in $kids) {
    if ($k.Current.Name -ne $winTitle) { continue }
    $p = Get-Process -Id $k.Current.ProcessId -ErrorAction SilentlyContinue
    if ($p -and $p.ProcessName -eq $procName) { $target = $k; break }
}
if (-not $target) { Write-Output "ERROR: khong tim thay cua so $App"; exit 3 }
Write-Output ("WINDOW: " + $target.Current.Name + " pid=" + $target.Current.ProcessId)

if (-not $DoNotFocus) {
    $hwnd = [IntPtr]$target.Current.NativeWindowHandle
    [Win32F]::ShowWindow($hwnd, 9) | Out-Null
    [Win32F]::SetForegroundWindow($hwnd) | Out-Null
    Start-Sleep -Milliseconds 500
}

$editCond = New-Object System.Windows.Automation.PropertyCondition([System.Windows.Automation.AutomationElement]::ControlTypeProperty, [System.Windows.Automation.ControlType]::Edit)
$edits = $target.FindAll([System.Windows.Automation.TreeScope]::Descendants, $editCond)
Write-Output ("EDITS: " + $edits.Count)
$composer = $null
foreach ($e in $edits) {
    Write-Output ("  EDIT name='" + $e.Current.Name + "' class=" + $e.Current.ClassName + " offscreen=" + $e.Current.IsOffscreen)
    if (-not $e.Current.IsOffscreen) { $composer = $e }
}
if (-not $composer) { Write-Output "ERROR: khong thay o soan"; exit 4 }

if ($Text -ne '') {
    try {
        $vp = $composer.GetCurrentPattern([System.Windows.Automation.ValuePattern]::Pattern)
        $vp.SetValue($Text)
        Start-Sleep -Milliseconds 300
        Write-Output ("SETVALUE: ok, doc lai='" + $vp.Current.Value + "'")
    } catch {
        Write-Output ("SETVALUE FAIL: " + $_.Exception.Message)
        exit 5
    }
}

if ($Send) {
    try {
        $composer.SetFocus()
        Start-Sleep -Milliseconds 300
        [System.Windows.Forms.SendKeys]::SendWait('{ENTER}')
        Start-Sleep -Milliseconds 800
        Write-Output "SENT: enter"
    } catch {
        Write-Output ("SEND FAIL: " + $_.Exception.Message)
        exit 6
    }
}
