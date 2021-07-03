import copy
import random
from typing import Sized
import numpy as np

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


class Block:
    """
    A block is a contiguous subset of bits in a shuffled key.
    """

    ERRORS_EVEN = 0
    """The block contains an odd number of errors."""
    ERRORS_ODD = 1
    """The block contains an even number of errors."""
    ERRORS_UNKNOWN = None
    """We don't know whether the block contains an even or an odd number of errors."""

    def __init__(self, key, shuffle, start_index, end_index, parent_block):
        """
        Create a block, which is a contiguous subset of bits in a shuffled key.

        Args:
            key (Key): The key for which to create one single block that covers a subset of the key.
            shuffle (Shuffle): The shuffle to apply to the key before creating the block.
            start_index (int): The shuffle index, inclusive, at which the block starts. Must be in
                range [0, shuffle._size).
            end_index (int): The shuffle index, exclusive, at which the block end. Must be in range
                [0, shuffle._size]. The range must encompass at least 1 bit, i.e.
                end_index > start_index.
            parent_block (Block): The parent block. None if there is no parent, i.e. if this is a
                top-level block.
        """

        # Store block attributes.
        self._key = key
        self._shuffle = shuffle
        self._start_index = start_index
        self._end_index = end_index

        # Keep track of parent block. None if there is no parent, i.e. if this is a top-level block.
        self._parent_block = parent_block

        # Keep track of left and right sub-block to avoid creating them more then once.
        self._left_sub_block = None
        self._right_sub_block = None

        # Calculate the current parity for this block.
        self._current_parity = shuffle.calculate_parity(
            key, start_index, end_index)

        # We don't yet know the correct parity for this block.
        self._correct_parity = None

    @staticmethod
    def create_covering_blocks(key, shuffle, block_size):
        """
        Create a list of blocks of a given size that cover a given shuffled key.

        Args:
            key (Key): The key for which to create a list of block that collectively cover the
                entire key.
            shuffle (Shuffle): The shuffle to apply to the key before creating the blocks.
            block_size (int): The size of each block. Each block in the list, except for the last
                one, will be exactly this size. The last block may be smaller.

        Returns:
            A list of blocks that cover the shuffled key.
        """

        # Generate the blocks.
        blocks = []
        remaining_bits = shuffle.get_size()
        start_index = 0
        while remaining_bits > 0:
            actual_block_size = min(block_size, remaining_bits)
            end_index = start_index + actual_block_size
            block = Block(key, shuffle, start_index, end_index, None)
            blocks.append(block)
            start_index += actual_block_size
            remaining_bits -= actual_block_size
        return blocks

    def __repr__(self):
        """
        Get the unambiguous string representation of the block.

        Returns:
            The unambiguous string representation of the block.
        """
        string = "Block:"
        for shuffle_index in range(self._start_index, self._end_index):
            key_index = self._shuffle.get_key_index(shuffle_index)
            key_bit = self._shuffle.get_bit(self._key, shuffle_index)
            string += f" {shuffle_index}->{key_index}={key_bit}"
        return string

    def __str__(self):
        """
        Get the human-readable string representation of the block.

        Returns:
            The human-readable string representation of the block.
        """
        string = ""
        for shuffle_index in range(self._start_index, self._end_index):
            string += str(self._shuffle.get_bit(self._key, shuffle_index))
        return string

    def __lt__(self, other):
        """
        Is this block "less than" the other block? This is needed to insert the blocks in a priority
        queue; for equal block sizes the priority queue want to order by increasing block size. We
        don't care about the order of blocks within a given block size, so we simply order based on
        the id().

        Returns:
            True if self < other, False otherwise.
        """
        return id(self) < id(other)

    def get_start_index(self):
        """
        Get the start index of the block, i.e. the shuffled key index for the first bit in the
        block.

        Returns:
            The start index.
        """
        return self._start_index

    def get_end_index(self):
        """
        Get the end index of the block, i.e. the shuffled key index for the first bit after the last
        bit in the block.

        Returns:
            The end index.
        """
        return self._end_index

    def get_shuffle(self):
        """
        Get the shuffle for this block.

        Returns:
            The shuffle for this block.
        """
        return self._shuffle

    def get_size(self):
        """
        Get the size of the block in bits.

        Returns:
            The size of the block in bits.
        """
        return self._end_index - self._start_index

    def get_key_indexes(self):
        """
        Get a list of key indexes for this block.

        Returns:
            The key indexes for this block (the ordering of the list is undefined; in particular
            don't assume that the key indexes are in increasing order.)
        """
        key_indexes = []
        for shuffle_index in range(self._start_index, self._end_index):
            key_index = self._shuffle.get_key_index(shuffle_index)
            key_indexes.append(key_index)
        return key_indexes

    def get_current_parity(self):
        """
        Get the current parity of the block.

        Returns:
            The current parity (0 or 1) of the block.
        """
        return self._current_parity

    def get_correct_parity(self):
        """
        Get the correct parity of the block, if we know it.

        Returns:
            The current parity (0 or 1) of the block, or None if we don't know it.
        """
        return self._correct_parity

    def set_correct_parity(self, correct_parity):
        """
        Set the correct parity of the block.

        Params:
            correct_parity (int): The current parity (0 or 1).
        """
        self._correct_parity = correct_parity

    def is_top_block(self):
        """
        Is this block a top-level block?

        Returns:
            True if the block was created by splitting a shuffled key into blocks. False if the
            block was created by splitting a block into sub-blocks.
        """
        return self._parent_block is None

    def get_parent_block(self):
        """
        Return the parent block of this block, if it has one.

        Returns:
            The parent block, or None if there is no parent block.
        """
        return self._parent_block

    def get_left_sub_block(self):
        """
        Return the left sub-block of this block, if it has one.

        Returns:
            The left sub-block, or None if there is no left sub-block.
        """
        return self._left_sub_block

    def create_left_sub_block(self):
        """
        Create the left sub-block of this block. If the block has an odd size, the left sub-block
        will be one bit larger than the right sub-block. The block must be at least 2 bits in size.

        Returns:
            The left sub-block.
        """
        middle_index = self._start_index + \
            (self._end_index - self._start_index + 1) // 2
        self._left_sub_block = Block(self._key, self._shuffle, self._start_index, middle_index,
                                     self)
        return self._left_sub_block

    def get_right_sub_block(self):
        """
        Return the right sub-block of this block, if it has one.

        Returns:
            The right sub-block, or None if there is no right sub-block.
        """
        return self._right_sub_block

    def create_right_sub_block(self):
        """
        Create the right sub-block of this block. If the block has an odd size, the left sub-block
        will be one bit larger than the right sub-block. The block must be at least 2 bits in size.

        Returns:
            The right sub-block.
        """
        middle_index = self._start_index + \
            (self._end_index - self._start_index + 1) // 2
        self._right_sub_block = Block(
            self._key, self._shuffle, middle_index, self._end_index, self)
        return self._right_sub_block

    def get_error_parity(self):
        """
        Does this block have an odd or an even number of errors?

        Returns:
            * ERRORS_ODD = The block contains an odd number of errors.
            * ERRORS_EVEN = The block contains an even number of errors.
            * ERRORS_UNKNOWN = We don't yet know whether the block contains an odd or even number of
              errors because we have not yet asked what the parity of the original key (witout
              noise) is.
        """
        if self._correct_parity is None:
            return Block.ERRORS_UNKNOWN
        if self._current_parity == self._correct_parity:
            return Block.ERRORS_EVEN
        return Block.ERRORS_ODD

    def get_key_index(self, shuffle_index):
        """
        The the key index that corresponds to a given shuffle index.

        Params:
            shuffle_index: The shuffle index.

        Returns:
            The key index.
        """
        return self._shuffle.get_key_index(shuffle_index)

    def flip_bit(self, flipped_shuffle_index):
        """
        Flip a bit in the block.

        Params:
            flipped_shuffle_index: The shuffle index of the bit to flip.
        """
        self._shuffle.flip_bit(self._key, flipped_shuffle_index)

    def flip_parity(self):
        """
        Flip the current parity of this block. This is needed when a single bit in the block is
        flipped as a result of a single bit error correction.
        """
        self._current_parity = 1 - self._current_parity

