param(
    [Parameter(Mandatory=$true)][string]$Root,
    [Parameter(Mandatory=$true)][int]$WaitPid,
    [int]$MaxWaitSeconds = 900
)
$ErrorActionPreference = 'Stop'
$statusFile = Join-Path $PSScriptRoot 'activation.json'
$deadline = (Get-Date).AddSeconds($MaxWaitSeconds)
$endpoint = 'http://127.0.0.1:7777'

function Write-Status([string]$Status, [string]$Detail) {
    [ordered]@{status=$Status; detail=$Detail; wait_pid=$WaitPid; at=(Get-Date).ToString('o')} |
        ConvertTo-Json | Set-Content -LiteralPath $statusFile -Encoding UTF8
}

function Is-Descendant($Process, $ProcessById, [int]$Ancestor) {
    $parentId = [int]$Process.ParentProcessId
    for ($depth=0; $depth -lt 20 -and $parentId -gt 0; $depth++) {
        if ($parentId -eq $Ancestor) { return $true }
        if (-not $ProcessById.ContainsKey($parentId)) { return $false }
        $parentId = [int]$ProcessById[$parentId].ParentProcessId
    }
    return $false
}

try {
    Write-Status 'waiting_for_turn' 'The installed files are ready. Waiting for the initiating chat process to exit.'
    while (Get-Process -Id $WaitPid -ErrorAction SilentlyContinue) {
        if ((Get-Date) -ge $deadline) {
            Write-Status 'not_activated' 'The initiating chat process was still running at the deadline.'
            exit 2
        }
        Start-Sleep -Seconds 3
    }
    Start-Sleep -Seconds 5

    do {
        $health = Invoke-RestMethod -Uri "$endpoint/health" -TimeoutSec 4
        if ($health.status -eq 'ok' -and $health.workflow_author_failover -eq $true) {
            Write-Status 'activated' 'Health confirmed workflow author failover.'
            exit 0
        }
        $listeners = @(Get-NetTCPConnection -LocalPort 7777 -State Listen)
        $rows = @(Get-CimInstance Win32_Process)
        $byId = @{}
        foreach ($row in $rows) { $byId[[int]$row.ProcessId] = $row }
        $cliBusy = $false
        foreach ($listener in $listeners) {
            foreach ($row in $rows) {
                if ($row.Name -in @('codex.exe','claude.exe','grok.exe','agy.exe') -and
                    (Is-Descendant $row $byId ([int]$listener.OwningProcess))) {
                    $cliBusy = $true
                    break
                }
            }
            if ($cliBusy) { break }
        }
        $kanban = Invoke-RestMethod -Uri "$endpoint/kanban?brain=brain" -TimeoutSec 4
        $workflows = Invoke-RestMethod -Uri "$endpoint/workflows/runs?brain=brain&limit=50" -TimeoutSec 4
        if ($null -eq $kanban.counts.running -or $workflows.PSObject.Properties.Name -notcontains 'runs') {
            throw 'Cannot verify whether Kanban and workflows are idle.'
        }
        $workflowBusy = @($workflows.runs | Where-Object status -eq 'running').Count -gt 0
        $busy = $cliBusy -or [int]$kanban.counts.running -gt 0 -or $workflowBusy
        if ($busy) {
            Write-Status 'waiting_for_work' 'An active Javis session, Kanban job or workflow is still running.'
            if ((Get-Date) -ge $deadline) {
                Write-Status 'not_activated' 'Javis still had active work at the deadline.'
                exit 3
            }
            Start-Sleep -Seconds 5
        }
    } while ($busy)

    $manifest = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'manifest.json') -Raw | ConvertFrom-Json
    foreach ($item in $manifest.after.PSObject.Properties) {
        $hash = Get-FileHash -LiteralPath (Join-Path $Root $item.Name) -Algorithm SHA256
        if ($hash.Hash -ne $item.Value) { throw "Installed source changed before activation: $($item.Name)" }
    }
    Write-Status 'restarting' 'Starting the installed Javis launcher.'
    Start-Process -FilePath 'wscript.exe' -ArgumentList @('//nologo', ('"' + (Join-Path $Root 'start-javis.vbs') + '"')) -WindowStyle Hidden
    for ($attempt=0; $attempt -lt 32; $attempt++) {
        Start-Sleep -Seconds 3
        try {
            $health = Invoke-RestMethod -Uri "$endpoint/health" -TimeoutSec 3
            if ($health.status -eq 'ok' -and $health.workflow_author_failover -eq $true) {
                Write-Status 'activated' 'The installed server loaded workflow author failover and passed /health.'
                exit 0
            }
        } catch {}
    }
    Write-Status 'activation_unverified' 'The launcher ran, but the new health marker was not confirmed.'
    exit 4
} catch {
    Write-Status 'activation_error' $_.Exception.Message
    exit 5
}
