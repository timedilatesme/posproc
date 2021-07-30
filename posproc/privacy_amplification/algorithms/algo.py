import hashlib
#import crakhash
from algorithms import chilkat
from algorithms.ripmed128 import ripemd128

encoding = 'utf-8'

class apply_hash_alorithms:
    """
    Hashing Algorithms to be used in Privacy amplification
    """
    def __init__(self,reconciled_key):
        self.raw_key = reconciled_key
        self.raw_key_bytes = bytes(reconciled_key,encoding)
        self.pa_key = None
        self.hash_function = None
        
        
    def sha1(self):
        self.hash_function = hashlib.sha1()
        self.hash_function.update(self.raw_key_bytes)
        self.pa_key = self.hash_function.hexdigest()
        return self.pa_key

    def sha256(self):
        self.hash_function = hashlib.sha256()
        self.hash_function.update(self.raw_key_bytes)
        self.pa_key = self.hash_function.hexdigest()
        return self.pa_key

    def sha512(self):
        self.hash_function = hashlib.sha512()
        self.hash_function.update(self.raw_key_bytes)
        self.pa_key = self.hash_function.hexdigest()
        return self.pa_key
    
    def md5(self):
        self.hash_function = hashlib.md5()
        self.hash_function.update(self.raw_key_bytes)
        self.pa_key = self.hash_function.hexdigest()
        return self.pa_key

    def md4(self):
        self.hash_function = hashlib.md4()
        self.hash_function.update(self.raw_key_bytes)
        self.pa_key = self.hash_function.hexdigest()
        return self.pa_key

    def ripemd160(self):
        self.hash_function = hashlib.new('ripemd160')
        print(self.hash_function)
        self.hash_function.update(self.raw_key_bytes)
        self.pa_key = self.hash_function.hexdigest()
        return self.pa_key

    '''def ripemd128(self):
        digest = ripemd128(self.raw_key_bytes)
        self.pa_key = digest.hex()
        return self.pa_key
    '''
    def ripemd256(self):
        crypt = chilkat.CkCrypt2()
        crypt.put_EncodingMode("bytes")
        crypt.put_HashAlgorithm("ripemed256")
        self.pa_key = crypt.hashStringENC(self.raw_key)
        return self.pa_key

    def ripemd128(self):
        crypt = chilkat.CkCrypt2()
        crypt.put_EncodingMode("bytes")
        crypt.put_HashAlgorithm("ripemed128")
        self.pa_key = crypt.hashStringENC(self.raw_key)
        return self.pa_key

    def ripemd320(self):
        crypt = chilkat.CkCrypt2()
        crypt.put_EncodingMode("bytes")
        crypt.put_HashAlgorithm("ripemed320")
        self.pa_key = crypt.hashStringENC(self.raw_key)
        return self.pa_key