from http.server import BaseHTTPRequestHandler
from database.SQLiteDatabase import SQLiteDatabase


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
        db = SQLiteDatabase()
        message = str(db.getAllUsers())
        self.sendResponse(message)


    def sendResponse(self, data):
        self.sendHeaders(data)
        self.sendContent(data)
