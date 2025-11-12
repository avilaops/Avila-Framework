"""
Semantic Analysis Core - Motor de Análise Semântica Avançada
Responsável por análise profunda de texto, extração de entidades e classificação
"""

import re
import json
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
import hashlib

# Para embeddings (simulado - pode ser integrado com OpenAI ou HuggingFace)
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

@dataclass
class Entity:
    """Entidade extraída do texto"""
    text: str
    type: str  # person, organization, date, money, etc.
    confidence: float
    start_pos: int
    end_pos: int
    context: str

@dataclass
class Topic:
    """Tópico identificado"""
    name: str
    confidence: float
    keywords: List[str]
    description: str

@dataclass
class SentimentAnalysis:
    """Análise de sentimento"""
    overall: str = "neutral"
    confidence: float = 0.5
    scores: Dict[str, float] = None
    
    def __post_init__(self):
        if self.scores is None:
            self.scores = {"positive": 0.33, "negative": 0.33, "neutral": 0.34}

@dataclass
class SemanticAnalysis:
    """Resultado completo da análise semântica"""
    entities: Dict[str, Any]
    topics: List[Topic]
    keywords: List[Dict[str, Any]]
    sentiment: SentimentAnalysis
    context: str
    intent: str
    urgency: str
    language: str
    confidence: float

@dataclass
class SemanticVector:
    """Vetor semântico para busca e similaridade"""
    text: str
    embedding: List[float]
    hash: str
    timestamp: datetime
    metadata: Dict[str, Any]

