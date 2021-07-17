from ellipticcurve.publicKey import PublicKey
import numpy as np
class User:
    """
    A Mock Implementation of a User with it's attributes.
    """
    def __init__(self, username = None, address = None, auth_id = None) -> None:
        self.username = username
        self.address = address
        self.auth_id = auth_id
        self.connected_to_server = False
    
    def set_connected_to_server(self, status : bool) -> None:
        self.connected_to_server = status
        
    def __repr__(self) -> str:
        return self.username
    def __eq__(self, other: object) -> bool:
        s = True
        for attr in self.__dict__.keys():
            s = s and self.__getattribute__(attr) == other.__getattribute__(attr)
        return s 

        
class UserData:
    """
    UserData stores the data about nickname, address and public key of every person,
    who uses the classical channel. This is for authentication purpose.
    This data will be available to all users of the network.
    """
    def __init__(self) -> None:
        self.users = {} # {publicKey:user} 
    
    def __repr__(self) -> str:
        s = ''
        for user in self.users.values():
            s += user.username + ' ,'
        return s
    
    def user_already_exists(self, client_user: User) -> PublicKey | False:
        exists = False
        for pubKey,user in self.users.items():
            if user == client_user:
                exists = True
                return pubKey
        if not exists:
            return False          
            
                
    
    def update_user_data(self,new_user:User) -> None:
        """
        Updates the existing user data with the new user.

        Args:
            new_user (User): [description]
        """
        self.users[new_user.auth_id] = new_user
    
    def get_user_by_address(self, address: tuple) -> User:
        """
        Gives the User corresponding to the given address.

        Args:
            address (tuple): the socket address for the user.

        Returns:
            User: the user with the given address.
        """
        # try:
        #     return self.users[address]
        # except:
        #     raise Exception("User doesn't exist.")
        
        self.users[address]        
    
    def get_user_by_name(self, username: str) -> User:
        """
        Gives the User corresponding to the given username.        

        Raises:
            Exception: If user doesn't exist in UserData.users

        Returns:
            [User]: the user corresponding to the given username.
        """
        for user in self.users.values():
            if user.username == username:
                user_needed = user
        try:
            return user_needed
        except Exception:
            raise Exception("User doesn't exist.")