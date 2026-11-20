param([ValidateSet('chatgpt','claude')][string]$App='chatgpt')
$ErrorActionPreference='Stop'
[Console]::OutputEncoding=[System.Text.Encoding]::UTF8
Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes
$procName = if ($App -eq 'chatgpt') { 'ChatGPT' } else { 'claude' }
$winTitle = if ($App -eq 'chatgpt') { 'ChatGPT' } else { 'Claude' }
$root=[System.Windows.Automation.AutomationElement]::RootElement
$kids=$root.FindAll([System.Windows.Automation.TreeScope]::Children,[System.Windows.Automation.Condition]::TrueCondition)
$target=$null
foreach($k in $kids){ if($k.Current.Name -ne $winTitle){continue}; $p=Get-Process -Id $k.Current.ProcessId -ErrorAction SilentlyContinue; if($p -and $p.ProcessName -eq $procName){$target=$k;break} }
if(-not $target){Write-Output "ERROR: no window";exit 3}
$btnCond=New-Object System.Windows.Automation.PropertyCondition([System.Windows.Automation.AutomationElement]::ControlTypeProperty,[System.Windows.Automation.ControlType]::Button)
$btns=$target.FindAll([System.Windows.Automation.TreeScope]::Descendants,$btnCond)
$i=0
foreach($b in $btns){
  $i++
  $n=$b.Current.Name
  if([string]::IsNullOrWhiteSpace($n)){ $n='<khong ten>' }
  if($n.Length -gt 60){ $n=$n.Substring(0,60) }
  Write-Output ("[" + $i + "] '" + $n + "' | id=" + $b.Current.AutomationId + " | class=" + $b.Current.ClassName)
}
