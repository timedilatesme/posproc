import socket
"""
This module contains code for active client who is going to be doing all the computation.
In theory we consider bob to be the active client who asks question to alice about parity
and Alice is an passive user who is just going to reply to all the questions that bob
asks.
"""


class Client(socket.socket):
    def __init__(self, **kwargs, 
                 server_address=(LOCAL_IP, LOCAL_PORT)):
        super().__init__()
        self.parity_dict = {}
        self.parity_msgs_sent = 0
        self.server_address = server_address
        #self.__setattr__("address",None)
        self.connect(self.server_address)
        self.connected = True

        #rthread = threading.Thread(target=self.receive_from_server)
        #wthread = threading.Thread(target=self.write_to_server)
        #rthread.start()
        #wthread.start()

    def ask_for_parity_from_server(self, indexes: list):
        self.parity_msgs_sent += 1
        msg_no = self.parity_msgs_sent

        def asking(indexes):
            indexes = str(indexes)
            indexes = indexes[1:-1]
            self.send_a_message_to_server(f"ask_parity:{msg_no}:{indexes}")

        def receiving():
            while True:
                msg_recvd = self.receive_a_message_from_server()

                if msg_recvd:
                    if msg_recvd.startswith("ask_parity"):

                        splitted_msg_recvd = msg_recvd.split(":")

                        def exists_in_parity_dict(msg_no):
                            parity = self.parity_dict.get(f"{msg_no}")
                            if parity == None:
                                return False
                            else:
                                return True

                        msg_no_returned = int(splitted_msg_recvd[1])
                        parity = int(splitted_msg_recvd[2])

                        if msg_no_returned == msg_no:
                            return parity
                        elif exists_in_parity_dict(msg_no):
                            parity = self.parity_dict.get(f"{msg_no}")
                            self.parity_dict.pop(f"{msg_no}")
                            return parity
                        else:
                            self.parity_dict.add(f"{msg_no_returned}", parity)

        '''athread = threading.Thread(target=asking, args=(indexes,))
        rthread = threading.Thread(target=receiving)
        athread.start()
        rthread.start()'''

        asking(indexes)
        parity = receiving()

        return parity

    def receive_a_message_from_server(self):
        msg_length = self.recv(HEADER).decode(FORMAT)
        if msg_length:
            try:
                msg_length = int(msg_length)
                message = self.recv(int(msg_length)).decode(FORMAT)
                return message
            except:
                if msg_length == ' ':
                    print("Invalid Literal for int")

    def send_a_message_to_server(self, message):
        msg_length = len(message)
        send_length = str(msg_length)
        send_length += " "*(HEADER - len(send_length))
        self.send(send_length.encode(FORMAT))
        self.send(message.encode(FORMAT))

    def receive_from_server(self):
        connected = True
        while connected:
            msg_received = self.receive_a_message_from_server()
            print(f"[SERVER]: {msg_received}")

    def write_to_server(self):
        connected = True
        while connected:
            msg_to_send = input("Enter your indexes: ")
            indexes_o = msg_to_send
            indexes_o = indexes_o.split(",")
            indexes = []
            for i in indexes_o:
                indexes.append(int(i))
            if msg_to_send == "disconnect":
                connected = False
            else:
                self.ask_for_parity_from_server(indexes)
        self.close()

class ActiveClient:
    def __init__(self) -> None:
        pass
    
