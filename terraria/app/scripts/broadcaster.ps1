param([string]$endpoint, [string]$msg)

import-module /media/scripts/common/gen-request-params.psm1

$restartStr = "The server will restart in {0} mins! Be ready to disconnect!"
$broadcastMsgs = @{
    displayDateTime = "The time is: $(Get-Date). Are you still playing?"
    restartWarning15 = $restartStr -f "15"
    restartWarning10 = $restartStr -f "10"
    restartWarning5 = $restartStr -f "5"
    restartWarning1 = $restartStr -f "1"
    restartWarningNow = "!!!!THE SERVER IS RESTARTING NOW!!!!"
}

$apiEndpoints = Get-Content -Path /media/api.endpoints.json | ConvertFrom-Json

$reqParams = gen-params $endpoint $apiEndpoints.broadcast $broadcastMsgs.$msg
$response = Invoke-WebRequest @reqParams
if ($response.StatusCode -ne 200) {
    Write-Host $response.Content
}