class SemanticAnalyzer:
    """Analisador semântico avançado"""
    
    def __init__(self, cache_dir: Optional[Path] = None):
        self.cache_dir = cache_dir or Path(__file__).parent / "cache"
        self.cache_dir.mkdir(exist_ok=True)
        
        # Cache de embeddings
        self.embedding_cache: Dict[str, List[float]] = {}
        self.load_embedding_cache()
        
        # Bases de conhecimento
        self.entity_patterns = self._load_entity_patterns()
        self.topic_keywords = self._load_topic_keywords()
        self.sentiment_lexicon = self._load_sentiment_lexicon()
        
    def analyze_semantics(self, text: str, context: Optional[Dict[str, Any]] = None) -> SemanticAnalysis:
        """
        Realiza análise semântica completa do texto.
        Método principal usado pelo sistema de orquestração.
        """
        return self.analyze(text, context=context)

    def analyze(self, text: str, context: Optional[Dict[str, Any]] = None) -> SemanticAnalysis:
        """
        Realiza análise semântica completa do texto.
        """
        if not text or not text.strip():
            return SemanticAnalysis(
                entities={},
                topics=[],
                keywords=[],
                sentiment=SentimentAnalysis(),
                context="empty",
                intent="unknown",
                urgency="low",
                language="unknown",
                confidence=0.0
            )
        
        # Análises individuais
        entities = self._convert_entities_to_dict(self.extract_entities(text))
        topics = self.identify_topics(text)
        keywords = self.extract_keywords(text)
        sentiment_data = self.analyze_sentiment(text)
        
        # Converte sentimento para estrutura padronizada
        sentiment = SentimentAnalysis(
            overall=sentiment_data.get('overall', 'neutral'),
            confidence=sentiment_data.get('confidence', 0.5),
            scores=sentiment_data.get('scores', {"positive": 0.33, "negative": 0.33, "neutral": 0.34})
        )
        
        # Análises contextuais
        detected_context = self._determine_context(text, entities, topics, context)
        intent = self._classify_intent(text, entities, topics)
        urgency = self._assess_urgency(text, sentiment_data, keywords)
        language = self._detect_language(text)
        
        # Cálculo de confiança
        confidence = self._calculate_confidence(text, entities, topics, keywords)
        
        return SemanticAnalysis(
            entities=entities,
            topics=topics,
            keywords=keywords,
            sentiment=sentiment,
            context=detected_context,
            intent=intent,
            urgency=urgency,
            language=language,
            confidence=confidence
        )

    def _convert_entities_to_dict(self, entities: List[Entity]) -> Dict[str, Any]:
        """Converte lista de entidades para dicionário"""
        result = {}
        for entity in entities:
            entity_type = entity.type
            if entity_type not in result:
                result[entity_type] = []
            result[entity_type].append({
                'text': entity.text,
                'confidence': entity.confidence,
                'start_pos': entity.start_pos,
                'end_pos': entity.end_pos,
                'context': entity.context
            })
        return result

    def _determine_context(
        self,
        text: str,
        entities: Dict[str, Any],
        topics: List[Topic],
        external_context: Optional[Dict[str, Any]] = None
    ) -> str:
        """Determina contexto geral do texto"""
        context_keywords = {
            'business': ['negócio', 'empresa', 'comercial', 'venda', 'cliente'],
            'technical': ['sistema', 'código', 'api', 'erro', 'bug', 'desenvolvimento'],
            'support': ['ajuda', 'problema', 'suporte', 'questão', 'dúvida'],
            'personal': ['pessoal', 'família', 'amigo', 'casa', 'vida'],
            'education': ['estudo', 'curso', 'escola', 'universidade', 'aprendizado'],
            'health': ['saúde', 'médico', 'consulta', 'remédio', 'sintoma']
        }
        
        # Contexto explícito informado tem prioridade
        if external_context and external_context.get('context_type'):
            return external_context['context_type']

        text_lower = text.lower()
        context_scores = {}
        
        for context_type, keywords in context_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                context_scores[context_type] = score
        
        if not context_scores:
            return 'general'
        
        return max(context_scores, key=context_scores.get)

    def _classify_intent(self, text: str, entities: Dict[str, Any], topics: List[Topic]) -> str:
        """Classifica intenção do texto"""
        intent_patterns = {
            'question': ['?', 'como', 'quando', 'onde', 'por que', 'qual'],
            'request': ['preciso', 'gostaria', 'pode', 'poderia', 'favor'],
            'complaint': ['problema', 'erro', 'não funciona', 'ruim', 'terrível'],
            'information': ['informação', 'dados', 'relatório', 'status'],
            'emergency': ['urgente', 'emergência', 'crítico', 'importante'],
            'task_request': ['fazer', 'criar', 'desenvolver', 'implementar']
        }
        
        text_lower = text.lower()
        intent_scores = {}
        
        for intent_type, patterns in intent_patterns.items():
            score = sum(1 for pattern in patterns if pattern in text_lower)
            if score > 0:
                intent_scores[intent_type] = score
        
        if not intent_scores:
            return 'general'
        
        return max(intent_scores, key=intent_scores.get)

    def _assess_urgency(self, text: str, sentiment: Dict[str, Any], keywords: List[Dict[str, Any]]) -> str:
        """Avalia urgência do texto"""
        urgency_keywords = {
            'critical': ['crítico', 'emergência', 'parar', 'grave'],
            'high': ['urgente', 'prioridade', 'rapidamente', 'já'],
            'medium': ['importante', 'necessário', 'breve', 'logo'],
            'low': ['quando possível', 'futuro', 'eventualmente']
        }
        
        text_lower = text.lower()
        urgency_scores = {}
        
        for urgency_level, patterns in urgency_keywords.items():
            score = sum(2 for pattern in patterns if pattern in text_lower)
            if score > 0:
                urgency_scores[urgency_level] = score
        
        # Sentimento negativo pode indicar urgência
        if sentiment.get('overall') == 'negative':
            urgency_scores['high'] = urgency_scores.get('high', 0) + 1
        
        if not urgency_scores:
            return 'low'
        
        return max(urgency_scores, key=urgency_scores.get)

    def _detect_language(self, text: str) -> str:
        """Detecta idioma do texto (simplificado)"""
        portuguese_words = ['o', 'a', 'de', 'que', 'e', 'do', 'da', 'em', 'um', 'para', 'é', 'com', 'não', 'uma', 'os']
        english_words = ['the', 'of', 'and', 'to', 'a', 'in', 'for', 'is', 'on', 'that', 'by', 'this', 'with', 'i']
        
        words = text.lower().split()
        pt_count = sum(1 for word in words if word in portuguese_words)
        en_count = sum(1 for word in words if word in english_words)
        
        if pt_count > en_count:
            return 'portuguese'
        elif en_count > pt_count:
            return 'english'
        else:
            return 'unknown'

    def _calculate_confidence(self, text: str, entities: Dict[str, Any], topics: List[Topic], keywords: List[Dict[str, Any]]) -> float:
        """Calcula confiança geral da análise"""
        confidence_factors = []
        
        # Fator baseado no comprimento do texto
        text_length_factor = min(1.0, len(text) / 100)
        confidence_factors.append(text_length_factor)
        
        # Fator baseado no número de entidades encontradas
        entity_count = sum(len(entity_list) for entity_list in entities.values())
        entity_factor = min(1.0, entity_count / 5)
        confidence_factors.append(entity_factor)
        
        # Fator baseado no número de tópicos
        topic_factor = min(1.0, len(topics) / 3)
        confidence_factors.append(topic_factor)
        
        # Fator baseado no número de keywords
        keyword_factor = min(1.0, len(keywords) / 10)
        confidence_factors.append(keyword_factor)
        
        # Média dos fatores
        return sum(confidence_factors) / len(confidence_factors) if confidence_factors else 0.5

    def extract_entities(self, text: str) -> List[Entity]:
        """Extrai entidades nomeadas do texto"""
        entities = []
        
        for entity_type, patterns in self.entity_patterns.items():
            for pattern in patterns:
                for match in re.finditer(pattern, text, re.IGNORECASE):
                    entity = Entity(
                        text=match.group(),
                        type=entity_type,
                        confidence=self._calculate_entity_confidence(match.group(), entity_type),
                        start_pos=match.start(),
                        end_pos=match.end(),
                        context=self._extract_context(text, match.start(), match.end())
                    )
                    entities.append(entity)
        
        return entities
    
    def identify_topics(self, text: str, top_n: int = 5) -> List[Topic]:
        """Identifica tópicos principais do texto"""
        topics = []
        text_lower = text.lower()
        
        topic_scores = {}
        for topic, keywords in self.topic_keywords.items():
            score = 0
            matched_keywords = []
            
            for keyword in keywords:
                if keyword.lower() in text_lower:
                    score += 1
                    matched_keywords.append(keyword)
            
            if score > 0:
                confidence = min(score / len(keywords), 1.0)
                topic_obj = Topic(
                    name=topic,
                    confidence=confidence,
                    keywords=matched_keywords,
                    description=f"Tópico identificado com {len(matched_keywords)} palavras-chave"
                )
                topics.append(topic_obj)
        
        # Ordena por confiança e retorna top_n
        topics.sort(key=lambda x: x.confidence, reverse=True)
        return topics[:top_n]
    
    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Análise detalhada de sentimento"""
        text_lower = text.lower()
        words = re.findall(r'\b\w+\b', text_lower)
        
        positive_score = 0
        negative_score = 0
        neutral_score = 0
        
        word_sentiments = []
        
        for word in words:
            if word in self.sentiment_lexicon:
                sentiment_data = self.sentiment_lexicon[word]
                word_sentiments.append({
                    'word': word,
                    'sentiment': sentiment_data['sentiment'],
                    'intensity': sentiment_data['intensity']
                })
                
                if sentiment_data['sentiment'] == 'positive':
                    positive_score += sentiment_data['intensity']
                elif sentiment_data['sentiment'] == 'negative':
                    negative_score += sentiment_data['intensity']
                else:
                    neutral_score += sentiment_data['intensity']
        
        total_score = positive_score + negative_score + neutral_score
        
        if total_score == 0:
            return {
                'overall': 'neutral',
                'confidence': 0.5,
                'scores': {'positive': 0, 'negative': 0, 'neutral': 1},
                'word_sentiments': []
            }
        
        scores = {
            'positive': positive_score / total_score,
            'negative': negative_score / total_score,
            'neutral': neutral_score / total_score
        }
        
        overall = max(scores.keys(), key=lambda x: scores[x])
        confidence = scores[overall]
        
        return {
            'overall': overall,
            'confidence': confidence,
            'scores': scores,
            'word_sentiments': word_sentiments
        }
    
    def extract_keywords(self, text: str, max_keywords: int = 10) -> List[Dict[str, Any]]:
        """Extrai palavras-chave com relevância"""
        # Preprocessing
        text_clean = re.sub(r'[^\w\s]', ' ', text.lower())
        words = re.findall(r'\b\w{3,}\b', text_clean)
        
        # Remove stopwords
        stopwords = self._get_stopwords()
        words = [word for word in words if word not in stopwords]
        
        # Calcula frequência
        word_freq = {}
        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        # Calcula TF-IDF simplificado (sem corpus)
        total_words = len(words)
        keywords = []
        
        for word, freq in word_freq.items():
            tf = freq / total_words
            # IDF simulado baseado no comprimento da palavra e posição no texto
            idf = len(word) / 10.0  # Palavras maiores são mais específicas
            score = tf * idf
            
            keywords.append({
                'word': word,
                'frequency': freq,
                'tf_idf_score': score,
                'relevance': min(score * 10, 1.0)  # Normaliza para 0-1
            })
        
        # Ordena por relevância
        keywords.sort(key=lambda x: x['tf_idf_score'], reverse=True)
        return keywords[:max_keywords]
    
    def get_embedding(self, text: str) -> Optional[List[float]]:
        """Obtém embedding do texto (com cache)"""
        text_hash = hashlib.md5(text.encode()).hexdigest()
        
        if text_hash in self.embedding_cache:
            return self.embedding_cache[text_hash]
        
        if OPENAI_AVAILABLE:
            try:
                # Aqui seria a chamada real para OpenAI
                # response = openai.embeddings.create(model="text-embedding-3-small", input=text)
                # embedding = response.data[0].embedding
                
                # Por ora, simula um embedding
                embedding = self._generate_mock_embedding(text)
                self.embedding_cache[text_hash] = embedding
                self._save_embedding_cache()
                return embedding
            
            except Exception as e:
                print(f"Erro ao obter embedding: {e}")
                return None
        
        # Fallback: embedding simulado
        return self._generate_mock_embedding(text)
    
    def calculate_similarity(self, text1: str, text2: str) -> float:
        """Calcula similaridade semântica entre dois textos"""
        emb1 = self.get_embedding(text1)
        emb2 = self.get_embedding(text2)
        
        if not emb1 or not emb2:
            # Fallback: similaridade baseada em palavras-chave
            return self._keyword_similarity(text1, text2)
        
        # Cosseno da similaridade
        return self._cosine_similarity(emb1, emb2)
    
    def classify_text(self, text: str, categories: List[str]) -> Dict[str, float]:
        """Classifica texto em categorias fornecidas"""
        classification = {}
        
        for category in categories:
            # Calcula similaridade com a categoria
            similarity = self.calculate_similarity(text, category)
            classification[category] = similarity
        
        # Normaliza scores
        total_score = sum(classification.values())
        if total_score > 0:
            classification = {k: v/total_score for k, v in classification.items()}
        
        return classification
    
    def _load_entity_patterns(self) -> Dict[str, List[str]]:
        """Carrega padrões para extração de entidades"""
        return {
            'email': [r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'],
            'phone': [r'\b\d{2}\s?\d{4,5}-?\d{4}\b', r'\(\d{2}\)\s?\d{4,5}-?\d{4}'],
            'cpf': [r'\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b'],
            'cnpj': [r'\b\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}\b'],
            'money': [r'R\$\s?\d+(?:[.,]\d{2})?', r'\d+(?:[.,]\d{2})?\s?reais?'],
            'date': [r'\b\d{1,2}/\d{1,2}/\d{4}\b', r'\b\d{1,2}-\d{1,2}-\d{4}\b'],
            'url': [r'https?://[^\s]+'],
            'percentage': [r'\b\d+(?:[.,]\d+)?%\b']
        }
    
    def _load_topic_keywords(self) -> Dict[str, List[str]]:
        """Carrega palavras-chave por tópico"""
        return {
            'tecnologia': ['software', 'sistema', 'aplicativo', 'codigo', 'api', 'database', 'server', 'cloud'],
            'financeiro': ['dinheiro', 'custo', 'orcamento', 'receita', 'lucro', 'investimento', 'pagamento'],
            'vendas': ['cliente', 'venda', 'produto', 'servico', 'mercado', 'campanha', 'lead'],
            'recursos_humanos': ['funcionario', 'colaborador', 'equipe', 'contratacao', 'treinamento', 'salario'],
            'juridico': ['contrato', 'lei', 'regulamentacao', 'compliance', 'processo', 'tribunal'],
            'operacional': ['processo', 'procedimento', 'fluxo', 'operacao', 'producao', 'qualidade'],
            'estrategico': ['estrategia', 'planejamento', 'meta', 'objetivo', 'visao', 'missao'],
            'marketing': ['marca', 'campanha', 'publicidade', 'social', 'conteudo', 'engajamento']
        }
    
    def _load_sentiment_lexicon(self) -> Dict[str, Dict[str, Any]]:
        """Carrega léxico de sentimentos"""
        return {
            # Positivos
            'bom': {'sentiment': 'positive', 'intensity': 0.6},
            'otimo': {'sentiment': 'positive', 'intensity': 0.8},
            'excelente': {'sentiment': 'positive', 'intensity': 0.9},
            'satisfeito': {'sentiment': 'positive', 'intensity': 0.7},
            'feliz': {'sentiment': 'positive', 'intensity': 0.8},
            'obrigado': {'sentiment': 'positive', 'intensity': 0.5},
            'parabens': {'sentiment': 'positive', 'intensity': 0.7},
            'sucesso': {'sentiment': 'positive', 'intensity': 0.8},
            
            # Negativos
            'ruim': {'sentiment': 'negative', 'intensity': 0.6},
            'pessimo': {'sentiment': 'negative', 'intensity': 0.8},
            'problema': {'sentiment': 'negative', 'intensity': 0.7},
            'erro': {'sentiment': 'negative', 'intensity': 0.6},
            'falha': {'sentiment': 'negative', 'intensity': 0.7},
            'insatisfeito': {'sentiment': 'negative', 'intensity': 0.8},
            'frustrante': {'sentiment': 'negative', 'intensity': 0.7},
            'dificuldade': {'sentiment': 'negative', 'intensity': 0.6},
            
            # Neutros
            'informacao': {'sentiment': 'neutral', 'intensity': 0.5},
            'dados': {'sentiment': 'neutral', 'intensity': 0.5},
            'relatorio': {'sentiment': 'neutral', 'intensity': 0.5},
            'status': {'sentiment': 'neutral', 'intensity': 0.5}
        }
    
    def _get_stopwords(self) -> set:
        """Retorna conjunto de stopwords em português"""
        return {
            'a', 'ao', 'aos', 'aquela', 'aquelas', 'aquele', 'aqueles', 'aquilo', 'as', 'ate',
            'com', 'como', 'da', 'das', 'de', 'dela', 'delas', 'dele', 'deles', 'depois',
            'do', 'dos', 'e', 'ela', 'elas', 'ele', 'eles', 'em', 'entre', 'essa', 'essas',
            'esse', 'esses', 'esta', 'estao', 'estas', 'este', 'estes', 'eu', 'foi', 'for',
            'isso', 'isto', 'ja', 'lhe', 'lhes', 'mais', 'mas', 'me', 'mesmo', 'meu', 'meus',
            'minha', 'minhas', 'muito', 'na', 'nao', 'nas', 'nem', 'no', 'nos', 'nossa',
            'nossas', 'nosso', 'nossos', 'num', 'numa', 'o', 'os', 'ou', 'para', 'pela',
            'pelas', 'pelo', 'pelos', 'por', 'qual', 'quando', 'que', 'quem', 'sao', 'se',
            'sem', 'sera', 'seu', 'seus', 'so', 'sua', 'suas', 'tambem', 'te', 'tem', 'ter',
            'todo', 'todos', 'tu', 'tua', 'tuas', 'tudo', 'um', 'uma', 'umas', 'uns', 'voce',
            'voces', 'vos'
        }
    
    def _calculate_entity_confidence(self, entity_text: str, entity_type: str) -> float:
        """Calcula confiança na extração da entidade"""
        # Lógica simplificada baseada no tipo e formato
        confidence_map = {
            'email': 0.95 if '@' in entity_text and '.' in entity_text else 0.5,
            'phone': 0.9 if len(re.sub(r'\D', '', entity_text)) >= 10 else 0.6,
            'url': 0.95 if entity_text.startswith('http') else 0.7,
            'money': 0.8,
            'date': 0.85,
            'cpf': 0.9,
            'cnpj': 0.9,
            'percentage': 0.9
        }
        return confidence_map.get(entity_type, 0.7)
    
    def _extract_context(self, text: str, start: int, end: int, window: int = 50) -> str:
        """Extrai contexto ao redor da entidade"""
        context_start = max(0, start - window)
        context_end = min(len(text), end + window)
        return text[context_start:context_end]
    
    def _generate_mock_embedding(self, text: str) -> List[float]:
        """Gera embedding simulado (para demonstração)"""
        # Simula embedding baseado em hash do texto
        import hashlib
        hash_obj = hashlib.md5(text.encode())
        hash_bytes = hash_obj.digest()
        
        # Converte para valores float normalizados
        embedding = []
        for i in range(0, len(hash_bytes), 2):
            if i + 1 < len(hash_bytes):
                val = (hash_bytes[i] * 256 + hash_bytes[i+1]) / 65535.0 - 0.5
                embedding.append(val)
        
        # Garante tamanho fixo (128 dimensões)
        while len(embedding) < 128:
            embedding.extend(embedding[:min(len(embedding), 128 - len(embedding))])
        
        return embedding[:128]
    
    def _keyword_similarity(self, text1: str, text2: str) -> float:
        """Similaridade baseada em palavras-chave (fallback)"""
        keywords1 = set(word['word'] for word in self.extract_keywords(text1))
        keywords2 = set(word['word'] for word in self.extract_keywords(text2))
        
        if not keywords1 or not keywords2:
            return 0.0
        
        intersection = keywords1.intersection(keywords2)
        union = keywords1.union(keywords2)
        
        return len(intersection) / len(union) if union else 0.0
    
    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calcula similaridade do cosseno entre dois vetores"""
        if len(vec1) != len(vec2):
            return 0.0
        
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        magnitude1 = sum(a * a for a in vec1) ** 0.5
        magnitude2 = sum(a * a for a in vec2) ** 0.5
        
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
        
        return dot_product / (magnitude1 * magnitude2)
    
    def load_embedding_cache(self):
        """Carrega cache de embeddings do disco"""
        cache_file = self.cache_dir / "embedding_cache.json"
        if cache_file.exists():
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    self.embedding_cache = json.load(f)
            except Exception:
                self.embedding_cache = {}
    
    def _save_embedding_cache(self):
        """Salva cache de embeddings no disco"""
        cache_file = self.cache_dir / "embedding_cache.json"
        try:
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.embedding_cache, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Erro ao salvar cache: {e}")


