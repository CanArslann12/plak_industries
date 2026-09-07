$ErrorActionPreference = 'Stop'
$project = Split-Path -Parent $MyInvocation.MyCommand.Path
$envPath = Join-Path $project '.env'
$examplePath = Join-Path $project '.env.example'

if (-not (Test-Path $envPath)) {
    Copy-Item $examplePath $envPath
}

$provider = Read-Host 'AI saglayicisi (varsayilan: groq)'
if ([string]::IsNullOrWhiteSpace($provider)) { $provider = 'groq' }
$apiKeySecure = Read-Host 'API anahtarini girin (ekranda gosterilmez)' -AsSecureString
$apiKeyPtr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($apiKeySecure)
try {
    $apiKey = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($apiKeyPtr)
}
finally {
    [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($apiKeyPtr)
}

if ([string]::IsNullOrWhiteSpace($apiKey)) {
    throw 'API anahtari bos birakilamaz.'
}

$content = Get-Content $envPath | Where-Object { $_ -notmatch '^GROQ_API_KEY=' -and $_ -notmatch '^AI_PROVIDER=' }
$content += "GROQ_API_KEY=$apiKey"
$content += "AI_PROVIDER=$provider"
Set-Content -Path $envPath -Value $content -Encoding utf8

Write-Host ''
Write-Host 'API ayari kaydedildi. Uygulamayi masaustu kisayolundan yeniden baslatin.' -ForegroundColor Green
Read-Host 'Kapatmak icin Enter'
