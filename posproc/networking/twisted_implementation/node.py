from twisted.internet import reactor
from twisted.protocols.basic import NetstringReceiver
from posproc import constants
from twisted.internet.protocol import ServerFactory, ClientFactory

class CommunicationProtocol(NetstringReceiver):
    MAX_LENGTH = constants.MAX_DATA_LENGTH
