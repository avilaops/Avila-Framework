# ÁVILA SYNC - ATALHO RÁPIDO
# Executa o sync center de qualquer lugar

param(
    [string]$Action = "menu"
)

# Diretório base do projeto
$AvilaRoot = "C:\Users\nicol\OneDrive\Avila"
$SyncScript = Join-Path $AvilaRoot "Scripts\sync-center.ps1"

# Verificar se está no diretório correto
if (-not (Test-Path $SyncScript)) {
    Write-Host "❌ Script não encontrado!" -ForegroundColor Red
    Write-Host "📍 Esperado em: $SyncScript" -ForegroundColor Yellow
    exit 1
}

# Mudar para diretório correto
Set-Location $AvilaRoot

Write-Host "🚀 ÁVILA SYNC - EXECUTANDO..." -ForegroundColor Cyan

# Executar script principal
try {
    & $SyncScript
    Write-Host "`n✅ Sync executado com sucesso!" -ForegroundColor Green
}
catch {
    Write-Host "`n❌ Erro na execução: $($_.Exception.Message)" -ForegroundColor Red
}

# Voltar para diretório original
Pop-Location
