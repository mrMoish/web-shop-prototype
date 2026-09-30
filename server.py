from http.server import BaseHTTPRequestHandler, HTTPServer


class ContactsHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # На любой GET-запрос отдаём страницу «Контакты»
        with open("contacts.html", "r", encoding="utf-8") as file:
            content = file.read()

        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(content.encode("utf-8"))


if __name__ == "__main__":
    server = HTTPServer(("localhost", 8000), ContactsHandler)
    print("Сервер запущен: http://localhost:8000")
    server.serve_forever()
