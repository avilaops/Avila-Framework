# 🧮 ÁVILA - FUNDAMENTOS MATEMÁTICOS

## Documento Técnico: Matemática por Trás da Orquestração

**Data:** 2025-11-10
**Autor:** Ávila Tech
**Área:** Machine Learning & AI Engineering

---

## 📐 1. EMBEDDINGS & ESPAÇO VETORIAL

### 1.1 Representação de Documentos

Cada documento `d` é transformado em um vetor `v ∈ ℝⁿ`:

```
d = "Este é um documento sobre Azure"
     ↓ [Modelo de Embedding]
v = [0.234, -0.891, 0.445, ..., 0.123] ∈ ℝ¹⁵³⁶
```

**Propriedades do Espaço Vetorial:**
- **Dimensionalidade:** n = 1536 (OpenAI Ada-003) ou 384 (MiniLM)
- **Norma:** Vetores normalizados (‖v‖ = 1)
- **Espaço:** Métrico com distância euclidiana ou cosseno

### 1.2 Similaridade Cosseno

Mede o ângulo entre dois vetores (independente da magnitude):

```
                    v₁ · v₂
cos(θ) = ─────────────────────────
          ‖v₁‖ × ‖v₂‖

Onde:
- v₁ · v₂ = Σ(v₁ᵢ × v₂ᵢ)  [produto escalar]
- ‖v‖ = √(Σ vᵢ²)           [norma L2]

Intervalo: [-1, 1]
  1.0  → idênticos
  0.0  → ortogonais (sem relação)
 -1.0  → opostos
```

**Implementação Otimizada (NumPy):**
```python
def cosine_similarity(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

# Vetorizada para batch:
def cosine_similarity_matrix(V):
    # V: matriz (n_docs × n_dims)
    V_norm = V / np.linalg.norm(V, axis=1, keepdims=True)
    return V_norm @ V_norm.T  # Produto matricial
    # Complexidade: O(n²d) onde d = dimensão
```

### 1.3 Distância Euclidiana

Alternativa à similaridade cosseno:

```
                _______________
d(v₁, v₂) = √ Σ (v₁ᵢ - v₂ᵢ)²
               i=1..n

Propriedades:
- Métrica: d(x,y) ≥ 0, d(x,x) = 0, simétrica, desigualdade triangular
- Sensível a magnitude (diferente do cosseno)
```

**Conversão entre Métricas:**
```
Para vetores normalizados (‖v‖ = 1):

d²_euclidean(v₁, v₂) = 2 × (1 - cos(v₁, v₂))

Portanto:
cos_sim = 1 - (d²_euclidean / 2)
```

---

## 🔍 2. DETECÇÃO DE DUPLICATAS

### 2.1 Threshold-Based Approach

Simples e interpretável:

```
duplicatas(d₁, d₂) = {
    True   se cos(v₁, v₂) ≥ τ
    False  caso contrário
}

Onde τ = threshold (tipicamente 0.85)

Trade-off:
- τ alto (0.95): Poucos falsos positivos, mais falsos negativos
- τ baixo (0.75): Mais falsos positivos, poucos falsos negativos
```

**Otimização: Precision-Recall Curve**
```
Precision = TP / (TP + FP)
Recall    = TP / (TP + FN)

F1-Score = 2 × (Precision × Recall) / (Precision + Recall)

Escolher τ que maximiza F1-Score em conjunto de validação
```

### 2.2 Locality-Sensitive Hashing (LSH)

Para escalar a milhões de documentos:

**Problema:** Comparar todos os pares = O(n²) → inviável

**Solução:** Hash que preserva similaridade

```
Princípio:
Se cos(v₁, v₂) alto → P(hash(v₁) = hash(v₂)) alto

Implementação (SimHash):
1. Para cada dimensão i:
   - Se vᵢ > 0: bit = 1
   - Se vᵢ ≤ 0: bit = 0

2. Hash = concatenação de bits

3. Hamming distance entre hashes ≈ Angular distance entre vetores

Complexidade: O(n log n) [busca em hash table]
```

