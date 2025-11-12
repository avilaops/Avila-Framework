# Plataforma de Vendas - Padaria Rio Preto

**Projeto:** Padaria Vendas  
**Setor:** AvilaOps/products/  
**Tecnologia:** Python Flask + HTML/CSS/JS  
**Status:** Em desenvolvimento

---

## Contexto
Plataforma genérica de vendas online para padaria, com catálogo de produtos, carrinho de compras e checkout básico.

## Objetivo
Criar solução simples e reutilizável para vendas de produtos de padaria (pães, bolos, salgados, etc.).

## Responsável
- Nome: Nicolas Avila
- Área: AvilaOps/products

## Última atualização
- Data: 2025-11-10
- Autor: Nicolas Avila

## Estrutura do Projeto

```
AvilaOps/products/padaria-vendas/
├── backend/
│   ├── app.py              # API Flask
│   ├── models.py           # Modelos de dados
│   └── requirements.txt    # Dependências
├── frontend/
│   ├── index.html          # Página principal
│   ├── styles.css          # Estilos
│   └── script.js           # JavaScript
├── database/
│   └── padaria.db          # SQLite database
└── docs/
    └── README.md           # Esta documentação
```

## Como Executar

### Backend
```bash
cd AvilaOps/products/padaria-vendas/backend
pip install -r requirements.txt
python app.py
```

### Frontend
Abrir `frontend/index.html` no navegador.

## Funcionalidades

- [ ] Catálogo de produtos
- [ ] Carrinho de compras
- [ ] Checkout básico
- [ ] Gerenciamento de pedidos

## Próximos Passos

1. Implementar backend Flask
2. Criar frontend responsivo
3. Adicionar banco de dados
4. Testar funcionalidades
5. Documentar uso

---

**Criado por:** Nicolas Avila  
**Data:** 2025-11-10  
**Versão:** 1.0
