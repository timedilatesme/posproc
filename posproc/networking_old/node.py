import os
import socket
import string, random
from ellipticcurve.privateKey import PrivateKey
from ellipticcurve.publicKey import PublicKey
from pyngrok import ngrok
from posproc import constants
from posproc.authentication import Authentication

class _Node(socket.socket):
    def __init__(self, username, auth_Keys: tuple[PublicKey, PrivateKey] = None):
        super().__init__()
        
        self.username = username
        
        self._add_authentication_token(auth_Keys=auth_Keys)
        
    def _get_auth_keys(self):
        """
        Public Key, Private Key
        """
        return self.auth_id,self._auth_key
    
    def save_auth_keys_as_txt(self,path):
        # os.path.join
        # fh = open()
        pass        
    
    def get_username(self):
        return self.username
    
    def get_auth_id(self):
        return self.auth_id
    
    def _add_authentication_token(self, auth_Keys):
        self._auth = Authentication(auth_Keys=auth_Keys)
        self.auth_id,self._auth_key = self._auth._get_key_pair()
    
    @staticmethod                 
    def reduce_original_message_to_one_byte(message: bytes) -> list[bytes]:
        """
        Gives a list containing the original message and the lengths to be send in each iteration.

        Args:
            message (bytes): original message to be sent.

        Returns:
            list[bytes]
        """
        all_msgs = [message]
        msg = message
        while True:
            if len(msg) == 1:
                break
            else:
                msg = str(len(msg))
                msg = msg.encode(constants.FORMAT)
                all_msgs.insert(0, msg)
        return all_msgs          
        
    def send_bytes_to_the_server(self, message:bytes) -> None:
        """
        Bob sends bytes to the server i.e. Alice 

        Args:
            message (bytes): The message to be sent in the form of a bytes.
        """
        messages = self.reduce_original_message_to_one_byte(message)
        # print("The messages being sent: ", messages[:-1], messages[-1][0:10])
        
        for msg in messages:
            self.sendall(msg)
    
    def receive_bytes_from_the_server(self) -> bytes:
        """
        Bob can receive bytes from the server i.e. Alice.

        Returns:
            message (bytes): The bytes received from the Server i.e. Alice.
        """
        '''msg_0 = self.recv(1) # Receive the first msg in messages = [b'oneDigitNo', ....]

        if msg_0:
            try:
                msg_len = msg_0
                while msg_len.isdigit():
                    msg_len = self.recv(int(msg_len))
                    
                return msg_len
            except:
                if msg_0 == ' ':
                    print("Blank Message!")'''
        BUFF_SIZE = 4096
        
        msg_0 = self.recv(1)
        
        data = b''
        if(msg_0):
            try:
                msg_len = self.recv(int(msg_0))
                while True:
                    part = self.recv(BUFF_SIZE)
                    data+=part
                    
                    if(len(part)<BUFF_SIZE):
                        #print("LENGTH OF RECIEVED DATA IS:",len(data))
                        #print("DATA IS:",data)
                        break
                return data
            except:
                if(msg_0 == ' '):
                    print("Blank Message!")    
        
    @staticmethod
    def send_bytes_to_the_client(client, message: bytes) -> None:
        """
        Alice (Server) can send a message to Bob(Client).

        Args:
            client (ActiveClient): The client who is going to receive message i.e. Bob.
            message (bytes): The message to be sent to Bob.
        """
        messages = Node.reduce_original_message_to_one_byte(message)

        for msg in messages:
            client.sendall(msg)

    @staticmethod
    def receive_bytes_from_the_client(client:socket.socket) -> bytes:
        """
        Alice (Server) can receive a message from Bob (Client)

        Args:
            client (ActiveClient): The client who is going to send the message i.e. Bob.

        Returns:
            message (bytes): The message received from Bob(Client)
        """
        '''msg_0 = client.recv(1)  # Receive the first msg in messages = [b'oneDigitNo', ....]

        if msg_0:
            try:
                msg_len = msg_0
                while msg_len.isdigit():
                    msg_len = client.recv(int(msg_len))
                return msg_len
            except:
                if msg_0 == ' ':
                    print("Blank Message!")'''
        
        BUFF_SIZE = 4096
        
        msg_0 = client.recv(1)
        
        data = b''
        if(msg_0):
            try:
                msg_len = client.recv(int(msg_0))
                while True:
                    part = client.recv(BUFF_SIZE)
                    data+=part
                    
                    if(len(part)<BUFF_SIZE):
                        #print("LENGTH OF RECIEVED DATA IS:",len(data))
                        #print("DATA IS:",data)
                        break
                return data
            except:
                if(msg_0 == ' '):
                    print("Blank Message!")   
    
    @staticmethod
    def start_ngrok_tunnel(port):
        """
        NGROK tunnel is used for port forwarding the ngrok address to the local address

        Args:
            port (int): Local Port which is to be used for forwarding. 
                        (Use the port that is not already being used by your system.)
        Returns:
            public_addr (tuple): This is what a public pc can use to connect to this Server.
                                 This is a pair (PUBLIC_IP, PUBLIC_PORT)
        """
        tunnel = ngrok.connect(port, "tcp")
        url = tunnel.public_url.split("://")[1].split(":")
        ip = socket.gethostbyaddr(url[0])[-1][0]
        public_addr = (ip, int(url[1]))
        return public_addr

