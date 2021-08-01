# posproc
This repository contains the code for an implementation of post processing in python and then using all those algorithms in an easy to use Software!


Dependencies:

hashlib(pip install hashlib)

pyngrok(pip install pyngrok) : For port forwarding and adding the functionality of remote QKD.

starbank-ecdsa (pip install starkbank-ecdsa) :For authentication.

# PosProc
Easy to use QKD (Quantum Key Distribution) library for post processing.
* Contains implemetation of Cascade and other error correction algorithms (More will be added in future).
* Based on an event based networking engine.
* Includes almost all hashing algorithms for privacy amplification.

## Getting Started
### Dependencies
1. For authentication using digital signatures: [ecdsa-python](https://github.com/starkbank/ecdsa-python.git). 
    ```
    pip install starkbank-ecdsa
    ```
2. For making public servers: [pyngrok](https://github.com/alexdlaird/pyngrok.git).
    ```
    pip install pyngrok
    ```
3. For pickling python objects to bytes: [jsonpickle](https://github.com/jsonpickle/jsonpickle.git).
    ```
    pip install jsonpickle
    ```

### Simple Installation
1. Clone this repo to your PC (*use github desktop, it's much more convenient.*).
2. Then in the directory of this repo run the file named [install.bat](install.bat).

### Developer Installation
1. Clone this repo to your PC (*use github desktop, it's much more convenient.*).
2. Then in the directory of this repo run the file named [install_develop.bat](install.bat).
  
