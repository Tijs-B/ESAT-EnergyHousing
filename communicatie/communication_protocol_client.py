__author__ = 'Stef Jochems'
import time
import string
from norx_algorithm_4 import *
import random



class message:
    def __init__(self, data):
        self.sender = data[2:4]
        self.receiver = data[0:2]
        self.time = self.string_generator(int(time.time()), 1)
        self.info= data [4:]
        self.nonce=self.nonce_generator()
        self.key=['0x1293','0x128746','0x218976','0x12123']

    def nonce_generator(self):
        nonce=['','']
        nonce[0]=self.time+'1'
        for i in range(0,32):
            nonce[1]+=str(random.randint(0,1))
        return nonce



    def string_generator(self, item, length):
        format_value = '#0' + str(length) + 'b'

        trans=str(format(int(item), format_value)[2:])
        return trans

    def send(self):
        a = NORX(32,4,1,128)
        encrypted_message=a.AEADEnc( self.key,self.nonce,self.sender + self.receiver ,self.time+ self.info)
        encrypted_message=self.sender + self.receiver+self.nonce[0]+self.nonce[1]+encrypted_message[0]+encrypted_message[1]
        return encrypted_message

def receive(received_message):
    key=['0x1293','0x128746','0x218976','0x12123']
    receiver= received_message[2:4]
    sender=received_message[0:2]
    nonce=['r','s']
    nonce[0]=received_message[4:36]
    nonce[1]=received_message[36:68]
    b=NORX(32,4,1,128)

    decrypted_message=b.AEADDec(key,nonce, sender+receiver, received_message[68:452],received_message[452:])
    
    info=decrypted_message[31:]
    message=receiver+sender+info
    return message
    



