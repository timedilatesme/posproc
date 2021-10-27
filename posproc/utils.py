from pyngrok import ngrok
import socket, pickle, jsonpickle
from typing import Any
from posproc import constants
import PySimpleGUI as sg

def start_ngrok_tunnel(port):
    """
    NGROK tunnel is used for port forwarding the ngrok address to the local address

    Args:
        port (int): Local Port which is to be used for forwarding. 
                    (Use the port that is not already being used by your system.)
    Returns:
        public_addr (tuple): This is what a public pc can use to connect to this Server.
                                This is a pair (PUBLIC_IP, PUBLIC_PORT)
    """
    tunnel = ngrok.connect(port, "tcp")
    url = tunnel.public_url.split("://")[1].split(":")
    ip = socket.gethostbyaddr(url[0])[-1][0]
    public_addr = (ip, int(url[1]))
    return public_addr
    

def dumps(Object: Any, format = constants.FORMAT) -> bytes:
    dataBytes = jsonpickle.dumps(Object, keys=True).encode(format)
    return dataBytes

def loads(dataBytes: bytes, format = constants.FORMAT) -> Any:
    Object = jsonpickle.loads(dataBytes.decode(format), keys=True)
    return Object

# def dump(Object: Any, path = constants.DATA_STORAGE, format=constants.FORMAT) -> bytes:
#     dataBytes = jsonpickle.dumps(Object).encode(format)
#     pickle.dump(
#     return dataBytes

# def load(dataBytes: bytes, format=constants.FORMAT) -> Any:
#     Object = jsonpickle.loads(dataBytes.decode(format))
#     return Object


CONSOLE_EVENT = '-console-'
def gui_console_print(text: str, window: sg.Window):
    current_text_console = window.Element(CONSOLE_EVENT).Get()
    window.Element(CONSOLE_EVENT).Update(
        current_text_console +'\n >>> ' +text)

def rename(newName):
    def decorator(f):
        f.__name__ = newName
        return f
    return decorator
