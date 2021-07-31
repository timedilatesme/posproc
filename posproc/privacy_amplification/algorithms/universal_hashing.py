import hashlib

from bitstring import BitArray
import chilkat
import random
# python -m posproc.privacy_amplification.algorithms.algo

#constants
encoding = 'utf-8'
seed = 10

# MAIN CLASS FOR PRIVACY AMPLIFICATION (UNIVERSAL HASHING)

class apply_hash_alorithms:
    """
    Hashing Algorithms to be used in Privacy amplification
    """
    def __init__(self,reconciled_key):
        """
        Initialize the reconciled_key,duplicate,its bytes form, priavcy amplified key(pa_key) and creaation of cypt instance -->see chilkat

        Args:
            reconciled_key ([str]): [error corrected key after reconcilation]
        """
        self.raw_key = reconciled_key
        self.raw_key_duplicate = reconciled_key
        self.raw_key_bytes = bytes(reconciled_key,encoding)
        self.pa_key = None
        self.hash_function = None
        self.crypt = chilkat.CkCrypt2()
        self.crypt.put_EncodingMode("hex")

        # set of hashing functions available till now in self.HASHING_ALGORITHMS #TODO add more given in paper
        self.HASHING_ALGORITHMS = {"sha1":self.sha1,
                                    "sha224":self.sha224,
                                    "sha256":self.sha256,
                                    "sha384":self.sha384,
                                    "sha512":self.sha512,
                                    "md5":self.md5,
                                    "md4":self.md4,
                                    "ripemd128":self.ripemd128,
                                    "ripemd160":self.ripemd160,
                                    "ripemd256":self.ripemd256,
                                    "ripemd320":self.ripemd320,
                                    "shake_128":self.shake_128,
                                    "shake_256":self.shake_256,
                                    "blake2s":self.blake2s,
                                    "blake2b":self.blake2b,
                                    "sha3_224":self.sha3_224,
                                    "sha3_256":self.sha3_256,
                                    "sha3_384":self.sha3_384,
                                    "sha3_512":self.sha3_512}
    
    #general conversion function needed everywhere

    def con_hexstr_to_bin(self,key):
        """
        Converts hexadecimal string to its binary form 

        Args:
            key ([str]): [any ranom hex string]

        Returns:
            [str]: [binary form]
        """
        key = hex(int(key,base = 16))
        key = BitArray(hex = key)
        key = key.bin
        return key
    

    # STANDARD EXISING METHODS TO IMPLEMENT HASHING MAINLY IMPORTED FROM HASHLIB AND CHILKET.
    # FORMING A CLASS OF UNIVERSAL HASH FUNCTIONS
    # TODO More of such functions can be added as per the requirement
    
    def sha1(self):
        """
        Standard SHA1 algorithm imported from hashlib library

        Returns:
            [str]: [pa_key]
        """
        self.hash_function = hashlib.sha1()
        self.hash_function.update(self.raw_key_bytes)
        self.pa_key = self.hash_function.hexdigest()
        self.pa_key = self.con_hexstr_to_bin(self.pa_key)
        return self.pa_key

    def sha256(self):
        """
        Standard SHA256 algorithm imported from hashlib library

        Returns:
            [str]: [pa_key]
        """
        self.hash_function = hashlib.sha256()
        self.hash_function.update(self.raw_key_bytes)
        self.pa_key = self.hash_function.hexdigest()
        self.pa_key = self.con_hexstr_to_bin(self.pa_key)
        return self.pa_key

    def sha512(self):
        """
        Standard SHA512 algorithm imported from hashlib library

        Returns:
            [str]: [pa_key]
        """
        self.hash_function = hashlib.sha512()
        self.hash_function.update(self.raw_key_bytes)
        self.pa_key = self.hash_function.hexdigest()
        self.pa_key = self.con_hexstr_to_bin(self.pa_key)
        return self.pa_key
    
    def md5(self):
        """
        Standard MD5 algorithm imported from hashlib library

        Returns:
            [str]: [pa_key]
        """
        self.hash_function = hashlib.md5()
        self.hash_function.update(self.raw_key_bytes)
        self.pa_key = self.hash_function.hexdigest()
        self.pa_key = self.con_hexstr_to_bin(self.pa_key)
        return self.pa_key

    def md4(self):
        """
        Standard MD4 algorithm imported from hashlib library

        Returns:
            [str]: [pa_key]
        """
        self.hash_function = hashlib.new("md4")
        self.hash_function.update(self.raw_key_bytes)
        self.pa_key = self.hash_function.hexdigest()
        self.pa_key = self.con_hexstr_to_bin(self.pa_key)
        return self.pa_key

    def ripemd128(self):
        """
        Standard RIPEMD128 algorithm used from chilket library

        Returns:
            [str]: [pa_key]
        """
        self.crypt.put_HashAlgorithm("ripemd128")
        self.pa_key = self.crypt.hashStringENC(self.raw_key)
        self.pa_key = self.con_hexstr_to_bin(self.pa_key)
        return (self.pa_key)

    def ripemd160(self):
        """
        Standard RIPEMD160 algorithm used from chilket library

        Returns:
            [str]: [pa_key]
        """
        self.crypt.put_HashAlgorithm("ripemd160")
        self.pa_key = self.crypt.hashStringENC(self.raw_key)
        self.pa_key = self.con_hexstr_to_bin(self.pa_key)
        return (self.pa_key)

    def ripemd256(self):
        """
        Standard RIPEMD256 algorithm used from chilket library

        Returns:
            [str]: [pa_key]
        """
        self.crypt.put_HashAlgorithm("ripemd256")
        self.pa_key = self.crypt.hashStringENC(self.raw_key)
        self.pa_key = self.con_hexstr_to_bin(self.pa_key)
        return self.pa_key


    def ripemd320(self):
        """
        Standard RIPEMD256 algorithm used from chilket library

        Returns:
            [str]: [pa_key]
        """
        self.crypt.put_HashAlgorithm("ripemd320")
        self.pa_key = self.crypt.hashStringENC(self.raw_key)
        self.pa_key = self.con_hexstr_to_bin(self.pa_key)
        return self.pa_key

    def shake_128(self,size):
        """
        Standard SHAKE_128 algorithm used from hashlib library

        Args:
            size ([int]): [the size of the final pa_key that user wants]

        Returns:
            [str]: [pa_key]
        """
        self.hash_function = hashlib.shake_128()
        self.hash_function.update(self.raw_key_bytes)
        self.pa_key = self.hash_function.hexdigest(size)
        self.pa_key = self.con_hexstr_to_bin(self.pa_key)
        return self.pa_key

    def shake_256(self,size):
        """
        Standard SHAKE_256 algorithm used from hashlib library

        Args:
            size ([int]): [the size of the final pa_key that user wants]

        Returns:
            [str]: [pa_key]
        """
        self.hash_function = hashlib.shake_256()
        self.hash_function.update(self.raw_key_bytes)
        self.pa_key = self.hash_function.hexdigest(size)
        self.pa_key = self.con_hexstr_to_bin(self.pa_key)
        return self.pa_key

    def sha3_512(self):
        """
        Standard SHA3_512 algorithm used from hashlib library

        Returns:
            [str]: [pa_key]
        """
        self.hash_function = hashlib.sha3_512()
        self.hash_function.update(self.raw_key_bytes)
        self.pa_key = self.hash_function.hexdigest()
        self.pa_key = self.con_hexstr_to_bin(self.pa_key)
        return self.pa_key

    def sha3_384(self):
        """
        Standard SHA3_512 algorithm used from hashlib library

        Returns:
            [str]: [pa_key]
        """
        self.hash_function = hashlib.sha3_384()
        self.hash_function.update(self.raw_key_bytes)
        self.pa_key = self.hash_function.hexdigest()
        self.pa_key = self.con_hexstr_to_bin(self.pa_key)
        return self.pa_key
    
    def sha3_256(self):
        """
        Standard SHA3_256 algorithm used from hashlib library

        Returns:
            [str]: [pa_key]
        """
        self.hash_function = hashlib.sha3_256()
        self.hash_function.update(self.raw_key_bytes)
        self.pa_key = self.hash_function.hexdigest()
        self.pa_key = self.con_hexstr_to_bin(self.pa_key)
        return self.pa_key

    def sha3_224(self):
        """
        Standard SHA3_224 algorithm used from hashlib library

        Returns:
            [str]: [pa_key]
        """
        self.hash_function = hashlib.sha3_224()
        self.hash_function.update(self.raw_key_bytes)
        self.pa_key = self.hash_function.hexdigest()
        self.pa_key = self.con_hexstr_to_bin(self.pa_key)
        return self.pa_key

    def sha224(self):
        """
        Standard SHA224 algorithm used from hashlib library

        Returns:
            [str]: [pa_key]
        """
        self.hash_function = hashlib.sha224()
        self.hash_function.update(self.raw_key_bytes)
        self.pa_key = self.hash_function.hexdigest()
        self.pa_key = self.con_hexstr_to_bin(self.pa_key)
        return self.pa_key

    def sha384(self):
        """
        Standard SHA384 algorithm used from hashlib library

        Returns:
            [type]: [description]
        """
        self.hash_function = hashlib.sha224()
        self.hash_function.update(self.raw_key_bytes)
        self.pa_key = self.hash_function.hexdigest()
        self.pa_key = self.con_hexstr_to_bin(self.pa_key)
        return self.pa_key
    
    def blake2s(self):
        """
        Standard BLAKE2S algorithm used from hashlib library

        Returns:
            [str]: [pa_key]
        """
        self.hash_function = hashlib.blake2s()
        self.hash_function.update(self.raw_key_bytes)
        self.pa_key = self.hash_function.hexdigest()
        self.pa_key = self.con_hexstr_to_bin(self.pa_key)
        return self.pa_key

    def blake2b(self):
        """
        Standard BLAKE2B algorithm used from hashlib library

        Returns:
            [str]: [pa_key]
        """
        self.hash_function = hashlib.blake2s()
        self.hash_function.update(self.raw_key_bytes)
        self.pa_key = self.hash_function.hexdigest()
        self.pa_key = self.con_hexstr_to_bin(self.pa_key)
        return self.pa_key


