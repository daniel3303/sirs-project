from http.server import BaseHTTPRequestHandler

class HTTPRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, request, clientAddress, server):
        super().__init__(request, clientAddress, server)

    def sendHeaders(self, data):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header("Content-Length", len(data.encode()))
        self.end_headers()


    def sendContent(self, data):
        self.wfile.write(data.encode())

    def do_GET(self):
        message = "Olá\n\n"
        self.sendResponse(message)


    def sendResponse(self, data):
        self.sendHeaders(data)
        self.sendContent(data)
