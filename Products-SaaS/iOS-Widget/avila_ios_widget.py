#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================================
ÁVILA STATUS WIDGET - iOS Scriptable Widget
Monitora status dos produtos Ávila em tempo real
Autor: Nicolas Avila | Framework: Avila Inc.
Data: 13/11/2025
============================================================================
"""

import requests
import json
from datetime import datetime
import os


class AvilaStatusWidget:
    """Widget para monitorar status dos produtos Ávila"""

    def __init__(self):
        self.base_url = "https://avila.inc/api"  # API da Ávila
        self.status_cache = {}
        self.cache_duration = 300  # 5 minutos

    def get_products_status(self):
        """Busca status de todos os produtos"""
        try:
            # Simula chamada para API (adaptar para API real)
            response = requests.get(f"{self.base_url}/products/status", timeout=10)
            if response.status_code == 200:
                return response.json()
        except:
            pass

        # Fallback: status mockado baseado no que sabemos
        return {
            "timestamp": datetime.now().isoformat(),
            "products": [
                {
                    "name": "Darwin Self-Healing",
                    "status": "online",
                    "version": "1.0.0",
                    "uptime": "99.9%",
                },
                {
                    "name": "AgentHub",
                    "status": "online",
                    "version": "0.8.0",
                    "uptime": "98.5%",
                },
                {
                    "name": "QuickDeploy",
                    "status": "maintenance",
                    "version": "0.5.0",
                    "uptime": "95.2%",
                },
                {
                    "name": "Avila Manager",
                    "status": "online",
                    "version": "2.1.0",
                    "uptime": "99.7%",
                },
                {
                    "name": "Learning System",
                    "status": "online",
                    "version": "1.2.0",
                    "uptime": "100%",
                },
            ],
            "system_health": "healthy",
            "last_updated": datetime.now().isoformat(),
        }

    def generate_scriptable_widget(self):
        """Gera código JavaScript para Scriptable widget"""

        widget_code = """// Ávila Status Widget - Scriptable
// Monitora produtos Ávila em tempo real

class AvilaWidget {

    async run() {
        try {
            // Busca dados da API
            const data = await this.fetchAvilaStatus();

            // Cria widget
            const widget = new ListWidget();
            widget.backgroundColor = new Color("#1a1a1a");

            // Header
            const header = widget.addText("🚀 Ávila Inc");
            header.font = Font.boldSystemFont(16);
            header.textColor = new Color("#00ff88");

            widget.addSpacer(8);

            // Status geral
            const healthText = widget.addText(`Status: ${data.system_health.toUpperCase()}`);
            healthText.font = Font.systemFont(12);
            healthText.textColor = data.system_health === 'healthy' ?
                new Color("#00ff88") : new Color("#ff6b6b");

            widget.addSpacer(12);

            // Lista de produtos
            for (const product of data.products.slice(0, 5)) {
                const productStack = widget.addStack();
                productStack.layoutHorizontally();
                productStack.spacing = 8;

                // Status indicator
                const statusColor = this.getStatusColor(product.status);
                const statusCircle = productStack.addText("●");
                statusCircle.textColor = statusColor;
                statusCircle.font = Font.systemFont(10);

                // Product info
                const productText = productStack.addText(`${product.name}`);
                productText.font = Font.systemFont(12);
                productText.textColor = new Color("#ffffff");
                productText.lineLimit = 1;

                // Uptime
                const uptimeText = productStack.addText(`${product.uptime}`);
                uptimeText.font = Font.systemFont(10);
                uptimeText.textColor = new Color("#888888");

                widget.addSpacer(4);
            }

            // Footer
            widget.addSpacer(8);
            const footer = widget.addText(`Atualizado: ${this.formatTime(data.last_updated)}`);
            footer.font = Font.systemFont(8);
            footer.textColor = new Color("#666666");

            // Refresh quando tocado
            widget.url = "scriptable:///run/AvilaWidget";

            return widget;

        } catch (error) {
            console.error("Erro no widget Ávila:", error);

            // Widget de erro
            const widget = new ListWidget();
            widget.backgroundColor = new Color("#1a1a1a");

            const errorText = widget.addText("❌ Erro de Conexão");
            errorText.font = Font.boldSystemFont(14);
            errorText.textColor = new Color("#ff6b6b");

            const retryText = widget.addText("Toque para tentar novamente");
            retryText.font = Font.systemFont(10);
            retryText.textColor = new Color("#888888");

            widget.url = "scriptable:///run/AvilaWidget";

            return widget;
        }
    }

