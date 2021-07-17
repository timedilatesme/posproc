import secrets
import random
from hashlib import sha256
from ellipticcurve.ecdsa import Ecdsa
from ellipticcurve.privateKey import PrivateKey
from ellipticcurve.publicKey import PublicKey
from ellipticcurve.curve import CurveFp, secp256k1,prime256v1

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
    _random = random.Random()
    CURVE_secp256k1 = secp256k1
    CURVE_prime256v1 = prime256v1
    """
    Generates Random Public Key, Private Key Pair for performing ecdsa.
    Or more generally known as Elliptic Curve Digital Signature Authentication.
    
    This class also has sign and verify methods.
    
    This Class uses {https://github.com/starkbank/ecdsa-python} repository for it's generation of authentication data. 
    
    """

    def __init__(self, curve : CurveFp = secp256k1, seed = None, auth_Keys: tuple[PublicKey, PrivateKey] = None) -> None:
        """
        Random Authentication Data Generator.

        Args:
            curve (CurveFp, optional): Curve to be used for ECDSA. Defaults to secp256k1.
            seed (Any, optional): The seed to be used for random auth. key generation. Defaults to None. If None a random int is used.
            auth_Keys: If the user already has a key pair then no need to reproduce another key pair.
        """
        
        if not auth_Keys:
            # set the seed to be the value provided or a random seq. of bytes.
            self.set_random_seed(seed or secrets.token_bytes())

            self.curve = curve
            self.secret = Authentication._random.randrange(1, self.curve.N)
            # This is the accompanying PubKey, PrivKey pair
            self._private_auth_key = PrivateKey(curve=self.curve, secret = self.secret)
            self.public_auth_key = self._private_auth_key.publicKey()
        else:
            self.public_auth_key = auth_Keys[0]
            self._private_auth_key = auth_Keys[1]
            
            

    def _get_key_pair(self):
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
    
    @staticmethod
    def set_random_seed(seed):
        """
        Set the seed for the isolated random number generated that is used only in the Authentication
        module and nowhere else. If two applications set the seed to the same value, the key module 
        produces the exact same sequence of random keys. This is used to make experiments reproduceable.

        Args:
            seed (int): The seed value for the random number generator which is isolated to the
                Authentication module.
        """
        Authentication._random = random.Random(seed)


    def start_authentication_protocol(self):
        auth_init_msg = "auth_init_request".encode(constants.FORMAT)
        self.send_bytes_to_the_server(auth_init_msg)
        while self.authenticating:
            msg_recvd = self.receive_bytes_from_the_server()
            if msg_recvd:
                if msg_recvd.startswith("authentication".encode(constants.FORMAT)):
                    msg_recvd_bytes = msg_recvd.removeprefix(
                        'authentication:'.encode(constants.FORMAT))
                    msg_recvd = pickle.loads(msg_recvd_bytes)
                    msg = msg_recvd[0]
                    signature = msg_recvd[1]
                    publicAuthKey_Server = self.user_data.get_user_by_address(
                        self.server_address).auth_id
                    self.server_authenticated = self._auth.verify(
                        msg, signature, publicAuthKey_Server)
                    if self.server_authenticated:
                        print("Server authentication successful!")
                        self.authentication_return_message()
                        self.authenticating = False  # Done Authenticating so break the loop
                    else:
                        print("Server authentication unsuccessful!")
                        # TODO: maybe add some way of restarting auth.
                        self.authenticating = False

    def authentication_return_message(self):
        #TODO: add something for random length
        # Send the first message for authentication
        msg_to_send_1 = self.random_string_generator()
        # TODO: can add more hash functions randomly
        msg_to_send_2 = self._auth.sign(msg_to_send_1)

        msg_to_send = (msg_to_send_1, msg_to_send_2)
        # TODO: add a way so that authentication is also hidden.
        msg_to_send_bytes = "authentication:".encode(
            constants.FORMAT) + pickle.dumps(msg_to_send)

        self.send_bytes_to_the_server(msg_to_send_bytes)
                    
                                        
            
