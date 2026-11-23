param(
    [string]$App = 'claude',
    [string]$PromptFile = '',
    [string]$Text = '',
    [int]$WaitSeconds = 300,
    [switch]$NoSend
)

$wrapper = @"
using System;
using System.IO;
using System.Text;
using System.Runtime.InteropServices;

public class HandoffRunner {
    [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Unicode)]
    public struct STARTUPINFO {
        public int cb;
        public string lpReserved;
        public string lpDesktop;
        public string lpTitle;
        public int dwX;
        public int dwY;
        public int dwXSize;
        public int dwYSize;
        public int dwXCountChars;
        public int dwYCountChars;
        public int dwFillAttribute;
        public int dwFlags;
        public short wShowWindow;
        public short cbReserved2;
        public IntPtr lpReserved2;
        public IntPtr hStdInput;
        public IntPtr hStdOutput;
        public IntPtr hStdError;
    }

    [StructLayout(LayoutKind.Sequential)]
    public struct PROCESS_INFORMATION {
        public IntPtr hProcess;
        public IntPtr hThread;
        public int dwProcessId;
        public int dwThreadId;
    }

    [DllImport("kernel32.dll", SetLastError = true, CharSet = CharSet.Unicode)]
    public static extern bool CreateProcess(
        string lpApplicationName,
        string lpCommandLine,
        IntPtr lpProcessAttributes,
        IntPtr lpThreadAttributes,
        bool bInheritHandles,
        uint dwCreationFlags,
        IntPtr lpEnvironment,
        string lpCurrentDirectory,
        ref STARTUPINFO lpStartupInfo,
        out PROCESS_INFORMATION lpProcessInformation);

    [DllImport("kernel32.dll")] public static extern uint WaitForSingleObject(IntPtr hHandle, uint dwMilliseconds);
    [DllImport("kernel32.dll")] public static extern bool GetExitCodeProcess(IntPtr hProcess, out uint lpExitCode);
    [DllImport("kernel32.dll")] public static extern bool CloseHandle(IntPtr hObject);

    public static uint Run(string cmdLine, uint timeoutMs) {
        STARTUPINFO si = new STARTUPINFO();
        si.cb = Marshal.SizeOf(si);
        si.lpDesktop = @"WinSta0\default";

        PROCESS_INFORMATION pi;
        bool ok = CreateProcess(null, cmdLine, IntPtr.Zero, IntPtr.Zero, false, 0, IntPtr.Zero, null, ref si, out pi);
        if (!ok) {
            int err = Marshal.GetLastWin32Error();
            Console.WriteLine("CreateProcess failed with error: " + err);
            return 999;
        }

        WaitForSingleObject(pi.hProcess, timeoutMs);
        uint exitCode = 0;
        GetExitCodeProcess(pi.hProcess, out exitCode);
        CloseHandle(pi.hProcess);
        CloseHandle(pi.hThread);
        return exitCode;
    }
}
"@

Add-Type $wrapper

$handoffScript = "C:\Users\Admin\JavisOS\brains\Brain Default\Javis\scripts\handoff.ps1"
$logFile = "C:\Users\Admin\JavisOS\brains\Brain Default\Javis\tmp\handoff_run.log"

$extraArgs = ""
if ($PromptFile -ne '') {
    $extraArgs += " -PromptFile `"$PromptFile`""
} elseif ($Text -ne '') {
    $extraArgs += " -Text `"$Text`""
}
if ($NoSend) {
    $extraArgs += " -NoSend"
}
$extraArgs += " -WaitSeconds $WaitSeconds"

$cmd = "powershell.exe -NoProfile -ExecutionPolicy Bypass -File `"$handoffScript`" -App $App $extraArgs"
$fullCmdLine = "cmd.exe /c `"$cmd > `"$logFile`" 2>&1`""

Write-Output "Executing via ProcLauncher on WinSta0\default..."
$timeoutMs = ($WaitSeconds + 60) * 1000
$code = [HandoffRunner]::Run($fullCmdLine, [uint32]$timeoutMs)
Write-Output "Finished with exit code: $code"
if (Test-Path $logFile) {
    Write-Output "--- LOG OUTPUT ---"
    Get-Content $logFile -Encoding UTF8
    Write-Output "--- END LOG ---"
}
exit $code
