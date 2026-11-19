param([ValidateSet('chatgpt','claude')][string]$App='chatgpt',[string]$Match='submit')
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
$all=$target.FindAll([System.Windows.Automation.TreeScope]::Descendants,[System.Windows.Automation.Condition]::TrueCondition)
$i=0
foreach($e in $all){
  $i++
  $cls=$e.Current.ClassName
  $nm=$e.Current.Name
  $hay = "$cls $nm"
  if($hay -notmatch $Match){ continue }
  if($nm.Length -gt 45){$nm=$nm.Substring(0,45)}
  if($cls.Length -gt 70){$cls=$cls.Substring(0,70)}
  Write-Output ("[" + $i + "] " + $e.Current.ControlType.ProgrammaticName + " | '" + $nm + "' | class=" + $cls + " | enabled=" + $e.Current.IsEnabled + " | offscreen=" + $e.Current.IsOffscreen)
}
