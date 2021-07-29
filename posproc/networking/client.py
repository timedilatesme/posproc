import os
import pickle
import secrets
from posproc.key import Key
from posproc import constants
from posproc.networking.uebn import AdvancedClient
from ellipticcurve.privateKey import PrivateKey
from ellipticcurve.publicKey import PublicKey
from posproc.networking.user_data import User
from posproc.error_correction.cascade.block import Block
from posproc.authentication import Authentication

class Client(AdvancedClient):
    def __init__(self, username: str, current_key: Key, auth_keys: tuple[PublicKey, PrivateKey] = None,
                 server_address = (constants.LOCAL_IP, constants.LOCAL_PORT)):
        super().__init__(server_address)
        
        self.username = username
        
        auth_keys = self.check_if_auth_keys_exist()
        self._add_authentication_token(auth_Keys=auth_keys)
        if not auth_keys:
            self.save_auth_keys_as_file()
        
        self._current_key = current_key

        self.user = User(username, address=None,
                         auth_id = self.auth_id)
        
        self.authenticating = True

        self.reconciliation_status = {'cascade': 'Not yet started',
                                      'winnow': 'Not yet started',
                                      'ldpc': 'Not yet started',
                                      'polar': 'Not yet started'}   
        
    def _get_auth_keys(self):
        """
        Public Key, Private Key
        """
        return self.auth_id, self._auth_key
    
    def _add_authentication_token(self, auth_Keys):
        self._auth = Authentication(auth_Keys=auth_Keys)
        self.auth_id, self._auth_key = self._auth._get_key_pair()        


    def ask_parities(self, blocks: list[Block]) :
        pass
    
    def start_reconciliation(self, reconciliation_algorithm: str):
        pass
    
    def end_reconciliation(self, reconciliation_algorithm: str):
        pass

    def get_bits_for_qber(self, indexes):
        pass
    
    def ask_server_for_bits_to_estimate_qber(self, indexes: list) -> dict:
        pass

    def disconnect_from_server(self):
        pass

    def check_network_speed(self, BytesSize = 1000):
        pass


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
            pickle.dump(privKey, privKeyFH)
        
        with open(dirpath + 'pubKey.pickle', 'wb') as pubKeyFH:
            pickle.dump(pubKey, pubKeyFH)

    def get_bits_for_qber(self, indexes):
        # bits_for_qber = {}
        # for index in indexes:
        #     bits_for_qber[index] = self._current_key._bits[index]
        # self._current_key.discard_bits(indexes)
        # return bits_for_qber
        bits = self._current_key.get_bits_for_qber_estimation(indexes)
        # print("Updated Noisy Key",self._current_key._bits)
        return bits
    
    def Initialize_Events(self):
        @self.event
        def authInit(Content):
            print('authInit')
            msg = secrets.token_hex()
            msg_sign = self._auth.sign(msg)
            msg_to_send_tuple = (self.user, msg, msg_sign)
            print("message being sent")
            self.send_message_to_server('authResponse', msg_to_send_tuple)
        # self.send_message_to_server('authResponse','duhhhhhh')    