
class UserData:
    """
    UserData stores the data about nickname and public key of every person,
    who uses the classical channel. This is for authentication purpose.
    """
    def __init__(self) -> None:
        self.users = {}
        
    def update_user_data(self,new_user):
        self.users[new_user.username] = new_user.get_auth_public_key()
