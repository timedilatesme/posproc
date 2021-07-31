import os
import pickle
from posproc.key import Key
from posproc import constants
from posproc import utils
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
        
        
        self._current_key = current_key
        self.set_user_data_variable(user_data)
        
        
        self.user = User(username, address=self.address, auth_id=self.auth_id)
        self.user_data.update_user_data(self.user)
        
    def Initialize_Events(self):
        @self.event
        def onClientConnected(Client):
            Client.send_message('authentication', 'Initialize')

        @self.event
        def authenticateClient(Client: UrsinaNetworkingConnectedClient, Content):
            verified = self.add_this_client_to_user_data_or_do_authentication_if_already_exists(
                Client, Content)
            if verified == None:
                Client.send_message('authentication', 'Welcome to the Server!')
            elif verified == True:
                Client.authenticated = True
                Client.send_message(
                    'authentication', 'Authentication Successful!')
            else:
                Client.authenticated = False
                Client.send_message(
                    'authentication', 'Authentication Unsuccessful!')
                # Client.socket.close()
            self.save_user_data_as_file()

        @self.event
        def askParities(Client, Content):
            #TODO: Store the information leaked into some new object to help in privacy amplification.
            index, block_indexes_list = Content

            parities = []
            for block_indexes in block_indexes_list:
                parity = self._current_key.get_indexes_parity(block_indexes)
                parities.append(parity)
            # + str(index)
            Client.send_message('askParitiesReply', parities)

        @self.event
        def updateReconciliationStatus(Client, Content):
            algorithmName, status = Content
            self.reconciliation_status[algorithmName] = status

        @self.event
        def qberEstimation(Client, Content):
            indexes = Content
            bits_dict = self._current_key.get_bits_for_qber_estimation(indexes)
            # print("Bits to send to Client: ", bits_dict)
            Client.send_message('qberEstimationReply', bits_dict)

        @self.event
        def privacyAmplification(Client, Content):
            algorithm_for_pa = Content

            #TODO: add logic here
            pass
        
        @self.event
        def shutdownServer(Client, Content):
            self.stopServer()

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
            constants.data_storage, 'server_' + self.username + '/', 'user_data.pickle')
        if os.path.exists(datapath):
            with open(datapath, 'rb') as fh:
                user_data = pickle.load(fh)
            return user_data
        else:
            return None
    
    def save_user_data_as_file(self):
        datapath = os.path.join(constants.data_storage,'server_' + self.username)
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
                self.ursinaServer.lock.acquire()
                self.user_data.users[pubKey.toPem()].address = clientObject.address
                self.ursinaServer.lock.release()
                print(
                    f"Authentication with Client @ {clientObject.address} was successful!")
            else:
                print(f"Authentication with Client @ {clientObject.address} was unsuccessful!")
            return verify
        else:
            self.update_user_data(client_user)
            # print("User Data after Client Add: ", self.user_data)
            return None    
