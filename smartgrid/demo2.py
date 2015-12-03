__author__ = 'Vincent'
import time
from NORX import *


def decrypt(hex_value, tag_value, nonce):
    print nonce
    print isinstance(nonce,list)
    hex_value = '0x' + hex_value
    message = BitArray(hex = hex_value).bin
    print len(message), message
    b = NORX(32,4,1,128)
    plain_bit = b.AEADDec(['0x1293','0x128746','0x218976','0x12123'],nonce,'010101010',message,tag_value,'10101101010')
    print len(plain_bit), plain_bit
    plain_hex = BitArray(bin=plain_bit).hex
    return plain_hex.decode('hex')

# a = time.time()
# print decrypt('abe926bc2dc8b2158410cd0c4c6f79ac6eadadb40de6d578fa8be79e024d317253c883910471bf43852746f03b23d4fb','00010011010100110100000110000110100110101101110110111011001100001010101001010111110101100011001000001001111001011000001000011001', ['10101100110000001101101011010001', '01111110110011010011011100100100'])
#
# b = time.time()
# print a
# print b-a
# c = NORX(32,4,1,128)
# d = c.AEADDec(['0x1293','0x128746','0x218976','0x12123'],['0x127a','0x123c'],'010101010',BitArray(hex = '0x808a1130d9404b5415f1dc31679b27bd4efea5377646a52e941a76f4abe683bf7fe8af40eba2ae73a9e4c7f73282be86').bin,'10101101010',[BitArray('0xfa3cb297'), BitArray('0x3c645600'), BitArray('0x0ff0fb25'), BitArray('0x4749b292')])
# print d