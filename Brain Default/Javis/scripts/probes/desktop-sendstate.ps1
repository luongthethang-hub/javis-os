param([ValidateSet('chatgpt','claude')][string]$App='chatgpt')
$ErrorActionPreference='Stop'
[Console]::OutputEncoding=[System.Text.Encoding]::UTF8
Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes
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
$c=New-Object System.Windows.Automation.PropertyCondition($AE::ControlTypeProperty,[System.Windows.Automation.ControlType]::Edit)
$composer=$null
foreach($e in $win.FindAll($TS::Descendants,$c)){ if(-not $e.Current.IsOffscreen){$composer=$e} }
$vp=$composer.GetCurrentPattern([System.Windows.Automation.ValuePattern]::Pattern)
Write-Output ("O SOAN (" + $vp.Current.Value.Length + " ky tu): '" + $vp.Current.Value + "'")
$bc=New-Object System.Windows.Automation.PropertyCondition($AE::ControlTypeProperty,[System.Windows.Automation.ControlType]::Button)
foreach($b in $win.FindAll($TS::Descendants,$bc)){
  if($b.Current.IsOffscreen){continue}
  $n=$b.Current.Name
  if($n -match '^Gửi' -or $n -match '^Send'){ Write-Output ("NUT '" + $n + "' enabled=" + $b.Current.IsEnabled) }
}
