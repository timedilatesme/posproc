# PosProc
Easy to use QKD (Quantum Key Distribution) library for post processing.
* Requires Python >= v3.9.5
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
2. Then in the directory of this repo run the file [install.bat](install.bat).

### Developer Installation
1. Clone this repo to your PC (*use github desktop, it's much more convenient.*).
2. Then in the directory of this repo run the file [install_develop.bat](install_develop.bat).

## Simple Authentication Example
### Creating the server
```python
from posproc import*

# Create the server
alice = QKDServer('Alice')

# Initialize all the protocols for authentication, error correction, privacy amplification.
alice.Initialize_Events()

# Start the server socket
alice.start_ursina_server()

# Important call for event based networking
alice.start_events_processing_thread()

```
### Creating the client
```python
from posproc import*

# Create the client
bob = QKDClient('Bob')

# Start the client socket
bob.start_ursina_client()

# Initialize all the protocols for authentication, error correction, privacy amplification.
bob.Initialize_Events()

# Important call for event based networking
bob.start_events_processing_thread()

# Cleanly stop the client after everything is done!
time.sleep(0.1) # For waiting until everything is done
bob.stopClient()
```

The above two files needs to be executed in different terminals. By default this will start a local server on the LOCAL_PORT defined in [constants](posproc/constants.py). If the necessary user data is not already stored in the current directory then on first connection it will be created and saved in the file path specified by [DATA_STORAGE](posproc/constants.py). And when this client connects again, then authentication will be done using data at server's end.
