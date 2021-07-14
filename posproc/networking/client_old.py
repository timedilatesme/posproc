from posproc.networking.user_data import UserData,User
from posproc.key import Key
from posproc.networking.node import Node
from posproc import constants
import pickle
from posproc.error_correction.cascade.block import Block
import random
import numpy as np

class Client(Node):
    def __init__(self, username, noisy_key: Key, user_data: UserData, server_address=(constants.LOCAL_IP, constants.LOCAL_PORT)):
        #TODO: Convert args to kwargs for easy implementation.
        super().__init__(username)
        #TODO add way to check for already existing username.
        self._noisy_key = noisy_key

        self.server_address = server_address
        self.user_data = user_data
        print(f"User Data: {self.user_data}")
        
        self.user = User(username=self.username,
                         auth_id=self.auth_id)
        self.user_data.update_user_data(self.user)
        self.connected_to_server = self.user.connected_to_server
        self.connect(self.server_address)
        self.send_username_to_server()
        
        verify = self.authentication_process()
        if verify:
            print("Authentication Successful!")
        else:
            print("Authentication Unsuccessful!")
            self.connected_to_server = False
            self.close()
            
        self.reconciliation_status = {'cascade': 'Not yet started', 
                                      'ldpc': 'Not yet started', 
                                      'polar': 'Not yet started'}
        
    
    def send_username_to_server(self):
        msg_to_send = "username:" + self.user.username
        self.send_bytes_to_the_server(msg_to_send.encode(constants.FORMAT))
    def start_receiving(self):
        while self.connected_to_server:
            msg_recvd = self.receive_bytes_from_the_server()
            if msg_recvd.startswith("username:?".encode(constants.FORMAT)):
                self.send_bytes_to_the_server(f"username:{self.user.username}".encode(constants.FORMAT))
            else:
                print(msg_recvd.decode(constants.FORMAT))
    def authentication_process(self):
        #TODO: add something for random length
        # Send the first message for authentication
        msg_to_send_1 = self.random_string_generator()
        # TODO: can add more hash functions randomly
        msg_to_send_2 = self._auth.sign(msg_to_send_1)

        msg_to_send = (msg_to_send_1, msg_to_send_2)
        # TODO: add a way so that authentication is also hidden.
        msg_to_send_bytes = "authentication:".encode(
            constants.FORMAT) + pickle.dumps(msg_to_send)

        self.send_bytes_to_the_server(msg_to_send_bytes)
        
        while self.connected_to_server:
            msg_recvd = self.receive_bytes_from_the_server()
            if msg_recvd:
                if msg_recvd.startswith('authentication'.encode(constants.FORMAT)):
                    # This initial number represents the 'authentication:' part to be removed
                    msg_recvd_bytes = msg_recvd.removeprefix(
                        'authentication:'.encode(constants.FORMAT))
                    msg_recvd = pickle.loads(msg_recvd_bytes)
                    msg = msg_recvd[0]
                    signature = msg_recvd[1]
                    server_user = self.user_data.get_user_by_address(self.server_address)
                    server_pub_key = server_user.auth_id
                    verify = self._auth.verify(msg, 
                                               signature, 
                                               server_pub_key)
                    return verify
        
    def ask_parities(self, blocks):
        """
        Sends blocks as bytes to the server and then the server
        replies with the appropriate parities of the blocks asked.

        Args:
            blocks (list(Block)): Contains all the blocks whose parity is to be asked.

        Returns:
            parities (list(int)): Contains parities in the same order as the blocks in blocks.
        """
        # Only send the indexes for parity.
        # TODO: make this algo faster it's currently very slow for large blocks.
        block_indexes_list = [block.get_key_indexes() for block in blocks]
        # TODO: add tracking of parity messages.
        block_indexes_list_bytes = pickle.dumps(block_indexes_list)
        msg_to_send = 'ask_parities:'.encode(constants.FORMAT) + block_indexes_list_bytes
        
        # asking:
        self.send_bytes_to_the_server(msg_to_send)
        
        # receiving:
        while self.connected_to_server:
            msg_recvd = self.receive_bytes_from_the_server()            
            if msg_recvd:
                if msg_recvd.startswith('ask_parities'.encode(constants.FORMAT)):
                    # This initial number represents the 'ask_parities:' part to be removed
                    parities_bytes = msg_recvd.removeprefix(
                        'ask_parities:'.encode(constants.FORMAT))
                    # TODO: change this if adding functionality of msg_no.
                    return pickle.loads(parities_bytes)

    def start_reconciliation(self, reconciliation_algorithm: str):
        """
        Informs the Server(Alice) that reconciliation has started.

        Args:
            reconciliation_algorithm (str): Specify which algorithm is being used eg. 'cascade' for cascade algo.
        """
        #TODO: Maybe add authentication here!
        self.reconciliation_status[reconciliation_algorithm] = 'Active'
        msg_to_send = 'reconciliation_status:' + reconciliation_algorithm + ':Active'
        self.send_bytes_to_the_server(msg_to_send.encode(constants.FORMAT))
        
    def end_reconciliation(self, reconciliation_algorithm: str):
        """
        Informs the Server(Alice) that reconciliation has ended.

        Args:
            reconciliation_algorithm (str): Specify which algorithm is being used eg. 'cascade' for cascade algo.
        """
        self.reconciliation_status[reconciliation_algorithm] = 'Completed'
        msg_to_send = 'reconciliation_status:' + reconciliation_algorithm + ':Completed'
        self.send_bytes_to_the_server(msg_to_send.encode(constants.FORMAT))
    
    def get_bits_for_qber(self, indexes):
        bits_for_qber = {}
        for index in indexes:
            bits_for_qber[index] = self._noisy_key._bits[index]
        self._noisy_key.discard_bits(indexes)
        return bits_for_qber            
     
    def ask_server_for_bits_to_estimate_qber(self, indexes: list) -> dict:
        indexes_bytes = pickle.dumps(indexes)
        #TODO: add message no. for this also.
        msg_to_send = 'qber_estimation:'.encode(constants.FORMAT) + indexes_bytes

        # asking:
        self.send_bytes_to_the_server(msg_to_send)

        # receiving:
        while self.connected_to_server:
            msg_recvd = self.receive_bytes_from_the_server()
            if msg_recvd:
                if msg_recvd.startswith('qber_estimation'.encode(constants.FORMAT)):
                    bits_dict_bytes = msg_recvd.removeprefix(
                        'qber_estimation:'.encode(constants.FORMAT))
                    # TODO: change this if adding functionality of msg_no.
                    return pickle.loads(bits_dict_bytes)
    
    def send_disconnect_message_to_server(self):
        pass
    
    def send_closing_message_to_the_server(self):
        """
        Sends a closing message to the server.
        """
        #TODO: It's not working make it work
        self.send_bytes_to_the_server('close_server'.encode(constants.FORMAT))
        self.connected_to_server = False

