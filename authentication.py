from hashlib import sha256
from ellipticcurve.ecdsa import Ecdsa
from ellipticcurve.privateKey import PrivateKey
from ellipticcurve.publicKey import PublicKey
from ellipticcurve.curve import secp256k1,prime256v1


'''
This file uses https://github.com/starkbank/ecdsa-python for authentication.
In future try to use https://github.com/AntonKueltz/fastecdsa -> Currently only available for MAC and LINUX
'''

'''
Everytime a new client joins the server he can create a new private key and 
keep that to himself and he can send his public key to the server for saving the
identity of the Client that has joined.

Now when two clients want to talk to each other and they wanna authenticate then
one client can sign his message so that the other party can easily confirm whether 
he/she has received the message from correct person.
'''

class Authentication:
    """
    Generates Random Public Key, Private Key Pair for performing ecdsa.
    Or more generally known as Elliptic Curve Digital Signature Authentication.
    
    This class also has sign and verify methods.
    
    This Class uses {https://github.com/starkbank/ecdsa-python} repository for it's generation of authentication data. 
    
    """

    def __init__(self, curve=secp256k1,secret = None) -> None:
        """
        Random Auth. Data Generator.

        Args:
            curve ([CurveFp], optional): [curve to be used for ECDSA]. Defaults to secp256k1.
            secret ([int], optional): [The secret key in int format]. Defaults to None. If None a random int is used.
        """
        
        self.curve = curve
        self.secret = secret
        
        #TODO: use seed to reproduce results.
        # This is the accompanying PubKey, PrivKey pair
        self._private_auth_key = PrivateKey(curve=self.curve, secret = self.secret)
        self.public_auth_key = self._private_auth_key.publicKey()

    def get_key_pair(self):
        """
        Returns:
            [tuple(PublicKey,PrivateKey)]: Gives the pub_key,priv_key pair.
        """
        return self.public_auth_key, self._private_auth_key
    
    def sign(self, message, hashfunc = sha256):
        """
        Signs a given message.

        Args:
            message (str): The message which is to be authenticated
            hashfunc (optional): Hashing function from hashlib. Defaults to sha256.

        Returns:
            signature (Signature): returns the signature object as defined in ECDSA.
        """
        signature = Ecdsa.sign(message,self._private_auth_key,hashfunc = hashfunc)
        return signature

    @staticmethod
    def verify(message, signature, publicAuthKey, hashfunc=sha256) -> bool:
        """
        Verifies whether the given signature is valid or not.

        Args:
            message (str): [The message that is to be verified.]
            signature ([type]): [The signature sent by the signer.]
            publicKey ([type]): [PublicKey of the signer.]
            hashfunc ([type], optional): [Hashing function used for computation.]. Defaults to sha256.

        Returns:
            bool: [True if the signature is valid => Auth. Successful
                    False if the signature is invalid => Auth. Unsuccessful.]
        """
        verify = Ecdsa.verify(message, signature, publicAuthKey, hashfunc)
        return verify
    
'''
msg = "I am Paras!"
ad = Authentication()

signature = ad.sign(msg)
vf = ad.verify("I am Paras!",signature,ad.public_key)
print(vf)'''
