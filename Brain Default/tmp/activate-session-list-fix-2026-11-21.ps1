param([int]$WaitPid)
$ErrorActionPreference = 'Stop'
$Root = 'C:\Users\Admin\JavisOS'
$Session = '8aada49d5784446c8765f85f800bd37b'
$OldPid = 8620
$Base = 'http://127.0.0.1:7777'
$Report = Join-Path $Root 'brains\Brain Default\reports\danh-sach-hoi-thoai-khoi-dong-lai-2026-11-21.md'
Set-Location -LiteralPath $Root
function Report([string]$Status, [string]$Detail) {
    $body = "# Khởi động lại Javis`r`n`r`n**$Status**`r`n`r`n$Detail`r`n`r`nCập nhật lúc $((Get-Date).ToString('HH:mm:ss dd/MM/yyyy zzz'))."
    [IO.File]::WriteAllText($Report, $body, [Text.UTF8Encoding]::new($false))
}
function Listener {
    @(Get-NetTCPConnection -LocalPort 7777 -State Listen -ErrorAction SilentlyContinue |
        Where-Object LocalAddress -eq '127.0.0.1' | Select-Object -ExpandProperty OwningProcess)
}
function NativeTurns($Rows) {
    $index = @{}
    foreach ($row in $Rows) { $index[[int]$row.ProcessId] = $row }
    foreach ($row in ($Rows | Where-Object Name -in 'codex.exe','claude.exe','grok.exe','agy.exe')) {
        $parent = [int]$row.ParentProcessId
        for ($i = 0; $i -lt 24 -and $index.ContainsKey($parent); $i++) {
            if ($parent -eq $OldPid) { $row.ProcessId; break }
            $parent = [int]$index[$parent].ParentProcessId
        }
    }
}
$ActivityProbe = @"
import json
import sqlite3
from contextlib import closing
from pathlib import Path

server = Path('server').resolve()
checks = {
    'chat': ('turn_ledger.sqlite3', 'SELECT COUNT(*) FROM turns'),
    'workflow': ('workflow_runs.sqlite3', "SELECT COUNT(*) FROM workflow_runs WHERE status='running'"),
    'kanban_team': ('kanban.sqlite3', "SELECT COUNT(*) FROM tasks WHERE status IN ('running','team_running')"),
}
counts = {}
for name, (db, sql) in checks.items():
    with closing(sqlite3.connect((server / db).as_uri() + '?mode=ro', uri=True, timeout=2)) as conn:
        counts[name] = conn.execute(sql).fetchone()[0]
jobs = server / 'chat_jobs.json'
counts['chat_api'] = sum(job.get('status') == 'running' for job in json.loads(jobs.read_text(encoding='utf-8')).values()) if jobs.is_file() else 0
print(sum(counts.values()))
"@
try {
    Report 'Đang chờ lượt chat hiện tại kết thúc' 'Lệnh khởi động lại chỉ chạy khi các lượt chat và tác vụ đang theo dõi đã dừng.'
    $deadline = (Get-Date).AddMinutes(12)
    $quiet = 0
    do {
        if ((Get-Date) -ge $deadline) { throw 'Hết thời gian chờ máy chủ rảnh. Javis chưa được khởi động lại.' }
        Start-Sleep -Seconds 3
        $listenerIds = @(Listener)
        if ($listenerIds.Count -ne 1 -or $listenerIds[0] -ne $OldPid) { throw 'Tiến trình Javis đã đổi trước khi khởi động lại. Đã dừng thao tác.' }
        if (Get-Process -Id $WaitPid -ErrorAction SilentlyContinue) { continue }
        $count = $ActivityProbe | & (Join-Path $Root '.venv\Scripts\python.exe') -
        if ($LASTEXITCODE -ne 0 -or $count -notmatch '^\d+$') { throw 'Không đọc được trạng thái lượt chat và công việc đang chạy.' }
        $schedule = Invoke-RestMethod "$Base/reminders?brain=brain" -TimeoutSec 4
        $update = Invoke-RestMethod "$Base/update/status" -TimeoutSec 4
        $rows = @(Get-CimInstance Win32_Process)
        $launcherTargets = @($rows | Where-Object { $_.Name -eq 'python.exe' -and $_.CommandLine -like '*server\main.py*' })
        $server = $rows | Where-Object ProcessId -eq $OldPid | Select-Object -First 1
        if (!$server -or @($launcherTargets | Where-Object { $_.ProcessId -notin @($OldPid, $server.ParentProcessId) }).Count) {
            throw 'Trình khởi động có thể dừng một tiến trình Python khác. Đã dừng thao tác.'
        }
        if ([int]$count -ne 0 -or @($schedule.pending | Where-Object running).Count -gt 0 -or
            $update.state.phase -in 'preparing','pulling','installing','restarting','health_check','rolling_back' -or
            @(NativeTurns $rows).Count -gt 0) {
            $quiet = 0
            continue
        }
        $quiet++
    } while ($quiet -lt 2)
    Report 'Đang khởi động lại' "Đã kiểm tra hai lần và không thấy lượt chat, workflow, Kanban, nhóm hay lượt CLI đang chạy. Tiến trình cũ có PID $OldPid."
    Start-Process -FilePath 'wscript.exe' -ArgumentList @('//nologo', ('"' + (Join-Path $Root 'start-javis.vbs') + '"')) -WindowStyle Hidden
    $lastError = 'Chưa thấy tiến trình mới lắng nghe cổng 7777.'
    for ($i = 0; $i -lt 42; $i++) {
        Start-Sleep -Seconds 3
        $listenerIds = @(Listener)
        if ($listenerIds.Count -ne 1 -or $listenerIds[0] -eq $OldPid) { continue }
        $newPid = $listenerIds[0]
        try {
            $health = Invoke-WebRequest "$Base/health" -UseBasicParsing -TimeoutSec 4
            $normal = Invoke-RestMethod "$Base/sessions?brain=brain&limit=21&unread_first=1" -TimeoutSec 5
            $archived = Invoke-RestMethod "$Base/sessions?brain=brain&limit=21&archived=1" -TimeoutSec 5
            $unread = Invoke-RestMethod "$Base/sessions/unread-summary?brain=brain" -TimeoutSec 5
            $projects = Invoke-RestMethod "$Base/projects?brain=brain" -TimeoutSec 5
            $chat = Invoke-RestMethod "$Base/sessions/${Session}?limit=1&tools=0" -TimeoutSec 5
            if ($health.StatusCode -ne 200 -or $normal.sessions.Count -lt 1 -or
                $archived.PSObject.Properties.Name -notcontains 'sessions' -or -not $unread.ok -or
                $projects.PSObject.Properties.Name -notcontains 'ungrouped_unread' -or $chat.id -ne $Session -or $chat.total -lt 1) {
                throw 'Phản hồi API chưa đúng cấu trúc hoặc chưa đọc được dữ liệu hội thoại đã có.'
            }
            Report 'Đã khởi động lại và xác minh danh sách hội thoại hoạt động' "PID mới $newPid. API lịch sử, lưu trữ, chưa đọc và dự án đều trả HTTP 200. Đọc được hội thoại đang mở và tin nhắn đã lưu."
            exit 0
        } catch {
            $lastError = $_.Exception.Message
        }
    }
    throw "Chưa xác minh được Javis sau khi gọi trình khởi động. $lastError"
} catch {
    Report 'Chưa hoàn tất' $_.Exception.Message
    exit 1
}