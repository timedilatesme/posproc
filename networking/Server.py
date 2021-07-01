import random
import threading
import socket
from pyngrok import ngrok
from constants import*

class Server(socket.socket):
    def __init__(self, server_type = LOCAL_SERVER, port = LOCAL_PORT):
        super().__init__()

        self.clients = []

        key_length = int(input("Enter Key-Length: "))
        self.alices_key = random_key(key_length) # currently assuming alices key to be alist
        
        self.server_type = server_type
        self.port = port
        
        if server_type == LOCAL_SERVER:
            self.address = (LOCAL_IP, self.port)
        if server_type == PUBLIC_SERVER:
            self.address = self.start_ngrok_tunnel(self.port)
        
        self.LOCAL_ADDRESS = (LOCAL_IP,LOCAL_PORT) # The Server will start on this address
        # Then we can port-forward the ngrok address to this address

        self.start_listening()     

        # Now Start accepting connections:
        self.start_receiving()
        
        
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
        self.listen(1)
        print(f"[LISTENING] Server is listening @ {self.get_address()}")
    
    def receive_a_message_from_client(self,client):
        msg_length = client.recv(HEADER).decode(FORMAT)
        if msg_length:
            try:
                msg_length = int(msg_length)
                message = client.recv(int(msg_length)).decode(FORMAT)
                return message
            except:
                if msg_length == ' ':
                    print("Blank Message!")
    
    def send_a_message_to_the_client(self,client,message):
        msg_length = len(message)
        send_length = str(msg_length)
        send_length += " "*(HEADER - len(send_length))
        client.send(send_length.encode(FORMAT))
        client.send(message.encode(FORMAT))

    def handle_client(self, client,address):
        connected = True
        while connected:
            msg_received = self.receive_a_message_from_client(client)
            if msg_received:
                print(f"[Client @ {address}]: {msg_received}")
                if msg_received.startswith("ask_parity"):
                    msg_to_send = self.ask_parity_return_message(msg_received)
                    self.send_a_message_to_the_client(client, msg_to_send)
                
    def ask_parity_return_message(self,msg_received:str):
        splitted_parity_msg = msg_received.split(":")
        msg_no = int(splitted_parity_msg[1])
        indexes_o = splitted_parity_msg[2].split(",")
        indexes = []
        for i in indexes_o:
            indexes.append(int(i))
        #indexes contains the indexes of bits to calculate parities!
        # Assuming Alice is the instance of this Server Class
        parity = parity_of_indexes(self.alices_key, indexes)
        msg_to_send = f"ask_parity:{msg_no}:{parity}"
        return msg_to_send

    def start_receiving(self):
        while True:
            client,addr = self.accept()
            #client.address = addr
            #self.clients.append(client)
            print(f"Connected with {addr}")

            thread = threading.Thread(target=self.handle_client, args = (client,addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS]: {threading.active_count() - 1} clients are connected!")
            #self.handle_client(client,addr)
            
    
    def stop_server(self):
        self.shutdown(socket.SHUT_RDWR)
        self.close()
    
    def broadcast_to_all(self, message):
        for client in self.clients:
            thread = threading.Thread(target=self.send_a_message_to_the_client, args = ())
            self.send_a_message_to_the_client(client)