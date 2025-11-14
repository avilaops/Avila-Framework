// Ávila Notification System
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
