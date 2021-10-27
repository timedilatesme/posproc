import os
import pickle
import threading
from posproc.key import Key
from posproc import constants
from posproc import utils
from ellipticcurve.publicKey import PublicKey
from ellipticcurve.privateKey import PrivateKey
from posproc.authentication import Authentication
from posproc.networking.user_data import User, UserData
from posproc.networking.uebn import AdvancedServer, UrsinaNetworkingConnectedClient, networking_log
from posproc.privacy_amplification.universal_hashing import MODEL_1
import PySimpleGUI as sg
from posproc.utils import gui_console_print
from posproc.networking.uebn import console_output as terminal_print
    
class Server(AdvancedServer):
    def __init__(self, username: str, current_key: Key = None,
                 user_data: UserData = None, server_type=constants.LOCAL_SERVER,
                 port=constants.LOCAL_PORT, auth_keys: tuple[PublicKey, PrivateKey] = None,
                 authentication_required = True, gui_window:sg.Window=None):
        
        self.authentication_required = authentication_required
        self.server_type = server_type
        self.port = port
        self._set_the_address_variable()
        
        super().__init__(self.address)
        
        self.username = username
        
        self._add_authentication_token(auth_keys)
        
        
        self._current_key = current_key
        self.set_user_data_variable(user_data)
        
        
        self.user = User(username, address=self.address, auth_id=self.auth_id)
        self.user_data.update_user_data(self.user)
        
        # The status of different algorithms for Error Correction.
        self.reconciliation_status = {'cascade': 'Not yet started',
                                      'winnow': 'Not yet started',
                                      'ldpc': 'Not yet started',
                                      'polar': 'Not yet started'}
        
        # GUI init
        self.gui_window = gui_window
            
    def console_output(self, message, *args):
        if self.gui_window:
            gui_console_print(message, self.gui_window)
            terminal_print(message, *args)
        else:
            terminal_print(message, *args)     
    
    
    def set_key(self, key: Key):
        self._current_key = key
    
    def get_key(self):
        return self._current_key
    
    def Initialize_Events(self):
        @self.event
        def onClientConnected(Client):
            if self.authentication_required:
                Client.send_message('authentication', 'Initialize')
            self.console_output(f'Client @ {Client.address} is connected!')
            
        @self.event
        def authenticateClient(Client: UrsinaNetworkingConnectedClient, Content):
            verified = self.add_this_client_to_user_data_or_do_authentication_if_already_exists(
                Client, Content)
            if verified == None:
                Client.send_message('authentication', 'Welcome to the Server! \n')
            elif verified == True:
                Client.authenticated.set()
                Client.send_message(
                    'authentication', 'Authentication Successful! \n')
            else:
                Client.authenticated = False
                Client.send_message(
                    'authentication', 'Authentication Unsuccessful! \n')
                # Client.socket.close()
            self.save_user_data_as_file()

        @self.event
        def askParities(Client: UrsinaNetworkingConnectedClient, Content):
            Client.authenticated.wait()
            #TODO: Store the information leaked into some new object to help in privacy amplification.
            block_indexes_list = Content

            parities = []
            for block_indexes in block_indexes_list:
                parity = self._current_key.get_indexes_parity(block_indexes)
                parities.append(parity)
            # + str(index)
            Client.send_message('askParitiesReply', parities)

        @self.event
        def updateReconciliationStatus(Client: UrsinaNetworkingConnectedClient, Content):
            Client.authenticated.wait()
            algorithmName, status = Content
            self.reconciliation_status[algorithmName] = status
            
        @self.event
        def qberEstimation(Client: UrsinaNetworkingConnectedClient, Content):
            Client.authenticated.wait()
            # networking_log('Server', 'qberEstimation', Content)
            # networking_log('Server','Current Key',self._current_key)
            
            indexes = Content
            bits_dict = self._current_key.get_bits_for_qber_estimation(indexes)
            # print("Bits to send to Client: ", bits_dict)
            Client.send_message('qberEstimationReply', bits_dict)
        
        @self.event
        def privacyAmplification(Client: UrsinaNetworkingConnectedClient, Content):
            Client.authenticated.wait()
            algo_name, final_key_bytes_size = Content
            self._current_key = MODEL_1(self._current_key, final_key_bytes_size, algorithm=algo_name)[1]
            alice_final_key_str = str(self._current_key)

            # with open('results/alice_final_key.txt', 'w') as f:
            #     f.write(alice_final_key_str)


            # print('PA KEY: ', self._current_key)
            
        @self.event
        def onClientDisconnected(Client: UrsinaNetworkingConnectedClient):
            Client.authenticated.wait()
            self.console_output(f'Client @ {Client.address} is disconnected!')
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
    
    def update_user_data(self, new_user: User):
        """
        Adds a new user to the server's user data.

        Args:
            new_user (User): The new user to be added. 
        """
        self.user_data.update_user_data(new_user)
    
    def _set_the_address_variable(self):
        if self.server_type == constants.LOCAL_SERVER:
            self.address = (constants.LOCAL_IP, self.port)
        if self.server_type == constants.PUBLIC_SERVER:
            self.address = utils.start_ngrok_tunnel(self.port)
                
    def check_if_user_data_file_exists(self):
        datapath = os.path.join(
            constants.DATA_STORAGE, 'server_' + self.username + '/', 'user_data.pickle')
        if os.path.exists(datapath):
            with open(datapath, 'rb') as fh:
                user_data = pickle.load(fh)
            return user_data
        else:
            return None
    
    def save_user_data_as_file(self):
        datapath = os.path.join(constants.DATA_STORAGE,'server_' + self.username)
        if not os.path.exists(datapath):
            os.makedirs(datapath)
        filepath = os.path.join(datapath, 'user_data.pickle')
        with open(filepath, 'wb') as fh:
            pickle.dump(self.user_data, fh)
                
    def add_this_client_to_user_data_or_do_authentication_if_already_exists(self,clientObject, auth_data_dict):
        """
        Asks the client for it's User object to update the current user data.
        If the user's Public Key already exists in the user data then authentication is done. 
        User object includes: User(username, address, publicAuthKey)
        """
        client_user, message, signature  = auth_data_dict['User'], auth_data_dict['Message'], auth_data_dict['Signature']
        pubKey = self.user_data.user_already_exists(client_user)
        # print("PubKey: ", pubKey)
        
        if pubKey:
            verify = self._auth.verify(message, signature, pubKey)
            if verify:
                self.user_data.users[pubKey.toPem()].address = clientObject.address
                self.console_output(
                    f"Authentication with Client @ {clientObject.address} was successful!")
            else:
                self.console_output(f"Authentication with Client @ {clientObject.address} was unsuccessful!")
            return verify
        else:
            self.update_user_data(client_user)
            # print("User Data after Client Add: ", self.user_data)
            return None 
    
    def start_listening(self):
        self.Initialize_Events()
        self.start_ursina_server()
        self.start_events_processing_thread()
        