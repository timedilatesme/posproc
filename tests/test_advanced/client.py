from posproc.networking.uebn import AdvancedClient
ADDR = ('127.0.0.1', 12345)
import secrets

class DataObject:
    def __init__(self) -> None:
        self.data = secrets.token_bytes(5)

# python -m client

c = AdvancedClient(ADDR)

c.start_ursina_client()
c.start_events_processing_thread()
c.send_message_to_server('requestData','')

@c.receiver_event
def receiveData():
    pass

data = receiveData()

print('Data Recvd: ', data.data)



c.stopClient()

