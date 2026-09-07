$ErrorActionPreference = 'Stop'
$project = Split-Path -Parent $MyInvocation.MyCommand.Path
$envPath = Join-Path $project '.env'
$wixPagePath = Join-Path $project 'wix\page.js'

function Normalize-Url([string] $value) {
    $url = $value.Trim()
    if (-not $url.StartsWith('http://') -and -not $url.StartsWith('https://')) {
        $url = "https://$url"
    }
    return $url.TrimEnd('/')
}

$siteDomain = Read-Host 'Wix alan adinizi girin (ornek: www.plakindustries.com)'
if ([string]::IsNullOrWhiteSpace($siteDomain)) { throw 'Wix alan adi bos birakilamaz.' }
$siteUrl = Normalize-Url $siteDomain

$backendUrl = Read-Host 'Canli Flask backend adresini girin (Render adresi)'
if ([string]::IsNullOrWhiteSpace($backendUrl)) { throw 'Backend adresi bos birakilamaz.' }
$backendUrl = Normalize-Url $backendUrl

if (-not (Test-Path $envPath)) { throw '.env dosyasi bulunamadi.' }
$envLines = Get-Content $envPath | Where-Object { $_ -notmatch '^CORS_ORIGINS=' }
$envLines += "CORS_ORIGINS=$siteUrl"
Set-Content -Path $envPath -Value $envLines -Encoding utf8

$page = Get-Content $wixPagePath -Raw
$page = [regex]::Replace($page, "const BACKEND_URL = '[^']*';", "const BACKEND_URL = '$backendUrl';")
Set-Content -Path $wixPagePath -Value $page -Encoding utf8

Write-Host ''
Write-Host 'Alan adi ve backend ayarlari kaydedildi.' -ForegroundColor Green
Write-Host "Wix alani: $siteUrl"
Write-Host "Backend: $backendUrl"
Write-Host 'Uygulamayi yeniden baslatin; wix/page.js kodunu Wix Velo sayfa koduna yapistirin.'
Read-Host 'Kapatmak icin Enter'
