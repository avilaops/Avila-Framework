// Avila Status Widget
// Developer Tools & Productivity Suite
// Insanely great monitoring - Built for developers who demand perfection

class AvilaWidget {
  async run() {
    const widget = new ListWidget();

    try {
      const data = await this.fetchAvilaStatus();

      // Pure white background - Apple's minimalism
      widget.backgroundColor = new Color("#ffffff");
      widget.setPadding(20, 20, 20, 20);

      // Hero typography - San Francisco font at its finest
      const title = widget.addText("Avila");
      title.font = Font.ultraLightSystemFont(44);
      title.textColor = new Color("#000000");
      title.minimumScaleFactor = 0.8;

      widget.addSpacer(2);

      // Subtitle - understated elegance
      const subtitle = widget.addText("Developer Suite");
      subtitle.font = Font.systemFont(11);
      subtitle.textColor = new Color("#86868b");
      subtitle.textOpacity = 0.8;

      widget.addSpacer(24);

      // Status dot - pixel-perfect
      const statusStack = widget.addStack();
      statusStack.layoutHorizontally();
      statusStack.centerAlignContent();
      statusStack.spacing = 8;

      const dot = this.createStatusDot(data.system_health);
      statusStack.addImage(dot);

      const statusLabel = statusStack.addText(
        data.system_health === "healthy"
          ? "All Systems Operational"
          : "System Alert"
      );
      statusLabel.font = Font.mediumSystemFont(13);
      statusLabel.textColor =
        data.system_health === "healthy"
          ? new Color("#1d1d1f")
          : new Color("#ff3b30");

      widget.addSpacer(28);

      // Products grid - clean hierarchy
      const productsTitle = widget.addText("ACTIVE PRODUCTS");
      productsTitle.font = Font.semiboldSystemFont(9);
      productsTitle.textColor = new Color("#86868b");
      productsTitle.textOpacity = 0.6;

      widget.addSpacer(12);

      // Show top 4 products with perfect spacing
      for (const product of data.products.slice(0, 4)) {
        const row = widget.addStack();
        row.layoutHorizontally();
        row.spacing = 0;
        row.centerAlignContent();

        // Product name - priority #1
        const name = row.addText(product.name);
        name.font = Font.systemFont(14);
        name.textColor = new Color("#1d1d1f");
        name.lineLimit = 1;
        name.minimumScaleFactor = 0.7;

        row.addSpacer();

        // Uptime - subtle but present
        const uptime = row.addText(product.uptime);
        uptime.font = Font.monospacedSystemFont(12);
        uptime.textColor =
          product.status === "online"
            ? new Color("#30d158")
            : new Color("#ff3b30");

        widget.addSpacer(10);
      }

      widget.addSpacer();

      // Minimal footer - timestamp only
      const now = new Date();
      const timeStr = now.toLocaleTimeString("en-US", {
        hour: "numeric",
        minute: "2-digit",
        hour12: false,
      });
      const footer = widget.addText(timeStr);
      footer.font = Font.monospacedSystemFont(10);
      footer.textColor = new Color("#86868b");
      footer.textOpacity = 0.5;

      widget.url = "scriptable:///run/AvilaWidget";
      widget.refreshAfterDate = new Date(Date.now() + 1000 * 60 * 5); // 5min

      return widget;
    } catch (error) {
      // Error state - beautiful even in failure
      widget.backgroundColor = new Color("#ffffff");
      widget.setPadding(20, 20, 20, 20);

      const errorIcon = widget.addText("Warning");
      errorIcon.font = Font.ultraLightSystemFont(56);
      errorIcon.textColor = new Color("#ff3b30");
      errorIcon.textOpacity = 0.3;

      widget.addSpacer(12);

      const errorMsg = widget.addText("Connection Failed");
      errorMsg.font = Font.systemFont(15);
      errorMsg.textColor = new Color("#1d1d1f");

      widget.addSpacer(4);

      const hint = widget.addText("Tap to retry");
      hint.font = Font.systemFont(11);
      hint.textColor = new Color("#86868b");

      widget.url = "scriptable:///run/AvilaWidget";

      return widget;
    }
  }

  // Create perfect status dot (8x8 circle)
  createStatusDot(health) {
    const size = new Size(8, 8);
    const canvas = new DrawContext();
    canvas.size = size;
    canvas.opaque = false;
    canvas.respectScreenScale = true;

    const color =
      health === "healthy" ? new Color("#30d158") : new Color("#ff3b30");

    canvas.setFillColor(color);
    const rect = new Rect(0, 0, 8, 8);
    canvas.fillEllipse(rect);

    return canvas.getImage();
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
        system_health: "unknown",
        products: [
          { name: "Darwin Self-Healing", status: "unknown", uptime: "N/A" },
          { name: "AgentHub", status: "unknown", uptime: "N/A" },
          { name: "QuickDeploy", status: "unknown", uptime: "N/A" },
          { name: "Avila Manager", status: "unknown", uptime: "N/A" },
          { name: "Learning System", status: "unknown", uptime: "N/A" },
        ],
        last_updated: new Date().toISOString(),
      };
    }
  }

  getStatusColor(status) {
    switch (status) {
      case "online":
        return new Color("#00ff88");
      case "maintenance":
        return new Color("#ffa500");
      case "offline":
        return new Color("#ff6b6b");
      default:
        return new Color("#888888");
    }
  }

  formatTime(isoString) {
    try {
      const date = new Date(isoString);
      return date.toLocaleTimeString("pt-BR", {
        hour: "2-digit",
        minute: "2-digit",
      });
    } catch {
      return "N/A";
    }
  }
}

// Export for Scriptable
module.exports = AvilaWidget;

// Run when called directly
if (typeof module !== "undefined" && !module.parent) {
  const widget = new AvilaWidget();
  widget.run().then((w) => Script.setWidget(w));
}
