import os
import pickle
import secrets
import time
from ellipticcurve.privateKey import PrivateKey

from ellipticcurve.publicKey import PublicKey
from posproc.key import Key
from posproc import constants
from posproc.networking.node import Node
from posproc.networking.user_data import User
from posproc.error_correction.cascade.block import Block

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

    def __init__(self, username: str, current_key: Key, auth_keys: tuple[PublicKey,PrivateKey] = None, 
                 server_address=(constants.LOCAL_IP, constants.LOCAL_PORT)):
        """
        Initialize the active client with the following parameters.

        Args:
            username (str): The username of this client.(Must be unique for every client.)
            current_key (Key): The initial key of the active client. Mostly this is the noisy Key.
            auth_keys (tuple[PubKey, PrivKey]): If the user already has a key pair then no need to reproduce another key pair.
            server_address (tuple, optional): The address of the server to connect to? Defaults to (constants.LOCAL_IP, constants.LOCAL_PORT).
        """
        self.username = username
        authKeys = self.check_if_auth_keys_exist()
        
        # print("Already Stored: ", authKeys[1].toPem())
                
        super().__init__(username, auth_Keys = authKeys)
        
        # print("Private Key: ", self._auth_key.toPem())
        
        
        if server_address == None:
            # FIXME: change it to something else from None!
            with open(constants.data_storage + 'server_address.pickle', 'rb') as fh:
                self.server_address = pickle.load(fh)
        else:
            self.server_address = server_address
        
        if not authKeys:
            self.save_auth_keys_as_file()   
        
        self._current_key = current_key
        
                
        self.connect(self.server_address)
        self.connected_to_server = True

        self.user = User(username, address=self.getsockname(),
                         auth_id = self.auth_id)
        self.authenticating = True
        self.start_authentication_protocol()    

        self.reconciliation_status = {'cascade': 'Not yet started',
                                      'winnow': 'Not yet started',
                                      'ldpc': 'Not yet started',
                                      'polar': 'Not yet started'}
    
    def start_authentication_protocol(self):
        while self.authenticating:
            msg_recvd = self.receive_bytes_from_the_server()
            if msg_recvd:
                if msg_recvd.startswith("user_object:?".encode(constants.FORMAT)):
                    msg_1 = self.user
                    msg_to_send = "user_object:".encode(
                        constants.FORMAT) + pickle.dumps(msg_1,protocol=pickle.HIGHEST_PROTOCOL)
                    self.send_bytes_to_the_server(msg_to_send)
                elif msg_recvd.startswith("auth_init:".encode(constants.FORMAT)):
                    msg_ = secrets.token_hex()
                    msg_sign = self._auth.sign(msg_)
                    msg_to_send_tuple = (msg_, msg_sign)
                    msg_to_send = "authentication:".encode(
                        constants.FORMAT) + pickle.dumps(msg_to_send_tuple,protocol=pickle.HIGHEST_PROTOCOL)
                    self.send_bytes_to_the_server(msg_to_send)
                    self.authenticating = False
        # print("Authentication Fn Done!")
    
    def check_if_auth_keys_exist(self) -> tuple[PublicKey, PrivateKey]:
        dirpath = constants.data_storage + self.username + '_auth_keys/'
        if os.path.exists(dirpath):
            with open(dirpath + 'privKey.pickle', 'rb') as privKeyFH:
                privKey = pickle.load(privKeyFH)

            with open(dirpath + 'pubKey.pickle', 'rb') as pubKeyFH:
                pubKey = pickle.load(pubKeyFH)
            
            # privKey = PrivateKey.fromString(b"a") #TODO: For checking authentication failure. 
            
            return (pubKey, privKey)
        else:
            return None
    
    def save_current_key_as_text(self, path = None):
        if not path:
            path = os.path.join(constants.data_storage, f'{self.username}_Key.txt')
        with open(path, 'w') as fh:
            fh.write(self._current_key.__str__())
                    
    def save_auth_keys_as_file(self):
        """
        Saves the randomly generated auth keys for future reference.
        These will only be used for a short amount of time!
        """
        pubKey, privKey = self._get_auth_keys() # (PubKey, PrivKey)
        
        dirpath = constants.data_storage + self.username + '_auth_keys/'
        if os.path.exists(dirpath) == False:
            os.makedirs(dirpath)
        with open(dirpath + 'privKey.pickle' , 'wb') as privKeyFH:
            pickle.dump(privKey, privKeyFH,protocol=pickle.HIGHEST_PROTOCOL)
        
        with open(dirpath + 'pubKey.pickle', 'wb') as pubKeyFH:
            pickle.dump(pubKey, pubKeyFH,protocol=pickle.HIGHEST_PROTOCOL)       
                    
                    
    def ask_parities(self, blocks: list[Block]) :
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
        block_indexes_list_bytes = pickle.dumps(block_indexes_list,protocol=pickle.HIGHEST_PROTOCOL) # 
        
        print(f"Block Indexes List Bytes Sent: {len(block_indexes_list_bytes)}")
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
        indexes_bytes = pickle.dumps(indexes,protocol=pickle.HIGHEST_PROTOCOL)
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
        
    def check_network_speed(self, BytesSize = 1000):
        msg = b'speed_test:'  + secrets.token_bytes(BytesSize)        
        
        startTime = time.perf_counter()
        
        self.send_bytes_to_the_server(msg)
        
        while True:
            msg_recvd = self.receive_bytes_from_the_server()
            if msg_recvd:
                if msg_recvd.startswith(b'speed_test:'):
                    endTime = time.perf_counter()
                    break
        deltaTime = (endTime - startTime)/2
        return f"Speed is {BytesSize/deltaTime} bytes/sec"
