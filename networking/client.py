from networking.node import Node



class Client(Node):
    def __init__(self, server_address=(LOCAL_IP, LOCAL_PORT)):
        super().__init__()
        self.parity_dict = {}
        self.parity_msgs_sent = 0
        self.server_address = server_address
        #self.__setattr__("address",None)
        self.connect(self.server_address)
        self.connected = True

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
        asking(indexes)
        parity = receiving()

        return parity

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