# Exemplo de uso
if __name__ == "__main__":
    analyzer = SemanticAnalyzer()
    
    text = """
    Prezados, preciso urgentemente de uma análise financeira do projeto X.
    O orçamento atual está estourando em 30% e precisamos tomar uma decisão
    estratégica sobre como proceder. Por favor, enviem o relatório para
    joao@empresa.com até amanhã.
    """
    
    print("=== ANÁLISE SEMÂNTICA ===")
    
    # Entidades
    entities = analyzer.extract_entities(text)
    print(f"\n🎯 ENTIDADES ({len(entities)}):")
    for entity in entities:
        print(f"  • {entity.text} ({entity.type}) - {entity.confidence:.1%}")
    
    # Tópicos
    topics = analyzer.identify_topics(text)
    print(f"\n📊 TÓPICOS ({len(topics)}):")
    for topic in topics:
        print(f"  • {topic.name} - {topic.confidence:.1%} - {', '.join(topic.keywords)}")
    
    # Sentimento
    sentiment = analyzer.analyze_sentiment(text)
    print(f"\n😊 SENTIMENTO:")
    print(f"  • Geral: {sentiment['overall']} ({sentiment['confidence']:.1%})")
    print(f"  • Scores: {sentiment['scores']}")
    
    # Keywords
    keywords = analyzer.extract_keywords(text)
    print(f"\n🔑 PALAVRAS-CHAVE ({len(keywords)}):")
    for kw in keywords:
        print(f"  • {kw['word']} (freq: {kw['frequency']}, rel: {kw['relevance']:.2f})")