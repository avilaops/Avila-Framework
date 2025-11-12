from pathlib import Path
import sys

# Adiciona o diretório core ao path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "core"))

from on_messaging import MessageBus, MessageType, MessagePriority, Message


class AtlasAgent:
    def __init__(self, message_bus: MessageBus):
        self.name = "Atlas"
        self.node = message_bus.register_agent(self.name, self.handle_message)
        self.knowledge_base = {
            "projetos": ["AvilaOps", "On Core", "Sistema de Agentes"],
            "tecnologias": ["Python", "YAML", "Rich"]
        }

    def handle_message(self, message: Message):
        """Processa mensagens recebidas"""
        print(f"\n[Atlas] Mensagem de {message.sender}: {message.content}")
        
        # Responde automaticamente a requisições
        if message.message_type == MessageType.REQUEST:
            if "projetos" in message.content.lower():
                response = f"Conheço estes projetos: {', '.join(self.knowledge_base['projetos'])}"
                self.node.reply(message, response)
            elif "tecnologias" in message.content.lower():
                response = f"Tecnologias em uso: {', '.join(self.knowledge_base['tecnologias'])}"
                self.node.reply(message, response)
            else:
                self.node.reply(message, "Sou Atlas, especialista em dados e conhecimento. Como posso ajudar?")

    def request_analysis(self, target_agent: str, data: str):
        """Solicita análise de outro agente"""
        self.node.send(
            recipient=target_agent,
            content=f"Preciso de análise sobre: {data}",
            message_type=MessageType.REQUEST,
            priority=MessagePriority.HIGH,
            metadata={"data_type": "analysis_request"}
        )

    def share_knowledge(self, topic: str):
        """Compartilha conhecimento com todos os agentes"""
        self.node.broadcast(
            content=f"Compartilhando conhecimento sobre: {topic}",
            priority=MessagePriority.NORMAL
        )


# Exemplo de uso
if __name__ == "__main__":
    from on_messaging import MessageBus
    from pathlib import Path
    
    logs_dir = Path(__file__).resolve().parents[2] / "logs"
    bus = MessageBus(logs_dir)
    
    atlas = AtlasAgent(bus)
    atlas.share_knowledge("Arquitetura de Agentes")
