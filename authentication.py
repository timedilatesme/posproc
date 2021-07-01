from ellipticcurve.ecdsa import Ecdsa
from ellipticcurve.privateKey import PrivateKey

'''This file uses https://github.com/starkbank/ecdsa-python for authentication.
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
