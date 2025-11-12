# ?? Guia Rápido: Salvamento de Análises

## ?? Objetivo

Padronizar o salvamento de análises, relatórios e documentos técnicos na estrutura Ávila.

---

## ?? Onde Salvar?

Todas as análises devem ser salvas em: **`Docs/Relatorios/`**

### Subpastas por Tipo:

| Tipo de Documento | Pasta | Exemplo |
|-------------------|-------|---------|
| Análise Geral | `Analises/` | Análise arquitetural, review de código |
| Auditoria | `Auditorias/` | Auditoria de segurança, compliance |
| Diagnóstico | `Diagnosticos/` | Debug, troubleshooting |
| Performance | `Performance/` | Benchmarks, profiling |
| Comparação | `Comparacoes/` | Before/After, A/B testing |

---

## ?? Métodos de Salvamento

### Método 1: Script PowerShell (Recomendado)

```powershell
# Na raiz do projeto Ávila
.\Shared\scripts\Salvar-Analise.ps1 -Arquivo "MINHA_ANALISE.md" -Tipo "ANALISE" -Versao "1.0"
```

**Parâmetros:**
- `-Arquivo`: Caminho do arquivo (obrigatório)
- `-Tipo`: ANALISE | AUDITORIA | DIAGNOSTICO | PERFIL | COMPARACAO (padrão: ANALISE)
- `-Versao`: Versão manual (padrão: timestamp automático)

### Método 2: Manual (PowerShell)

```powershell
# Mover para pasta correta
Move-Item -Path "ANALISE.md" -Destination "Docs/Relatorios/Analises/ANALISE_PROJETO_v1.0_2025-11-10.md"
```

### Método 3: Copilot

> "Salve esta análise na pasta padrão Ávila com tipo ANALISE e versão 2.0"

---

## ?? Padrão de Nomenclatura

### Formato:
```
TIPO_NOME-DESCRITIVO_vVERSAO_DATA.md
```

### Exemplos Válidos:
```
ANALISE_PROJETO_AVILA_v2.0_2025-11-10.md
AUDITORIA_SEGURANCA_v1.0_2025-11-15.md
DIAGNOSTICO_PERFORMANCE_API_v1.5_2025-11-20.md
PERFIL_MEMORIA_PRODUCAO_v3.2_2025-11-25.md
COMPARACAO_V1_VS_V2_v1.0_2025-11-30.md
```

### Exemplos Inválidos:
```
? analise.md (falta tipo, versão, data)
? Minha Analise.md (espaços, falta padrão)
? ANALISE-2025.md (falta nome descritivo)
```

---

## ? Checklist Pré-Salvamento

Antes de salvar, verifique:

- [ ] **Cabeçalho completo:**
  ```markdown
  # ?? TÍTULO DA ANÁLISE
  
  **Data:** 2025-11-10
  **Analista:** Nome
  **Versão:** 1.0
  **Status:** Rascunho | Revisão | Aprovado
  ```

- [ ] **Seções principais:**
  - [ ] Sumário Executivo
  - [ ] Contexto
  - [ ] Análise/Diagnóstico
  - [ ] Conclusões
  - [ ] Recomendações
  - [ ] Próximos Passos

- [ ] **Formatação:**
  - [ ] Markdown válido
  - [ ] Links funcionando
  - [ ] Imagens referenciadas corretamente
  - [ ] Code blocks com syntax highlighting

- [ ] **Metadados:**
  - [ ] Nome segue padrão
  - [ ] Tipo correto
  - [ ] Versão definida
  - [ ] Data incluída

---

## ?? Buscando Análises Salvas

### Listar Todas:
```powershell
Get-ChildItem -Path "Docs/Relatorios" -Recurse -Filter "*.md" | Select-Object Name, Directory, Length, LastWriteTime
```

### Por Tipo:
```powershell
Get-ChildItem -Path "Docs/Relatorios/Analises" -Filter "ANALISE*.md"
```

### Por Data:
```powershell
Get-ChildItem -Path "Docs/Relatorios/Analises" | Where-Object { $_.Name -like "*2025-11*" }
```

### Mais Recentes:
```powershell
Get-ChildItem -Path "Docs/Relatorios/Analises" -Filter "*.md" | Sort-Object LastWriteTime -Descending | Select-Object -First 5
```

---

## ?? Exemplos Práticos

### Exemplo 1: Salvar Análise Completa
```powershell
# Após criar análise em ANALISE_SISTEMA.md
.\Shared\scripts\Salvar-Analise.ps1 -Arquivo "ANALISE_SISTEMA.md" -Tipo "ANALISE" -Versao "1.0"

# Resultado:
# ? Salvo em: Docs/Relatorios/Analises/ANALISE_ANALISE_SISTEMA_v1.0_2025-11-10.md
```

### Exemplo 2: Salvar Auditoria de Segurança
```powershell
.\Shared\scripts\Salvar-Analise.ps1 -Arquivo "AUDITORIA_SEC.md" -Tipo "AUDITORIA" -Versao "2.0"

# Resultado:
# ? Salvo em: Docs/Relatorios/Auditorias/AUDITORIA_AUDITORIA_SEC_v2.0_2025-11-10.md
```

### Exemplo 3: Diagnóstico Urgente (timestamp automático)
```powershell
.\Shared\scripts\Salvar-Analise.ps1 -Arquivo "BUG_CRITICO.md" -Tipo "DIAGNOSTICO"

# Resultado:
# ? Salvo em: Docs/Relatorios/Diagnosticos/DIAGNOSTICO_BUG_CRITICO_v2025-11-10_143022.md
```

---

## ?? Troubleshooting

### Erro: "Arquivo não encontrado"
```powershell
# Verificar caminho correto
Get-Location  # Ver pasta atual
Get-Item "ARQUIVO.md"  # Verificar se arquivo existe
```

### Erro: "Pasta não existe"
```powershell
# Criar estrutura manualmente
New-Item -Path "Docs/Relatorios/Analises" -ItemType Directory -Force
```

### Nome de arquivo muito longo
```
# Usar abreviações:
ANALISE_PROJ_AVILA_v1.0_2025-11-10.md  # ?
```

---

## ?? Suporte

Para dúvidas:
- **Documentação:** `Docs/Relatorios/README.md`
- **Script:** `Shared/scripts/Salvar-Analise.ps1`
- **Governança:** `AvilaInc/governance_framework/procedimentos/`

---

**Última atualização:** 2025-11-10  
**Mantenedor:** Ávila Ops - Governança
