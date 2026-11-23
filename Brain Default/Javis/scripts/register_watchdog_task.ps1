# Script dang ky Windows Scheduled Task cho Javis Emergency Watchdog
$taskName = "JavisEmergencyWatchdog"
$scriptDir = "C:\Users\Admin\JavisOS\brains\Brain Default\Javis\scripts"
$batPath = Join-Path $scriptDir "run_emergency_watchdog.bat"

Write-Host "=== DANG KY TASK SCHEDULE: $taskName ==="

$action = New-ScheduledTaskAction -Execute "cmd.exe" -Argument "/c `"$batPath`"" -WorkingDirectory $scriptDir
$trigger = New-ScheduledTaskTrigger -AtLogOn
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -ExecutionTimeLimit (New-TimeSpan -Days 365) -RestartCount 3 -RestartInterval (New-TimeSpan -Minutes 1)

try {
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false -ErrorAction SilentlyContinue
    Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -Description "Javis Out-of-Band Emergency Kill-Switch Watchdog Daemon" | Out-Null
    Write-Host "[THANH CONG] Da dang ky task '$taskName' khoi dong cung Windows Logon." -ForegroundColor Green
} catch {
    Write-Host "[LOI] Dang ky task that bai: $_" -ForegroundColor Red
}
