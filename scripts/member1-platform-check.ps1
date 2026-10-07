Write-Host "=== NoctiHex Platform Validation ==="

Write-Host "[1] Docker services"
docker compose ps

Write-Host "`n[2] HTTPS platform"
curl.exe -k -I https://noctihex.local

Write-Host "`n[3] Checking MySQL exposure"
docker compose port mysql 3306

Write-Host "`n[4] Checking Redis exposure"
docker compose port redis 6379

Write-Host "`n[5] NHX-05 service"
Test-NetConnection 127.0.0.1 -Port 2225