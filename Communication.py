import socket
from thread import *
# from huis1 import *
class Client():
    def __init__ (self, Adress=('169.254.158.9',7000)):
        self.s=socket.socket()
        self.s.connect(Adress)
        self.s.send('01')
        start_new_thread(self.receive,())
        print self.s.recv(1024)
    def send(self, str):
        self.s.send(str)
        
    """
    def receive(self):
        print 'listening'
        while True:
            data = self.s.recv(1024)
            uitvoeren(data)
    """
print 'imported!'

