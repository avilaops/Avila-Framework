---
title: "Optimize Prompts | OpenAI Cookbook"
source: "https://cookbook.openai.com/examples/optimize_prompts#1-system-overview"
author:
published:
created: 2025-11-10
description: "Crafting effective prompts is a critical skill when working with AI models. Even experienced users can inadvertently introduce contradict..."
tags:
  - "clippings"
---
### 14 de julho de 2025

## Otimizar prompts

[Abrir no GitHub](https://github.com/openai/openai-cookbook/blob/main/examples/Optimize_Prompts.ipynb) [Exibir como Markdown](https://nbviewer.org/format/script/github/openai/openai-cookbook/blob/main/examples/Optimize_Prompts.ipynb)

Criar prompts eficazes é uma habilidade crítica ao trabalhar com modelos de IA. Mesmo usuários experientes podem inadvertidamente introduzir contradições, ambiguidades ou inconsistências que levam a resultados abaixo do ideal. O sistema demonstrado aqui ajuda a identificar e corrigir problemas comuns, resultando em prompts mais confiáveis e eficazes.

O processo de otimização usa uma abordagem multiagente com agentes de IA especializados colaborando para analisar e reescrever prompts. O sistema identifica e resolve automaticamente vários tipos de problemas comuns:

- **Contradições nas instruções imediatas**
- **Especificações de formato** ausentes ou pouco claras
- **Inconsistências** entre o prompt e os exemplos de poucos disparos

---

**Objetivo**: Este livro de receitas demonstra as melhores práticas para usar o Agents SDK junto com o Evals para criar uma versão inicial do sistema de otimização de prompt da OpenAI. Você pode otimizar seu prompt usando este código ou usar o otimizador [em nosso playground!](https://platform.openai.com/playground/prompts)

Pergunte ao ChatGPT

**Estrutura do**  
livro de receitas Este caderno segue esta estrutura:

- [Passo 1. Visão geral do sistema](https://cookbook.openai.com/examples/#1-system-overview) - Saiba como funciona o sistema de otimização imediata
- [Etapa 2. Modelos de dados](https://cookbook.openai.com/examples/#2-data-models) - Entenda as estruturas de dados usadas pelo sistema
- [Etapa 3. Definindo os agentes](https://cookbook.openai.com/examples/#3-defining-the-agents) - Veja os agentes que analisam e melhoram os prompts
- [Etapa 4. Avaliações](https://cookbook.openai.com/examples/#4-using-evaluations-to-arrive-at-these-agents) - Use o Evals para verificar nossa escolha e instruções de modelo de agente
- [Etapa 5. Executar fluxo de trabalho de otimização](https://cookbook.openai.com/examples/#4-run-optimization-workflow) - Veja como o fluxo de trabalho entrega os prompts
- [Etapa 6. Exemplos](https://cookbook.openai.com/examples/#5-examples) - Explore exemplos reais de otimização imediata

**Pré-requisitos**

- O pacote Python `openai`
- O pacote `openai-agents`
- Uma chave de API OpenAI definida como em suas variáveis de ambiente `OPENAI_API_KEY`

## 1\. Visão geral do sistema

O sistema de otimização de prompt usa uma abordagem multiagente colaborativa para analisar e melhorar os prompts. Cada agente é especializado em detectar ou reescrever um tipo específico de problema:

1. **Dev-Contradiction-Checker**: Verifica o prompt em busca de contradições lógicas ou instruções impossíveis, como "usar apenas números positivos" e "incluir exemplos negativos" no mesmo prompt.
2. **Verificador de formato**: identifica quando um prompt espera uma saída estruturada (como JSON, CSV ou Markdown), mas não especifica claramente os requisitos exatos de formato. Esse agente garante que todos os campos, tipos de dados e regras de formatação necessários sejam definidos explicitamente.
3. **Verificador de consistência de poucos tiros**: examina exemplos de conversas para garantir que as respostas do assistente realmente sigam as regras especificadas no prompt. Isso detecta incompatibilidades entre o que o prompt requer e o que os exemplos demonstram.
4. **Dev-Rewriter**: depois que os problemas são identificados, esse agente reescreve o prompt para resolver contradições e esclarecer as especificações de formato, preservando a intenção original.
5. **Few-Shot-Rewriter**: atualiza respostas de exemplo inconsistentes para se alinhar às regras no prompt, garantindo que todos os exemplos estejam em conformidade com o novo prompt do desenvolvedor.

Trabalhando juntos, esses agentes podem identificar e corrigir sistematicamente problemas em prompts.

```
# Import required modules

from openai import AsyncOpenAI

import asyncio

import json

import os

from enum import Enum

from typing import Any, List, Dict

from pydantic import BaseModel, Field

from agents import Agent, Runner, set_default_openai_client, trace

openai_client: AsyncOpenAI | None = None

def _get_openai_client() -> AsyncOpenAI:

    global openai_client

    if openai_client is None:

        openai_client = AsyncOpenAI(

            api_key=os.environ.get("OPENAI_API_KEY", "your-api-key"),

        )

    return openai_client

set_default_openai_client(_get_openai_client())
```

## 2\. Modelos de dados

Para facilitar a comunicação estruturada entre os agentes, o sistema utiliza modelos Pydantic para definir o formato esperado para entradas e saídas. Esses modelos Pydantic ajudam a validar dados e garantir a consistência em todo o fluxo de trabalho.

Os modelos de dados incluem:

1. **Função** - Uma enumeração para funções de mensagem (usuário/assistente)
2. **ChatMessage** - Representa uma única mensagem em uma conversa
3. **Problemas** - Modelo base para relatar problemas detectados
4. **FewShotIssues** - Modelo estendido que adiciona sugestões de reescrita para mensagens de exemplo
5. **MessagesOutput** - Contém mensagens de conversa otimizadas
6. **DevRewriteOutput** - Contém o prompt do desenvolvedor aprimorado

O uso do Pydantic permite que o sistema valide se todos os dados estão em conformidade com o formato esperado em cada etapa do processo.

```
class Role(str, Enum):

    """Role enum for chat messages."""

    user = "user"

    assistant = "assistant"

class ChatMessage(BaseModel):

    """Single chat message used in few-shot examples."""

    role: Role

    content: str

class Issues(BaseModel):

    """Structured output returned by checkers."""

    has_issues: bool

    issues: List[str]

    

    @classmethod

    def no_issues(cls) -> "Issues":

        return cls(has_issues=False, issues=[])

class FewShotIssues(Issues):

    """Output for few-shot contradiction detector including optional rewrite suggestions."""

    rewrite_suggestions: List[str] = Field(default_factory=list)

    

    @classmethod

    def no_issues(cls) -> "FewShotIssues":

        return cls(has_issues=False, issues=[], rewrite_suggestions=[])

class MessagesOutput(BaseModel):

    """Structured output returned by \`rewrite_messages_agent\`."""

    messages: list[ChatMessage]

class DevRewriteOutput(BaseModel):

    """Rewriter returns the cleaned-up developer prompt."""

    new_developer_message: str
```

## 3\. Definindo os Agentes

Nesta seção, criamos agentes de IA especializados usando a classe do pacote. Observar essas definições de agente revela várias práticas recomendadas para criar instruções de IA eficazes:`Agent` `openai-agents`

### Práticas recomendadas em instruções do agente

1. **Definição de escopo clara**: cada agente tem um propósito estritamente definido com limites explícitos. Por exemplo, o verificador de contradições se concentra apenas em "autocontradições genuínas" e afirma explicitamente que "sobreposições ou redundâncias não são contradições".
2. **Processo passo a passo**: as instruções fornecem uma metodologia clara, como a forma como o verificador de formato primeiro categoriza a tarefa antes de analisar os requisitos de formato.
3. **Definições explícitas**: Os termos-chave são definidos com precisão para evitar ambiguidade. O verificador de consistência de poucos disparos inclui uma "Rubrica de Conformidade" detalhada explicando exatamente o que constitui conformidade.
4. **Configuração de limite**: As instruções especificam o que o agente NÃO deve fazer. O verificador de poucos tiros lista explicitamente o que está "fora do escopo" para evitar problemas de sinalização excessiva.
5. **Requisitos de saída estruturada**: cada agente tem um formato de saída estritamente definido com exemplos, garantindo consistência no pipeline de otimização.

Esses princípios criam agentes confiáveis e focados que trabalham efetivamente juntos no sistema de otimização. Abaixo, vemos as definições completas do agente com suas instruções detalhadas.

```
dev_contradiction_checker = Agent(

    name="contradiction_detector",

    model="gpt-4.1",

    output_type=Issues,

    instructions="""

    You are **Dev-Contradiction-Checker**.

    Goal

    Detect *genuine* self-contradictions or impossibilities **inside** the developer prompt supplied in the variable \`DEVELOPER_MESSAGE\`.

    Definitions

    • A contradiction = two clauses that cannot both be followed.

    • Overlaps or redundancies in the DEVELOPER_MESSAGE are *not* contradictions.

    What you MUST do

    1. Compare every imperative / prohibition against all others.

    2. List at most FIVE contradictions (each as ONE bullet).

    3. If no contradiction exists, say so.

    Output format (**strict JSON**)

    Return **only** an object that matches the \`Issues\` schema:

    \`\`\`json

    {"has_issues": <bool>,

    "issues": [

        "<bullet 1>",

        "<bullet 2>"

    ]

    }

    - has_issues = true IFF the issues array is non-empty.

    - Do not add extra keys, comments or markdown.

""",

)

format_checker = Agent(

    name="format_checker",

    model="gpt-4.1",

    output_type=Issues,

    instructions="""

    You are Format-Checker.

    Task

    Decide whether the developer prompt requires a structured output (JSON/CSV/XML/Markdown table, etc.).

    If so, flag any missing or unclear aspects of that format.

    Steps

    Categorise the task as:

    a. "conversation_only", or

    b. "structured_output_required".

    For case (b):

    - Point out absent fields, ambiguous data types, unspecified ordering, or missing error-handling.

    Do NOT invent issues if unsure. be a little bit more conservative in flagging format issues

    Output format

    Return strictly-valid JSON following the Issues schema:

    {

    "has_issues": <bool>,

    "issues": ["<desc 1>", "..."]

    }

    Maximum five issues. No extra keys or text.

""",

)

fewshot_consistency_checker = Agent(

    name="fewshot_consistency_checker",

    model="gpt-4.1",

    output_type=FewShotIssues,

    instructions="""

    You are FewShot-Consistency-Checker.

    Goal

    Find conflicts between the DEVELOPER_MESSAGE rules and the accompanying **assistant** examples.

    USER_EXAMPLES:      <all user lines>          # context only

    ASSISTANT_EXAMPLES: <all assistant lines>     # to be evaluated

    Method

    Extract key constraints from DEVELOPER_MESSAGE:

    - Tone / style

    - Forbidden or mandated content

    - Output format requirements

    Compliance Rubric - read carefully

    Evaluate only what the developer message makes explicit.

    Objective constraints you must check when present:

    - Required output type syntax (e.g., "JSON object", "single sentence", "subject line").

    - Hard limits (length ≤ N chars, language required to be English, forbidden words, etc.).

    - Mandatory tokens or fields the developer explicitly names.

    Out-of-scope (DO NOT FLAG):

    - Whether the reply "sounds generic", "repeats the prompt", or "fully reflects the user's request" - unless the developer text explicitly demands those qualities.

    - Creative style, marketing quality, or depth of content unless stated.

    - Minor stylistic choices (capitalisation, punctuation) that do not violate an explicit rule.

    Pass/Fail rule

    - If an assistant reply satisfies all objective constraints, it is compliant, even if you personally find it bland or loosely related.

    - Only record an issue when a concrete, quoted rule is broken.

    Empty assistant list ⇒ immediately return has_issues=false.

    For each assistant example:

    - USER_EXAMPLES are for context only; never use them to judge compliance.

    - Judge each assistant reply solely against the explicit constraints you extracted from the developer message.

    - If a reply breaks a specific, quoted rule, add a line explaining which rule it breaks.

    - Optionally, suggest a rewrite in one short sentence (add to rewrite_suggestions).

    - If you are uncertain, do not flag an issue.

    - Be conservative—uncertain or ambiguous cases are not issues.

    be a little bit more conservative in flagging few shot contradiction issues

    Output format

    Return JSON matching FewShotIssues:

    {

    "has_issues": <bool>,

    "issues": ["<explanation 1>", "..."],

    "rewrite_suggestions": ["<suggestion 1>", "..."] // may be []

    }

    List max five items for both arrays.

    Provide empty arrays when none.

    No markdown, no extra keys.

    """,

)

dev_rewriter = Agent(

    name="dev_rewriter",

    model="gpt-4.1",

    output_type=DevRewriteOutput,

    instructions="""

    You are Dev-Rewriter.

    You receive:

    - ORIGINAL_DEVELOPER_MESSAGE

    - CONTRADICTION_ISSUES (may be empty)

    - FORMAT_ISSUES (may be empty)

    Rewrite rules

    Preserve the original intent and capabilities.

    Resolve each contradiction:

    - Keep the clause that preserves the message intent; remove/merge the conflicting one.

    If FORMAT_ISSUES is non-empty:

    - Append a new section titled ## Output Format that clearly defines the schema or gives an explicit example.

    Do NOT change few-shot examples.

    Do NOT add new policies or scope.

    Output format (strict JSON)

    {

    "new_developer_message": "<full rewritten text>"

    }

    No other keys, no markdown.

""",

)

fewshot_rewriter = Agent(

    name="fewshot_rewriter",

    model="gpt-4.1",

    output_type=MessagesOutput,

    instructions="""

    You are FewShot-Rewriter.

    Input payload

    - NEW_DEVELOPER_MESSAGE (already optimized)

    - ORIGINAL_MESSAGES (list of user/assistant dicts)

    - FEW_SHOT_ISSUES (non-empty)

    Task

    Regenerate only the assistant parts that were flagged.

    User messages must remain identical.

    Every regenerated assistant reply MUST comply with NEW_DEVELOPER_MESSAGE.

    After regenerating each assistant reply, verify:

    - It matches NEW_DEVELOPER_MESSAGE. ENSURE THAT THIS IS TRUE.

    Output format

    Return strict JSON that matches the MessagesOutput schema:

    {

    "messages": [

        {"role": "user", "content": "..."},

        {"role": "assistant", "content": "..."}

        ]

    }

    Guidelines

    - Preserve original ordering and total count.

    - If a message was unproblematic, copy it unchanged.

    """,

)
```

## 4\. Usando avaliações para chegar a esses agentes

Vamos ver como usamos o OpenAI Evals para ajustar as instruções do agente e escolher o modelo correto a ser usado. Para fazer isso, construímos um conjunto de exemplos de ouro: cada um contém mensagens originais (mensagem do desenvolvedor + mensagem do usuário/assistente) e as alterações que nosso fluxo de trabalho de otimização deve fazer. Aqui estão dois exemplos de pares dourados que usamos:

```
[

  {

    "focus": "contradiction_issues",

    "input_payload": {

      "developer_message": "Always answer in **English**.\nNunca respondas en inglés.",

      "messages": [

        {

          "role": "user",

          "content": "¿Qué hora es?"

        }

      ]

    },

    "golden_output": {

      "changes": true,

      "new_developer_message": "Always answer **in English**.",

      "new_messages": [

        {

          "role": "user",

          "content": "¿Qué hora es?"

        }

      ],

      "contradiction_issues": "Developer message simultaneously insists on English and forbids it.",

      "few_shot_contradiction_issues": "",

      "format_issues": "",

      "general_improvements": ""

    }

  },

  {

    "focus": "few_shot_contradiction_issues",

    "input_payload": {

      "developer_message": "Respond with **only 'yes' or 'no'** – no explanations.",

      "messages": [

        {

          "role": "user",

          "content": "Is the sky blue?"

        },

        {

          "role": "assistant",

          "content": "Yes, because wavelengths …"

        },

        {

          "role": "user",

          "content": "Is water wet?"

        },

        {

          "role": "assistant",

          "content": "Yes."

        }

      ]

    },

    "golden_output": {

      "changes": true,

      "new_developer_message": "Respond with **only** the single word \"yes\" or \"no\".",

      "new_messages": [

        {

          "role": "user",

          "content": "Is the sky blue?"

        },

        {

          "role": "assistant",

          "content": "yes"

        },

        {

          "role": "user",

          "content": "Is water wet?"

        },

        {

          "role": "assistant",

          "content": "yes"

        }

      ],

      "contradiction_issues": "",

      "few_shot_contradiction_issues": "Assistant examples include explanations despite instruction not to.",

      "format_issues": "",

      "general_improvements": ""

    }

  }

]
```

A partir dessas 20 saídas douradas rotuladas manualmente que cobrem uma variedade de problemas de contradição, poucos problemas de tiro, problemas de formato, nenhum problema ou uma combinação de problemas, construímos um classificador de verificação de string python para verificar duas coisas: se um problema foi detectado para cada par dourado e se o problema detectado correspondia ao esperado. A partir desse sinal, ajustamos as instruções do agente e qual modelo usar para maximizar nossa precisão nessa avaliação. Chegamos ao modelo 4.1 como um equilíbrio entre precisão, custo e velocidade. Os prompts específicos que usamos também seguem o guia de prompts 4.1. Como você pode ver, alcançamos os rótulos corretos em todos os 20 resultados de ouro: identificando os problemas certos e evitando falsos positivos.

![Precisão para o conjunto dourado](https://cookbook.openai.com/images/optimizepromptfig1.png)

![Avaliação para o conjunto dourado](https://cookbook.openai.com/images/optimizepromptfig2.png)

## 5\. Execute o fluxo de trabalho de otimização

Vamos nos aprofundar em como o sistema de otimização realmente funciona de ponta a ponta. O fluxo de trabalho principal consiste em várias execuções dos agentes em paralelo para processar e otimizar prompts com eficiência.

```
def _normalize_messages(messages: List[Any]) -> List[Dict[str, str]]:

    """Convert list of pydantic message models to JSON-serializable dicts."""

    result = []

    for m in messages:

        if hasattr(m, "model_dump"):

            result.append(m.model_dump())

        elif isinstance(m, dict) and "role" in m and "content" in m:

            result.append({"role": str(m["role"]), "content": str(m["content"])})

    return result

async def optimize_prompt_parallel(

    developer_message: str,

    messages: List["ChatMessage"],

) -> Dict[str, Any]:

    """

    Runs contradiction, format, and few-shot checkers in parallel,

    then rewrites the prompt/examples if needed.

    Returns a unified dict suitable for an API or endpoint.

    """

    with trace("optimize_prompt_workflow"):

        # 1. Run all checkers in parallel (contradiction, format, fewshot if there are examples)

        tasks = [

            Runner.run(dev_contradiction_checker, developer_message),

            Runner.run(format_checker, developer_message),

        ]

        if messages:

            fs_input = {

                "DEVELOPER_MESSAGE": developer_message,

                "USER_EXAMPLES": [m.content for m in messages if m.role == "user"],

                "ASSISTANT_EXAMPLES": [m.content for m in messages if m.role == "assistant"],

            }

            tasks.append(Runner.run(fewshot_consistency_checker, json.dumps(fs_input)))

        results = await asyncio.gather(*tasks)

        # Unpack results

        cd_issues: Issues = results[0].final_output

        fi_issues: Issues = results[1].final_output

        fs_issues: FewShotIssues = results[2].final_output if messages else FewShotIssues.no_issues()

        # 3. Rewrites as needed

        final_prompt = developer_message

        if cd_issues.has_issues or fi_issues.has_issues:

            pr_input = {

                "ORIGINAL_DEVELOPER_MESSAGE": developer_message,

                "CONTRADICTION_ISSUES": cd_issues.model_dump(),

                "FORMAT_ISSUES": fi_issues.model_dump(),

            }

            pr_res = await Runner.run(dev_rewriter, json.dumps(pr_input))

            final_prompt = pr_res.final_output.new_developer_message

        final_messages: list[ChatMessage] | list[dict[str, str]] = messages

        if fs_issues.has_issues:

            mr_input = {

                "NEW_DEVELOPER_MESSAGE": final_prompt,

                "ORIGINAL_MESSAGES": _normalize_messages(messages),

                "FEW_SHOT_ISSUES": fs_issues.model_dump(),

            }

            mr_res = await Runner.run(fewshot_rewriter, json.dumps(mr_input))

            final_messages = mr_res.final_output.messages

        return {

            "changes": True,

            "new_developer_message": final_prompt,

            "new_messages": _normalize_messages(final_messages),

            "contradiction_issues": "\n".join(cd_issues.issues),

            "few_shot_contradiction_issues": "\n".join(fs_issues.issues),

            "format_issues": "\n".join(fi_issues.issues),

        }
```

![Rastreio para o fluxo de trabalho](https://cookbook.openai.com/images/optimizepromptfig3.png)

### Noções básicas sobre o fluxo de trabalho de otimização

A função implementa um fluxo de trabalho para maximizar a eficiência por meio da paralelização:`optimize_prompt_parallel`

1. **Detecção de problemas paralelos**: A primeira fase executa todos os agentes verificadores simultaneamente:
	- `dev_contradiction_checker` procura contradições lógicas no prompt
	- `format_checker` procura especificações de formato pouco claras
	- `fewshot_consistency_checker` (se existirem exemplos) verifica se há incompatibilidades entre o prompt e os exemplos

Após a fase de verificação paralela, o fluxo de trabalho lida com as dependências com cuidado:

1. **Regravação de prompt (condicional):** o agente só é executado se forem detectados problemas de contradição ou formato. Esse agente depende das saídas de:`dev_rewriter`
	- `dev_contradiction_checker` (a variável) `cd_issues`
	- `format_checker` (a variável) `fi_issues`
2. **Exemplo de regravação (condicional):** o agente só é executado se forem detectadas inconsistências de exemplo. Este agente depende de:`fewshot_rewriter`
	- O prompt reescrito (deve ser feito após a regravação do prompt)
	- As mensagens originais
	- As questões de poucos tiros (a variável) `fs_issues`

## 6\. Exemplos

Vamos ver o sistema de otimização em ação com alguns exemplos práticos.

### Exemplo 1: Corrigindo contradições

```
async def example_contradiction():

    # A prompt with contradictory instructions

    prompt = """Quick-Start Card — Product Parser

Goal  

Digest raw HTML of an e-commerce product detail page and emit **concise, minified JSON** describing the item.

**Required fields:**  

name | brand | sku | price.value | price.currency | images[] | sizes[] | materials[] | care_instructions | features[]

**Extraction priority:**  

1. schema.org/JSON-LD blocks  

2. <meta> & microdata tags  

3. Visible DOM fallback (class hints: "product-name", "price")

** Rules:**  

- If *any* required field is missing, short-circuit with: \`{"error": "FIELD_MISSING:<field>"}\`.

- Prices: Numeric with dot decimal; strip non-digits (e.g., "1.299,00 EUR" → 1299.00 + "EUR").

- Deduplicate images differing only by query string. Keep ≤10 best-res.

- Sizes: Ensure unit tag ("EU", "US") and ascending sort.

- Materials: Title-case and collapse synonyms (e.g., "polyester 100%" → "Polyester").

**Sample skeleton (minified):**

\`\`\`json

{"name":"","brand":"","sku":"","price":{"value":0,"currency":"USD"},"images":[""],"sizes":[],"materials":[],"care_instructions":"","features":[]}

Note: It is acceptable to output null for any missing field instead of an error ###"""

    

    result = await optimize_prompt_parallel(prompt, [])

    

    # Display the results

    if result["contradiction_issues"]:

        print("Contradiction issues:")

        print(result["contradiction_issues"])

        print()

        

    print("Optimized prompt:")

    print(result["new_developer_message"])

    

# Run the example

await example_contradiction()
```

```
Contradiction issues:
There is a contradiction between the rule that says to short-circuit and output an error if *any* required field is missing ('{"error": "FIELD_MISSING:<field>"}') and the final note which states that it is acceptable to output null for any missing field instead of an error. Both behaviors cannot be followed simultaneously when a required field is missing.

Optimized prompt:
Quick-Start Card — Product Parser

Goal  
Digest raw HTML of an e-commerce product detail page and emit **concise, minified JSON** describing the item.

**Required fields:**  
name | brand | sku | price.value | price.currency | images[] | sizes[] | materials[] | care_instructions | features[]

**Extraction priority:**  
1. schema.org/JSON-LD blocks  
2. <meta> & microdata tags  
3. Visible DOM fallback (class hints: "product-name", "price")

**Rules:**  
- If *any* required field is missing, short-circuit and output: \`{"error": "FIELD_MISSING:<field>"}\`
- Prices: Numeric with dot decimal; strip non-digits (e.g., "1.299,00 EUR" → 1299.00 + "EUR").
- Deduplicate images differing only by query string. Keep ≤10 best-res.
- Sizes: Ensure unit tag ("EU", "US") and ascending sort.
- Materials: Title-case and collapse synonyms (e.g., "polyester 100%" → "Polyester").

## Output Format

- Successful Output: Emit a minified JSON object with the following fields and types (order not enforced):
  - name: string
  - brand: string
  - sku: string
  - price: object with:
    - value: number
    - currency: string
  - images: array of string URLs
  - sizes: array of strings (each including a unit tag, e.g., "37 EU")
  - materials: array of strings
  - care_instructions: string
  - features: array of strings

Example:
{"name":"Product Name","brand":"Brand","sku":"SKU123","price":{"value":1299.00,"currency":"EUR"},"images":["https://example.com/image1.jpg","https://example.com/image2.jpg"],"sizes":["37 EU","38 EU"],"materials":["Cotton","Polyester"],"care_instructions":"Machine wash cold","features":["Feature 1","Feature 2"]}

- If any required field is missing, return:
  {"error": "FIELD_MISSING:<field>"}
  (Where <field> is the missing required field name.)
```

Isso demonstra como o sistema pode detectar e resolver contradições críticas que podem levar a saídas inconsistentes ou confusão para o modelo.

### Exemplo 2: Corrigindo inconsistências entre exemplos de prompt e poucos disparos

```
async def example_fewshot_fix():

    prompt = "Respond **only** with JSON using keys \`city\` (string) and \`population\` (integer)."

    

    messages = [

        {"role": "user", "content": "Largest US city?"},

        {"role": "assistant", "content": "New York City"},

        {"role": "user", "content": "Largest UK city?"},

        {"role": "assistant", "content": "{\"city\":\"London\",\"population\":9541000}"}

    ]

    

    

    print("Few-shot examples before optimization:")

    print(f"User: {messages[0]['content']}")

    print(f"Assistant: {messages[1]['content']}")

    print(f"User: {messages[2]['content']}")

    print(f"Assistant: {messages[3]['content']}")

    print()

    

    # Call the optimization API

    result = await optimize_prompt_parallel(prompt, [ChatMessage(**m) for m in messages])

    

    # Display the results

    if result["few_shot_contradiction_issues"]:

        print("Inconsistency found:", result["few_shot_contradiction_issues"])

        print()

    

    # Show the optimized few-shot examples

    optimized_messages = result["new_messages"]

    print("Few-shot examples after optimization:")

    print(f"User: {optimized_messages[0]['content']}")

    print(f"Assistant: {optimized_messages[1]['content']}")

    print(f"User: {optimized_messages[2]['content']}")

    print(f"Assistant: {optimized_messages[3]['content']}")

    

# Run the example

await example_fewshot_fix()
```

```
Few-shot examples before optimization:
User: Largest US city?
Assistant: New York City
User: Largest UK city?
Assistant: {"city":"London","population":9541000}

Inconsistency found: The response 'New York City' does not use JSON format and is missing the required keys \`city\` and \`population\` as stated in the rule 'Respond **only** with JSON using keys \`city\` (string) and \`population\` (integer).'

Few-shot examples after optimization:
User: Largest US city?
Assistant: {"city":"New York City","population":8468000}
User: Largest UK city?
Assistant: {"city":"London","population":9541000}
```

This is particularly important because few-shot examples have a strong influence on how models respond. If examples don't follow the stated rules, the model may learn to ignore those rules in favor of mimicking the examples. By ensuring consistency between the prompt instructions and examples, the optimization system creats a more reliable prompt.

### Example 3: Clarifying Formats in a Longer Prompt

```
async def example_format_issue():

    # A prompt with unclear or inconsistent formatting instructions

    prompt = """Task → Translate dense patent claims into 200-word lay summaries with a glossary.

Operating Steps:

1. Split the claim at semicolons, "wherein", or numbered sub-clauses.

2. For each chunk:

   a) Identify its purpose.

   b) Replace technical nouns with everyday analogies.

   c) Keep quantitative limits intact (e.g., "≥150 C").

3. Flag uncommon science terms with asterisks, and later define them.

4. Re-assemble into a flowing paragraph; do **not** broaden or narrow the claim’s scope.

5. Omit boilerplate if its removal does not alter legal meaning.

Output should follow a Markdown template:

- A summary section.

- A glossary section with the marked terms and their definitions.

Corner Cases:

- If the claim is over 5 kB, respond with CLAIM_TOO_LARGE.

- If claim text is already plain English, skip glossary and state no complex terms detected.

Remember: You are *not* providing legal advice—this is for internal comprehension only."""

    # Call the optimization API to check for format issues

    result = await optimize_prompt_parallel(prompt, [])

    # Display the results

    if result.get("format_issues"):

        print("Format issues found:", result["format_issues"])

        print()

    print("Optimized prompt:")

    print(result["new_developer_message"])

# Run the example

await example_format_issue()
```

```
Format issues found: Output must follow a precise Markdown template, but the expected structure (headers, formatting) for the summary and glossary sections is not fully specified.
Ambiguity if output should be a Markdown string or a structured object containing Markdown—data type of output is implicit.
No explicit ordering instruction for the summary and glossary sections—potentially ambiguous.
Word count limit (200 words) is mentioned for the summary but not for the glossary section—scope unclear.
No specific format for CLAIM_TOO_LARGE error or for indicating 'no complex terms'—should these be Markdown or plaintext?

Optimized prompt:
Task → Translate dense patent claims into 200-word lay summaries with a glossary.

Operating Steps:
1. Split the claim at semicolons, "wherein", or numbered sub-clauses.
2. For each chunk:
   a) Identify its purpose.
   b) Replace technical nouns with everyday analogies.
   c) Keep quantitative limits intact (e.g., ">=150 C").
3. Flag uncommon science terms with asterisks, and later define them.
4. Re-assemble into a flowing paragraph; do **not** broaden or narrow the claim’s scope.
5. Omit boilerplate if its removal does not alter legal meaning.

## Output Format
- All outputs must be provided as a Markdown string.
- If the claim exceeds 5 kB, respond only with the text: \`CLAIM_TOO_LARGE\` (no Markdown formatting).
- If the claim is already in plain English, output the following Markdown:
  
  \`\`\`markdown
  ## Summary
  <summary text>
  
  ## Glossary
  No complex terms detected.
  \`\`\`
- Otherwise, follow this Markdown template:
  
  \`\`\`markdown
  ## Summary
  <Lay summary of the claim (max 200 words)>
  
  ## Glossary
  - *Term1*: Definition of Term1
  - *Term2*: Definition of Term2
  ...
  \`\`\`
- The 'Summary' section comes before the 'Glossary' section in all cases.
- The word count limit (200 words) applies to the summary only; the glossary has no length limit.

Remember: You are *not* providing legal advice—this is for internal comprehension only.
```

This example highlights how the format checker identifies and resolves ambiguous format specifications. The prompt requested a Markdown output and the optimization flow significantly improved these format specifications.