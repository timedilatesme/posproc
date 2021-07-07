from posproc.key import Key
from posproc.networking.node import Node
from posproc import constants
import pickle
from posproc.error_correction.cascade.block import Block
import random

class Client(Node):
    def __init__(self, username, noisy_key:Key,server_address=(constants.LOCAL_IP, constants.LOCAL_PORT)):
        #TODO: Convert args to kwargs for easy implementation.
        super().__init__(username)
        
        self.__noisy_key = noisy_key
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
            bits_for_qber[index] = self.__noisy_key._bits[index]
        self.__noisy_key.discard_bits(indexes)
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