**Código Python:**
```python
import numpy as np
from collections import defaultdict

def simhash(vector, num_bits=128):
    """Gera hash binário de 128 bits"""
    # Projeções aleatórias
    random_vectors = np.random.randn(len(vector), num_bits)
    projections = vector @ random_vectors
    return tuple(projections > 0)  # Boolean array

def find_candidates(vectors, threshold=0.85):
    """Encontra pares candidatos a duplicatas"""
    hash_buckets = defaultdict(list)

    # Indexar por hash
    for i, v in enumerate(vectors):
        h = simhash(v)
        hash_buckets[h].append(i)

    # Pares no mesmo bucket são candidatos
    candidates = []
    for bucket in hash_buckets.values():
        if len(bucket) > 1:
            # Verificar similaridade exata
            for i in range(len(bucket)):
                for j in range(i+1, len(bucket)):
                    sim = cosine_similarity(vectors[bucket[i]], vectors[bucket[j]])
                    if sim >= threshold:
                        candidates.append((bucket[i], bucket[j], sim))

    return candidates
```

---

## 📊 3. CLUSTERING HIERÁRQUICO

### 3.1 Agglomerative Clustering

Abordagem bottom-up:

```
Algoritmo:
1. Iniciar: cada documento = 1 cluster
2. Repetir até k clusters:
   a) Encontrar par de clusters mais próximos
   b) Mesclar em novo cluster
   c) Atualizar distâncias

Complexidade: O(n³) naive, O(n² log n) otimizado
```

**Medidas de Linkage:**

1. **Single Linkage** (Mínimo)
   ```
   d(C₁, C₂) = min{d(x, y) : x ∈ C₁, y ∈ C₂}

   → Clusters em "cadeia"
   → Sensível a outliers
   ```

2. **Complete Linkage** (Máximo)
   ```
   d(C₁, C₂) = max{d(x, y) : x ∈ C₁, y ∈ C₂}

   → Clusters compactos
   → Mais robusto
   ```

3. **Ward Linkage** (Variância) ⭐ **RECOMENDADO**
   ```
   d(C₁, C₂) = Σ ‖xᵢ - μ‖² após merge
              i∈C₁∪C₂

   Onde μ = centroid do cluster mesclado

   → Minimiza variância intra-cluster
   → Balanceado e robusto
   ```

**Implementação (scikit-learn):**
```python
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram, linkage
import matplotlib.pyplot as plt

# Clustering
model = AgglomerativeClustering(
    n_clusters=None,  # Automático
    distance_threshold=0.5,  # Cortar em distância
    linkage='ward'
)
labels = model.fit_predict(embeddings)

# Dendrograma
linkage_matrix = linkage(embeddings, method='ward')
plt.figure(figsize=(12, 8))
dendrogram(linkage_matrix, truncate_mode='lastp', p=30)
plt.title('Dendrograma Hierárquico')
plt.xlabel('Cluster ID')
plt.ylabel('Distância')
plt.show()
```

### 3.2 HDBSCAN (Density-Based)

Clustering baseado em densidade → encontra k automaticamente:

```
Princípio:
- Clusters = regiões de alta densidade
- Outliers = pontos em regiões de baixa densidade

Vantagens:
✓ Não precisa especificar k
✓ Detecta outliers
✓ Clusters de formas arbitrárias

Desvantagens:
✗ Mais lento (O(n log n))
✗ Sensível a hiperparâmetros (min_cluster_size)
```

**Hiperparâmetros:**
- `min_cluster_size`: Mínimo de pontos para formar cluster (ex: 5)
- `min_samples`: Densidade necessária (ex: 3)

**Código:**
```python
import hdbscan

clusterer = hdbscan.HDBSCAN(
    min_cluster_size=5,
    min_samples=3,
    metric='euclidean',
    cluster_selection_method='eom'  # excess of mass
)
labels = clusterer.fit_predict(embeddings)

# Outliers têm label = -1
num_outliers = np.sum(labels == -1)
print(f"Outliers: {num_outliers} ({100*num_outliers/len(labels):.1f}%)")
```

### 3.3 Número Ótimo de Clusters

