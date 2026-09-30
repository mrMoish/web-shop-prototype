from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

HOST = "localhost"
PORT = 8000


def read_file(path):
    """Читает файл через контекстный менеджер."""
    with open(path, "r", encoding="utf-8") as file:
        return file.read()


class ContactsHandler(BaseHTTPRequestHandler):
    def send_html(self, status, content):
        self.send_response(status)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(content.encode("utf-8"))

    def send_page(self, status, filename):
        try:
            content = read_file(filename)
        except OSError as error:
            print(f"Ошибка чтения {filename}: {error}")
            try:
                content = read_file("500.html")
            except OSError:
                content = "<h1>500 Internal Server Error</h1>"
            self.send_html(500, content)
            return
        self.send_html(status, content)

    def do_GET(self):
        path = urlparse(self.path).path
        # Запросы за файлами (например, /favicon.ico) — 404,
        # на любой другой GET-запрос отдаём «Контакты»
        if "." in path.rsplit("/", 1)[-1] and not path.endswith(".html"):
            self.send_page(404, "404.html")
            return
        self.send_page(200, "contacts.html")

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8")
        content_type = self.headers.get("Content-Type", "")

        print("--- POST-запрос ---")
        print(f"Путь: {self.path}")
        print(f"Content-Type: {content_type}")
        if "application/x-www-form-urlencoded" in content_type:
            for key, values in parse_qs(body).items():
                print(f"{key}: {', '.join(values)}")
        else:
            print(f"Тело: {body}")
        print("-------------------")

        self.send_page(200, "contacts.html")


if __name__ == "__main__":
    server = HTTPServer((HOST, PORT), ContactsHandler)
    print(f"Сервер запущен: http://{HOST}:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nСервер остановлен")
        server.server_close()
