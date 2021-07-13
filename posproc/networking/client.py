import pickle
from posproc.key import Key
from posproc import constants
from posproc.networking.node import Node
from posproc.networking.user_data import UserData, User

"""
This module contains code for active client who is going to be doing all the computation.
In theory we consider bob to be the active client who asks question to alice about parity
and Alice is an passive client who is just going to reply to all the questions that bob
asks.
"""

class Client(Node):
    """
    Adds the active client and connects it to the server

    Super Class:
        Node : The parent class containing all necessary details similar to both Server and Client.
    """
    def __init__(self, username: str, current_key: Key, server_address=(constants.LOCAL_IP, constants.LOCAL_PORT)):
        """
        Initialize the active client with the following parameters.

        Args:
            username (str): The username of this client.
            current_key (Key): The initial key of the active client. Mostly this is the noisy Key.
            server_address (tuple, optional): The address of the server to connect to? Defaults to (constants.LOCAL_IP, constants.LOCAL_PORT).
        """
        #TODO: Convert args to kwargs for easy implementation.
        super().__init__(username)
        #TODO add way to check for already existing username.
        self._current_key = current_key

        self.server_address = server_address
        self.connect(self.server_address)
        self.connected_to_server = True
        # self.user_data = user_data

        self.reconciliation_status = {'cascade': 'Not yet started',
                                      'ldpc': 'Not yet started',
                                      'polar': 'Not yet started'}

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
        msg_to_send = 'reconciliation_status:' + \
            reconciliation_algorithm + ':Completed'
        self.send_bytes_to_the_server(msg_to_send.encode(constants.FORMAT))

    def get_bits_for_qber(self, indexes):
        # bits_for_qber = {}
        # for index in indexes:
        #     bits_for_qber[index] = self._current_key._bits[index]
        # self._current_key.discard_bits(indexes)
        # return bits_for_qber
        bits = self._current_key.get_bits_for_qber_estimation(indexes)
        # print("Updated Noisy Key",self._current_key._bits)
        return bits

    def ask_server_for_bits_to_estimate_qber(self, indexes: list) -> dict:
        indexes_bytes = pickle.dumps(indexes)
        #TODO: add message no. for this also.
        msg_to_send = 'qber_estimation:'.encode(
            constants.FORMAT) + indexes_bytes
        # print("Message Send for QBER: ", msg_to_send)

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
    
    def disconnect_from_server(self):
        self.send_bytes_to_the_server("disconnect".encode(constants.FORMAT))
        