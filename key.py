import copy
import random
from typing import Sized
import numpy as np


class Key:
    """
    A key that the Cascade protocol reconciles.
    This class is used from Bruno Rijsman's repo. 
    (https://github.com/brunorijsman/cascade-python.git)
    {MIT Licence}
    
    We have added some modifications to work better with our program.
    """

    ERROR_METHOD_BERNOULLI = "bernoulli"
    ERROR_METHOD_EXACT = "exact"
    ERROR_METHODS = [ERROR_METHOD_BERNOULLI, ERROR_METHOD_EXACT]

    def __init__(self, **kwargs):
        """
        Generates a Key Object with the given data

        Kwargs:
            key_as_list (list, optional): [Key with proper indexing as a list].
            key_as_str  (str, optional): [Key as a string].
            key_as_dict (dict, optional): [Key as a dict with dict.keys as indexes and values as bit values].
        """

        # Bits are stored as dictionary, indexed by index [0..size), value 0 or 1.
        if "key_as_list" in kwargs:
            key_as_list = kwargs["key_as_list"]
            self._size = len(key_as_list)
            self._bits = {}
            for i in range(self._size):
                self._bits[i] = key_as_list[i]
        elif "key_as_str" in kwargs:
            key_as_str = kwargs["key_as_str"]
            self._size = len(key_as_str)
            self._bits = {}
            for i in range(self._size):
                self._bits[i] = key_as_str[i]
        elif "key_as_dict" in kwargs:
            key_as_dict = kwargs["key_as_dict"]
            self._size = len(key_as_dict)
            self._bits = key_as_dict
        else:
            self._size = 0
            self._bits = {}

    def __repr__(self):
        """
        Get the unambiguous string representation of the key.

        Returns:
            The unambiguous string representation of the key.
        """
        return "Key: " + self.__str__()

    def __str__(self):
        """
        Get the human-readable string representation of the key.

        Returns:
            The human-readable string representation of the key.
        """
        string = ""
        for i in range(self._size):
            string += str(self._bits[i])
        return string

    def get_size(self):
        """
        Get the size of the key in bits.

        Returns:
            The size of the key in bits.
        """
        return self._size

    def get_bit(self, index):
        """
        Get the value of the key bit at a given index.

        Args:
            index (int): The index of the bit. Index must be in range [0, key.size).

        Returns:
            The value (0 or 1) of the key bit at the given index.
        """
        return self._bits[index]

    def get_block(self, indexes: list):
        # TODO: Make this work by returning block!
        """
        Get the value of the key bit at given indexes.

        Args:
            indexes (list): The indexes of the bits.

        Returns:
            Key object with the indexes as chosen from indexes:list.
        """
        bits = {}
        for index in indexes:
            bits[index] = self._bits[index]
        return Key(key_as_dict=bits)

    def set_bit(self, index, value):
        """
        Set the value of the key bit at a given index.

        Args:
            index (int): The index of the bit. Index must be in range [0, key.size).
            value (int): The new value of the bit. Must be 0 or 1.
        """
        self._bits[index] = value

    def flip_bit(self, index):
        """
        Flip the value of the key bit at a given index (0 to 1, and vice versa).

        Args:
            index (int): The index of the bit. Index must be in range [0, key.size).
        """
        self._bits[index] = 1 - self._bits[index]

    def copy(self, error_rate, error_method):
        """
        Copy a key and optionally apply noise.

        Args:
            error_rate (float): The requested error rate.
            error_method (str): The method for choosing errors. Must be one of the error methods in
                ERROR_METHODS.

        Returns:
            A new Key instance, which is a copy of this key, with noise applied.
        """
        # pylint:disable=protected-access
        key = Key()
        key._size = self._size
        key._bits = copy.deepcopy(self._bits)

        if error_method == self.ERROR_METHOD_EXACT:
            error_count = round(error_rate * self._size)
            bits_to_flip = Key._random.sample(self._bits.keys(), error_count)
            for index in bits_to_flip:
                key._bits[index] = 1 - key._bits[index]

        if error_method == self.ERROR_METHOD_BERNOULLI:
            for index in self._bits.keys():
                if Key._random.random() <= error_rate:
                    key._bits[index] = 1 - key._bits[index]

        return key

    def difference(self, other_key):
        """
        Return the number of bits that are different between this key and the other_key (also known
        as the Hamming distance).

        Args:
            other_key (Key): The other key that this key has to be compared with. Must be the same
                size as this key.

        Returns:
            The number of bits that are different between this key and the other key.
        """
        difference = 0
        for i in range(self._size):
            # pylint:disable=protected-access
            if self._bits[i] != other_key._bits[i]:
                difference += 1
        return difference


class Random_Key_Generator:
    """
    Generates a random Key Object for experimentation.
           
    Returns:
        Key Object: A randomly initialized Key-Object with given size.
    """
    _random = random.Random()
    
    def __init__(self, size) -> None:
        """
        Generates a random Key Object for experimentation

        Args:
            size (int): Size of the Key to be generated.

        Returns:
            Key: A randomly initialized Key-Object with given size.
        """
        self.size = size
    
    def get_random_key(self):
        return self.create_random_key(self.size)    
    @staticmethod
    def create_random_key(size):
        """
        Create an random key.

        Args:
            size (int): The size of the key in bits. Must be >= 0.

        Returns:
            A random key of the specified size.
        """
        # pylint:disable=protected-access
        key = Key()
        key._size = size
        for i in range(size):
            key._bits[i] = Random_Key_Generator._random.randint(0, 1)
        return key
    
    @staticmethod
    def set_random_seed(seed):
        """
        Set the seed for the isolated random number generated that is used only in the key
        module and nowhere else. If two applications set the seed to the same value, the key
        module produces the exact same sequence of random keys. This is used to make experiments
        reproduceable.

        Args:
            seed (int): The seed value for the random number generator which is isolated to the
                key module.
        """
        Random_Key_Generator._random = random.Random(seed)

