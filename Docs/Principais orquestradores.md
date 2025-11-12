**LangChain**
	Força: ecosssistema gigantesco, toolkits prontos, agentes e chains
	Quando escolher: prototipagem rápida multi-provedor; Python-first.
    Cuidado: projetos grandes podem acumular acoplamento em abstrações internas.  
    
**LlamaIndex**
	Força: RAG avançado, índices híbridos, ingestion pipelines, síntese de grafos.
	Quando escolher: RAG complexo com múltiplas fontes e consultas compostas.
	Cuidado: foca mais em dados/índices do que em agentes gerais.
	
**Haystack**
	Força: busca, pipelines de QA, componentes modulares de IR.
	Quando escolher: times que querem controle fino de pipelines de recuperação.
    Cuidado: menor foco em agentes generalistas.
    
**DSPy**
	Força: “programação declarativa de prompts” com **otimização automática**.
    Quando escolher: você quer _tunar_ prompts como se fosse ML, com objetivos.
    Cuidado: curva de aprendizado e integração de produção.

**Azure Prompt flow**
	Força: dev-loop, avaliação, tracing, dados, deploy CI/CD no Azure.
    Quando escolher: governança e rastreabilidade end-to-end em Azure.
    Cuidado: dependência de Azure.
    
**AutoGen / CrewAI**
	Força: **multi-agente**, papéis e coordenação.
    Quando escolher: fluxos colaborativos entre agentes com ferramentas.
    Cuidado: custo de tokens e complexidade de orquestração.
    

**Guardrails / NeMo Guardrails / Outlines / Pydantic-AI**
	Força: **validação e segurança** de saída, esquemas, bloqueios.
    -Quando escolher: conformidade, controle estrito de formato e políticas.
    Cuidado: integração correta para não engessar UX.