# Runs only local deployment, test and recovery actions authorized by the user.
# Never commits, pushes, deletes CTFd volumes, or imports over the primary platform.
param([switch]$RecoveryOnly)
$ErrorActionPreference = 'Stop'
Push-Location (Split-Path $PSScriptRoot -Parent)
$taskTranscriptStarted = $false
function Invoke-Checked {
    param([string]$Program, [string[]]$Arguments)
    & $Program @Arguments 2>&1 | Tee-Object -FilePath 'testing/test-results/finish-local-command-output.txt' -Append | Out-Host
    if ($LASTEXITCODE -ne 0) { throw "Step failed: $Program $($Arguments -join ' '). Details: testing/test-results/finish-local-command-output.txt" }
}
function Wait-LocalPort {
    param([int]$Port)
    for ($taskAttempt = 0; $taskAttempt -lt 45; $taskAttempt++) {
        $taskClient = [System.Net.Sockets.TcpClient]::new()
        try { $taskClient.Connect('127.0.0.1', $Port); return }
        catch { Start-Sleep -Seconds 2 }
        finally { $taskClient.Dispose() }
    }
    throw "Local port $Port did not become ready"
}
try {
    New-Item -ItemType Directory -Force testing/test-results | Out-Null
    Start-Transcript -Path (Join-Path (Get-Location) 'testing/test-results/finish-local-transcript.txt') -Force | Out-Null
    $taskTranscriptStarted = $true
    $taskPython = (Resolve-Path '.venv/Scripts/python.exe').Path
    if (-not $RecoveryOnly) {
    Invoke-Checked docker @('compose','config','--quiet')
    # Validate the gateway image's stream configuration before disrupting SSH.
    Invoke-Checked docker @('compose','run','--rm','--no-deps','ssh_gateway','-t')
    Invoke-Checked docker @('compose','up','-d','--build','nhx05','ssh_gateway')
    Invoke-Checked docker @('compose','restart','nginx')
    Wait-LocalPort 443
    Wait-LocalPort 2225
    Invoke-Checked $taskPython @('scripts/enroll-ssh-host.py')
    Invoke-Checked $taskPython @('scripts/member4-integration-test.py','--downloads','testing/downloads')
    Invoke-Checked $taskPython @('scripts/isolation-test.py')
    Invoke-Checked $taskPython @('scripts/reset-test.py')
    Wait-LocalPort 443
    Wait-LocalPort 2225
    Invoke-Checked $taskPython @('scripts/enroll-ssh-host.py')
    Invoke-Checked $taskPython @('scripts/isolation-test.py')
    Invoke-Checked $taskPython @('scripts/player-flow-test.py')
    }
    Invoke-Checked docker @('compose','-p','noctihex-recovery','-f','docker-compose.yml','-f','testing/recovery-compose.yml','config','--quiet')
    Invoke-Checked docker @('compose','-p','noctihex-recovery','-f','docker-compose.yml','-f','testing/recovery-compose.yml','up','-d','--build')
    Wait-LocalPort 8443
    Wait-LocalPort 2226
    Invoke-Checked $taskPython @('scripts/recovery-test.py')
    Invoke-Checked $taskPython @('scripts/enroll-ssh-host.py','--project','noctihex-recovery','--port','2226')
    Invoke-Checked $taskPython @('scripts/player-flow-test.py','--base-url','https://127.0.0.1:8443','--ssh-port','2226','--report-name','recovery-player-flow')
    Invoke-Checked $taskPython @('scripts/member4-integration-test.py','--downloads','testing/downloads')
    Write-Host 'Automated primary isolation, resets, player flow and separate recovery checks completed. Logs are in testing/. The group video and human review remain required.'
} finally {
    if ($taskTranscriptStarted) { Stop-Transcript | Out-Null }
    Pop-Location
}
