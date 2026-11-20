param(
    [ValidateSet('chatgpt','claude')][string]$App='chatgpt',
    [string]$Text='',
    [switch]$Clear,
    [switch]$Send
)
$ErrorActionPreference='Stop'
Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes
Add-Type -AssemblyName System.Windows.Forms
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class Win32S {
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr hWnd);
  [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
}
"@
$procName = if ($App -eq 'chatgpt') { 'ChatGPT' } else { 'claude' }
$winTitle = if ($App -eq 'chatgpt') { 'ChatGPT' } else { 'Claude' }
$root=[System.Windows.Automation.AutomationElement]::RootElement
$kids=$root.FindAll([System.Windows.Automation.TreeScope]::Children,[System.Windows.Automation.Condition]::TrueCondition)
$target=$null
foreach($k in $kids){ if($k.Current.Name -ne $winTitle){continue}; $p=Get-Process -Id $k.Current.ProcessId -ErrorAction SilentlyContinue; if($p -and $p.ProcessName -eq $procName){$target=$k;break} }
if(-not $target){Write-Output "ERROR: no window for $App";exit 3}
$hwnd=[IntPtr]$target.Current.NativeWindowHandle
[Win32S]::ShowWindow($hwnd,9)|Out-Null
[Win32S]::SetForegroundWindow($hwnd)|Out-Null
Start-Sleep -Milliseconds 600

$editCond=New-Object System.Windows.Automation.PropertyCondition([System.Windows.Automation.AutomationElement]::ControlTypeProperty,[System.Windows.Automation.ControlType]::Edit)
$edits=$target.FindAll([System.Windows.Automation.TreeScope]::Descendants,$editCond)
$composer=$null
foreach($e in $edits){ if(-not $e.Current.IsOffscreen){$composer=$e} }
if(-not $composer){Write-Output "ERROR: khong thay o soan";exit 4}

if($Clear -or $Text -ne ''){
  $newText = if($Clear){''}else{$Text}
  try{
    $vp=$composer.GetCurrentPattern([System.Windows.Automation.ValuePattern]::Pattern)
    $vp.SetValue($newText)
    Start-Sleep -Milliseconds 400
    $after = $vp.Current.Value
    Write-Output ("DAT: '" + $after + "'")
    if($after -ne $newText){Write-Output "CANH BAO: o soan khong nhan dung gia tri";}
  }catch{
    Write-Output ("LOI dat gia tri: " + $_.Exception.Message)
    exit 5
  }
}

if($Send){
  $composer.SetFocus()
  Start-Sleep -Milliseconds 400
  [System.Windows.Forms.SendKeys]::SendWait('{ENTER}')
  Start-Sleep -Milliseconds 1200
  try{
    $vp=$composer.GetCurrentPattern([System.Windows.Automation.ValuePattern]::Pattern)
    Write-Output ("SAU KHI GUI, o soan con: '" + $vp.Current.Value + "'")
  }catch{}
}
