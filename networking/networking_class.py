import threading
import socket
from pyngrok import ngrok
from constants import*
#from participant import Participant

class Server(socket.socket):
    def __init__(self, server_type = LOCAL_SERVER, port = LOCAL_PORT):
        super().__init__()
        
        self.server_type = server_type
        self.port = port
        
        if server_type == LOCAL_SERVER:
            self.__setattr__("address", (LOCAL_IP, LOCAL_PORT))
        if server_type == PUBLIC_SERVER:
            self.address = self.start_ngrok_tunnel(self.port)
        
        LOCAL_ADDRESS = (LOCAL_IP,LOCAL_PORT) # The Server will start on this address
        # Then we can port-forward the ngrok address to this address

        print(f"[STARTING] {self.server_type} server is starting...")
        self.bind(LOCAL_ADDRESS)
        self.listen()
        print(f"[LISTENING] Server is listening @ {self.get_address()}")

    
    def start_ngrok_tunnel(self,port):
        tunnel = ngrok.connect(port, "tcp")
        url = tunnel.public_url.split("://")[1].split(":")
        ip = socket.gethostbyaddr(url[0])[-1][0]
        public_addr = (ip, int(url[1]))
        return public_addr

    def start(self):
        pass

    def get_address(self):
        return self.address

class Client:
    pass
