import os
import pickle
from posproc.networking_old import client
from posproc.networking.client import Client
from posproc.key import Key
from posproc import constants
from posproc.utils import Utilities
from ellipticcurve.publicKey import PublicKey
from ellipticcurve.privateKey import PrivateKey
from posproc.authentication import Authentication
from posproc.networking.user_data import User, UserData
from posproc.networking.uebn import AdvancedServer, UrsinaNetworkingConnectedClient, UrsinaNetworkingServer
    
class Server(AdvancedServer):
    def __init__(self, username: str, current_key: Key,
                 user_data: UserData = None, server_type=constants.LOCAL_SERVER,
                 port=constants.LOCAL_PORT, auth_keys: tuple[PublicKey, PrivateKey] = None):
        self.server_type = server_type
        self.port = port
        self._set_the_address_variable()
        
        super().__init__(self.address)

        
        self.username = username
        
        self._add_authentication_token(auth_keys)
        
        
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
        verify = self.add_this_client_to_user_data_or_do_authentication_if_already_exists()

    def add_this_client_to_user_data_or_do_authentication_if_already_exists(self):
        """
        Asks the client for it's User object to update the current user data.
        If the user's Public Key already exists in the user data then authentication is done. 
        User object includes: User(username, address, publicAuthKey)
        """
        @self.receiver_event
        def authResponse():
            print('authresp')

        @self.get_connected_client_object
        def onClientConnected():
            pass

        clientObject = onClientConnected()
        print("ClientObject",clientObject)
        self.send_message_to_client(clientObject, 'authInit', '')
        
        client_user, message, signature = authResponse()
        print("Auth response received")
        
        pubKey = self.user_data.user_already_exists(client_user)
        # print("PubKey: ", pubKey)
        
        if pubKey:
            verify = self._auth.verify(message, signature, pubKey)
            if verify:
                self.user_data.users[pubKey.toPem()].address = clientObject.address
                print(
                    f"Authentication with Client @ {clientObject.address} was successful!")
            else:
                print(f"Authentication with Client @ {clientObject.address} was unsuccessful!")
                clientObject.socket.close() #FIXME: Make This cleaner!
            return verify
        else:
            self.update_user_data(client_user)
            # print("User Data after Client Add: ", self.user_data)
            return None    
