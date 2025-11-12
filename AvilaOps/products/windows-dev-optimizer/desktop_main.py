"""
Windows Dev Optimizer | Desktop Launcher
Embeds FastAPI + HTMX interface inside a native WebView window.
Maintains ON Platform integration and privacy-first architecture.
"""

from __future__ import annotations

import asyncio
import socket
import sys
import threading
import time
from pathlib import Path
from typing import Optional, Tuple

try:
    import webview  # type: ignore
except ImportError as exc:  # pragma: no cover - dependency issue handled at runtime
    print("❌ pywebview não está instalado. Execute `pip install pywebview` ou reinstale as dependências.")
    raise

from uvicorn.config import Config
from uvicorn.server import Server

ROOT_DIR = Path(__file__).resolve().parent
FRAMEWORK_DIR = ROOT_DIR / "framework"
if str(FRAMEWORK_DIR) not in sys.path:
    sys.path.insert(0, str(FRAMEWORK_DIR))

# Reutiliza setup dos módulos do app principal
from app import setup_optimization_modules  # type: ignore
from framework.app.fastapi_framework import create_app
from framework.core.on_integration import get_on_integration


def _find_free_port() -> int:
    """Find an available TCP port on localhost."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]

def _start_uvicorn_server(app, host: str, port: int) -> Tuple[Server, threading.Thread, asyncio.AbstractEventLoop]:
    """Launch uvicorn server in a dedicated background thread."""
    config = Config(app=app, host=host, port=port, log_level="info", loop="asyncio")
    server = Server(config=config)

    loop = asyncio.new_event_loop()

    def run_server() -> None:
        asyncio.set_event_loop(loop)
        loop.run_until_complete(server.serve())

    thread = threading.Thread(target=run_server, name="uvicorn-server", daemon=True)
    thread.start()
    return server, thread, loop


def _wait_for_server(host: str, port: int, timeout: float = 15.0) -> bool:
    """Wait until the HTTP server responds or timeout."""
    try:
        import httpx
    except ImportError:
        print("⚠️ httpx não disponível para checar a porta. Aguarde inicialização do servidor.")
        time.sleep(3.0)
        return True

    deadline = time.time() + timeout
    url = f"http://{host}:{port}/"

    while time.time() < deadline:
        try:
            response = httpx.get(url, timeout=1.0)
            if response.status_code < 500:
                return True
        except Exception:
            time.sleep(0.5)

    return False


def _handle_shutdown(server: Server, thread: threading.Thread, loop: asyncio.AbstractEventLoop) -> None:
    """Gracefully stop uvicorn server and wait for thread."""
    server.should_exit = True
    try:
        if loop.is_running():
            loop.call_soon_threadsafe(lambda: None)
    except RuntimeError:
        pass
    thread.join(timeout=5.0)
    if not loop.is_closed():
        loop.close()


def launch_desktop_app() -> None:
    """Main entry point for the desktop experience."""
    print("🚀 Iniciando Windows Dev Optimizer (modo desktop)...")

    # Inicializa integração com ON Platform
    try:
        on_integration = get_on_integration()
    except Exception as exc:  # pragma: no cover - runtime environment issue
        print(f"⚠️ Não foi possível conectar à plataforma ON automaticamente: {exc}")
        on_integration = get_on_integration(bus=None)

    setup_optimization_modules(on_integration)

    framework = create_app(enable_on_integration=on_integration.on_available)

    host = "127.0.0.1"
    port = _find_free_port()

    server, thread, loop = _start_uvicorn_server(framework.app, host, port)

    if not _wait_for_server(host, port):
        print("❌ O servidor FastAPI não inicializou corretamente. Abortando.")
        server.should_exit = True
        return

    url = f"http://{host}:{port}/"
    print(f"🌐 Interface disponível em {url}")

    window = webview.create_window(
        title="Windows Dev Optimizer",
        url=url,
        width=1200,
        height=800,
        resizable=True,
        confirm_close=True,
    )

    def on_closed() -> None:
        print("👋 Encerrando aplicação...")
        server.should_exit = True
        if loop.is_running():
            loop.call_soon_threadsafe(lambda: None)

    async def _notify_loaded() -> None:
        try:
            await on_integration.broadcast_status("desktop_ui_loaded")
        except Exception:
            pass

    def on_loaded() -> None:
        asyncio.run(_notify_loaded())

    window.events.closed += on_closed
    window.events.loaded += on_loaded

    # Inicia loop do webview (bloqueante)
    webview.start(debug=False)

    _handle_shutdown(server, thread, loop)


if __name__ == "__main__":
    # Trata interrupção via Ctrl+C quando rodando pelo console
    try:
        launch_desktop_app()
    except KeyboardInterrupt:
        print("\nInterrompido pelo usuário.")
        sys.exit(0)