**Método 1: Silhouette Score**
```
Para cada ponto i:
  a(i) = distância média a pontos no mesmo cluster
  b(i) = distância média ao cluster mais próximo

  s(i) = (b(i) - a(i)) / max(a(i), b(i))

Silhouette = média de s(i)

Intervalo: [-1, 1]
  1  → bem clusterizado
  0  → na fronteira
 -1  → no cluster errado

Escolher k que maximiza Silhouette
```

**Método 2: Davies-Bouldin Index**
```
Para cada par de clusters (i, j):
  σᵢ = dispersão do cluster i
  σⱼ = dispersão do cluster j
  d(cᵢ, cⱼ) = distância entre centroids

  Rᵢⱼ = (σᵢ + σⱼ) / d(cᵢ, cⱼ)

DB = (1/k) Σ max(Rᵢⱼ)
            i  j≠i

Menor DB = melhor (clusters compactos e separados)
```

**Método 3: Elbow Method**
```
Inércia(k) = Σ  Σ  ‖x - μₖ‖²
            k x∈Cₖ

Plot Inércia vs k → "cotovelo" indica k ótimo
```

**Implementação:**
```python
from sklearn.metrics import silhouette_score, davies_bouldin_score

def find_optimal_k(embeddings, k_range=(2, 20)):
    scores = []
    for k in range(k_range[0], k_range[1]+1):
        model = AgglomerativeClustering(n_clusters=k)
        labels = model.fit_predict(embeddings)

        sil = silhouette_score(embeddings, labels)
        db = davies_bouldin_score(embeddings, labels)

        scores.append({
            'k': k,
            'silhouette': sil,
            'davies_bouldin': db
        })

    # Melhor k: maior silhouette, menor DB
    best = max(scores, key=lambda x: x['silhouette'])
    return best['k'], scores
```

---

## 🕸️ 4. KNOWLEDGE GRAPHS

### 4.1 Representação

**Grafo Direcionado Ponderado:**
```
G = (V, E, W)

V = {d₁, d₂, ..., dₙ}  [documentos]
E ⊆ V × V               [relações]
W: E → [0, 1]           [pesos = similaridade]

Exemplo:
(d₁, d₂, 0.87) significa: d₁ relacionado a d₂ com 87% de similaridade
```

**Matriz de Adjacência:**
```
A ∈ ℝⁿˣⁿ

Aᵢⱼ = {
    w(dᵢ, dⱼ)  se (dᵢ, dⱼ) ∈ E
    0          caso contrário
}

Propriedades:
- Simétrica (grafo não-direcionado)
- Diagonal zero (sem self-loops)
- Esparsa (poucas conexões)
```

### 4.2 PageRank

Calcula "importância" de cada documento:

```
Fórmula Iterativa:

PR(dᵢ) = (1-α)/n + α · Σ PR(dⱼ) / L(dⱼ)
                       j→i

Onde:
- α = damping factor (0.85) [prob de seguir link]
- n = número total de documentos
- L(dⱼ) = número de links saindo de dⱼ
- j→i = todos j que linkam para i

Convergência:
|PR^(t+1) - PR^(t)| < ε  (tipicamente ε = 0.0001)
```

**Forma Matricial:**
```
PR = (1-α) · 1/n · 1ⁿ + α · M · PR

Onde M é a matriz de transição:
Mᵢⱼ = Aᵢⱼ / Σₖ Aᵢₖ

Solução: autovetor correspondente ao autovalor λ=1
```

**Implementação (NetworkX):**
```python
import networkx as nx

# Criar grafo
G = nx.Graph()
for i, doc in enumerate(documents):
    G.add_node(i, title=doc['title'], category=doc['category'])

# Adicionar arestas
for i in range(len(embeddings)):
    for j in range(i+1, len(embeddings)):
        sim = cosine_similarity(embeddings[i], embeddings[j])
        if sim > 0.65:  # Threshold
            G.add_edge(i, j, weight=sim)

# PageRank
pr = nx.pagerank(G, alpha=0.85, max_iter=100, tol=1e-6)

# Documentos mais importantes
top_docs = sorted(pr.items(), key=lambda x: x[1], reverse=True)[:10]
for doc_id, score in top_docs:
    print(f"{documents[doc_id]['title']}: {score:.4f}")
```

