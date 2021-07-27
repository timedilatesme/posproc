# python -m posproc.testing.standalone_server_test.server
import hashlib
import os
import pickle
import threading
import gc
from ellipticcurve.privateKey import PrivateKey

from ellipticcurve.publicKey import PublicKey
from posproc.key import Key
from posproc import constants
from posproc.networking_old.node import Node
from posproc.networking.user_data import User, UserData

MSG_NO_HEADER = 10
#What is the maximum length of the msg_no. for eg if MSG_NO_HEADER = 2 => maximum value of msg_no is 99.
gc.disable()

class Server(Node):
    """
    Creates the Server (Alice's) socket.

    """

    def __init__(self, username: str, current_key: Key, 
                 user_data: UserData = None, server_type=constants.LOCAL_SERVER, 
                 port=constants.LOCAL_PORT, auth_keys : tuple[PublicKey, PrivateKey] = None):
        """
        Alice's key is needed for performing computation.
        This Node will only run on Alice's address so only she knows the correct key.
        
        Args:
            username (str): Name the Server!
            current_key (Key): Alice's Key Obtained from the QKD protocol.
            user_data (UserData): Initialize user data with some users. Defaults to None.             
            server_type (str, optional): [Either LOCAL_SERVER or PUBLIC_SERVER {defined in constants.py}]. Defaults to LOCAL_SERVER.
            port (int, optional): [The local port to be used for hosting the server. Defaults to LOCAL_PORT]. Defaults to LOCAL_PORT.
        """
        self.username = username
        
        #Get the __init__ of Node class.
        super().__init__(username, auth_Keys= auth_keys)
        
        
        #This is the correct_key i.e. the Key that Alice has.
        #TODO: __ or _ for best security?
        self._current_key = current_key
        
        self.server_type = server_type
        self.port = port


        # The User Data for all people on this server 
        user_data_loaded = self.check_if_user_data_file_exists()
        
        if user_data:
            self.user_data = user_data
        elif user_data_loaded:
            self.user_data = user_data_loaded
            # print(self.user_data)
        else:
            self.user_data = UserData()
        
        # set the address corresponding to Local or Public Server.
        self._set_the_address_variable()
        self.user = User(username, address=self.address, auth_id=self.auth_id)
        self.user_data.update_user_data(self.user)
        # print("UserData (After Server Add): ", self.user_data.users)
        
        if server_type == constants.PUBLIC_SERVER:
            with open(constants.data_storage + 'server_address.pickle', 'wb') as fh:
                pickle.dump(self.address, fh,protocol=pickle.HIGHEST_PROTOCOL)
                
        self.threads = [];
        
        # The Server will start on this address
        # Then we can port-forward the ngrok address to this address
        self.LOCAL_ADDRESS = (constants.LOCAL_IP, constants.LOCAL_PORT)
        
        # The status of different algorithms for Error Correction.
        self.reconciliation_status = {'cascade': 'Not yet started',
                                      'winnow': 'Not yet started',
                                      'ldpc': 'Not yet started',
                                      'polar': 'Not yet started'}
        
        # Start Listening!
        self.start_listening()
        self.server_is_active = True

        # Now Start accepting connections:
        self.start_receiving()
        
    
    def save_user_data_as_file(self):
        datapath = os.path.join(constants.data_storage,'server_' + self.username)
        if os.path.exists(datapath) == False:
            os.makedirs(datapath)
        filepath = os.path.join(datapath, 'user_data.pickle')
        with open(filepath, 'wb') as fh:
            pickle.dump(self.user_data, fh,protocol=pickle.HIGHEST_PROTOCOL)
    
    def check_if_user_data_file_exists(self):
        datapath = os.path.join(
            constants.data_storage, 'server_' + self.username + '/', 'user_data.pickle')
        if os.path.exists(datapath):  
            with open(datapath, 'rb') as fh:
                user_data = pickle.load(fh)
            return user_data
        else:
            return None
        
    def update_user_data(self, new_user: User):
        """
        Adds a new user to the server's user data.

        Args:
            new_user (User): The new user to be added. 
        """
        self.user_data.update_user_data(new_user)

    def get_user_data(self):
        """
        Get the user data currently stored at the server

        Returns:
            [UserData]: an instance of class UserData which stores all users.
        """
        return self.user_data
    
    def add_this_client_to_user_data_or_do_authentication_if_already_exists(self,client,address):
        """
        Asks the client for it's User object to update the current user data.
        If the user's Public Key already exists in the user data then authentication is done. 
        User object includes: User(username, address, publicAuthKey)
        """
        msg_to_send = "user_object:?".encode(constants.FORMAT)
        self.send_bytes_to_the_client(client, msg_to_send)
        
        while True:
            msg_recvd = self.receive_bytes_from_the_client(client)
            if msg_recvd:
                if msg_recvd.startswith("user_object:".encode(constants.FORMAT)):
                    msg_bytes = msg_recvd.removeprefix(
                        "user_object:".encode(constants.FORMAT))
                    client_user = pickle.loads(msg_bytes) 
                    
                    auth_init_msg = "auth_init:".encode(constants.FORMAT)
                    self.send_bytes_to_the_client(client, auth_init_msg)
                    
                elif msg_recvd.startswith("authentication:".encode(constants.FORMAT)):
                    msg_bytes = msg_recvd.removeprefix("authentication:".encode(constants.FORMAT))
                    message,signature = pickle.loads(msg_bytes)
                    break
                    
        # print("User Data: ",self.user_data)
        pubKey = self.user_data.user_already_exists(client_user)
        # print("PubKey: ", pubKey)
        
        if pubKey:
            verify = self._auth.verify(message, signature, pubKey)
            if verify:
                self.user_data.users[pubKey.toPem()].address = address
                print(
                    f"Authentication with Client @ {address} was successful!")
            else:
                print(f"Authentication with Client @ {address} was unsuccessful!")
                client.close()
            return verify
        else:
            self.update_user_data(client_user)
            # print("User Data after Client Add: ", self.user_data)
            return None
        
    def start_listening(self):
        print(f"[STARTING] {self.server_type} server is starting...")
        self.bind(self.LOCAL_ADDRESS)
        self.listen()
        print(f"[LISTENING] Server is listening @ {self.get_address()}")    

    def start_receiving(self):
        #TODO: Make some way to stop the server!
        while self.server_is_active:
            client, addr = self.accept()
            print(f"Connected with {addr}")
            
            verified = self.add_this_client_to_user_data_or_do_authentication_if_already_exists(client, addr)

            if verified != False:  
                thread = threading.Thread(
                    target=self.handle_client, args=(client, addr))
                self.threads.append(thread)
                thread.start()
                
            self.save_user_data_as_file()

            print(
                f"[ACTIVE CONNECTIONS]: {threading.active_count() - 1} clients are connected!")
        self.close()
        # sys.exit()

    def handle_client(self, client, address: tuple) -> None:
        connected = True
        while connected:
            msg_received = self.receive_bytes_from_the_client(client)
            
            if msg_received:
                if msg_received.startswith("auth_init_request".encode(constants.FORMAT)):
                    self.handle_authentication(client)
                
                elif msg_received.startswith("authentication".encode(constants.FORMAT)):
                    msg_recvd_bytes = msg_recvd.removeprefix(
                        'authentication:'.encode(constants.FORMAT))
                    msg_recvd = pickle.loads(msg_recvd_bytes)
                    msg = msg_recvd[0]
                    signature = msg_recvd[1]
                    publicAuthKey_Client = self.user_data.get_user_by_address(
                        client.getsockname()).auth_id
                    self.client_authenticated = self._auth.verify(
                        msg, signature, publicAuthKey_Client)
                    if self.client_authenticated:
                        print(f"Client @ {address} authentication successful!")
                    else:
                        print(f"Client @ {address} authentication unsuccessful!")
                    
                elif msg_received.startswith("username:".encode(constants.FORMAT)):
                    client_username = msg_received.removeprefix(
                        "username:".encode(constants.FORMAT))
                    client_username = client_username.decode(constants.FORMAT)
                    self._pending_clients_for_setting_active[client_username] = address

                elif msg_received.startswith('ask_parities'.encode(constants.FORMAT)):
                    msg_to_send = self._ask_parities_return_message(
                        msg_received)
                    self.send_bytes_to_the_client(client, msg_to_send)

                elif msg_received.startswith('qber_estimation'.encode(constants.FORMAT)):
                    indexes_bytes = msg_received.removeprefix(
                        'qber_estimation:'.encode(constants.FORMAT))
                    print("Length of indexes bytes:",len(indexes_bytes))
                    indexes = pickle.loads(indexes_bytes)
                    bits_dict = self._current_key.get_bits_for_qber_estimation(
                        indexes)
                    # print("Bits to send to Client: ", bits_dict)
                    bits_dict_bytes = pickle.dumps(bits_dict,protocol=pickle.HIGHEST_PROTOCOL)
                    msg_to_send = 'qber_estimation:'.encode(
                        constants.FORMAT) + bits_dict_bytes
                    self.send_bytes_to_the_client(client, msg_to_send)
                    print("Final Key: ", hashlib.sha256(
                        self._current_key.__str__().encode(constants.FORMAT)))
                    # self._current_key = hash(self._current_key)
                    # self.save_current_key_as_text() # TODO: make it so that it can be accesed from outside!
                
                elif msg_received.startswith('reconciliation_status'.encode(constants.FORMAT)):
                    splitted_msg = msg_received.split(b':')
                    reconciliation_algorithm = splitted_msg[1].decode(
                        constants.FORMAT)
                    status = splitted_msg[2].decode(constants.FORMAT)
                    self.reconciliation_status[reconciliation_algorithm] = status
                    # if self.reconciliation_status['cascade'] == 'Completed':
                        # print("Alice's New Key:", self._current_key._bits)
                
                elif msg_received == 'disconnect'.encode(constants.FORMAT):
                    connected = False

                elif msg_received == 'close_server'.encode(constants.FORMAT):
                    self.server_is_active = False
                    # self.shutdown(
                    #self.close() # TODO: Is it good?
                elif msg_received.startswith(b'speed_test:'):
                    self.send_bytes_to_the_client(client, msg_received)
                
                elif msg_received.startswith(b'test:'):
                    print(f"[Client @ {address}]: {len(msg_received)}")
            else:
                continue
        client.close()
    
    def _ask_parities_return_message(self, msg_recvd: bytes):
        #message_recvd = b'ask_parities:[block_indexes as list,[],[],...[]]'
        block_indexes_list_bytes = msg_recvd.removeprefix(
            'ask_parities:'.encode(constants.FORMAT))
        print(f"Block Indexes List Bytes Received: {len(block_indexes_list_bytes)}")
        #print(block_indexes_list_bytes)
        try:
            block_indexes_list = pickle.loads(block_indexes_list_bytes)
        except:
            #pickled_list_bytes = pickle.dumps(block_indexes_list_bytes)
            #block_indexes_list = pickle.loads(pickled_list_bytes)
            print("BLOCK INDEXES LIST BYTES:", block_indexes_list_bytes)

        #TODO: Store the information leaked into some new object to help in privacy amplification.
        parities = []
        for block_indexes in block_indexes_list:
            parity = self._current_key.get_indexes_parity(block_indexes)
            parities.append(parity)
        msg_to_send = 'ask_parities:'.encode(
            constants.FORMAT) + pickle.dumps(parities,protocol=pickle.HIGHEST_PROTOCOL)
        return msg_to_send

    def stop_server(self):
        #TODO: Make it work!
        self.server_is_active = False
        exit()

    def broadcast_to_all(self, message: bytes):
        for client in self.active_clients:
            self.send_bytes_to_the_client(client, message)
    
    def get_address(self):
        """
        Returns the current address either local or public

        Returns:
            server_address [tuple]: In the form (IP,PORT).
            returns None. if the Server is not Started!
        """
        if self.address:
            return self.address

    def _set_the_address_variable(self):
        if self.server_type == constants.LOCAL_SERVER:
            self.address = (constants.LOCAL_IP, self.port)
        if self.server_type == constants.PUBLIC_SERVER:
            self.address = self.start_ngrok_tunnel(self.port)
            
    def save_current_key_as_text(self, path=None):
        if not path:
            path = os.path.join(constants.data_storage,
                                f'{self.username}_Key.txt')
        with open(path, 'w') as fh:
            fh.write(self._current_key.__str__())

class Server_to_simulate_eavesdropping(Server):
    pass
