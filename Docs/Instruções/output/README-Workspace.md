# WORKSPACE DOCUMENTATION

## Visão Geral
Este workspace contém documentação técnica e scripts de automação para consolidação de documentos.

## Estrutura de Diretórios
- **Templates**: .\templates - **Cache**: .\cache - **Logs**: .\logs - **Output**: .\output - **Scripts**: .\scripts - **Backup**: .\backup -join "
")

## Scripts Principais
- **DocumentDirector.ps1**: Script principal de direcionamento
- **Consolidate-Documents.ps1**: Consolidação automática de documentos
- **consolidation-config.ps1**: Arquivo de configuração

## Uso Rápido
`powershell
# Executar menu principal
.\DocumentDirector.ps1

# Consolidação direta
.\DocumentDirector.ps1 -Action "consolidate"

# Limpeza do workspace
.\DocumentDirector.ps1 -Action "cleanup"
`

## Configuração
Edite o arquivo \consolidation-config.ps1\ para personalizar o comportamento dos scripts.

## Suporte
Para dúvidas ou problemas, verifique os logs em \.\logs\ ou execute o dashboard para diagnóstico.

---
**Última atualização**: 10/11/2025 18:20:26
