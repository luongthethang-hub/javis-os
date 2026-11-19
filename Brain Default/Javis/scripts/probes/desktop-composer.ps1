param([ValidateSet('chatgpt','claude')][string]$App='chatgpt')
$ErrorActionPreference='Stop'
Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes
$procName = if ($App -eq 'chatgpt') { 'ChatGPT' } else { 'claude' }
$winTitle = if ($App -eq 'chatgpt') { 'ChatGPT' } else { 'Claude' }
$root=[System.Windows.Automation.AutomationElement]::RootElement
$kids=$root.FindAll([System.Windows.Automation.TreeScope]::Children,[System.Windows.Automation.Condition]::TrueCondition)
$target=$null
foreach($k in $kids){ if($k.Current.Name -ne $winTitle){continue}; $p=Get-Process -Id $k.Current.ProcessId -ErrorAction SilentlyContinue; if($p -and $p.ProcessName -eq $procName){$target=$k;break} }
if(-not $target){Write-Output "ERROR: no window";exit 3}
$editCond=New-Object System.Windows.Automation.PropertyCondition([System.Windows.Automation.AutomationElement]::ControlTypeProperty,[System.Windows.Automation.ControlType]::Edit)
$edits=$target.FindAll([System.Windows.Automation.TreeScope]::Descendants,$editCond)
foreach($e in $edits){
  $val=''
  try{ $vp=$e.GetCurrentPattern([System.Windows.Automation.ValuePattern]::Pattern); $val=$vp.Current.Value }catch{ $val='<ValuePattern khong dung duoc>' }
  Write-Output ("EDIT name='" + $e.Current.Name + "' | gia tri hien tai: '" + $val + "'")
}
$btnCond=New-Object System.Windows.Automation.PropertyCondition([System.Windows.Automation.AutomationElement]::ControlTypeProperty,[System.Windows.Automation.ControlType]::Button)
$btns=$target.FindAll([System.Windows.Automation.TreeScope]::Descendants,$btnCond)
Write-Output ("BUTTONS: " + $btns.Count)
foreach($b in $btns){ $n=$b.Current.Name; if($n -match 'end|gửi|Gui|Send|G$|Stop|Dừng'){ Write-Output ("  BTN '" + $n + "' enabled=" + $b.Current.IsEnabled) } }
