import json
import os
import subprocess
import sys
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse


PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
PORT = int(os.getenv("WEB_PORT", "8765"))
_tracker_lock = threading.Lock()
_tracker_state = {
    "running": False,
    "stage": "idle",
    "message": "Ready",
    "error": "",
}


def update_state(**values):
    with _tracker_lock:
        _tracker_state.update(values)


def run_tracker():
    update_state(running=True, stage="fetching", message="Fetching latest members...", error="")
    try:
        process = subprocess.run(
            [sys.executable, "tracker.py"],
            cwd=PROJECT_DIR,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        if process.returncode:
            raise RuntimeError(process.stderr.strip() or process.stdout.strip() or "tracker.py failed")
        update_state(stage="refreshing", message="Refreshing retained comparison...")
        process = subprocess.run(
            [sys.executable, "tracker.py", "--refresh-period"],
            cwd=PROJECT_DIR,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        if process.returncode:
            raise RuntimeError(process.stderr.strip() or process.stdout.strip() or "period refresh failed")
        update_state(running=False, stage="done", message="Latest members loaded")
    except Exception as error:
        update_state(running=False, stage="error", message="Refresh failed", error=str(error))


class DashboardHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if urlparse(self.path).path == "/api/refresh/status":
            self.send_json(_tracker_state)
            return
        super().do_GET()

    def do_POST(self):
        if urlparse(self.path).path != "/api/refresh":
            self.send_error(404)
            return
        with _tracker_lock:
            if _tracker_state["running"]:
                self.send_json(_tracker_state, 409)
                return
            _tracker_state.update(running=True, stage="queued", message="Starting refresh...", error="")
        threading.Thread(target=run_tracker, daemon=True).start()
        self.send_json(_tracker_state, 202)

    def send_json(self, payload, status=200):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    os.chdir(PROJECT_DIR)
    print("Dashboard: http://localhost:%s/web/" % PORT)
    ThreadingHTTPServer(("", PORT), DashboardHandler).serve_forever()
