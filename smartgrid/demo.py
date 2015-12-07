__author__ = 'Bert'
import random
import time
from NORX import *

def demo(string):
       hex_value = '0x' + string.encode('hex')
       message = BitArray(hex = hex_value).bin
       a = NORX(32,4,1,128)
       nonce = nonce_generator()
       cipher_bit = a.AEADEnc(['0x1293','0x128746','0x218976','0x12123'],nonce,'010101010',message,'10101101010')
       cipher_hex = BitArray(bin=cipher_bit[0]).hex
       return cipher_hex, cipher_bit[1], nonce


def nonce_generator():
        nonce=['','']
        nonce[0]= string_generator(int(time.time()),32)+'1'
        for i in range(0,32):
            nonce[1]+=str(random.randint(0,1))
        return nonce

def string_generator(item, length):
        format_value = '#0' + str(length) + 'b'

        trans=str(format(int(item), format_value)[2:])
        return trans
