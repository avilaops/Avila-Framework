
Vamos padronizar um atalho para criação de imagens tanto dos agentes quanto de marketing dos produtos e de soluções

###### O ChatGPT disse:

Segue um padrão único de **Atalho iOS “Ávila: Criar Imagem”** para agentes, produtos e soluções.

## Entradas

- **Tipo**: `Agente | Produto | Solução`
    
- **Estilo**: `Pintura a Óleo | Aquarela | Vetor | Animê | 3D Render | Fotoreal | Isométrico | Flat UI`
    
- **Assunto**: texto livre
    
- **Formato**: `1:1 | 16:9 | 9:16 | 4:5`
    
- **Tamanho**: `1024 | 1536 | 2048` px
    
- **BG Transparente**: `Sim/Não`
    
- **Destino**: `Fotos | OneDrive/Ávila/Marketing/Renders | iCloud Drive/Shortcuts/Ávila`
    

## Variáveis do atalho

- `vTipo`, `vEstilo`, `vAssunto`, `vFormato`, `vTamanho`, `vBG`, `vDestino`.
    
- `vData` = Data atual `yyyyMMdd-HHmm`.
    
- `vSlug` = `vAssunto` → minúsculas → substituir espaços por `-` → remover acentos.
    
- `vNomeArquivo` = `vData`-`vTipo`-`vSlug`-`vEstilo`-`vFormato`.`png`.
    

## Prompt base (montado em um bloco “Texto”)

Use exatamente um destes templates conforme `vTipo`:

**Agente (ícone/mascote)**

`Crie uma ilustração no estilo {{vEstilo}} de um agente chamado “{{vAssunto}}”. Direção: busto frontal, luz limpa, contornos nítidos, alta legibilidade em 128–256 px. Paleta Ávila: #0077FF, #00E0FF, #0B0F17, branco. Cenário neutro, foco no personagem. Sem texto. Sem marca d’água. Composição centrada, espaço negativo para recorte.`

**Produto (hero/ads)**

`Crie uma imagem de marketing para o produto “{{vAssunto}}” em {{vEstilo}}. Direção: foco no produto, fundo limpo, contraste forte, áreas para sobreposição de copy. Paleta Ávila: #0077FF, #00E0FF, #0B0F17, branco. Estética premium, luz suave, reflexos sutis. Sem logotipo incorporado, sem texto.`

**Solução (diagrama/serviço)**

`Crie um visual explicativo em {{vEstilo}} para a solução “{{vAssunto}}”. Direção: ícones coerentes, setas discretas, hierarquia clara, sensação corporativa. Paleta Ávila: #0077FF, #00E0FF, #0B0F17, branco. Sem rótulos de texto. Sem marca d’água. Fundo clean.`

Ao final do bloco, acrescente:

`Formato: {{vFormato}}. Tamanho: {{vTamanho}}px. Fundo transparente: {{vBG}}.`

## Passo a passo no **Atalhos**

1. **Perguntar** “Tipo” → menu com as 3 opções → guardar em `vTipo`.
    
2. **Perguntar** “Estilo” → menu com as opções listadas → `vEstilo`.
    
3. **Pedir Entrada de Texto** “Assunto” → `vAssunto`.
    
4. **Escolher no Menu** “Formato” → `vFormato`.
    
5. **Escolher no Menu** “Tamanho (px)” → `vTamanho`.
    
6. **Escolher no Menu** “Fundo Transparente?” → `vBG` = `Sim/Não`.
    
7. **Definir Data Atual** → `vData`.
    
8. **Gerar Slug**
    
    - Ação “Substituir Texto”: espaços→`-`
        
    - “Transformar Texto”: minúsculas
        
    - (opcional) “Remover Acentos” usando “Alternar Caso/Remover Diacríticos” → `vSlug`.
        
9. **Texto** → cole o _Prompt base_ correspondente usando as variáveis.
    
10. **Criar Imagem (ChatGPT)**
    
    - **Prompt**: conteúdo do passo 9.
        
    - **Estilo**: usar variável `vEstilo` no campo Estilo.
        
    - **Tamanho**: `vTamanho`.
        
    - **Transparência**: `vBG` = Sim.
        
11. **Definir Nome de Arquivo** = `vNomeArquivo`.
    
12. **Salvar Arquivo**
    
    - Se `Destino = Fotos`: “Salvar em Álbuns” → Álbum “Ávila Renders”.
        
    - Se `Destino = OneDrive`: “Salvar Arquivo” → escolher `OneDrive/Ávila/Marketing/Renders/{{vTipo}}/`.
        
    - Se `Destino = iCloud`: `iCloud Drive/Shortcuts/Ávila/Renders/{{vTipo}}/`.
        
13. **Compartilhar** (opcional) → Folha de Compartilhamento.
    
14. **Log** (opcional) → Acrescentar linha em `OneDrive/Ávila/Logs/renders.csv` com:  
    `vData,vTipo,vEstilo,vAssunto,vFormato,vTamanho,vBG,vNomeArquivo`.
    

## Boas práticas

- **Presets**: crie três sub-atalhos que só predefinem `vFormato` e `vTamanho`:  
    Social 1:1 (2048), Story 9:16 (1536×2732), Banner 16:9 (2048×1152).
    
- **Padronização de cor**: mantenha a paleta no prompt. Ajuste se a peça exigir contraste diferente.
    
- **Nomeação** consistente garante busca rápida no OneDrive e no Obsidian.
    

## Extensões opcionais

- **Rodar em lote**: “Repetir com Cada Item” sobre uma lista de assuntos.
    
- **Registro no Obsidian**: “Anexar a Arquivo” em `Ávila/Docs/Design/renders.md` com miniatura e metadados.
    
- **Validação**: se `vAssunto` < 3 palavras, mostrar alerta e cancelar.
    

Se quiser, descrevo a árvore completa do atalho com cada ação numerada para você montar em 3 minutos.

O ChatGPT pode cometer erros. Por isso, lembre-se de conferir informações relevantes.