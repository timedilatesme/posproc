class User:
    """
    A Mock Implementation of a User with it's attributes.
    """
    def __init__(self, name = None, address = None, auth_id = None) -> None:
        self.name = name
        self.address = address
        self.auth_id = auth_id
class UserData:
    """
    UserData stores the data about nickname, address and public key of every person,
    who uses the classical channel. This is for authentication purpose.
    This data will be available to all users of the network.
    """
    def __init__(self) -> None:
        self.users = [] # 
        
    def update_user_data(self,new_user:User):
        self.users[new_user.username] = new_user.get_auth_id()
    
    def get_user_by_address(self, address):
        for user in self.users: