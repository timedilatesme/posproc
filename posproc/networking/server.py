from posproc.networking.uebn import UrsinaNetworkingServer, ursina_networking_log
from posproc.utils import Utilities
import socket
import pickle
import os
from posproc.authentication import Authentication
import threading
from posproc.key import Key
from posproc.networking.user_data import User, UserData
from ellipticcurve.privateKey import PrivateKey
from ellipticcurve.publicKey import PublicKey
from posproc import constants
    
class Server:
    def __init__(self, username: str, current_key: Key,
                 user_data: UserData = None, server_type=constants.LOCAL_SERVER,
                 port=constants.LOCAL_PORT, auth_keys: tuple[PublicKey, PrivateKey] = None):
        
        self._add_authentication_token(auth_keys)
        self.username = username
        
        self.server_type = server_type
        self.port = port
        self._set_the_address_variable()
        
        self.ursinaServer = UrsinaNetworkingServer(self.address)
        
        self.current_key = current_key
        self.set_user_data_variable(user_data)
        
        
        self.user = User(username, address=self.address, auth_id=self.auth_id)
        self.user_data.update_user_data(self.user)

    def _get_auth_keys(self):
        """
        Public Key, Private Key
        """
        return self.auth_id, self._auth_key
    
    def _add_authentication_token(self, auth_Keys):
        self._auth = Authentication(auth_Keys=auth_Keys)
        self.auth_id, self._auth_key = self._auth._get_key_pair()
    
    def set_user_data_variable(self, user_data):
        # The User Data for all people on this server
        user_data_loaded = self.check_if_user_data_file_exists()

        if user_data:
            self.user_data = user_data
        elif user_data_loaded:
            self.user_data = user_data_loaded
            # print(self.user_data)
        else:
            self.user_data = UserData()
    
    def _set_the_address_variable(self):
        if self.server_type == constants.LOCAL_SERVER:
            self.address = (constants.LOCAL_IP, self.port)
        if self.server_type == constants.PUBLIC_SERVER:
            self.address = Utilities.start_ngrok_tunnel(self.port)
    
    def check_if_user_data_file_exists(self):
        datapath = os.path.join(
            constants.data_storage, 'server_' + self.username + '/', 'user_data.pickle')
        if os.path.exists(datapath):
            with open(datapath, 'rb') as fh:
                user_data = pickle.load(fh)
            return user_data
        else:
            return None
    
    def Initialize_Events(self):
        @self.ursinaServer.event
        def onClientConnected(CLient):
            pass
