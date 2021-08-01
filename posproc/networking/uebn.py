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
import zlib
import socket
import threading
from typing import Tuple
from posproc import constants
from posproc.utils import dumps, loads, rename

HEADERSIZE = 10
MESSAGE_LENGTH = 10
BUFFERSIZE = 4096*2

BUILTIN_EVENT_CONNECTION_ESTABLISHED = "onConnectionEstablished"
BUILTIN_EVENT_CONNECTION_ERROR      = "onConnectionError"

BUILTIN_EVENT_CLIENT_CONNECTED      = "onClientConnected"
BUILTIN_EVENT_CLIENT_DISCONNECTED   = "onClientDisconnected"

STATE_HEADER    = "STATE_HEADER"
STATE_PAYLOAD   = "STATE_PAYLOAD"

FORMAT = constants.FORMAT

def ursina_networking_log(Class_, Context_, Message_):

    print(f"[{Class_} / {Context_}] {Message_}")

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
            "Message"   :   Message_,
            "Content"   :   Content_
        }
        EncodedMessage = dumps(Message)
        MessageLength = len(EncodedMessage)
        LengthToBytes = MessageLength.to_bytes(MESSAGE_LENGTH, byteorder = "big")
        FinalMessage = LengthToBytes + EncodedMessage
        return FinalMessage
    except Exception as e:
        ursina_networking_log("ursina_networking_encode_message", "func", e)
    return b""

class UrsinaNetworkingEvents():

    def __init__(self, lock):
        self.events = []
        # self.static_events = []
        self.event_table = {}
        self.lock = lock

    def push_event(self, name, *args):
        self.lock.acquire()
        # if name.startswith('static_'):
        #     self.static_events.append((name,args))
        self.events.append((name, args))
        self.lock.release()

    def process_net_events(self):
        self.lock.acquire()
        for event in self.events:
            Func = event[0] #name of func
            Args = event[1] 
            try:
                for events_ in self.event_table:
                    for event_ in self.event_table[ events_ ]:
                        if Func in event_.__name__:
                            event_(*Args)
            except Exception as e:
                ursina_networking_log("UrsinaNetworkingEvents", "process_net_events", f"Unable to correctly call '{Func}' : '{e}'")
        
        # for staticEvent in self.static_events:
        #     if staticEvent in self.events:
                
        # if len(self.events) != 0:
        #     print("self.event_table: ", self.event_table)
        
        self.events.clear()
        # self.events.extend(self.static_events)
        
        self.lock.release()                

    def event(self, func):
        # NOTE: Currently it is not possible to define an event inside an event
        # FIXME: Maybe add some functionality for the above!
        if func.__name__ in self.event_table:
            self.event_table[func.__name__].append(func)
        else:
            self.event_table[func.__name__]= [func]

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

                    self.payload_length = int.from_bytes(self.header, byteorder = "big", signed = False)

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
        self.authenticated = False
        self.isNewClient = True
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
                ursina_networking_log("UrsinaNetworkingConnectedClient", "send_message", e)
                return False

class UrsinaNetworkingServer():

    def __init__(self, Ip_, Port_):
        self.shutdown = threading.Event()
        self.socketAddress = (Ip_, Port_)

        self.lock = threading.Lock()
        self.events_manager = UrsinaNetworkingEvents(self.lock)
        self.network_buffer = UrsinaNetworkingDatagramsBuffer()
        self.event = self.events_manager.event
        self.clients = []
        self.lock = threading.Lock()

        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.serverSocket = self.server
            self.server.bind(self.socketAddress)
            self.server.listen()
            self.receiveThread = threading.Thread(target = self.receive)
            self.receiveThread.start()

            # ursina_networking_log("UrsinaNetworkingServer", "__init__", "Server started !")
            # ursina_networking_log("UrsinaNetworkingServer", "__init__", f"Ip   :   {Ip_}")
            # ursina_networking_log("UrsinaNetworkingServer", "__init__", f"Port :   {Port_}")
        except Exception as e:
            ursina_networking_log("UrsinaNetworkingServer", "__init__", f"Cannot create the server : {e} \n")

    def process_net_events(self):
        self.events_manager.process_net_events()

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

    def broadcast(self, Message_, Content_, IgnoreList = []):
        for Client in self.clients:
            if not Client in IgnoreList:
                Client.send_message(Message_, Content_)

    def handle(self, Client_: socket.socket):
        while not self.shutdown.is_set():
            try:
                self.network_buffer.receive_datagrams(Client_)

                for datagram in self.network_buffer.datagrams:

                    self.events_manager.push_event(datagram["Message"], self.get_client(Client_), datagram["Content"])

                self.network_buffer.datagrams = []

            except ConnectionError as e:
                ClientCopy = self.get_client(Client_)
                for Client in self.clients:
                    if Client.socket == Client_:
                        self.clients.remove(Client)
                        break

                self.events_manager.push_event(BUILTIN_EVENT_CLIENT_DISCONNECTED, ClientCopy)
                Client_.close()
                break

            except Exception as e:
                ursina_networking_log("UrsinaNetworkingServer", "handle", f"unknown error : {e}")
                break

    def receive(self):

        while not self.shutdown.is_set():

            client, address = self.server.accept()

            self.clients.append(UrsinaNetworkingConnectedClient(client, address, len(self.clients)))

            self.events_manager.push_event(BUILTIN_EVENT_CLIENT_CONNECTED, self.get_client(client))
            
            self.handle_thread = threading.Thread(target = self.handle, args = (client,))
            self.handle_thread.start()
    
    def stop(self):
        """
        Cleanly stop the server and complete all remaining threads!
        """
        self.shutdown.set()