### 4.3 Community Detection

Encontrar grupos de documentos densamente conectados:

**Algoritmo de Louvain:**
```
Objetivo: Maximizar Modularidade

         1     ⎡          kᵢkⱼ ⎤
Q = ───────── Σ ⎢ Aᵢⱼ - ────── ⎥ δ(cᵢ, cⱼ)
      2m    i,j ⎣          2m   ⎦

Onde:
- m = número de arestas
- kᵢ = grau do nó i
- δ(cᵢ, cⱼ) = 1 se i e j na mesma comunidade, 0 caso contrário
- Aᵢⱼ = peso da aresta

Q ∈ [-0.5, 1]
  Q > 0.3 → estrutura de comunidade forte
```

**Implementação:**
```python
from networkx.algorithms import community

# Louvain
communities = community.louvain_communities(G, weight='weight', resolution=1.0)

# Modularidade
modularity = community.modularity(G, communities, weight='weight')
print(f"Modularidade: {modularity:.3f}")

# Visualizar
import matplotlib.pyplot as plt
pos = nx.spring_layout(G, k=0.5, iterations=50)
colors = [0] * G.number_of_nodes()
for i, comm in enumerate(communities):
    for node in comm:
        colors[node] = i

nx.draw(G, pos, node_color=colors, cmap=plt.cm.rainbow,
        node_size=100, with_labels=False, edge_color='gray', alpha=0.6)
plt.show()
```

### 4.4 Shortest Path

Encontrar "caminho de conhecimento" entre documentos:

```
Dijkstra's Algorithm:

dist[s] = 0
dist[v] = ∞ para v ≠ s

Q = priority_queue(all nodes by dist)

while Q not empty:
    u = extract_min(Q)
    for each neighbor v of u:
        alt = dist[u] + weight(u, v)
        if alt < dist[v]:
            dist[v] = alt
            prev[v] = u

Complexidade: O(|E| + |V| log |V|) com heap
```

**Uso:**
```python
# Caminho entre dois documentos
path = nx.shortest_path(G, source=doc1_id, target=doc2_id, weight='weight')
print("Caminho de conhecimento:")
for node in path:
    print(f"  → {documents[node]['title']}")

# Todos os caminhos mais curtos
lengths = nx.shortest_path_length(G, weight='weight')
avg_path_length = sum(sum(l.values()) for l in lengths.values()) / (n * (n-1))
print(f"Caminho médio: {avg_path_length:.2f}")
```

---

## 📈 5. MODELOS DE PRODUTIVIDADE

### 5.1 Time Series Analysis

**Decomposição:**
```
Yₜ = Trendₜ + Seasonalityₜ + Noiseₜ

Onde:
- Trend: tendência de longo prazo
- Seasonality: padrões cíclicos (diário, semanal)
- Noise: variações aleatórias

Método: STL (Seasonal-Trend decomposition using Loess)
```

**ARIMA para Previsão:**
```
ARIMA(p, d, q):
  p = ordem autoregressiva
  d = grau de diferenciação
  q = ordem média móvel

Modelo:
Yₜ = c + φ₁Yₜ₋₁ + ... + φₚYₜ₋ₚ + θ₁εₜ₋₁ + ... + θᵧεₜ₋ᵧ + εₜ

Auto-seleção: auto.arima() testa múltiplas combinações
```

**Código:**
```python
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.arima.model import ARIMA
import pandas as pd

# Dados: horas de trabalho por dia
df = pd.read_csv('productivity.csv', parse_dates=['date'])
df.set_index('date', inplace=True)

# Decomposição
decomposition = seasonal_decompose(df['hours'], model='additive', period=7)
decomposition.plot()

# ARIMA
model = ARIMA(df['hours'], order=(1, 1, 1))
fitted = model.fit()

# Previsão próximos 7 dias
forecast = fitted.forecast(steps=7)
print(forecast)
```

