class Raw_Key:
    def __init__(self,*args):
        self.__setattr__("as_list",list(args))
        self.__setattr__("parity",sum(self.as_list)%2)
    
    def get_parity(self):
        return self.__getattribute__("parity")    

class Block:
    def __init__(self, raw_key, indexes = []):
        self.indexes = indexes
        self.as_list = [raw_key[i] for i in self.indexes]
        

