import http.server, ssl
from handlers.HTTPRequestHandler import HTTPRequestHandler
from Logger import ConsoleLogger


class Server:
    def __init__(self, address, port, secure=True):
        self.address = address
        self.port = port
        self.certificate = "cert.pem"
        self.privateKey = "key.pem"
        self.httpServer = http.server.HTTPServer((self.address, self.port), HTTPRequestHandler)
        self.logger = ConsoleLogger()

        #Insecure socket (plain text on the network)
        self.insecureSocket = self.httpServer.socket

        #Secure socket, uses TLS 1.2
        self.secureSocket = None


        #If secure==True then wraps the server socket with a socket using TLS 1.2
        if(secure == True):
            #SSL/TLS allowed versions. Forces the client to use TLS 1.2
            sslTLSVersion = ssl.PROTOCOL_TLSv1_2

            #Wraps the server socket to use tls
            self.secureSocket = ssl.wrap_socket(self.httpServer.socket,
                   server_side=True,
                   keyfile=self.privateKey,
                   certfile=self.certificate,
                   ssl_version=sslTLSVersion
            )

            self.httpServer.socket = self.secureSocket
        else:
            self.logger.warning("The server is running in insecure mode!")


    def start(self):
        self.logger.info("Server started at port: "+str(self.port))
        self.httpServer.serve_forever()