#END OF STANDARD ALGORITHMS
# START OF THE IMPLEMENTATION METHODS

    def digest_hash_fn(self,algo = None):
        """
        Function to implement the list of hashing functions on the given key.Applied to binary string (x) of length (N) and 
        outputs a hashed string of selected hash function signature length which changes the number of (1’s) and (0’s) and randomly 
        shuffle their locations.

        Args:
            algo ([str], optional): [algo to implement if any , else randomly chosen from the existing ones]. Defaults to None.

        Returns:
            [str]: [final key: implentation of a random hashing function]
        """
        if algo:
            try:
                if algo in self.HASHING_ALGORITHMS.keys():
                    print("Algorithm used is:",self.HASHING_ALGORITHMS[algo].__name__)
                    return self.HASHING_ALGORITHMS[algo]()
            except:
                print(f"Sorry,we are not using {algo}. Try any from the list below: {self.HASHING_ALGORITHMS.keys}")
        else:

            algo = random.choice(list(self.HASHING_ALGORITHMS.keys()))
            print("Algorithm used is:",algo)
            return self.HASHING_ALGORITHMS[algo]()

    def permutation(self):
        """
        Applied to binary string (x) of length (N) and outputs a permutated string of 
        same length (N) which preserves the number of (1’s) and (0’s), while randomly shuffle their locations.

        Returns:
            [str]: [permuted key]
        """
        raw_key_list = list(self.raw_key)
        random.Random(seed).shuffle(raw_key_list)
        pa_key_list = raw_key_list
        self.pa_key = ''.join(map(str,pa_key_list))
        return self.pa_key
    

    def mod_fn(self,no_of_bits):
        """
        Applied to binary string (x) of length (N) and outputs a compressed string of 
        length (R)-bit which is made of rightmost (R)-bits of string (x).

        Args:
            no_of_bits ([int]): [value of R]

        Returns:
            [str]: [pa_key]
        """
        self.pa_key = self.raw_key[len(self.raw_key)-no_of_bits:]
        return self.pa_key

    def div_fn(self,no_of_bits):
        """
        applied to binary string (x) of length (N) and outputs a compressed string of length (N-R)-bit which is made 
        of string (x) by deleting its rightmost (R)-bits and proceeding with rest of bits of string (x).

        Args:
            no_of_bits ([int]): [value of R]

        Returns:
            [str]: [pa_key]
        """
        self.pa_key = self.raw_key[:len(self.raw_key)-no_of_bits]
        return self.pa_key

    def perm_mod_fn(self,no_of_bits):
        """
        applied to binary string (x) of length (N) where permutation function is applied first to 
        string (x) and then apply the Mod function

        Args:
            no_of_bits ([int]): [value of R for mod fn]

        Returns:
            [int]: [pa_key]
        """
        self.raw_key = self.permutation()
        self.pa_key = self.mod_fn(no_of_bits)
        self.raw_key = self.raw_key_duplicate
        return self.pa_key

    def perm_div_fn(self,no_of_bits):
        """
        Applied to binary string (x) of length (N) where permutation function is applied first to string (x) 
        and then apply the Div function. 

        Args:
            no_of_bits ([int]): [value of R for div fn]

        Returns:
            [str]: [pa_key]
        """
        self.raw_key = self.permutation()
        self.pa_key = self.div_fn(no_of_bits)
        self.raw_key = self.raw_key_duplicate
        return self.pa_key
        
    def hash_mod_fn(self,no_of_bits):
        """
        Applied to binary string (x) of length (N) where digest hash 
        function is applied first to string (x) and then apply the Mod function. 

        Args:
            no_of_bits ([int]): [value of R for mod fn]

        Returns:
            [str]: [pa_key]
        """
        self.raw_key = self.digest_hash_fn()
        self.pa_key = self.mod_fn(no_of_bits)
        self.raw_key = self.raw_key_duplicate
        return self.pa_key
    
    def hash_div_fn(self,no_of_bits):
        """
        Applied to binary string (x) of length (N) where digest hash function is applied first 
        to string (x) and then apply the Div function.

        Args:
            no_of_bits ([int]): [value of R for div fn]

        Returns:
            [str]: [pa_key]
        """
        self.raw_key = self.digest_hash_fn()
        self.pa_key = self.div_fn(no_of_bits)
        self.raw_key = self.raw_key_duplicate
        return self.pa_key

