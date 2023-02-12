
$apiTokens = Get-Content -Path /run/secrets/apitokens | ConvertFrom-Json
$servers = Get-Content -Path /media/endpoints.json | ConvertFrom-Json

Function gen-params ([string]$endpoint, [string]$msgType, [string]$msg) {
    $reqParams = @{
        uri = "$($servers.$endpoint.uri):$($servers.$endpoint.port)$($msgType)$($msg)&token=$($apiTokens.$endpoint)"
        method = "GET"
        headers = @{accept = "application/json"}
    }
    return $reqParams
}
