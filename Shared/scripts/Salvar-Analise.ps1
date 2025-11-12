# Script para salvar analises automaticamente na pasta padrao Avila
# Uso: .\Salvar-Analise.ps1 -Arquivo "ANALISE.md" -Tipo "ANALISE"

param(
    [Parameter(Mandatory=$true)]
    [string]$Arquivo,
    
    [Parameter(Mandatory=$false)]
    [ValidateSet("ANALISE", "AUDITORIA", "DIAGNOSTICO", "PERFIL", "COMPARACAO")]
    [string]$Tipo = "ANALISE",
    
    [Parameter(Mandatory=$false)]
    [string]$Versao = $null
)

# Configuracoes
$WorkspaceRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$PastaRelatorios = Join-Path $WorkspaceRoot "Docs\Relatorios"

$PastasPorTipo = @{
    "ANALISE"     = "Analises"
    "AUDITORIA"   = "Auditorias"
    "DIAGNOSTICO" = "Diagnosticos"
    "PERFIL"      = "Performance"
    "COMPARACAO"  = "Comparacoes"
}

$PastaDestino = Join-Path $PastaRelatorios $PastasPorTipo[$Tipo]

# Verificar se arquivo existe
if (-not (Test-Path $Arquivo)) {
    Write-Error "Erro: Arquivo nao encontrado: $Arquivo"
    exit 1
}

# Gerar nome padronizado
$Timestamp = Get-Date -Format "yyyy-MM-dd_HHmmss"
$VersaoStr = if ($Versao) { $Versao } else { $Timestamp }

$ArquivoInfo = Get-Item $Arquivo
$NomeBase = $ArquivoInfo.BaseName
$Extensao = $ArquivoInfo.Extension

# Formato: TIPO_NOME_vVERSAO.md
$NomeDestino = "${Tipo}_${NomeBase}_v${VersaoStr}${Extensao}"
$CaminhoDestino = Join-Path $PastaDestino $NomeDestino

# Criar pasta se não existir
if (-not (Test-Path $PastaDestino)) {
    New-Item -Path $PastaDestino -ItemType Directory -Force | Out-Null
}

# Copiar arquivo
try {
    Copy-Item -Path $Arquivo -Destination $CaminhoDestino -Force
    
    $TamanhoKB = [math]::Round((Get-Item $CaminhoDestino).Length / 1KB, 2)
    $CaminhoRelativo = $CaminhoDestino.Replace($WorkspaceRoot, "").TrimStart('\')
    
    Write-Host "? Analise salva com sucesso!" -ForegroundColor Green
    Write-Host "?? Local: $CaminhoRelativo" -ForegroundColor Cyan
    Write-Host "?? Tamanho: $TamanhoKB KB" -ForegroundColor Cyan
    
    # Atualizar indice (simples)
    Atualizar-Indice -PastaDestino $PastaDestino
    
    return $true
}
catch {
    Write-Error "Erro ao salvar: $_"
  return $false
}

function Atualizar-Indice {
    param([string]$PastaDestino)
    
    $ReadmePath = Join-Path $PastaDestino "README.md"
 $Analises = Get-ChildItem -Path $PastaDestino -Filter "*.md" | Where-Object { $_.Name -ne "README.md" } | Sort-Object LastWriteTime -Descending
    
    $Conteudo = @"
# $($PastasPorTipo.Keys | Where-Object { $PastasPorTipo[$_] -eq (Split-Path $PastaDestino -Leaf) }) - Projeto Avila

**Ultima atualizacao:** $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")

## Documentos Disponiveis ($($Analises.Count))

"@
    
    if ($Analises.Count -gt 0) {
        $Conteudo += "`n| Data | Arquivo | Tamanho |`n"
  $Conteudo += "|------|---------|---------|`n"
     
        foreach ($Analise in $Analises) {
    $DataMod = $Analise.LastWriteTime.ToString("yyyy-MM-dd HH:mm")
          $TamanhoKB = [math]::Round($Analise.Length / 1KB, 2)
  
            $Conteudo += "| $DataMod | [$($Analise.Name)](./$($Analise.Name)) | $TamanhoKB KB |`n"
        }
    }
    else {
        $Conteudo += "`n*Nenhum documento ainda.*`n"
    }
    
    $Conteudo += "`n---`n`n**Gerado automaticamente por:** ``Shared/scripts/Salvar-Analise.ps1```n"
  
  Set-Content -Path $ReadmePath -Value $Conteudo -Encoding UTF8
    Write-Host "?? Indice atualizado!" -ForegroundColor Yellow
}
