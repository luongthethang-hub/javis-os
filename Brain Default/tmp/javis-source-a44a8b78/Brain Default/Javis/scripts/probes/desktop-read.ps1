param(
    [ValidateSet('chatgpt','claude')][string]$App = 'chatgpt',
    [int]$Tail = 3000
)
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes

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

$docCond = New-Object System.Windows.Automation.PropertyCondition([System.Windows.Automation.AutomationElement]::ControlTypeProperty, [System.Windows.Automation.ControlType]::Document)
$docs = $target.FindAll([System.Windows.Automation.TreeScope]::Descendants, $docCond)
$best = $null
$bestLen = -1
foreach ($d in $docs) {
    try {
        $tp = $d.GetCurrentPattern([System.Windows.Automation.TextPattern]::Pattern)
        $txt = $tp.DocumentRange.GetText(-1)
        Write-Output ("DOC '" + $d.Current.Name + "' len=" + $txt.Length)
        if ($txt.Length -gt $bestLen) { $bestLen = $txt.Length; $best = $txt }
    } catch {
        Write-Output ("DOC '" + $d.Current.Name + "' -> khong doc duoc: " + $_.Exception.Message)
    }
}
if ($best) {
    if ($best.Length -gt $Tail) { $best = $best.Substring($best.Length - $Tail) }
    Write-Output "----- CUOI VAN BAN -----"
    Write-Output $best
} else {
    Write-Output "ERROR: khong doc duoc van ban"
    exit 4
}
