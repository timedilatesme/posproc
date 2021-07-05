class Raw_Key:
    def __init__(self,l:list):
        self.__setattr__("as_list",l)
        self.__setattr__("parity",sum(self.as_list)%2)
        self.__setattr__("length",len(self.as_list))
    
    def get_parity(self):
        return self.__getattribute__("parity") 

    def create_blocks(self,size):
        pass        
        
    def remove(self,index):
        del self.as_list[index]

    def shuffle(self):
        #TODO: try thsi algo!: did try in test2.py #DONE!
        dicts = self.get_dictionary()
        keys = list(dicts.keys())
        random.shuffle(keys)
        shuffle_dict = dict()
        for key in keys:
            shuffle_dict[key] = self.as_list[key]
        return shuffle_dict 


##correct get_dictionary()
    def get_dictionary(self):
        dicts = {}
        for i in range(self.length):
            dicts[i] =self.as_list[i]
        return dicts