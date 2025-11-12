# Validador de Configuracao IDE - Avila Framework
# Verifica se todas configuracoes foram aplicadas corretamente

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  VALIDADOR DE CONFIGURACAO IDE" -ForegroundColor Cyan
Write-Host "  Avila Framework" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

$root = "C:\Users\nicol\OneDrive\Avila"
$errors = 0
$warnings = 0

function Test-FileExists {
    param([string]$Path, [string]$Name)
    
    $fullPath = Join-Path $root $Path
    if (Test-Path $fullPath) {
      Write-Host "[OK] " -NoNewline -ForegroundColor Green
        Write-Host $Name
        return $true
  } else {
        Write-Host "[FALTA] " -NoNewline -ForegroundColor Red
     Write-Host $Name -NoNewline
        Write-Host " ($Path)" -ForegroundColor DarkGray
        $script:errors++
     return $false
    }
}

function Test-FileContent {
    param([string]$Path, [string]$Pattern, [string]$Name)
    
    $fullPath = Join-Path $root $Path
    if (Test-Path $fullPath) {
        $content = Get-Content $fullPath -Raw
        if ($content -match $Pattern) {
          Write-Host "[OK] " -NoNewline -ForegroundColor Green
            Write-Host $Name
      return $true
 } else {
 Write-Host "[AVISO] " -NoNewline -ForegroundColor Yellow
        Write-Host $Name -NoNewline
  Write-Host " (padrao nao encontrado)" -ForegroundColor DarkGray
            $script:warnings++
     return $false
        }
    } else {
        Write-Host "[FALTA] " -NoNewline -ForegroundColor Red
        Write-Host $Name
    $script:errors++
        return $false
    }
}

Write-Host "Validando VS Code..." -ForegroundColor Cyan
Write-Host ""

Test-FileExists ".vscode\avila.code-workspace" "Workspace"
Test-FileExists ".vscode\settings.json" "Settings"
Test-FileExists ".vscode\extensions.json" "Extensions"
Test-FileExists ".vscode\tasks.json" "Tasks"
Test-FileExists ".vscode\launch.json" "Launch Configs"
Test-FileExists ".vscode\avila-snippets.code-snippets" "Snippets"

Write-Host ""
Write-Host "Validando conteudo VS Code..." -ForegroundColor Cyan
Write-Host ""

Test-FileContent ".vscode\settings.json" "avila" "Settings contem config Avila"
Test-FileContent ".vscode\extensions.json" "github.copilot" "Extensions contem Copilot"
Test-FileContent ".vscode\tasks.json" "Archivus" "Tasks contem automacoes Avila"
Test-FileContent ".vscode\avila-snippets.code-snippets" "avila-py-header" "Snippets Avila presentes"

Write-Host ""
Write-Host "Validando Visual Studio 2022..." -ForegroundColor Cyan
Write-Host ""

Test-FileExists ".visualstudio\Avila-VS2022-Settings.vssettings" "VS 2022 Settings"
Test-FileExists ".visualstudio\Avila-VS2022-Components.vsconfig" "VS 2022 Components"

Write-Host ""
Write-Host "Validando documentacao..." -ForegroundColor Cyan
Write-Host ""

Test-FileExists "Setup\CONFIGURACAO_IDES.md" "Guia Configuracao"
Test-FileExists ".github\copilot-instructions.md" "Copilot Instructions"

Write-Host ""
Write-Host "Validando Agente Archivus..." -ForegroundColor Cyan
Write-Host ""

Test-FileExists "AvilaOps\Agente Bibliotecario (Archivus)\config.yaml" "Archivus Config"
Test-FileExists "AvilaOps\Agente Bibliotecario (Archivus)\README.md" "Archivus README"
Test-FileExists "AvilaOps\Agente Bibliotecario (Archivus)\Run-Archivus.ps1" "Archivus Automacao"

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan

if ($errors -eq 0 -and $warnings -eq 0) {
    Write-Host "  STATUS: PERFEITO!" -ForegroundColor Green
    Write-Host "  Todas configuracoes OK" -ForegroundColor Green
} elseif ($errors -eq 0) {
    Write-Host "  STATUS: OK COM AVISOS" -ForegroundColor Yellow
    Write-Host "  $warnings avisos encontrados" -ForegroundColor Yellow
} else {
    Write-Host "  STATUS: INCOMPLETO" -ForegroundColor Red
    Write-Host "  $errors erros, $warnings avisos" -ForegroundColor Red
}

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

if ($errors -eq 0) {
    Write-Host "PROXIMOS PASSOS:" -ForegroundColor Cyan
    Write-Host "1. Abrir workspace: code .vscode\avila.code-workspace"
    Write-Host "2. Instalar extensoes recomendadas"
    Write-Host "3. Testar task: Ctrl+Shift+P > Tasks: Run Task"
Write-Host "4. Testar snippet: criar teste.py > digitar 'avila-py-header'"
    Write-Host ""
}
