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
foreach($e in $win.FindAll($TS::Descendants,$c)){
  Write-Output ("EDIT '" + $e.Current.Name + "' enabled=" + $e.Current.IsEnabled + " readonly=" + $e.Current.IsReadOnly + " offscreen=" + $e.Current.IsOffscreen)
}
$txtCond=New-Object System.Windows.Automation.PropertyCondition($AE::ControlTypeProperty,[System.Windows.Automation.ControlType]::Text)
$hits=@()
foreach($t in $win.FindAll($TS::Descendants,$txtCond)){
  $n=$t.Current.Name
  if($n -match 'giới hạn|nâng cấp|thử lại vào|hết luật|quota|limit'){ $hits += $n }
}
Write-Output "----- CANH BAO / GIOI HAN -----"
foreach($h in $hits){ Write-Output ("  * " + $h) }
if($hits.Count -eq 0){ Write-Output "  (khong thay canh bao gioi han nao)" }