class Node(_Node):
    pass

# class Node(_Node):
#     CHUNK_SIZE = 100 # must be greater than the packet start delimeter length.
#     PACKET_START_DELIMETER = b'###'
#     PACKET_END_DELIMETER = b'$$$'
#     PACKER_DATA_SEPARATOR = b':::'
    
#     def send_bytes_to_the_server(self, message: bytes) -> None:
#         messageLength = len(message)
#         messageToSend = self.PACKET_START_DELIMETER + messageLength + \
#             self.PACKER_DATA_SEPARATOR + message + self.PACKET_END_DELIMETER
#         self.sendall(messageToSend)
    
#     def receive_bytes_from_the_server(self) -> bytes:
#         messageReceived = self.recv(self.CHUNK_SIZE)
#         if messageReceived.startswith(self.PACKET_START_DELIMETER):
#             messageReceived = messageReceived.removeprefix(self.PACKET_START_DELIMETER)
#             sepStartIndex1 = messageReceived.find(self.PACKER_DATA_SEPARATOR)
#             messageLength = messageReceived[0:sepStartIndex1]
#             messageReceived.removeprefix(messageLength + self.PACKER_DATA_SEPARATOR)
#             messageLength = int(messageLength)
            
#             if messageLength <= len(messageReceived):
#                 return messageReceived[0:messageLength]
#             else:
#                 while not messageReceived.endswith(self.PACKET_END_DELIMETER):
#                     messageReceived += self.recv(self.CHUNK_SIZE)
#                 messageReceived.removesuffix(self.PACKET_END_DELIMETER)
#                 return messageReceived
            
#     @staticmethod
#     def send_bytes_to_the_client(client, message: bytes) -> None:
#         messageLength = len(message)
#         messageToSend = Node.PACKET_START_DELIMETER +  str(messageLength).encode(constants.FORMAT) + \
#             Node.PACKER_DATA_SEPARATOR + message + Node.PACKET_END_DELIMETER
#         client.sendall(messageToSend)    
            
#     @staticmethod
#     def receive_bytes_from_the_client(client: socket.socket) -> bytes:
#         messageReceived = client.recv(Node.CHUNK_SIZE)
#         if messageReceived.startswith(Node.PACKET_START_DELIMETER):
#             messageReceived = messageReceived.removeprefix(
#                 Node.PACKET_START_DELIMETER)
#             sepStartIndex1 = messageReceived.find(Node.PACKER_DATA_SEPARATOR)
#             messageLength = messageReceived[0:sepStartIndex1]
#             messageReceived.removeprefix(
#                 messageLength + Node.PACKER_DATA_SEPARATOR)
#             messageLength = int(messageLength)

#             if messageLength <= len(messageReceived):
#                 return messageReceived[0:messageLength]
#             else:
#                 while not messageReceived.endswith(Node.PACKET_END_DELIMETER):
#                     messageReceived += client.recv(Node.CHUNK_SIZE)
#                 messageReceived.removesuffix(Node.PACKET_END_DELIMETER)
#                 return messageReceived 