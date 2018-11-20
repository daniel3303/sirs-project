from Server import Server

server = Server("", 8080, secure=False) #set secure = False for debug only
server.start()
