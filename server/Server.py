import http.server, ssl
from handlers.HTTPRequestHandler import HTTPRequestHandler


class Server:
    def __init__(self, address, port):
        self.address = address
        self.port = port
        self.certificate = "cert.pem"
        self.privateKey = "key.pem"
        self.httpServer = http.server.HTTPServer((self.address, self.port), HTTPRequestHandler)

        #SSL/TLS allowed versions. Forces the client to use TLS 1.2
        #sslTLSVersion = ssl.PROTOCOL_TLSv1_2
        #sslTLSVersion |= ssl.OP_NO_SSLv3
        #sslTLSVersion |= ssl.OP_NO_TLSv1
        #sslTLSVersion |= ssl.OP_NO_TLSv1_1

        #Wraps the server socket to use tls
        #self.httpServer.socket = ssl.wrap_socket(self.httpServer.socket,
               #server_side=True,
               #keyfile=self.privateKey,
               #certfile=self.certificate,
               #ssl_version=sslTLSVersion
        #)

    def start(self):
        print("Server started at port: "+str(self.port))
        self.httpServer.serve_forever()
