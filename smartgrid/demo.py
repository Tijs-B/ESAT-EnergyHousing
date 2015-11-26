__author__ = 'Bert'
from NORX import *
from bitstring import *

def demo(string):
       hex_value = '0x' + string.encode('hex')
       message = BitArray(hex = hex_value).bin
       a = NORX(32,4,1,128)
       cipher_bit = a.AEADEnc(['0x1293','0x128746','0x218976','0x12123'],['0x127a','0x123c'],'010101010',message,'10101101010')
       cipher_hex = BitArray(bin=cipher_bit[0]).hex
       return cipher_hex.decode('hex')