    async fetchAvilaStatus() {
        try {
            const req = new Request("https://avila.inc/api/products/status");
            req.timeoutInterval = 10;
            const response = await req.loadJSON();

            return response;
        } catch (error) {
            // Fallback data
            return {
                "system_health": "unknown",
                "products": [
                    {"name": "Darwin Self-Healing", "status": "unknown", "uptime": "N/A"},
                    {"name": "AgentHub", "status": "unknown", "uptime": "N/A"},
                    {"name": "QuickDeploy", "status": "unknown", "uptime": "N/A"},
                    {"name": "Avila Manager", "status": "unknown", "uptime": "N/A"},
                    {"name": "Learning System", "status": "unknown", "uptime": "N/A"},
                ],
                "last_updated": new Date().toISOString()
            };
        }
    }

    getStatusColor(status) {
        switch (status) {
            case 'online': return new Color("#00ff88");
            case 'maintenance': return new Color("#ffa500");
            case 'offline': return new Color("#ff6b6b");
            default: return new Color("#888888");
        }
    }

    formatTime(isoString) {
        try {
            const date = new Date(isoString);
            return date.toLocaleTimeString('pt-BR', {
                hour: '2-digit',
                minute: '2-digit'
            });
        } catch {
            return "N/A";
        }
    }
}

// Export for Scriptable
module.exports = AvilaWidget;

// Run when called directly
if (typeof module !== 'undefined' && !module.parent) {
    const widget = new AvilaWidget();
    widget.run().then(w => Script.setWidget(w));
}
"""

        return widget_code

    def generate_shortcut_automation(self):
        """Gera instruções para atalho iOS que abre produtos Ávila"""

        shortcut_data = {
            "name": "Ávila Quick Access",
            "description": "Acesso rápido aos produtos Ávila",
            "actions": [
                {
                    "type": "open_url",
                    "url": "https://avila.inc",
                    "title": "Abrir Site Ávila",
                },
                {
                    "type": "open_url",
                    "url": "https://avilaops.com",
                    "title": "Abrir Ávila Ops",
                },
                {
                    "type": "run_shortcut",
                    "shortcut": "Check Ávila Status",
                    "title": "Verificar Status",
                },
            ],
        }

        return json.dumps(shortcut_data, indent=2, ensure_ascii=False)

    def create_notification_system(self):
        """Sistema de notificações push para produtos Ávila"""

        notification_code = """// Ávila Notification System
// Notificações push quando produtos ficam offline

class AvilaNotifications {

    async checkAndNotify() {
        const data = await this.fetchAvilaStatus();

        for (const product of data.products) {
            if (product.status !== 'online') {
                // Envia notificação
                const notification = new Notification();
                notification.title = `🚨 ${product.name} - ${product.status.toUpperCase()}`;
                notification.body = `Status alterado para ${product.status}`;
                notification.sound = "failure";

                await notification.schedule();
            }
        }
    }

    async fetchAvilaStatus() {
        // Mesmo código do widget
        try {
            const req = new Request("https://avila.inc/api/products/status");
            return await req.loadJSON();
        } catch {
            return { products: [] };
        }
    }
}

// Agendar verificação a cada 5 minutos
const notifications = new AvilaNotifications();
Timer.schedule(300, true, () => notifications.checkAndNotify());
"""

        return notification_code


# Função principal
if __name__ == "__main__":
    widget = AvilaStatusWidget()

    # Gera arquivos
    with open("avila-status-widget.js", "w", encoding="utf-8") as f:
        f.write(widget.generate_scriptable_widget())

    with open("avila-shortcut.json", "w", encoding="utf-8") as f:
        f.write(widget.generate_shortcut_automation())

    with open("avila-notifications.js", "w", encoding="utf-8") as f:
        f.write(widget.create_notification_system())

    print("✅ Arquivos iOS gerados:")
    print("- avila-status-widget.js (para Scriptable)")
    print("- avila-shortcut.json (para Shortcuts)")
    print("- avila-notifications.js (para notificações)")
