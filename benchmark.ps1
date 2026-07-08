# benchmark.ps1Write-Host "`n=== POKRETANJE BENCHMARK TESTOVA ===`n" -ForegroundColor Cyan

function Measure-Build {
    param($Name, $Tag, $Dockerfile, $Context, [switch]$NoCache)

    Write-Host "Build-ujem: $Name ..." -ForegroundColor Yellow

    if ($NoCache) {
        $time = Measure-Command {
            docker build --no-cache -t $Tag -f $Dockerfile $Context *> $null
        }
    } else {
        $time = Measure-Command {
            docker build -t $Tag -f $Dockerfile $Context *> $null
        }
    }

    $seconds = [math]::Round($time.TotalSeconds, 2)
    Write-Host "  Zavrseno za $seconds s" -ForegroundColor Green

    return $seconds
}

function Get-ImageSizeMB {
    param($Tag)
    $sizeStr = docker images --format "{{.Size}}" $Tag | Select-Object -First 1
    return $sizeStr
}

# ===================== FAZA 1: BEZ KESA =====================
Write-Host "`n--- FAZA 1: Build BEZ kesa (--no-cache) ---`n" -ForegroundColor Magenta

$backendOptNoCache    = Measure-Build -Name "Backend optimizovan (bez kesa)"   -Tag "gym-backend-bench-opt"   -Dockerfile "backend/Dockerfile"                -Context "backend/"  -NoCache
$backendNeoptNoCache  = Measure-Build -Name "Backend neoptimizovan (bez kesa)" -Tag "gym-backend-bench-neopt" -Dockerfile "backend/Dockerfile.neoptimizovan"  -Context "backend/"  -NoCache
$frontendOptNoCache   = Measure-Build -Name "Frontend optimizovan (bez kesa)"   -Tag "gym-frontend-bench-opt"   -Dockerfile "frontend/Dockerfile"               -Context "frontend/" -NoCache
$frontendNeoptNoCache = Measure-Build -Name "Frontend neoptimizovan (bez kesa)" -Tag "gym-frontend-bench-neopt" -Dockerfile "frontend/Dockerfile.neoptimizovan" -Context "frontend/" -NoCache

# ===================== FAZA 2: SA KESOM =====================
Write-Host "`n--- FAZA 2: Build SA kesom (koristi kes iz Faze 1) ---`n" -ForegroundColor Magenta

$backendOptCached    = Measure-Build -Name "Backend optimizovan (sa kesom)"   -Tag "gym-backend-bench-opt"   -Dockerfile "backend/Dockerfile"                -Context "backend/"
$backendNeoptCached  = Measure-Build -Name "Backend neoptimizovan (sa kesom)" -Tag "gym-backend-bench-neopt" -Dockerfile "backend/Dockerfile.neoptimizovan"  -Context "backend/"
$frontendOptCached   = Measure-Build -Name "Frontend optimizovan (sa kesom)"   -Tag "gym-frontend-bench-opt"   -Dockerfile "frontend/Dockerfile"               -Context "frontend/"
$frontendNeoptCached = Measure-Build -Name "Frontend neoptimizovan (sa kesom)" -Tag "gym-frontend-bench-neopt" -Dockerfile "frontend/Dockerfile.neoptimizovan" -Context "frontend/"

# ===================== VELICINE =====================
Write-Host "`nMerim velicine image-a..." -ForegroundColor Yellow

$backendOptSize    = Get-ImageSizeMB "gym-backend-bench-opt"
$backendNeoptSize  = Get-ImageSizeMB "gym-backend-bench-neopt"
$frontendOptSize   = Get-ImageSizeMB "gym-frontend-bench-opt"
$frontendNeoptSize = Get-ImageSizeMB "gym-frontend-bench-neopt"

# ===================== TABELA =====================
$table = @(
    [PSCustomObject]@{ Servis = "Backend";  Verzija = "Neoptimizovan"; "Bez kesa (s)" = $backendNeoptNoCache;  "Sa kesom (s)" = $backendNeoptCached;  Velicina = $backendNeoptSize }
    [PSCustomObject]@{ Servis = "Backend";  Verzija = "Optimizovan";   "Bez kesa (s)" = $backendOptNoCache;    "Sa kesom (s)" = $backendOptCached;    Velicina = $backendOptSize }
    [PSCustomObject]@{ Servis = "Frontend"; Verzija = "Neoptimizovan"; "Bez kesa (s)" = $frontendNeoptNoCache; "Sa kesom (s)" = $frontendNeoptCached; Velicina = $frontendNeoptSize }
    [PSCustomObject]@{ Servis = "Frontend"; Verzija = "Optimizovan";   "Bez kesa (s)" = $frontendOptNoCache;   "Sa kesom (s)" = $frontendOptCached;   Velicina = $frontendOptSize }
)

Write-Host "`n=== REZULTATI ===`n" -ForegroundColor Cyan
$table | Format-Table -AutoSize

$table | Format-Table -AutoSize | Out-String | Out-File -FilePath "benchmark_rezultati.txt"
Write-Host "Rezultati sacuvani i u benchmark_rezultati.txt`n" -ForegroundColor Green

# ===================== CISCENJE =====================
Write-Host "Da li zelis da obrises test image-e kreirane ovom skriptom? (y/n)" -ForegroundColor Yellow
$cleanup = Read-Host
if ($cleanup -eq "y") {
    docker rmi gym-backend-bench-opt gym-backend-bench-neopt gym-frontend-bench-opt gym-frontend-bench-neopt -f
    Write-Host "Test image-i obrisani." -ForegroundColor Green
}