class UserData:
    def __init__(self) -> None:
        self.users = {}
    def update_users(self, key, value):
        self.users[key] = value
    def __repr__(self) -> str:
        return str(self.users)
    def get_user_by_address(self, address):
        return self.users[address]

class Server:
    def __init__(self, user_data:UserData) -> None:
        self.user_data = user_data
        self.user_data.update_users(("123",123), "Alice")
    def __eq__(self, o: object) -> bool:
        a =  self.user_data == o.user_data
        return a


class Client:
    def __init__(self, user_data: UserData) -> None:
        self.user_data = user_data
        self.user_data.update_users(("124", 124), "Bob")

ud = UserData()
# print("Initially: ", ud)
# s = Server(ud)
# print("After Server: ", ud)
# c = Client(ud)
# print("After Client: ", ud)

# a = ud.get_user_by_address(('124', 124))

# print("Bob: ", a)

s = Server(ud)
s2 = Server(ud)
print(s.__dict__.keys())
print(s == s2)