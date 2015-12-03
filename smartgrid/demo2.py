__author__ = 'Vincent'

from NORX import *
from bitstring import *


def decrypt(hex_value, tag_value):
    hex_value = '0x' + hex_value
    message = BitArray(hex = hex_value).bin
    b = NORX(32,4,1,128)
    plain_bit = b.AEADDec(['0x1293','0x128746','0x218976','0x12123'],['0x127a','0x123c'],'010101010',message,tag_value,'10101101010')
    plain_hex = BitArray(bin=plain_bit).hex
    return plain_hex.decode('hex')

