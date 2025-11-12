// JavaScript para Plataforma de Vendas - Padaria Rio Preto

const API_BASE = 'http://localhost:5000/api';

// Estado da aplicação
let produtos = [];
let carrinho = [];
let pedidos = [];

// Elementos DOM
const produtosGrid = document.getElementById('produtos-grid');
const carrinhoItens = document.getElementById('carrinho-itens');
const carrinhoCount = document.getElementById('carrinho-count');
const totalSpan = document.getElementById('total');
const pedidosLista = document.getElementById('pedidos-lista');
const checkoutModal = document.getElementById('checkout-modal');
const checkoutForm = document.getElementById('checkout-form');

// Navegação
document.getElementById('btn-produtos').addEventListener('click', () => showSection('produtos'));
document.getElementById('btn-carrinho').addEventListener('click', () => showSection('carrinho'));
document.getElementById('btn-pedidos').addEventListener('click', () => showSection('pedidos'));

// Checkout
document.getElementById('btn-finalizar').addEventListener('click', () => {
    if (carrinho.length === 0) {
        alert('Carrinho vazio!');
        return;
    }
    checkoutModal.classList.add('active');
});

document.getElementById('btn-cancelar').addEventListener('click', () => {
    checkoutModal.classList.remove('active');
});

checkoutForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const clienteNome = document.getElementById('cliente-nome').value;
    const clienteTelefone = document.getElementById('cliente-telefone').value;

    const total = carrinho.reduce((sum, item) => sum + (item.preco * item.quantidade), 0);

    try {
        const response = await fetch(`${API_BASE}/pedidos`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                cliente_nome: clienteNome,
                cliente_telefone: clienteTelefone,
                itens: carrinho,
                total: total
            })
        });

        const data = await response.json();

        if (data.success) {
            alert(`Pedido #${data.pedido_id} criado com sucesso!`);
            carrinho = [];
            updateCarrinho();
            checkoutModal.classList.remove('active');
            checkoutForm.reset();
            loadPedidos();
        } else {
            alert('Erro ao criar pedido: ' + data.error);
        }
    } catch (error) {
        alert('Erro de conexão: ' + error.message);
    }
});

// Funções principais
function showSection(sectionName) {
    // Esconder todas as seções
    document.querySelectorAll('.section').forEach(section => {
        section.classList.remove('active');
    });

    // Mostrar seção selecionada
    document.getElementById(`${sectionName}-section`).classList.add('active');

    // Atualizar botões de navegação
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    document.getElementById(`btn-${sectionName}`).classList.add('active');

    // Carregar dados se necessário
    if (sectionName === 'produtos') {
        loadProdutos();
    } else if (sectionName === 'pedidos') {
        loadPedidos();
    }
}

async function loadProdutos() {
    try {
        produtosGrid.innerHTML = '<div class="loading">Carregando produtos...</div>';

        const response = await fetch(`${API_BASE}/produtos`);
        const data = await response.json();

        if (data.success) {
            produtos = data.produtos;
            renderProdutos();
        } else {
            produtosGrid.innerHTML = '<div class="error">Erro ao carregar produtos</div>';
        }
    } catch (error) {
        produtosGrid.innerHTML = '<div class="error">Erro de conexão</div>';
    }
}

function renderProdutos() {
    produtosGrid.innerHTML = '';

    if (produtos.length === 0) {
        produtosGrid.innerHTML = '<p>Nenhum produto disponível</p>';
        return;
    }

    produtos.forEach(produto => {
        const produtoCard = document.createElement('div');
        produtoCard.className = 'produto-card';

        produtoCard.innerHTML = `
            <div class="produto-imagem">
                ${produto.imagem ? `<img src="${produto.imagem}" alt="${produto.nome}">` : '🍞'}
            </div>
            <div class="produto-info">
                <h3 class="produto-nome">${produto.nome}</h3>
                <p class="produto-descricao">${produto.descricao || 'Delicioso produto da padaria'}</p>
                <p class="produto-preco">R$ ${produto.preco.toFixed(2)}</p>
                <button class="btn-adicionar" onclick="adicionarAoCarrinho(${produto.id})">
                    Adicionar ao Carrinho
                </button>
            </div>
        `;

        produtosGrid.appendChild(produtoCard);
    });
}

function adicionarAoCarrinho(produtoId) {
    const produto = produtos.find(p => p.id === produtoId);
    if (!produto) return;

    const itemExistente = carrinho.find(item => item.id === produtoId);

    if (itemExistente) {
        itemExistente.quantidade++;
    } else {
        carrinho.push({
            id: produto.id,
            nome: produto.nome,
            preco: produto.preco,
            quantidade: 1
        });
    }

    updateCarrinho();
}

function removerDoCarrinho(produtoId) {
    carrinho = carrinho.filter(item => item.id !== produtoId);
    updateCarrinho();
}

