import threading
import socket
from pyngrok import ngrok
from constants import*
#from participant import Participant

#TODO: use zero knowledge proof for auth. 
# recursive zero knowledge proof

def parity_of_indexes(raw_key,indexes):
    s = 0
    for i in indexes:
        s += raw_key[i]
    return s%2

class Server(socket.socket):
    def __init__(self, server_type = LOCAL_SERVER, port = LOCAL_PORT):
        super().__init__()

        self.clients = []
        self.nicknames = []
        self.alices_key = [0,1,1,0] # currently assuming alices key to be alist
        
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
        self.listen()
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
        send_length += " "*(HEADER - msg_length)
        client.send(send_length.encode(FORMAT))
        client.send(message.encode(FORMAT))

    def handle_client(self, client,address):
        connected = True
        while connected:
            msg_received = self.receive_a_message_from_client(client)
            print(f"[Client @ {address}]: {msg_received}")
            if msg_received.startswith("ask_parity"):
                self.ask_parity_return_message(msg_received)
                
            if msg_received == "disconnect":
                try :
                    self.send_a_message_to_the_client(client, "Goodbye!")
                    connected = False                    
                except:
                    client.close()
                finally:
                    print(f"[SERVER]: Client @ {address} Disconnected!")

            '''
            if msg_received == "stop server":
                self.stop_server()
                print(f"[STOPPING] local server is closing")
                connected = False'''

    def ask_parity_return_message(self,msg_received,client):
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
        self.send_a_message_to_the_client(client, msg_to_send)

    def start_receiving(self):
        while True:
            client,addr = self.accept()
            #client.address = addr
            self.clients.append(client)
            print(f"Connected with {addr}")

            thread = threading.Thread(target=self.handle_client, args = (client,addr))
            print(f"[ACTIVE CONNECTIONS]: {threading.active_count()} clients are connected!")
            thread.start()
            
    
    def stop_server(self):
        self.shutdown(socket.SHUT_RDWR)
        self.close()
    
    def broadcast_to_all(self, message):
        for client in self.clients:
            thread = threading.Thread(target=self.send_a_message_to_the_client, args = ())
            self.send_a_message_to_the_client(client)

class Client(socket.socket):
    def __init__(self, server_address = (LOCAL_IP,LOCAL_PORT)):
        super().__init__()
        self.parity_dict = {}
        self.parity_msgs_sent = 0
        self.server_address = server_address
        #self.__setattr__("address",None)
        self.connect(self.server_address)

        rthread = threading.Thread(target=self.receive_from_server)
        #wthread = threading.Thread(target=self.write_to_server)
        rthread.start()
        #wthread.start()

    
    def ask_for_parity_from_server(self,indexes:list):
        self.parity_msgs_sent += 1
        msg_no = self.parity_msgs_sent
        indexes = str(indexes)
        indexes = indexes[1:-1]
        self.send_a_message_to_server(f"ask_parity:{msg_no}:{indexes}")
        msg_recvd = self.receive_a_message_from_server()
        splitted_msg_recv = msg_recvd.split(":")
        ap = splitted_msg_recv[0]
        if ap == "ask_parity":
            def exists_in_parity_dict(msg_no):
                parity = self.parity_dict.get(f"{msg_no}")
                if parity == None:
                    return False
                else:
                    return True

            msg_no_returned = int(splitted_msg_recv[1])
            parity = int(splitted_msg_recv[2])
            if msg_no_returned == msg_no:
                return  parity
            elif exists_in_parity_dict(msg_no):                
                parity = self.parity_dict.get(f"{msg_no}")
                self.parity_dict.pop(f"{msg_no}")
                return parity                
            else:
                self.parity_dict.add(f"{msg_no_returned}",parity)
            
    
    def receive_a_message_from_server(self):
        msg_length = self.recv(HEADER).decode(FORMAT)
        if msg_length:
            try:
                msg_length = int(msg_length)
                message = self.recv(int(msg_length)).decode(FORMAT)
                return message
            except:
                if msg_length == ' ':
                    print("Invalid Literal for int")

    def send_a_message_to_server(self,message):
        msg_length = len(message)
        send_length = str(msg_length)
        send_length += " "*(HEADER - msg_length)
        self.send(send_length.encode(FORMAT))
        self.send(message.encode(FORMAT))


    def receive_from_server(self):
        connected = True
        while connected:
            msg_received = self.receive_a_message_from_server()
            print(f"[SERVER]: {msg_received}")
                

    def write_to_server(self):
        connected = True
        while connected:
            msg_to_send = input("Enter your message: ")
            if msg_to_send == "disconnect":
                connected = False
            else:
                self.send_a_message_to_server(msg_to_send)
        self.close()
