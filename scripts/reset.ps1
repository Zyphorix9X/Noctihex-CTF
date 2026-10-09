param([ValidateSet('nhx03','nhx05','all')][string]$Stage = 'all')
$ErrorActionPreference = 'Stop'
Push-Location (Split-Path $PSScriptRoot -Parent)
try {
    $services = if ($Stage -eq 'all') { @('nhx03','nhx05') } else { @($Stage) }
    & docker compose config --quiet
    if ($LASTEXITCODE -ne 0) { throw 'Compose validation failed' }
    & docker compose up -d --no-deps --force-recreate @services
    if ($LASTEXITCODE -ne 0) { throw 'Challenge recreation failed' }
    if ($services -contains 'nhx03') {
        & docker compose restart nginx
        if ($LASTEXITCODE -ne 0) { throw 'Nginx restart failed' }
    }
    foreach ($service in $services) {
        $id = & docker compose ps -q $service
        if (!$id) { throw "$service has no running container" }
        $running = & docker inspect --format '{{.State.Running}}' $id
        if ($LASTEXITCODE -ne 0 -or $running -ne 'true') { throw "$service is not running" }
    }
    Write-Host 'Containers recreated. Repeat login and intended-path checks to validate reset behavior.'
} finally { Pop-Location }