### 5.2 LSTM para Séries Temporais

Deep learning para capturar padrões complexos:

**Arquitetura:**
```
Input: [activity_t-n, ..., activity_t-1]
       shape = (batch, timesteps, features)

LSTM Cell:
  fₜ = σ(Wf · [hₜ₋₁, xₜ] + bf)  [forget gate]
  iₜ = σ(Wi · [hₜ₋₁, xₜ] + bi)  [input gate]
  C̃ₜ = tanh(Wc · [hₜ₋₁, xₜ] + bc)  [candidate]
  Cₜ = fₜ ⊙ Cₜ₋₁ + iₜ ⊙ C̃ₜ  [cell state]
  oₜ = σ(Wo · [hₜ₋₁, xₜ] + bo)  [output gate]
  hₜ = oₜ ⊙ tanh(Cₜ)  [hidden state]

Output: produtividade prevista em t+1
```

**Implementação (PyTorch):**
```python
import torch
import torch.nn as nn

class ProductivityLSTM(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers=2):
        super().__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers,
                            batch_first=True, dropout=0.2)
        self.fc = nn.Linear(hidden_size, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        # x: (batch, seq_len, features)
        out, (h, c) = self.lstm(x)
        # Pegar último timestep
        out = self.fc(out[:, -1, :])
        out = self.sigmoid(out)
        return out

# Treinamento
model = ProductivityLSTM(input_size=10, hidden_size=64)
criterion = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

for epoch in range(100):
    for batch in dataloader:
        X, y = batch
        pred = model(X)
        loss = criterion(pred, y)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
```

### 5.3 Anomaly Detection

Detectar dias anormalmente improdutivos:

**Z-Score:**
```
z = (x - μ) / σ

Se |z| > 3 → outlier (99.7% dos dados em ±3σ)

Vantagens: Simples, interpretável
Desvantagens: Assume distribuição normal
```

**Isolation Forest:**
```
Princípio:
- Anomalias são "fáceis de isolar"
- Construir árvores aleatórias
- Anomalias têm path length curto

Score:
s(x) = 2^(-E[h(x)] / c(n))

s(x) ≈ 1 → anomalia
s(x) << 0.5 → normal
```

**Implementação:**
```python
from sklearn.ensemble import IsolationForest

# Treinar
clf = IsolationForest(contamination=0.05, random_state=42)
clf.fit(features)  # shape: (n_days, n_features)

# Detectar anomalias
predictions = clf.predict(features)
anomalies = predictions == -1

# Investigar
anomaly_days = df[anomalies]
print("Dias anômalos:")
print(anomaly_days[['date', 'hours', 'deep_work_ratio']])
```

---

## 💰 6. OTIMIZAÇÃO DE CUSTOS AZURE

### 6.1 Modelo de Custo

```
Custo Total = Σ (preço_i × quantidade_i × tempo_i)
             i∈recursos

Recursos comuns:
- VMs: $0.096/hora (B2s)
- Storage: $0.02/GB/mês
- Bandwidth: $0.087/GB (saída)
- Functions: $0.20/milhão execuções
```

### 6.2 Problema de Otimização

```
minimize: C = Σ cᵢxᵢ
             i

subject to:
  Performance(x) ≥ SLA_min
  Latency(x) ≤ L_max
  xᵢ ≥ 0 ∀i
  xᵢ ∈ ℤ (se VM count)

Onde:
- cᵢ = custo do recurso i
- xᵢ = quantidade do recurso i
```

**Abordagem: Linear Programming**
```python
from scipy.optimize import linprog

# Coeficientes de custo
c = [0.096, 0.02, 0.087]  # [VM/hora, Storage/GB, Bandwidth/GB]

# Inequações (Ax ≤ b)
A = [
    [-100, 0, 0],  # Performance: -100*VM ≤ -1000 → VM ≥ 10
    [50, 0, 0],    # Latency: 50*VM ≤ 500 → VM ≤ 10
]
b = [-1000, 500]

# Limites
x_bounds = [(0, None), (0, None), (0, None)]

# Resolver
result = linprog(c, A_ub=A, b_ub=b, bounds=x_bounds, method='highs')
print(f"Configuração ótima: {result.x}")
print(f"Custo mínimo: ${result.fun:.2f}")
```

