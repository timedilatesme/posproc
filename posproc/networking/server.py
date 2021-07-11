import pickle
import sys
import threading
from socket import socket
import numpy as np

from posproc.networking.node import Node
from posproc.networking.user_data import User, UserData
from posproc import constants
from posproc.key import Key

"""
This module contains code for active client who is going to be doing all the computation.
In theory we consider bob to be the active client who asks question to alice about parity
and Alice is an passive client who is just going to reply to all the questions that bob
asks.
"""

MSG_NO_HEADER = 10 
#What is the maximum length of the msg_no. for eg if MSG_NO_HEADER = 2 => maximum value of msg_no is 99.


class Server(Node):
    """
    Creates the Server (Alice's) socket.

    """
    def __init__(self, username,correct_key:Key, user_data:UserData = None,server_type=constants.LOCAL_SERVER, port=constants.LOCAL_PORT):
        """
        Alice's key is needed for performing computation.
        This Node will only run on Alice's address so only she knows the correct key.
        
        Args:
            correct_key (Key): Alice's Key Obtained from the QKD protocol.
            user_data (UserData): The object that will store all the data about users on the network.
            server_type (str, optional): [Either LOCAL_SERVER or PUBLIC_SERVER {defined in constants.py}]. Defaults to LOCAL_SERVER.
            port (int, optional): [The local port to be used for hosting the server. Defaults to LOCAL_PORT]. Defaults to LOCAL_PORT.
        """
        super().__init__(username)
        #This is the correct_key i.e. the Key that Alice has.
        #TODO: __ or _ for best security?
        self._correct_key = correct_key
        self.server_type = server_type
        self.port = port
        
        self._pending_clients_for_setting_active = {}
        
        self.reconciliation_status = {'cascade': 'Not yet started', 
                                      'winnow': 'Not yet started', 
                                      'ldpc': 'Not yet started', 
                                      'polar': 'Not yet started'}
        
        self.address = None
        self._set_the_address_variable()
        
        #userdata, an instance of UserData contains the data of all clients connected to Alice (SERVER)
        self.user_data = user_data
        
        #Add server data to user_data:
        self.user = User(self.username, self.address, self.auth_id)
        self.user_data.update_user_data(self.user)

        self.server_type = server_type
        self.port = port

        # The Server will start on this address
        self.LOCAL_ADDRESS = (constants.LOCAL_IP, constants.LOCAL_PORT)
        # Then we can port-forward the ngrok address to this address

        self.start_listening()
        self.server_is_active = True

        # Now Start accepting connections:
        self.start_receiving()

    def get_address(self):
        """
        Returns the current address either local or public

        Returns:
            server_address [tuple]: In the form (IP,PORT)
        """
        return self.address
    
    def _set_the_address_variable(self):
        if self.server_type == constants.LOCAL_SERVER:
            self.address = (constants.LOCAL_IP, self.port)
        if self.server_type == constants.PUBLIC_SERVER:
            self.address = self.start_ngrok_tunnel(self.port)
        

    def start_listening(self):
        print(f"[STARTING] {self.server_type} server is starting...")
        self.bind(self.LOCAL_ADDRESS)
        self.listen()
        print(f"[LISTENING] Server is listening @ {self.get_address()}")
    
    def _authentication_process_return(self, msg_received, client_user):
        """
        Checks whether authentication message is valid or not.      

        Args:
            msg_received ([str]): The message received from client.
            client_user ([User]): The client User object.

        Returns:
            [bool]: Returns whether or not the message received is valid or not  
        """
        # This initial number represents the 'authentication:' part to be removed
        msg_recvd_bytes = msg_received.removeprefix(
            'authentication:'.encode(constants.FORMAT))
        msg_recvd = pickle.loads(msg_recvd_bytes)
        msg = msg_recvd[0]
        signature = msg_recvd[1]
        client_pub_key = client_user.auth_id
        verify = self._auth.verify(msg,
                                   signature,
                                   client_pub_key)      
        return verify

    def _ask_parities_return_message(self,msg_recvd:bytes):
        #message_recvd = b'ask_parities:[block_indexes as list,[],[],...]'
        block_indexes_list_bytes = msg_recvd.removeprefix('ask_parities:'.encode(constants.FORMAT))
        #print(block_indexes_list_bytes)
        block_indexes_list = pickle.loads(block_indexes_list_bytes)
        
        #TODO: Store the information leaked into some new object to help in privacy amplification.
        parities = []
        for block_indexes in block_indexes_list:
            parity = self._correct_key.get_indexes_parity(block_indexes)
            parities.append(parity)
        msg_to_send = 'ask_parities:'.encode(constants.FORMAT) + pickle.dumps(parities)
        return msg_to_send
    
    def start_receiving(self):
        #TODO: Make some way to stop the server!
        while self.server_is_active:
            client, addr = self.accept()
            print(f"Connected with {addr}")
            #client_user.set_connected_to_server(self, True) #TODO: check if this updates the user_data.            

            thread = threading.Thread(
                target=self.handle_client, args=(client, addr))
            thread.start()
            
            if addr in self._pending_clients_for_setting_active.keys():
                client_username = self._pending_clients_for_setting_active.pop(addr)
                client_user = self.user_data.get_user_by_name(client_username)
                client_user.address = addr
            else:
                for addre,username in self._pending_clients_for_setting_active.items():
                    client_user = self.user_data.get_user_by_name(username)
                    client_user.address = addre
                    
                    
            
            print(
                f"[ACTIVE CONNECTIONS]: {threading.active_count() - 1} clients are connected!")
    
    def handle_client(self, client: socket, address: tuple) -> None:
        connected = True
        while connected:
            msg_received = self.receive_bytes_from_the_client(client)

            if msg_received:
                if msg_received.startswith("username:".encode(constants.FORMAT)):
                    client_username = msg_received.removeprefix(
                        "username:".encode(constants.FORMAT))
                    client_username = client_username.decode(constants.FORMAT)
                    self._pending_clients_for_setting_active[client_username] = address
                if msg_received.startswith('authentication'.encode(constants.FORMAT)):
                    verify = self._authentication_process_return(
                        msg_received, client_user)
                    if verify:
                        #TODO: add something for random length
                        # Send the first message for authentication
                        msg_to_send_1 = self.random_string_generator()
                        # TODO: can add more hash functions randomly
                        msg_to_send_2 = self._auth.sign(msg_to_send_1)

                        msg_to_send = (msg_to_send_1, msg_to_send_2)
                        # TODO: add a way so that authentication is also hidden.
                        msg_to_send_bytes = "authentication:".encode(
                            constants.FORMAT) + pickle.dumps(msg_to_send)

                        self.send_bytes_to_the_client(msg_to_send_bytes)
                    else:
                        connected = False
                        client.close()

                elif msg_received.startswith('ask_parities'.encode(constants.FORMAT)):
                    msg_to_send = self._ask_parities_return_message(
                        msg_received)
                    self.send_bytes_to_the_client(client, msg_to_send)

                elif msg_received.startswith('reconciliation_status'.encode(constants.FORMAT)):
                    splitted_msg = msg_received.split(b':')
                    reconciliation_algorithm = splitted_msg[1].decode(
                        constants.FORMAT)
                    status = splitted_msg[2].decode(constants.FORMAT)
                    self.reconciliation_status[reconciliation_algorithm] = status
                    if self.reconciliation_status['cascade'] == 'Completed':
                        print("Alice's New Key:", self._correct_key)

                elif msg_received.startswith('qber_estimation'.encode(constants.FORMAT)):
                    indexes_bytes = msg_received.removeprefix(
                        'qber_estimation:'.encode(constants.FORMAT))
                    indexes = pickle.loads(indexes_bytes)
                    bits_dict = self._correct_key.get_bits_for_qber_estimation(
                        indexes)
                    bits_dict_bytes = pickle.dumps(bits_dict)
                    msg_to_send = 'qber_estimation:'.encode(
                        constants.FORMAT) + bits_dict_bytes
                    self.send_bytes_to_the_client(client, msg_to_send)

                elif msg_received == 'close_server'.encode(constants.FORMAT):
                    self.server_is_active = False
                    #TODO : Is this good enough?
                    sys.exit()

                else:
                    print(f"[Client @ {address}]: {msg_received}")
            else:
                continue                
    
    def stop_server(self):
        #TODO: Make it work!
        self.server_is_active = False
        exit()

    def broadcast_to_all(self, message: bytes):
        for client in self.active_clients:
            self.send_bytes_to_the_client(client, message)
        

class Server_to_simulate_eavesdropping(Server):
    pass