class UrsinaNetworkingClient():

    def __init__(self, Ip_, Port_):

            try:
                self.shutdown = threading.Event()
                self.lock = threading.Lock()
                self.events_manager = UrsinaNetworkingEvents(self.lock)
                self.network_buffer = UrsinaNetworkingDatagramsBuffer()
                self.event = self.events_manager.event
                self.connected = threading.Event()
                self.handle_thread = threading.Thread(target = self.handle, args = (Ip_, Port_,))
                self.handle_thread.start()
                self.lock = threading.Lock()
            except Exception as e:
                ursina_networking_log("UrsinaNetworkingClient", "__init__", f"Cannot connect to the server : {e}")

    def process_net_events(self):
        self.events_manager.process_net_events()

    def handle(self, Ip_, Port_):
            try:
                self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.clientSocket = self.client
                self.connection_response = self.client.connect_ex((Ip_, Port_))

                if self.connection_response == 0:
                    self.socketAddress = self.clientSocket.getsockname()
                    self.events_manager.push_event(BUILTIN_EVENT_CONNECTION_ESTABLISHED)

                    #ursina_networking_log("UrsinaNetworkingClient", "handle", "Client connected successfully !")
                    print(f'\n QKDClient connected to {(Ip_, Port_)} \n')
                    self.connected.set()
                    
                    while not self.shutdown.is_set():
                        try:
                            self.network_buffer.receive_datagrams(self.client)
                            for datagram in self.network_buffer.datagrams:
                                self.events_manager.push_event(datagram["Message"], datagram["Content"])

                            self.network_buffer.datagrams = []
                        except ConnectionError as e:
                            if self.shutdown.is_set():
                                ursina_networking_log("UrsinaNetworkingClient", "handle", f"You are disconnected from the Server!")
                            else:
                                self.events_manager.push_event(BUILTIN_EVENT_CONNECTION_ERROR, e)
                                ursina_networking_log("UrsinaNetworkingClient", "handle", f"connectionError : {e}")
                                break
                        except Exception as e:
                            ursina_networking_log("UrsinaNetworkingClient", "handle", f"unknown error : {e}")
                            break
                else:
                    self.events_manager.push_event(BUILTIN_EVENT_CONNECTION_ERROR, self.connection_response)

            except Exception as e:
                self.events_manager.push_event("connectionError", e)
                ursina_networking_log("UrsinaNetworkingClient", "handle", f"Connection Error : {e}")

    def send_message(self, Message_, Content_):
        try:
            if self.connected.is_set():
                encoded_message = ursina_networking_encode_message(Message_, Content_)
                self.client.sendall(encoded_message)
                return True
            else:
                ursina_networking_log("UrsinaNetworkingClient", "send_message", f"WARNING : You are trying to send a message but the socket is not connected !")
        except Exception as e:
            ursina_networking_log("UrsinaNetworkingClient", "send_message", e)
            return False
    
    def stop(self):
        """
        Cleanly stop the client and complete all remaining threads!
        """
        self.shutdown.set()