class Eavesdropper(Client):
    # TODO: needs updating this is not currently working.
    def __init__(self, username, noisy_key: Key, server_address=(constants.LOCAL_IP, constants.LOCAL_PORT)):
        #TODO: Convert args to kwargs for easy implementation.
        super().__init__(username)

        self._noisy_key = noisy_key
        #TODO: Add authentication protocol for when a new client connects.

        self.server_address = server_address
        self.connect(self.server_address)
        self.connected_to_server = True
        self.reconciliation_status = {
            'cascade': 'Not yet started', 'ldpc': 'Not yet started', 'polar': 'Not yet started'}

    def ask_parities(self, blocks):
        """
        Sends blocks as bytes to the server and then the server
        replies with the appropriate parities of the blocks asked.

        Args:
            blocks (list(Block)): Contains all the blocks whose parity is to be asked.

        Returns:
            parities (list(int)): Contains parities in the same order as the blocks in blocks.
        """
        # Only send the indexes for parity.
        # TODO: make this algo faster it's currently very slow for large blocks.
        block_indexes_list = [block.get_key_indexes() for block in blocks]
        # TODO: add tracking of parity messages.
        block_indexes_list_bytes = pickle.dumps(block_indexes_list)
        msg_to_send = 'ask_parities:'.encode(
            constants.FORMAT) + block_indexes_list_bytes

        # asking:
        self.send_bytes_to_the_server(msg_to_send)

        # receiving:
        while self.connected_to_server:
            msg_recvd = self.receive_bytes_from_the_server()
            if msg_recvd:
                if msg_recvd.startswith('ask_parities'.encode(constants.FORMAT)):
                    # This initial number represents the 'ask_parities:' part to be removed
                    parities_bytes = msg_recvd.removeprefix(
                        'ask_parities:'.encode(constants.FORMAT))
                    # TODO: change this if adding functionality of msg_no.
                    return pickle.loads(parities_bytes)
