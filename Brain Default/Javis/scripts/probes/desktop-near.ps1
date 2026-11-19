param([ValidateSet('chatgpt','claude')][string]$App='chatgpt',[int]$PadTop=0)
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
if(-not $composer){Write-Output "ERROR: no composer";exit 4}
$cr=$composer.Current.BoundingRectangle
Write-Output ("COMPOSER rect: L=" + [int]$cr.X + " T=" + [int]$cr.Y + " W=" + [int]$cr.Width + " H=" + [int]$cr.Height)

$all=$win.FindAll($TS::Descendants,[System.Windows.Automation.Condition]::TrueCondition)
foreach($e in $all){
  $b=$e.Current.BoundingRectangle
  if($b.Width -le 0 -or $b.Height -le 0){continue}
  if($b.Top -lt ($cr.Top - 60) -or $b.Top -gt ($cr.Bottom + 120)){continue}
  if($b.Left -lt ($cr.Left - 200) -or $b.Left -gt ($cr.Right + 400)){continue}
  $ct=$e.Current.ControlType.ProgrammaticName
  if($ct -notmatch 'Button|Hyperlink|Image'){continue}
  $n=$e.Current.Name
  if([string]::IsNullOrWhiteSpace($n)){$n='<khong ten>'}
  if($n.Length -gt 40){$n=$n.Substring(0,40)}
  Write-Output ("  " + $ct + " | '" + $n + "' | rect L=" + [int]$b.X + " T=" + [int]$b.Y + " W=" + [int]$b.Width + " H=" + [int]$b.Height + " | enabled=" + $e.Current.IsEnabled)
}
