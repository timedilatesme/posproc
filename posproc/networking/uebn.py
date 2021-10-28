"""
Part of the code here was taken from Ursina Networking Library.
https://github.com/kstzl/UrsinaNetworking.git {MIT Licence}

Since it provides neat event based networking.
Therefore we are using it for our ask parity, authentication and
other messages.
"""

"""
Copyright 2021, Kevin STOETZEL

Permission is hereby granted, free of charge, to any person obtaining a copy of this software
and associated documentation files (the "Software"), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge, publish, distribute,
sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall
be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE
FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""

from os import name
import PySimpleGUI as sg
import zlib
import socket
import threading
from typing import Any, List, Tuple
from posproc import constants
from posproc.utils import dumps, loads, rename
from termcolor import colored
from posproc.utils import gui_console_print
HEADERSIZE = 10
MESSAGE_LENGTH = 10
BUFFERSIZE = 4096*2

BUILTIN_EVENT_CONNECTION_ESTABLISHED = "onConnectionEstablished"
BUILTIN_EVENT_CONNECTION_ERROR = "onConnectionError"

BUILTIN_EVENT_CLIENT_CONNECTED = "onClientConnected"
BUILTIN_EVENT_CLIENT_DISCONNECTED = "onClientDisconnected"

STATE_HEADER = "STATE_HEADER"
STATE_PAYLOAD = "STATE_PAYLOAD"

FORMAT = constants.FORMAT


def networking_log(Class_, Context_, Message_):
    class_ = colored(Class_, 'cyan')
    context_ = colored(Context_, 'magenta')
    message_ = colored(Message_, 'white')
    print(f"[{class_} / {context_}] {message_}")
    
def console_output(Message,*args):
    toPrint = '\n ' + '>>>' + f' {Message}\n'
    print(toPrint,*args)

terminal_print = console_output

def ursina_networking_decompress_file(Datas_):

    return zlib.decompress(Datas_)


def ursina_networking_encode_file(Path_):

    file = open(Path_, "rb")
    datas = file.read()
    file.close()
    return zlib.compress(datas)


def ursina_networking_encode_message(Message_, Content_):

    try:
        Message = {
            "Message":   Message_,
            "Content":   Content_
        }
        EncodedMessage = dumps(Message)
        MessageLength = len(EncodedMessage)
        LengthToBytes = MessageLength.to_bytes(MESSAGE_LENGTH, byteorder="big")
        FinalMessage = LengthToBytes + EncodedMessage
        return FinalMessage
    except Exception as e:
        networking_log("ursina_networking_encode_message", "func", e)
    return b""


class UrsinaNetworkingEvents():

    def __init__(self, lock: threading.Lock):
        self.events = []
        self.event_table = {}
        self.lock = lock
        self.received_data = {} 
        # self.received_data = { msgnameEvent : { 'threadEvent' : threading.Event() , 'Content' : data} }

    def push_event(self, name, **kwargs):
        self.lock.acquire()
        self.events.append((name, kwargs))
        self.lock.release()

    def process_net_events(self):
        self.lock.acquire()
        Events = self.events
        EventTable = self.event_table
        for event in Events:
            Func = event[0]  # name of func
            Kwargs = event[1]
            # try:
            for events_ in EventTable:
                # print("EVENT TABLE:",self.event_table)
                for event_ in EventTable[events_]:
                    if Func in event_.__name__:
                        if Func in self.received_data:
                            self.received_data[Func]['Content'] = Kwargs['Content']
                            self.received_data[Func]['threadEvent'].set()
                        else:
                            event_(**Kwargs)
                        
            # except Exception as e:
            #     networking_log(
            #         "UrsinaNetworkingEvents", "process_net_events", f"Unable to correctly call '{Func}' : '{e}'")

        self.events.clear()

        self.lock.release()

    def event(self, func):
        """
        1. For eg. on client side::
        >>> @event
            def some_function(Content):
                pass
            
        >>> dataOutput = some_function(*args) # == Content
        
        2. For eg. on server side::
        >>> @event
            def some_function(Client, Content):
                pass
        """
        # NOTE: Currently it is not possible to define an event inside an event
        # FIXME: Maybe add some functionality for the above!
        self.lock.acquire()
        
        if func.__name__ in self.event_table:
            self.event_table[func.__name__].append(func)
        else:
            self.event_table[func.__name__] = [func]
        
        self.lock.release()
    
    def receiver_event(self, func):
        """
        A decorator used for returning data!
        
        For eg. we can use this as:
        >>> @receiver_event
            def some_function(*args):
                # some Logic ...
                pass
            
        >>> dataOutput = some_function(*args) # == Content        
        """
        self.lock.acquire()

        if func.__name__ in self.event_table:
            self.event_table[func.__name__].append(func)
        else:
            self.event_table[func.__name__] = [func]

        self.received_data[func.__name__] = {'threadEvent' : threading.Event(), 'Content' : None}
        
        self.lock.release()
        
        def wrapper(*args):
                
            self.received_data[func.__name__]['threadEvent'].wait()
            
            self.lock.acquire()
            data = self.received_data.pop(func.__name__)['Content']
            self.lock.release()
               
            func(*args)
            return  data
        return wrapper

class UrsinaNetworkingDatagramsBuffer():

    def __init__(self):
        self.header = bytes()
        self.payload = bytes()
        self.buf = bytearray()
        self.pickled_datas = None
        self.payload_length = 0
        self.receive_all = False
        self.datagrams = []
        self.state = STATE_HEADER

    def receive_datagrams(self, client_):

        self.buf += client_.recv(BUFFERSIZE)

        while True:

            self.state_changed = False

            if self.state == STATE_HEADER:

                if len(self.buf) >= MESSAGE_LENGTH:

                    self.header = self.buf[:MESSAGE_LENGTH]

                    del self.buf[:MESSAGE_LENGTH]

                    self.payload_length = int.from_bytes(
                        self.header, byteorder="big", signed=False)

                    self.state = STATE_PAYLOAD
                    self.state_changed = True

            elif self.state == STATE_PAYLOAD:

                if len(self.buf) >= self.payload_length:

                    self.payload = self.buf[:self.payload_length]

                    del self.buf[:self.payload_length]

                    self.state = STATE_HEADER
                    self.state_changed = True
                    self.receive_all = True
                    self.pickled_datas = loads(self.payload)
                    self.datagrams.append(self.pickled_datas)

            if not self.state_changed:
                break

    def receive(self):
        if self.receive_all:
            self.receive_all = False
            return True
        else:
            return False


class UrsinaNetworkingConnectedClient():

    def __init__(self, socket, address, id):
        self.socket = socket
        self.address = address
        self.id = id
        self.name = f"Client {id}"
        self.datas = {}
        self.authenticated = threading.Event()
        self.connected = True

    def __repr__(self):
        return self.name

    def send_message(self, Message_, Content_):
        if self.connected:
            try:
                Encoded = ursina_networking_encode_message(Message_, Content_)

                self.socket.sendall(Encoded)
                return True
            except Exception as e:
                networking_log(
                    "UrsinaNetworkingConnectedClient", "send_message", e)
                return False

class SocketServer:
    def __init__(self, Ip_: str, Port_: int, 
                 events_manager: UrsinaNetworkingEvents, 
                 clients : List[UrsinaNetworkingConnectedClient],
                 gui_window:sg.Window = None):
        
        self.shutdown = threading.Event()
        self.socketAddress = (Ip_, Port_)
        self.network_buffer = UrsinaNetworkingDatagramsBuffer()
        self.events_manager = events_manager
        self.clients = clients

        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.bind(self.socketAddress)
            self.socket.listen()
            self.receiveThread = threading.Thread(target=self.receive)
            self.receiveThread.start()
        except Exception as e:
            networking_log(
                "SocketServer", "__init__", f"Cannot create the server : {e}")
        
        # GUI init
        self.gui_window = gui_window

    def console_output(self, message, *args):
        if self.gui_window:
            gui_console_print(message, self.gui_window)
            terminal_print(message, *args)
        else:
            terminal_print(message, *args)

    def get_client_id(self, Client_):
        for Client in self.clients:
            if Client.socket == Client_:
                return Client.id
        return None

    def get_clients_ids(self):
        Ret = []
        for Client in self.clients:
            Ret.append(Client.id)
        return Ret

    def get_client(self, Client_):
        for Client in self.clients:
            if Client.socket == Client_:
                return Client
        return None

    def get_clients(self):
        return self.clients

    def broadcast(self, Message_, Content_, IgnoreList=[]):
        for Client in self.clients:
            if not Client in IgnoreList:
                Client.send_message(Message_, Content_)

    def handle(self, Client_: socket.socket):
        while not self.shutdown.is_set():
            try:
                self.network_buffer.receive_datagrams(Client_)

                for datagram in self.network_buffer.datagrams:

                    self.events_manager.push_event(
                        name = datagram["Message"], Client = self.get_client(Client_), Content = datagram["Content"])

                self.network_buffer.datagrams = []

            except ConnectionError as e:
                ClientCopy = self.get_client(Client_)
                for Client in self.clients:
                    if Client.socket == Client_:
                        self.clients.remove(Client)
                        break

                self.events_manager.push_event(
                    name = BUILTIN_EVENT_CLIENT_DISCONNECTED, Client =  ClientCopy)
                Client_.close()
                break

            except Exception as e:
                networking_log(
                    "UrsinaNetworkingServer", "handle", f"unknown error : {e}")
                break

    def receive(self):

        while not self.shutdown.is_set():

            client, address = self.socket.accept()

            self.clients.append(UrsinaNetworkingConnectedClient(
                client, address, len(self.clients)))

            self.events_manager.push_event(
                name = BUILTIN_EVENT_CLIENT_CONNECTED, Client = self.get_client(client))

            self.handle_thread = threading.Thread(
                target=self.handle, args=(client,))
            self.handle_thread.start()

    def stop(self):
        """
        Cleanly stop the server and complete all remaining threads!
        """
        
        # self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()
        self.shutdown.set()
        

class SocketClient:

    def __init__(self, Ip_: str, Port_: int, events_manager: UrsinaNetworkingEvents,
                 gui_window: sg.Window = None):

        try:
            self.shutdown = threading.Event()            
            self.network_buffer = UrsinaNetworkingDatagramsBuffer()
            self.events_manager = events_manager            
            self.connected = threading.Event()            
            
            self.handle_thread = threading.Thread(
                target=self.handle, args=(Ip_, Port_,))
            self.handle_thread.start()
            
        except Exception as e:
            networking_log(
                "SocketClient", "__init__", f"Cannot connect to the server : {e}")
        
        # GUI init
        self.gui_window = gui_window

    def console_output(self, message, *args):
        if self.gui_window:
            gui_console_print(message, self.gui_window)
            terminal_print(message, *args)
        else:
            terminal_print(message, *args)

    def process_net_events(self):
        self.events_manager.process_net_events()

    def handle(self, Ip_, Port_):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connection_response = self.socket.connect_ex((Ip_, Port_))

            if self.connection_response == 0:
                self.socketAddress = self.socket.getsockname()
                self.events_manager.push_event(
                    name = BUILTIN_EVENT_CONNECTION_ESTABLISHED)

                # networking_log("UrsinaNetworkingClient", "handle",
                #                f'\n QKDClient connected to {(Ip_, Port_)} \n')
                
                self.connected.set()

                while not self.shutdown.is_set():
                    try:
                        self.network_buffer.receive_datagrams(self.socket)
                        for datagram in self.network_buffer.datagrams:
                            self.events_manager.push_event(
                                name = datagram["Message"], Content = datagram["Content"])

                        self.network_buffer.datagrams = []
                    except ConnectionError as e:
                        if self.shutdown.is_set():
                            self.console_output('You are disconnected from the Server!')
                        else:
                            self.events_manager.push_event(
                                name = BUILTIN_EVENT_CONNECTION_ERROR, Reason = e)
                            networking_log(
                                "SocketClient", "handle", f"connectionError : {e}")
                            break
                    except Exception as e:
                        if self.shutdown.is_set():
                            self.console_output('You are disconnected from the Server!')
                        else:
                            networking_log(
                                "SocketClient", "handle", f"unknown error : {e}")
                        break
            else:
                self.events_manager.push_event(
                    BUILTIN_EVENT_CONNECTION_ERROR, Reason = self.connection_response)

        except Exception as e:
            self.events_manager.push_event(name="connectionError", Reason = e)
            networking_log(
                "SocketClient", "handle", f"Connection Error : {e}")

    def send_message(self, Message_, Content_):
        try:
            if self.connected.is_set():
                encoded_message = ursina_networking_encode_message(
                    Message_, Content_)
                self.socket.sendall(encoded_message)
                return True
            else:
                networking_log("SocketClient", "send_message",
                                      f"WARNING : You are trying to send a message but the socket is not connected !")
        except Exception as e:
            networking_log("SocketClient", "send_message", e)
            return False

    def stop(self):
        """
        Cleanly stop the client and complete all remaining threads!
        """
        # self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()
        self.shutdown.set()


class AdvancedServer:
    def __init__(self, address: Tuple[str, int]) -> None:
        
        self.address = address
        self.lock = threading.Lock()
        self.shutdown = threading.Event()  # Keeps a tab on whether to keep the server running or not?
        self.events_manager = UrsinaNetworkingEvents(self.lock)
        self.event = self.events_manager.event
        self.receiver_event = self.events_manager.receiver_event
        self.clients = []       

    def start_ursina_server(self):
        self.ursinaServer = SocketServer(*self.address, events_manager=self.events_manager,clients=self.clients,gui_window=self.gui_window)
        self.socket = self.ursinaServer.socket
        self.console_output(f'QKDServer listening @ {self.address}.')
    
    def start_events_processing_thread(self):
        def process_net_events():
            while not self.shutdown.is_set():
                self.events_manager.process_net_events()
        self.processEventsThread = threading.Thread(target=process_net_events)
        self.processEventsThread.start()

    def send_message_to_client(self, Client_: UrsinaNetworkingConnectedClient, Message_, Content_):
        Client_.send_message(Message_, Content_)

    def stopServer(self):
        self.shutdown.set()
        self.ursinaServer.stop()


class AdvancedClient:
    def __init__(self, server_address) -> None:
        
        self.server_address = server_address
        self.lock = threading.Lock()
        self.shutdown = threading.Event()
        self.events_manager = UrsinaNetworkingEvents(self.lock)
        self.event = self.events_manager.event
        self.receiver_event = self.events_manager.receiver_event

    def start_ursina_client(self):
        self.ursinaClient = SocketClient(
            *self.server_address, events_manager=self.events_manager, gui_window=self.gui_window)
        self.ursinaClient.connected.wait()
        self.address = self.ursinaClient.socketAddress
        self.console_output(f'Connection established with Server @ {self.ursinaClient.socket.getpeername()}')

    def start_events_processing_thread(self):
        def process_net_events():
            while not self.shutdown.is_set():
                self.events_manager.process_net_events()
        self.processEventsThread = threading.Thread(target=process_net_events)
        self.processEventsThread.start()

    def send_message_to_server(self, Message_: str, Content_ : Any):
        self.ursinaClient.send_message(Message_, Content_)

    def stopClient(self):
        self.ursinaClient.stop()
        self.shutdown.set()