### 6.3 Previsão de Custos

**Prophet (Facebook):**
```python
from prophet import Prophet

# Histórico de custos
df = pd.DataFrame({
    'ds': date_range,  # datas
    'y': costs         # custos diários
})

# Treinar
model = Prophet(
    yearly_seasonality=False,
    weekly_seasonality=True,
    daily_seasonality=False
)
model.fit(df)

# Prever próximos 30 dias
future = model.make_future_dataframe(periods=30)
forecast = model.predict(future)

# Alertar se previsão > orçamento
budget = 1000  # $/mês
predicted_monthly = forecast['yhat'].tail(30).sum()
if predicted_monthly > budget:
    print(f"⚠️  ALERTA: Custo previsto ${predicted_monthly:.2f} excede orçamento!")
```

---

## 🎲 7. PROBABILIDADE & ESTATÍSTICA

### 7.1 Distribuições Importantes

**Normal (Gaussian):**
```
f(x | μ, σ²) = (1/√(2πσ²)) · exp(-(x-μ)²/(2σ²))

Usado para: métricas de produtividade, tempos de resposta
```

**Poisson:**
```
P(X = k) = (λᵏ e^(-λ)) / k!

Usado para: contagem de eventos (commits/dia, deploys/semana)
```

**Exponencial:**
```
f(x | λ) = λ e^(-λx)  para x ≥ 0

Usado para: tempo entre eventos (intervalo entre deploys)
```

### 7.2 Testes de Hipótese

**A/B Testing:**
```
H₀: μ_A = μ_B  (não há diferença)
H₁: μ_A ≠ μ_B  (há diferença)

t-test:
t = (x̄_A - x̄_B) / √(s²_A/n_A + s²_B/n_B)

Se |t| > t_crítico (α=0.05) → rejeitar H₀
```

**Implementação:**
```python
from scipy.stats import ttest_ind

# Produtividade antes e depois de mudança
before = [7.2, 6.8, 7.5, 7.0, 6.9]
after = [8.1, 8.3, 7.9, 8.2, 8.0]

t_stat, p_value = ttest_ind(before, after)
if p_value < 0.05:
    print(f"Mudança significativa! (p = {p_value:.4f})")
else:
    print("Sem evidência de mudança significativa")
```

---

## 🧩 8. TEORIA DA INFORMAÇÃO

### 8.1 Entropia

Mede "surpresa" / incerteza:

```
H(X) = -Σ p(x) log₂ p(x)
        x

Exemplo: Categorias de documentos
P(Trabalho) = 0.5
P(Aprendizado) = 0.3
P(Ferramentas) = 0.2

H = -0.5·log₂(0.5) - 0.3·log₂(0.3) - 0.2·log₂(0.2)
  = 1.49 bits

Máxima entropia: log₂(n) quando todas categorias equiprováveis
```

### 8.2 Informação Mútua

Quanto uma variável "informa" sobre outra:

```
I(X;Y) = Σ  Σ  p(x,y) log₂(p(x,y) / (p(x)p(y)))
         x  y

I(X;Y) = 0 → independentes
I(X;Y) = H(X) = H(Y) → perfeitamente correlacionadas

Uso: Feature selection (selecionar features com alta MI com target)
```

---

## 📚 REFERÊNCIAS

1. **Linear Algebra:** Gilbert Strang - "Linear Algebra and Its Applications"
2. **Machine Learning:** Bishop - "Pattern Recognition and Machine Learning"
3. **Information Retrieval:** Manning et al. - "Introduction to Information Retrieval"
4. **Time Series:** Hyndman & Athanasopoulos - "Forecasting: Principles and Practice"
5. **Graph Theory:** Newman - "Networks: An Introduction"
6. **Deep Learning:** Goodfellow et al. - "Deep Learning"

---

**🧮 "Na matemática, encontramos a linguagem universal da inteligência."**

---

*Atualizar com novos métodos conforme implementados*
