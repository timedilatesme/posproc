import secrets
from posproc.networking.uebn import AdvancedServer, console_output

ADDR = ('127.0.0.1', 12345)

s = AdvancedServer(ADDR)


class DataObject:
    def __init__(self) -> None:
        self.data = secrets.token_bytes(5)

@s.event
def requestData(Client, Content):
    dent = DataObject()
    Client.send_message('receiveData', dent)
    print('Data Sent :', dent.data)
    
@s.event
def onClientConnected(Client):
    print(f'Client @ {Client.address} is here!')

s.start_ursina_server()
s.start_events_processing_thread()