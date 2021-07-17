import socket
import string, random
from ellipticcurve.privateKey import PrivateKey
from ellipticcurve.publicKey import PublicKey
from pyngrok import ngrok
from posproc import constants
from posproc.authentication import Authentication

class Node(socket.socket):
    def __init__(self, username, auth_Keys: tuple[PublicKey, PrivateKey] = None):
        super().__init__()
        
        self.username = username
        
        self._add_authentication_token(auth_Keys=auth_Keys)
        
    def _get_auth_keys(self):
        """
        Public Key, Private Key
        """
        return self.auth_id,self._auth_key
    
    def get_username(self):
        return self.username
    
    def get_auth_id(self):
        return self.auth_id
    
    def _add_authentication_token(self, auth_Keys):
        self._auth = Authentication(auth_Keys=auth_Keys)
        self.auth_id,self._auth_key = self._auth._get_key_pair()
                       
    def send_bytes_to_the_server(self, message:bytes) -> None:
        """
        Bob sends bytes to the server i.e. Alice 

        Args:
            message (bytes): The message to be sent in the form of a bytes.
        """
        msg_length = len(message)
        send_length = str(msg_length)
        send_length += " "*(constants.HEADER - len(send_length))
        
        self.send(send_length.encode(constants.FORMAT))
        self.send(message)

    def receive_bytes_from_the_server(self) -> bytes:
        """
        Bob can receive bytes from the server i.e. Alice.

        Returns:
            message (bytes): The bytes received from the Server i.e. Alice.
        """
        msg_length = self.recv(constants.HEADER).decode(constants.FORMAT)
        if msg_length:
            try:
                msg_length = int(msg_length)
                message = self.recv(int(msg_length))
                return message
            except:
                if msg_length == ' ':
                    print("Invalid Literal for int")  # TODO : fix this error!

    @staticmethod
    def send_bytes_to_the_client(client, message: bytes) -> None:
        """
        Alice (Server) can send a message to Bob(Client).

        Args:
            client (ActiveClient): The client who is going to receive message i.e. Bob.
            message (bytes): The message to be sent to Bob.
        """
        msg_length = len(message)
        send_length = str(msg_length)
        send_length += " "*(constants.HEADER - len(send_length))
        client.send(send_length.encode(constants.FORMAT))
        client.send(message)

    @staticmethod
    def receive_bytes_from_the_client(client) -> bytes:
        """
        Alice (Server) can receive a message from Bob (Client)

        Args:
            client (ActiveClient): The client who is going to send the message i.e. Bob.

        Returns:
            message (str): The message received from Bob(Client)
        """
        msg_length = client.recv(constants.HEADER).decode(constants.FORMAT)
        if msg_length:
            try:
                msg_length = int(msg_length)
                message = client.recv(int(msg_length))
                return message
            except:
                if msg_length == ' ':
                    print("Blank Message!")  # TODO : fix this error!
    
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