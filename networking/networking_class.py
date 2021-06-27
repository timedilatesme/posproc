import threading
import socket
from pyngrok import ngrok
from constants import*
#from participant import Participant

#TODO: use zero knowledge proof for auth. 
# recursive zero knowledge proof

def parity(*args):
    return sum(args)%2

class Server(socket.socket):
    def __init__(self, server_type = LOCAL_SERVER, port = LOCAL_PORT):
        super().__init__()

        self.clients = []
        self.nicknames = []
        
        self.server_type = server_type
        self.port = port
        
        if server_type == LOCAL_SERVER:
            self.__setattr__("address", (LOCAL_IP, LOCAL_PORT))
        if server_type == PUBLIC_SERVER:
            self.__setattr__("address", self.start_ngrok_tunnel(self.port))
        
        self.LOCAL_ADDRESS = (LOCAL_IP,LOCAL_PORT) # The Server will start on this address
        # Then we can port-forward the ngrok address to this address

        self.start_listening()     

        # Now Start accepting connections:


        



    
    def start_ngrok_tunnel(self,port):
        tunnel = ngrok.connect(port, "tcp")
        url = tunnel.public_url.split("://")[1].split(":")
        ip = socket.gethostbyaddr(url[0])[-1][0]
        public_addr = (ip, int(url[1]))
        return public_addr

    def start_listening(self):
        print(f"[STARTING] {self.server_type} server is starting...")
        self.bind(self.LOCAL_ADDRESS)
        self.listen()
        print(f"[LISTENING] Server is listening @ {self.get_address()}")

    def get_address(self):
        return self.address

class Client(socket.socket):
    def __init__(self, server_address = (LOCAL_IP,LOCAL_PORT)):
        super().__init__()
        self.server_address = server_address
        self.connect(self.server_address)
    
    def ask_for_parity(bits_indexes):
        

    def start_receiving():
        #while True:
            #try:
                # Receiving Message From Server
                #message = self.recv(BYTES_TO_RECV).decode(FORMAT)
        pass
