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

        
class UserData:
    """
    UserData stores the data about nickname, address and public key of every person,
    who uses the classical channel. This is for authentication purpose.
    This data will be available to all users of the network.
    """
    def __init__(self, *args) -> None:
        """
        Initialize with some users.
        Just enter as much users as you want.
        """
        self.users = {}  # {publicKeyAsPem:user}
        
        for user in args:
            self.users[user.auth_id] = user   
         
    
    def __repr__(self) -> str:
        return str(self.users)
    
    def user_already_exists(self, client_user: User):
        if client_user.auth_id.toPem() in self.users.keys():
            return client_user.auth_id
        else:
            return None
                
    
    def update_user_data(self,new_user:User) -> None:
        """
        Updates the existing user data with the new user.

        Args:
            new_user (User): The user object of the user that needs to be added.
        """
        self.users[new_user.auth_id.toPem()] = new_user
    
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
