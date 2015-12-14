k__author__ = 'Bert'

import socket
import sys
from thread import *
from communication_protocol import *
from ontvang_CCU import *

HOST = ''
PORT = 7000
class Server():
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print "Socket created!"

        #Bind socket to host and port
        try:
            self.s.bind((HOST, PORT))
        except socket.error , msg:
            print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
            sys.exit()

        print "Socket bind succesfull!"

        #Start socket listening
        self.s.listen(10)
        print 'Socket now listening!'
        self.connections = {}
        start_new_thread(self.wait_for_connection,())



    def wait_for_connection(self):
        while 1:
            conn, addr = self.s.accept()
            print 'Connected with ' + addr[0] + ':' + str(addr[1])
            house_id = conn.recv(1024)
            self.connections[house_id]=conn
            start_new_thread(self.recv_clientthread ,(conn,))

        self.s.close()

    def recv_clientthread(self, conn):
    #Sending message to connected client

        conn.send('Connection established!')

        #infinite loop so that function do not terminate and thread do not end.
        while True:

            #Receiving from client
            data = conn.recv(1024)
            if data == 'STOP':
                break
            print receive(data)
            ontvang_CCU(receive(data))

            reply = 'OK!'
            #conn.sendall(reply)

        #came out of loop
        conn.close()
    def send(self, msg):
        house_address = self.connections[msg[0:2]]
        data = message(msg)
        data = data.send()
        house_address.send(data)

S=Server()
