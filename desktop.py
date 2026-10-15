"""Desktop launcher: runs the server in-process and shows the UI in a native window (WebView2)."""
import socket
import sys
import threading
import time

import uvicorn
import webview

from app.config import SETTINGS
from app.main import app


def _wait_port(port: int, timeout: float = 15) -> bool:
    end = time.time() + timeout
    while time.time() < end:
        with socket.socket() as s:
            s.settimeout(0.3)
            if s.connect_ex(("127.0.0.1", port)) == 0:
                return True
        time.sleep(0.2)
    return False


def main() -> None:
    port = int(SETTINGS["port"])
    server = uvicorn.Server(uvicorn.Config(app, host=SETTINGS["host"], port=port, log_level="warning"))
    threading.Thread(target=server.run, daemon=True).start()
    if not _wait_port(port):
        print(f"Server nije pokrenut (port {port} je mozda zauzet).")
        sys.exit(1)
    webview.create_window("DJ asistent", f"http://127.0.0.1:{port}", width=1400, height=900, min_size=(900, 600))
    webview.start()
    server.should_exit = True


if __name__ == "__main__":
    main()

