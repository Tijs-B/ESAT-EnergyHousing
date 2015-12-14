import socket
import sys
from thread import *
from communication_protocol_client import *
#from Programma_Huis_met_zonwind import *
from bestuur import Bestuur

class Client():
    def __init__ (self, config_file,  Adress=('169.254.237.43',7000)):        
        self.bestuur = Bestuur(client=self, config_file=config_file)
        print 'Initialized bestuur' 
        self.s=socket.socket()
        self.s.connect(Adress)
        self.s.send('01')
        start_new_thread(self.receive,())
        print self.s.recv(1024)
        
    def send(self, str):
        data = message(str)
        data = data.send()
        self.s.send(data)
        
    def receive(self):
        print 'listening'
        while True: 
            data = self.s.recv(1024)
            data=receive(data)
            print data
            self.bestuur.uitvoeren(data)
            #uitvoeren(data)
            


if __name__ == '__main__':
    print sys.argv
    Huis=Client(config_file=sys.argv[1])

