import random
from copy import deepcopy
from typing import Pattern

class Raw_Key:
    def __init__(self,*args):
        self.__setattr__("as_list",list(args))
        self.__setattr__("parity",sum(self.as_list)%2)
        self.__setattr__("length",len(self.as_list))
    
    def get_parity(self):
        return self.__getattribute__("parity") 

    def create_blocks(self,size):
        pass        
        
    def shuffle(self):
        #TODO: try thsi algo!: did try in test2.py
        dicts = self.get_dictionary()
        keys = list(dicts.keys())
        random.shuffle(keys)
        shuffle_dict = dict()
        for key in keys:
            shuffle_dict[key] = self.as_list[key]
        return shuffle_dict 

    def get_dictionary(self):
        dicts = {}
        for i in range(self.length):
            dicts[i] =self.as_list[i]
        return dicts

class Block:
    def __init__(self, block_data:dict):
        self.indexes = indexes
        self.as_list = [raw_key[i] for i in self.indexes]

rk = Raw_Key(1,0,1,0,0,0,1,0,1)
print(rk.as_list)
print(rk.shuffle())