function alterarQuantidade(produtoId, delta) {
    const item = carrinho.find(item => item.id === produtoId);
    if (!item) return;

    item.quantidade += delta;

    if (item.quantidade <= 0) {
        removerDoCarrinho(produtoId);
    } else {
        updateCarrinho();
    }
}

function updateCarrinho() {
    // Atualizar contador
    const totalItens = carrinho.reduce((sum, item) => sum + item.quantidade, 0);
    carrinhoCount.textContent = totalItens;

    // Renderizar itens
    carrinhoItens.innerHTML = '';

    if (carrinho.length === 0) {
        carrinhoItens.innerHTML = '<p>Carrinho vazio</p>';
        totalSpan.textContent = '0.00';
        return;
    }

    carrinho.forEach(item => {
        const itemDiv = document.createElement('div');
        itemDiv.className = 'carrinho-item';

        itemDiv.innerHTML = `
            <div class="carrinho-item-info">
                <h4>${item.nome}</h4>
                <p>R$ ${item.preco.toFixed(2)} cada</p>
            </div>
            <div class="carrinho-item-quantidade">
                <button class="btn-quantidade" onclick="alterarQuantidade(${item.id}, -1)">-</button>
                <span>${item.quantidade}</span>
                <button class="btn-quantidade" onclick="alterarQuantidade(${item.id}, 1)">+</button>
                <button class="btn-remover" onclick="removerDoCarrinho(${item.id})">Remover</button>
            </div>
        `;

        carrinhoItens.appendChild(itemDiv);
    });

    // Calcular total
    const total = carrinho.reduce((sum, item) => sum + (item.preco * item.quantidade), 0);
    totalSpan.textContent = total.toFixed(2);
}

async function loadPedidos() {
    try {
        pedidosLista.innerHTML = '<div class="loading">Carregando pedidos...</div>';

        const response = await fetch(`${API_BASE}/pedidos`);
        const data = await response.json();

        if (data.success) {
            pedidos = data.pedidos;
            renderPedidos();
        } else {
            pedidosLista.innerHTML = '<div class="error">Erro ao carregar pedidos</div>';
        }
    } catch (error) {
        pedidosLista.innerHTML = '<div class="error">Erro de conexão</div>';
    }
}

function renderPedidos() {
    pedidosLista.innerHTML = '';

    if (pedidos.length === 0) {
        pedidosLista.innerHTML = '<p>Nenhum pedido encontrado</p>';
        return;
    }

    pedidos.forEach(pedido => {
        const pedidoCard = document.createElement('div');
        pedidoCard.className = 'pedido-card';

        const statusClass = pedido.status === 'pendente' ? 'status-pendente' : 'status-confirmado';

        pedidoCard.innerHTML = `
            <div class="pedido-header">
                <div>
                    <strong>Pedido #${pedido.id}</strong>
                    <br>
                    <small>${pedido.cliente_nome} - ${pedido.cliente_telefone}</small>
                </div>
                <div>
                    <span class="pedido-status ${statusClass}">${pedido.status}</span>
                    <br>
                    <small>${pedido.criado_em}</small>
                </div>
            </div>
            <div>
                <strong>Itens:</strong>
                <ul>
                    ${pedido.itens.map(item => `<li>${item.quantidade}x ${item.nome} - R$ ${(item.preco * item.quantidade).toFixed(2)}</li>`).join('')}
                </ul>
                <strong>Total: R$ ${pedido.total.toFixed(2)}</strong>
            </div>
        `;

        pedidosLista.appendChild(pedidoCard);
    });
}

// Inicialização
document.addEventListener('DOMContentLoaded', () => {
    showSection('produtos');
});

// Dados de exemplo (para desenvolvimento)
function carregarProdutosExemplo() {
    if (produtos.length === 0) {
        produtos = [
            {
                id: 1,
                nome: 'Pão Francês',
                descricao: 'Pão francês fresquinho da padaria',
                preco: 0.50,
                categoria: 'pães',
                disponivel: true
            },
            {
                id: 2,
                nome: 'Bolo de Chocolate',
                descricao: 'Bolo caseiro de chocolate com cobertura',
                preco: 25.00,
                categoria: 'bolos',
                disponivel: true
            },
            {
                id: 3,
                nome: 'Coxinha',
                descricao: 'Coxinha de frango com catupiry',
                preco: 4.50,
                categoria: 'salgados',
                disponivel: true
            },
            {
                id: 4,
                nome: 'Café Expresso',
                descricao: 'Café expresso premium',
                preco: 3.00,
                categoria: 'bebidas',
                disponivel: true
            }
        ];
        renderProdutos();
    }
}

// Carregar dados de exemplo se API não estiver rodando
setTimeout(() => {
    if (produtos.length === 0) {
        carregarProdutosExemplo();
    }
}, 2000);
