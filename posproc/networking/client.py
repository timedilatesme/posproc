from posproc.key import Key
from posproc.networking.node import Node
from posproc import constants
import pickle
from posproc.error_correction.cascade.block import Block

class Client(Node):
    def __init__(self, username, incorrect_key:Key,server_address=(constants.LOCAL_IP, constants.LOCAL_PORT)):
        #TODO: Convert args to kwargs for easy implementation.
        super().__init__(username)
        
        self.__incorrect_key = incorrect_key
        #TODO: Add authentication protocol for when a new client connects.
        self.parity_dict = {}
        self.ask_parities_msgs_sent = 0
        self.server_address = server_address
        self.connect(self.server_address)
        self.connected = True
        
    def ask_parities(self, blocks):
        """
        Sends blocks as bytes to the server and then the server
        replies with the appropriate parities of the blocks asked.

        Args:
            blocks (list(Block)): Contains all the blocks whose parity is to be asked.

        Returns:
            parities (list(int)): Contains parities in the same order as the blocks in blocks.
        """
        # Only send the indexes for parity.
        blocks_indexes = [block.get_key_indexes() for block in blocks]
        # TODO: add tracking of parity messages.
        msg_to_send = b'ask_parities' + b':' + pickle.dumps(blocks_indexes)
        
        # asking:
        self.send_a_message_to_the_server(msg_to_send)
        
        # receiving:
        while True:
            msg_recvd = self.receive_a_message_from_server()
            
            if msg_recvd:
                if msg_recvd.startswith("ask_parities".encode(constants.FORMAT)):
                    splitted_msg_recvd = msg_recvd.split(":".encode(constants.FORMAT))
                    parities = pickle.loads(splitted_msg_recvd[-1])
                    return parities                          


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
            print(f"[SERVER @ {self.server_address}]: {msg_received}")

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
