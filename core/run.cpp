#include <windows.h>
#include <psapi.h>

#include <cstdint>
#include <stdio.h>

extern "C" struct RunInfo {
    bool error;
    bool timeout;
    size_t time_used;
    size_t memory_used;
    uint8_t exit_code;
};
RunInfo _run(const char* exec, const char* in_file, const char* out_file, size_t time_limit) {
    STARTUPINFO si;
    PROCESS_INFORMATION pi;

    ZeroMemory(&si, sizeof(si));
    si.cb = sizeof(si);
    ZeroMemory(&pi, sizeof(pi));

    char* cmd = new char[strlen(exec) + strlen(in_file) + strlen(out_file) + 10];
    sprintf(cmd, "/c %s < %s > %s", exec, in_file, out_file);

    // Start the child process.
    if (!CreateProcess(
            (LPSTR) "C:\\Windows\\System32\\cmd.exe",  // No module name (use command line)
            (LPSTR)cmd,                                // Command line
            NULL,                                      // Process handle not inheritable
            NULL,                                      // Thread handle not inheritable
            FALSE,                                     // Set handle inheritance to FALSE
            0,                                         // No creation flags
            NULL,                                      // Use parent's environment block
            NULL,                                      // Use parent's starting directory
            &si,                                       // Pointer to STARTUPINFO structure
            &pi)                                       // Pointer to PROCESS_INFORMATION structure
    ) {
        printf("CreateProcess failed (%d).\n", GetLastError());
        return {true, false, 0, 0, 0};
    }

    // Wait until child process exits.
    if (WaitForSingleObject(pi.hProcess, time_limit) == WAIT_TIMEOUT) {
        TerminateProcess(pi.hProcess, 0);
        CloseHandle(pi.hProcess);
        CloseHandle(pi.hThread);
        return {false, true, 0, 0, 0};
    }

    // Get time used
    FILETIME startTime, exitTime, kernelTime, userTime;
    if (!GetProcessTimes(pi.hProcess, &startTime, &exitTime, &kernelTime, &userTime)) {
        printf("GetProcessTimes failed (%d).\n", GetLastError());
        return {true, false, 0, 0, 0};
    }
    size_t start = (uint64_t(startTime.dwHighDateTime) << 32) + startTime.dwLowDateTime;
    size_t end = (uint64_t(exitTime.dwHighDateTime) << 32) + exitTime.dwLowDateTime;

    // Get memory usage
    PROCESS_MEMORY_COUNTERS pmc;
    if (!GetProcessMemoryInfo(pi.hProcess, &pmc, sizeof(pmc))) {
        printf("GetProcessMemoryInfo failed (%d).\n", GetLastError());
        return {true, false, 0, 0, 0};
    }

    // Get exit code
    DWORD exitCode;
    GetExitCodeProcess(pi.hProcess, &exitCode);

    // Close process and thread handles.
    CloseHandle(pi.hProcess);
    CloseHandle(pi.hThread);
    return {
        false, false,
        end - start,
        pmc.PeakPagefileUsage + pmc.PeakWorkingSetSize,
        (uint8_t)exitCode};
}

extern "C" __declspec(dllexport) RunInfo run(const char* exec, const char* in_file, const char* out_file, size_t time_limit);
RunInfo run(const char* exec, const char* in_file, const char* out_file, size_t time_limit) {
    return _run(exec, in_file, out_file, time_limit);
}
