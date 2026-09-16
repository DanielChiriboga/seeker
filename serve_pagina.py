#!/usr/bin/env python3

from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import os


PROJECT_DIR = Path(__file__).resolve().parent
PAGE_NAME = "Pagina.html"
PORT = int(os.environ.get("PORT", "8080"))


class PageHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(PROJECT_DIR), **kwargs)

    def do_GET(self):
        if self.path.split("?", 1)[0] not in ("/", f"/{PAGE_NAME}"):
            self.send_error(404, "Not Found")
            return
        self.path = f"/{PAGE_NAME}"
        super().do_GET()


if not (PROJECT_DIR / PAGE_NAME).is_file():
    raise SystemExit(f"No se encontró {PAGE_NAME} en {PROJECT_DIR}")


server = ThreadingHTTPServer(("127.0.0.1", PORT), PageHandler)
print(f"Sirviendo {PAGE_NAME} en http://127.0.0.1:{PORT}")

try:
    server.serve_forever()
except KeyboardInterrupt:
    print("\nServidor detenido")
finally:
    server.server_close()