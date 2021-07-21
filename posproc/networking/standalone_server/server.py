import os
import pickle
import threading
from ellipticcurve.privateKey import PrivateKey

from ellipticcurve.publicKey import PublicKey
from posproc.key import Key
from posproc import constants
from posproc.networking.node import Node
from posproc.networking.user_data import User, UserData

MSG_NO_HEADER = 10
#What is the maximum length of the msg_no. for eg if MSG_NO_HEADER = 2 => maximum value of msg_no is 99.


class Server(Node):
    """
    Creates the Server socket.

    """

    def __init__(self, username: str, user_data: UserData = None, server_type=constants.LOCAL_SERVER,
                 port=constants.LOCAL_PORT, auth_keys: tuple[PublicKey, PrivateKey] = None):
        """
        The Server to assist in Communication.
        
        Args:
            username (str): Name the Server!
            current_key (Key): Alice's Key Obtained from the QKD protocol.
            user_data (UserData): Initialize user data with some users. Defaults to None.             
            server_type (str, optional): [Either LOCAL_SERVER or PUBLIC_SERVER {defined in constants.py}]. Defaults to LOCAL_SERVER.
            port (int, optional): [The local port to be used for hosting the server. Defaults to LOCAL_PORT]. Defaults to LOCAL_PORT.
        """
        self.username = username

        #Get the __init__ of Node class.
        super().__init__(username, auth_Keys=auth_keys)

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
                pickle.dump(self.address, fh)

        self.active_clients = {}

        # The Server will start on this address
        # Then we can port-forward the ngrok address to this address
        self.LOCAL_ADDRESS = (constants.LOCAL_IP, constants.LOCAL_PORT)

        # Start Listening!
        self.start_listening()
        self.server_is_active = True

        # Now Start accepting connections:
        self.start_receiving()

    def save_user_data_as_file(self):
        datapath = os.path.join(constants.data_storage,
                                'server_' + self.username)
        if os.path.exists(datapath) == False:
            os.makedirs(datapath)
        filepath = os.path.join(datapath, 'user_data.pickle')
        with open(filepath, 'wb') as fh:
            pickle.dump(self.user_data, fh)

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

    def add_this_client_to_user_data_or_do_authentication_if_already_exists(self, client, address):
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
                    msg_bytes = msg_recvd.removeprefix(
                        "authentication:".encode(constants.FORMAT))
                    message, signature = pickle.loads(msg_bytes)
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
                print(
                    f"Authentication with Client @ {address} was unsuccessful!")
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
            
            self.active_clients[addr] = client

            print(
                f"[ACTIVE CONNECTIONS]: {threading.active_count() - 1} clients are connected!")
        # self.close()
        # sys.exit()

    def handle_client(self, client, address: tuple) -> None:
        connected = True
        while connected:
            msg_received = self.receive_bytes_from_the_client(client)
            if msg_received:
                self.broadcast_to_all(f'[Client @ {address}]: {msg_received}')
            
        client.close()

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


class Server_to_simulate_eavesdropping(Server):
    pass
