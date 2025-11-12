# ?? Relatórios e Análises - Projeto Ávila

**Localização Padrão:** `Docs/Relatorios/`

---

## ?? Estrutura de Pastas

```
Docs/Relatorios/
??? Analises/          # Análises técnicas e estratégicas
??? Auditorias/# Auditorias de conformidade e segurança
??? Diagnosticos/      # Diagnósticos de sistemas
??? Performance/       # Relatórios de performance
??? Comparacoes/       # Comparações entre versões/sistemas
```

---

## ?? Padrão de Nomenclatura

### Formato Geral:
```
TIPO_NOME-DESCRITIVO_vVERSAO_DATA.md
```

### Exemplos:
- `ANALISE_PROJETO_AVILA_v2.0_2025-11-10.md`
- `AUDITORIA_SEGURANCA_v1.0_2025-11-10.md`
- `DIAGNOSTICO_PERFORMANCE_v1.5_2025-11-10.md`
- `PERFIL_PRODUCAO_v3.2_2025-11-10.md`

---

## ??? Tipos de Documentos

| Tipo | Descrição | Pasta | Exemplo |
|------|-----------|-------|---------|
| **ANALISE** | Análise geral de projeto/sistema | `Analises/` | Análise arquitetural completa |
| **AUDITORIA** | Auditoria de conformidade/segurança | `Auditorias/` | Auditoria de código, compliance |
| **DIAGNOSTICO** | Diagnóstico de problemas específicos | `Diagnosticos/` | Debug de performance, erros |
| **PERFIL** | Perfil de uso/performance | `Performance/` | Perfil de memória, CPU |
| **COMPARACAO** | Comparação entre versões/sistemas | `Comparacoes/` | Before/After, benchmarks |

---

## ?? Como Salvar Análises

### Opção 1: Manual (Recomendado)
```powershell
# Mover arquivo para pasta padrão
Move-Item -Path "ANALISE.md" -Destination "Docs/Relatorios/Analises/ANALISE_NOME_v1.0_2025-11-10.md"
```

### Opção 2: Script Python (Futuro)
```bash
python Shared/scripts/salvar_analise.py ANALISE.md
```

### Opção 3: Copilot
> "Salve esta análise na pasta padrão Ávila"

---

## ?? Checklist para Nova Análise

Antes de salvar uma análise, verifique:

- [ ] Nome segue padrão: `TIPO_NOME_vVERSAO_DATA.md`
- [ ] Documento tem cabeçalho com:
  - [ ] Título
  - [ ] Data da análise
  - [ ] Analista/Autor
  - [ ] Versão
  - [ ] Status (Rascunho/Revisão/Aprovado)
- [ ] Markdown válido (sem erros de formatação)
- [ ] Salvo na pasta correta:
  - Análise geral ? `Analises/`
  - Auditoria ? `Auditorias/`
  - Diagnóstico ? `Diagnosticos/`
  - Performance ? `Performance/`
  - Comparação ? `Comparacoes/`
- [ ] Referências externas funcionando (links, imagens)

---

## ?? Buscando Análises

### Por Data:
```powershell
Get-ChildItem -Path "Docs/Relatorios/Analises" | Where-Object { $_.Name -like "*2025-11*" }
```

### Por Tipo:
```powershell
Get-ChildItem -Path "Docs/Relatorios/Analises" | Where-Object { $_.Name -like "ANALISE*" }
```

### Por Versão:
```powershell
Get-ChildItem -Path "Docs/Relatorios/Analises" | Where-Object { $_.Name -like "*v2.0*" }
```

---

## ?? Análises Recentes

*(Será atualizado automaticamente quando houver script de indexação)*

---

## ?? Governança

### Retenção:
- **Análises Gerais:** 2 anos
- **Auditorias:** 5 anos (compliance)
- **Diagnósticos:** 1 ano
- **Performance:** 6 meses
- **Comparações:** 1 ano

### Versionamento:
- **v1.0**: Primeira versão (rascunho)
- **v1.x**: Revisões menores (correções, atualizações)
- **v2.0+**: Revisões maiores (mudanças estruturais)

### Aprovação:
- **Rascunho**: Em desenvolvimento
- **Revisão**: Aguardando revisão
- **Aprovado**: Validado e oficial

---

## ?? Contato

Para dúvidas sobre padrões de relatórios:
- **Governança:** `AvilaInc/governance_framework/`
- **Documentação Técnica:** `Docs/OnKnowledge/`
- **Scripts:** `Shared/scripts/`

---

**Última atualização:** 2025-11-10  
**Responsável:** Ávila Ops - Governança
