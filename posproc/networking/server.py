from uebn import UrsinaNetworkingServer, ursina_networking_log
import socket
import threading
class Server(UrsinaNetworkingServer):
    def __init__(self, Ip_, Port_):
        super().__init__(Ip_, Port_)
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.bind((Ip_, Port_))
            self.server.listen()
            self.receiveThread = threading.Thread(target=self.receive)
            self.receiveThread.start()

            ursina_networking_log("Server",
                                  "__init__", "Server started !")
            ursina_networking_log("Server",
                                  "__init__", f"Ip   :   {Ip_}")
            ursina_networking_log("Server",
                                  "__init__", f"Port :   {Port_}")

        except Exception as e:
            ursina_networking_log("UrsinaNetworkingServer",
                                  "__init__", f"Cannot create the server : {e}")
