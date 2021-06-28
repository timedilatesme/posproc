import threading
import socket
from pyngrok import ngrok
from constants import*
#from participant import Participant

#TODO: use zero knowledge proof for auth. 
# recursive zero knowledge proof


class Server(socket.socket):
    def __init__(self, server_type = LOCAL_SERVER, port = LOCAL_PORT):
        super().__init__()

        self.clients = []
        self.nicknames = []
        
        self.server_type = server_type
        self.port = port
        
        if server_type == LOCAL_SERVER:
            self.address = (LOCAL_IP, LOCAL_PORT)
        if server_type == PUBLIC_SERVER:
            self.address = self.start_ngrok_tunnel(self.port)
        
        self.LOCAL_ADDRESS = (LOCAL_IP,LOCAL_PORT) # The Server will start on this address
        # Then we can port-forward the ngrok address to this address

        self.start_listening()     

        # Now Start accepting connections:     
        
    def get_address(self):
        return self.address
    
    def start_ngrok_tunnel(self, port):
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
    
    def receive_a_message_from_client(self,client) -> str:
        msg_length = client.recv(HEADER).decode(FORMAT)
        if msg_length:
            message = client.recv(int(msg_length)).decode(FORMAT)
        return message
    
    def send_a_message_to_the_client(self,client,message) -> None:
        msg_length = len(message)
        send_length = msg_length.encode(FORMAT)
        send_length += " "*(HEADER - msg_length)
        client.send(send_length)
        client.send(message)

    def handle_client(self, client):
        connected = True
        while connected:
            msg_received = self.receive_a_message_from_client(client)
            if msg_received == "Hi":
                self.send_a_message_to_the_client(client, "Hello")
            if msg_received == "disconnect":
                self.send_a_message_to_the_client(client, "Goodbye!")
                connected = False
        client.close()

    def start_receiving(self):
        while True:
            client,addr = self.accept()
            client.address = addr
            self.clients.append(client)
            print(f"Connected with {addr}")

    

class Client(socket.socket):
    def __init__(self, server_address = (LOCAL_IP,LOCAL_PORT)):
        super().__init__()
        self.server_address = server_address
        self.address = None
        self.connect(self.server_address)
    
    def ask_for_parity_to_server(self,block):
        pass
    
    def receive_a_message_from_server(self) -> str:
        msg_length = self.recv(HEADER).decode(FORMAT)
        if msg_length:
            message = self.recv(int(msg_length)).decode(FORMAT)
        return message

    def send_a_message_to_server(self,message) -> None:
        msg_length = len(message)
        send_length = msg_length.encode(FORMAT)
        send_length += " "*(HEADER - msg_length)
        self.send(send_length)
        self.send(message)

    def start_receiving(self):
        pass
