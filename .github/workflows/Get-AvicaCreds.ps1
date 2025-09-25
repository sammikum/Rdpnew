# PowerShell script to retrieve Avica RDP connection info locally

# Function to check if Avica app is installed and get default install path
function Get-AvicaPath {
    $possiblePaths = @(
        "C:\Program Files\Avica\",
        "C:\Program Files (x86)\Avica\"
    )
    foreach ($path in $possiblePaths) {
        if (Test-Path $path) {
            return $path
        }
    }
    return $null
}

# Retrieve AVICA installation path
$avicaPath = Get-AvicaPath

if ($avicaPath -eq $null) {
    Write-Host "Avica app not found on this system." -ForegroundColor Red
    exit 1
}

# Sample: Read credential file or config where Avica may store ID/password
# (Adjust file path & format based on actual Avica app specifics)
$credentialsFile = Join-Path $avicaPath "config\credentials.ini"

if (Test-Path $credentialsFile) {
    $content = Get-Content $credentialsFile | Where-Object {$_ -match "ID|Password"}
    Write-Host "Avica Connection Credentials (from local config):" -ForegroundColor Green
    $content | ForEach-Object { Write-Host $_ }
} else {
    Write-Host "Credential file not found. Trying to extract info from Avica logs or registry..." -ForegroundColor Yellow
    
    # Example: Check Avica logs or Windows Event logs for connection info
    # Note: Specify actual Avica log location and keywords
    $logPath = Join-Path $avicaPath "logs\connection.log"
    if (Test-Path $logPath) {
        $logContent = Get-Content $logPath | Select-String -Pattern "ID|Password"
        Write-Host "Found the following connection info in logs:" -ForegroundColor Green
        $logContent | ForEach-Object { Write-Host $_ }
    } else {
        Write-Host "No logs found. Consider enabling 'Allow Remote Access' option inside Avica app to view credentials directly." -ForegroundColor Red
    }
}
