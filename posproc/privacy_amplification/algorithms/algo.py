import hashlib

from bitstring import BitArray
import chilkat
import random
# python -m posproc.privacy_amplification.algorithms.algo

encoding = 'utf-8'
seed = 10

class apply_hash_alorithms:
    """
    Hashing Algorithms to be used in Privacy amplification
    """
    def __init__(self,reconciled_key):
        self.raw_key = reconciled_key
        self.raw_key_duplicate = reconciled_key
        self.raw_key_bytes = bytes(reconciled_key,encoding)
        self.pa_key = None
        self.hash_function = None
        self.crypt = chilkat.CkCrypt2()
        self.crypt.put_EncodingMode("hex")

        self.HASHING_ALGORITHMS = {"sha1":self.sha1,
                                    "sha256":self.sha256,
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
                                    "sha3_256":self.sha3_256,
                                    "sha3_384":self.sha3_384,
                                    "sha3_512":self.sha3_512}
        

    def con_hexstr_to_bin(self,key):
        key = hex(int(key,base = 16))
        key = BitArray(hex = key)
        key = key.bin
        return key
    
    def sha1(self):
        self.hash_function = hashlib.sha1()
        self.hash_function.update(self.raw_key_bytes)
        self.pa_key = self.hash_function.hexdigest()
        self.pa_key = self.con_hexstr_to_bin(self.pa_key)
        return self.pa_key

    def sha256(self):
        self.hash_function = hashlib.sha256()
        self.hash_function.update(self.raw_key_bytes)
        self.pa_key = self.hash_function.hexdigest()
        self.pa_key = self.con_hexstr_to_bin(self.pa_key)
        return self.pa_key

    def sha512(self):
        self.hash_function = hashlib.sha512()
        self.hash_function.update(self.raw_key_bytes)
        self.pa_key = self.hash_function.hexdigest()
        self.pa_key = self.con_hexstr_to_bin(self.pa_key)
        return self.pa_key
    
    def md5(self):
        self.hash_function = hashlib.md5()
        self.hash_function.update(self.raw_key_bytes)
        self.pa_key = self.hash_function.hexdigest()
        self.pa_key = self.con_hexstr_to_bin(self.pa_key)
        return self.pa_key

    def md4(self):
        self.hash_function = hashlib.new("md4")
        self.hash_function.update(self.raw_key_bytes)
        self.pa_key = self.hash_function.hexdigest()
        self.pa_key = self.con_hexstr_to_bin(self.pa_key)
        return self.pa_key

    def ripemd128(self):
        self.crypt.put_HashAlgorithm("ripemd128")
        self.pa_key = self.crypt.hashStringENC(self.raw_key)
        self.pa_key = self.con_hexstr_to_bin(self.pa_key)
        return (self.pa_key)

    def ripemd160(self):
        self.crypt.put_HashAlgorithm("ripemd160")
        self.pa_key = self.crypt.hashStringENC(self.raw_key)
        self.pa_key = self.con_hexstr_to_bin(self.pa_key)
        return (self.pa_key)

    def ripemd256(self):
        self.crypt.put_HashAlgorithm("ripemd256")
        self.pa_key = self.crypt.hashStringENC(self.raw_key)
        self.pa_key = self.con_hexstr_to_bin(self.pa_key)
        return self.pa_key


    def ripemd320(self):
        self.crypt.put_HashAlgorithm("ripemd320")
        self.pa_key = self.crypt.hashStringENC(self.raw_key)
        self.pa_key = self.con_hexstr_to_bin(self.pa_key)
        return self.pa_key

    def shake_128(self,size):
        self.hash_function = hashlib.shake_128()
        self.hash_function.update(self.raw_key_bytes)
        self.pa_key = self.hash_function.hexdigest(size)
        self.pa_key = self.con_hexstr_to_bin(self.pa_key)
        return self.pa_key

    def shake_256(self,size):
        self.hash_function = hashlib.shake_256()
        self.hash_function.update(self.raw_key_bytes)
        self.pa_key = self.hash_function.hexdigest(size)
        self.pa_key = self.con_hexstr_to_bin(self.pa_key)
        return self.pa_key

    def sha3_512(self):
        self.hash_function = hashlib.sha3_512()
        self.hash_function.update(self.raw_key_bytes)
        self.pa_key = self.hash_function.hexdigest()
        self.pa_key = self.con_hexstr_to_bin(self.pa_key)
        return self.pa_key

    def sha3_384(self):
        self.hash_function = hashlib.sha3_384()
        self.hash_function.update(self.raw_key_bytes)
        self.pa_key = self.hash_function.hexdigest()
        self.pa_key = self.con_hexstr_to_bin(self.pa_key)
        return self.pa_key
    
    def sha3_256(self):
        self.hash_function = hashlib.sha3_256()
        self.hash_function.update(self.raw_key_bytes)
        self.pa_key = self.hash_function.hexdigest()
        self.pa_key = self.con_hexstr_to_bin(self.pa_key)
        return self.pa_key

    def sha3_224(self):
        self.hash_function = hashlib.sha3_224()
        self.hash_function.update(self.raw_key_bytes)
        self.pa_key = self.hash_function.hexdigest()
        self.pa_key = self.con_hexstr_to_bin(self.pa_key)
        return self.pa_key

    def sha224(self):
        self.hash_function = hashlib.sha224()
        self.hash_function.update(self.raw_key_bytes)
        self.pa_key = self.hash_function.hexdigest()
        self.pa_key = self.con_hexstr_to_bin(self.pa_key)
        return self.pa_key

    def sha384(self):
        self.hash_function = hashlib.sha224()
        self.hash_function.update(self.raw_key_bytes)
        self.pa_key = self.hash_function.hexdigest()
        self.pa_key = self.con_hexstr_to_bin(self.pa_key)
        return self.pa_key
    
    def blake2s(self):
        self.hash_function = hashlib.blake2s()
        self.hash_function.update(self.raw_key_bytes)
        self.pa_key = self.hash_function.hexdigest()
        self.pa_key = self.con_hexstr_to_bin(self.pa_key)
        return self.pa_key

    def blake2b(self):
        self.hash_function = hashlib.blake2s()
        self.hash_function.update(self.raw_key_bytes)
        self.pa_key = self.hash_function.hexdigest()
        self.pa_key = self.con_hexstr_to_bin(self.pa_key)
        return self.pa_key



    def digest_hash_fn(self,algo = None):
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
        raw_key_list = list(self.raw_key)
        random.Random(seed).shuffle(raw_key_list)
        pa_key_list = raw_key_list
        self.pa_key = ''.join(map(str,pa_key_list))
        return self.pa_key
    

    def mod_fn(self,no_of_bits):
        self.pa_key = self.raw_key[len(self.raw_key)-no_of_bits:]
        return self.pa_key

    def div_fn(self,no_of_bits):
        self.pa_key = self.raw_key[:len(self.raw_key)-no_of_bits]
        return self.pa_key

    def perm_mod_fn(self,no_of_bits):
        self.raw_key = self.permutation()
        self.pa_key = self.mod_fn(no_of_bits)
        self.raw_key = self.raw_key_duplicate
        return self.pa_key

    def perm_div_fn(self,no_of_bits):
        self.raw_key = self.permutation()
        self.pa_key = self.div_fn(no_of_bits)
        self.raw_key = self.raw_key_duplicate
        return self.pa_key
        
    def hash_mod_fn(self,no_of_bits):
        self.raw_key = self.digest_hash_fn()
        self.pa_key = self.mod_fn(no_of_bits)
        self.raw_key = self.raw_key_duplicate
        return self.pa_key
    
    def hash_div_fn(self,no_of_bits):
        self.raw_key = self.digest_hash_fn()
        self.pa_key = self.div_fn(no_of_bits)
        self.raw_key = self.raw_key_duplicate
        return self.pa_key