class AdvancedServer:
    def __init__(self, address: Tuple[str, int]) -> None:
        self.messages_to_send = {} # stores messages to be sent as { Client_ : (Message_,Content_) }
        self.address = address
        self.shutdown = threading.Event() # Keeps a tab on whether to keep the server running or not?

        
    def receiver_event(self, func):
        self.tempVar = None
        dataAvailable = threading.Event()

        @self.event
        @rename(func.__name__)
        def receivingLogic(Client, Content):
            self.ursinaServer.lock.acquire()
            self.tempVar = Content
            dataAvailable.set()
            self.ursinaServer.lock.release()
        
        def wrapper(*args):
            dataAvailable.wait()
            tempVar = self.tempVar
            del self.tempVar
            func(*args)
            return tempVar
        
        return wrapper
    
    def get_connected_client_object(self, func):

        self.clientObject = None
        clientObjectAvailable = threading.Event()

        @self.event
        @rename(func.__name__)
        def receivingLogic(Client):
            self.ursinaServer.lock.acquire()
            self.clientObject = Client
            clientObjectAvailable.set()
            self.ursinaServer.lock.release()

        def wrapper(*args):
            clientObjectAvailable.wait()
            clientObject = self.clientObject
            del self.clientObject
            func(*args)
            return clientObject
                
        return wrapper
    
    def start_ursina_server(self):
        self.ursinaServer = UrsinaNetworkingServer(*self.address)
        self.events_manager = self.ursinaServer.events_manager
        self.event = self.events_manager.event
        self.socket = self.ursinaServer.serverSocket

    def start_events_processing_thread(self):
        def process_net_events():
            while not self.shutdown.is_set():
                self.ursinaServer.process_net_events()
        self.processEventsThread = threading.Thread(target=process_net_events)
        self.processEventsThread.start()
    
    def send_message_to_client(self, Client_:UrsinaNetworkingConnectedClient, Message_, Content_):
        self.ursinaServer.lock.acquire()
        self.messages_to_send[Client_] = (Message_, Content_)        
        self.ursinaServer.lock.release()
    
    def start_sending_messages_thread(self):
        def messageSending():
            while not self.shutdown.is_set():
                if self.messages_to_send:
                    self.ursinaServer.lock.acquire()
                    for Client_ in self.messages_to_send:
                        arguments = self.messages_to_send[Client_]
                        Client_.send_message(*arguments)
                    self.messages_to_send.clear()
                    self.ursinaServer.lock.release()
        
        messagingThread = threading.Thread(target = messageSending)
        messagingThread.start()
    
    def stopServer(self):
        self.ursinaServer.shutdown.set()
        self.shutdown.set()

class AdvancedClient:
    def __init__(self, server_address) -> None:
        # stores messages to be sent to server as { Message_ : Content_ }
        self.messages_to_send = {}
        self.server_address = server_address
        # Keeps a tab on whether to keep the client running or not?
        self.shutdown = threading.Event()
    
    def receiver_event(self, func):
        """
        makes the function return the content of an event!
        """
        self.tempVar = None
        dataAvailable = threading.Event()
        
        @self.event
        @rename(func.__name__)
        def receivingLogic(Content):
            self.ursinaClient.lock.acquire()
            self.tempVar = Content
            dataAvailable.set()
            self.ursinaClient.lock.release()
        
        def wrapper(*args):
            dataAvailable.wait()
            tempVar = self.tempVar
            del self.tempVar
            func(*args)            
            return tempVar
        
        return wrapper
        

    def start_ursina_client(self):
        self.ursinaClient = UrsinaNetworkingClient(*self.server_address)
        
        self.ursinaClient.connected.wait()
        
        self.events_manager = self.ursinaClient.events_manager
        self.event = self.events_manager.event
        self.socket = self.ursinaClient.client
        self.address = self.ursinaClient.socketAddress
        
    def start_events_processing_thread(self):
        def process_net_events():
            while not self.shutdown.is_set():
                self.ursinaClient.process_net_events()
        self.processEventsThread = threading.Thread(target=process_net_events)
        self.processEventsThread.start()

    def start_sending_messages_thread(self):
        def messageSending():
            while not self.shutdown.is_set():
                if self.messages_to_send:
                    self.ursinaClient.lock.acquire()
                    for message,content in self.messages_to_send.items():
                        self.ursinaClient.send_message(message, content)
                    self.messages_to_send.clear()
                    self.ursinaClient.lock.release()
        messagingThread = threading.Thread(target = messageSending)
        messagingThread.start()

    def send_message_to_server(self, Message_: str, Content_):
        self.ursinaClient.lock.acquire()
        self.messages_to_send[Message_] = Content_
        self.ursinaClient.lock.release()

    def stopClient(self):
        self.ursinaClient.shutdown.set()
        self.shutdown.set()
        self.ursinaClient.clientSocket.close()    
