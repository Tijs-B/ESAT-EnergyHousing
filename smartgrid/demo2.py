__author__ = 'Vincent'

from NORX import *
from bitstring import *

def decrypt(hex_value, tag_value):
    hex_value = '0x' + hex_value
    message = BitArray(hex = hex_value).bin
    b = NORX(32,4,1,128)
    plain_bit = b.AEADDec(['0x1293','0x128746','0x218976','0x12123'],['0x127a','0x123c'],'010101010',message,'10101101010',tag_value)
    plain_hex = BitArray(bin=plain_bit[0]).hex
    return plain_hex.decode('hex')


#print decrypt('0x808a1130d9404b5415f1dc31679b27bd4efea5377646a52e941a76f4abe683bf7fe8af40eba2ae73a9e4c7f73282be86',"[BitArray('0xfa3cb297'), BitArray('0x3c645600'), BitArray('0x0ff0fb25'), BitArray('0x4749b292')]")
#
# c = NORX(32,4,1,128)
# d = c.AEADDec(['0x1293','0x128746','0x218976','0x12123'],['0x127a','0x123c'],'010101010',BitArray(hex = '0x808a1130d9404b5415f1dc31679b27bd4efea5377646a52e941a76f4abe683bf7fe8af40eba2ae73a9e4c7f73282be86').bin,'10101101010',[BitArray('0xfa3cb297'), BitArray('0x3c645600'), BitArray('0x0ff0fb25'), BitArray('0x4749b292')])
# print d