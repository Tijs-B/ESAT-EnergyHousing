from bitstring import *

class NORX():
    def __init__(self,wordlength,number_of_rounds,parallellism,tagsize):
        """Creates a NORX instance given the correct wordlength,number_of_rounds,parallellism and tagsize.
        Currently only the instance featuring a wordlength of 32bit, 4 rounds, a parallellism degree of 1 and
        a tagsize of 4*wordlength is available."""
#        assert(wordlength == 32)

        self.r = [8,11,16,31]
        u = [
            [ '0x243f6a88', '0x0', '0x0', '0x85a308d3' ],
            [ '0x0', '0x0', '0x0', '0x0' ],
            [ '0x13198a2e', '0x03707344', '0x254f537a', '0x38531d48' ],
            [ '0x839c6e83', '0xf97a3ae5', '0x8c91d88c', '0x11eafb59' ]]

        self.u = [[self.bitarray_creator(u[i][k]) for k in range(4)] for i in range(4)]


        self.wordlength = self.bitarray_creator(str(hex(wordlength)))
        self.number_of_rounds = self.bitarray_creator(str(hex(number_of_rounds)))
        self.parallellism = self.bitarray_creator(str(hex(parallellism)))
        self.tagsize = self.bitarray_creator(str(hex(tagsize)))

    def AEADEnc(self, key, nonce, header, message, trailer = '0101001101110100011001010110011001101011011001010111001100100000011100110111010001110010011000010110011001100110011001010010000001101011011011110111001101110100'):
        """This is the high level encryption function, which takes several inputs and generates an encrypted message,
        aswell as a tag"""
        self.initialize(key, nonce)
        self.absorb(header, '0x1')
        ciphertext = self.encrypt(message, '0x2')
        self.absorb(trailer,'0x4')
        tag = self.finalise('0x8')
        return ciphertext, tag


    def AEADDec(self, key, nonce, header, ciphertext,tag1, trailer = '0101001101110100011001010110011001101011011001010111001100100000011100110111010001110010011000010110011001100110011001010010000001101011011011110111001101110100'):
        """This is the high level decryption function, which takes several inputs and generates an encrypted message
        """
        self.initialize(key, nonce)
        self.absorb(header, '0x1')
        message = self.decrypt(ciphertext, '0x2')
        self.absorb(trailer,'0x4')
        tag2 = self.finalise('0x8')
        if tag1 == tag2:
            return message
        else:
            assert(False)

    def get_state(self):
        return self.u

    def write_state(self,state):
        self.u = state


    def initialize(self, key, nonce):
        temp_state  = self.get_state()
        assert isinstance(nonce, list)
        assert(len(nonce)== 2)
        assert isinstance(key, list)
        assert(len(key) == 4)

        temp_state[0][1] = self.bitarray_creator(nonce[0])
        temp_state[0][2] = self.bitarray_creator(nonce[1])
        for i in range(4):
            temp_state[1][i] = self.bitarray_creator(key[i])
        temp_state[3][0] ^= self.wordlength
        temp_state[3][1] ^= self.number_of_rounds
        temp_state[3][2] ^= self.parallellism
        temp_state[3][3] ^= self.tagsize

        self.write_state(temp_state)

    def rate_converter(self,bitstring):


        remainder= 384 - len(bitstring)%384

        if remainder != 384:
            bitstring += '1' + (remainder-2)*'0' + '1'


        bitlist = [self.bitarray_creator(bitstring[i:i+32]) for i in range(0, len(bitstring), 32)]
        u = [bitlist[i:i+12] for i in range(0,len(bitlist),12)]
        return [[u[j][l:l+4] for l in range(0,9,4)] for j in range(len(u))]
  #      return [bitlist[i:i+12] for i in range(0,len(bitlist),12)]


    def absorb(self,ad,dsc):
        temp_state = self.get_state()


        adata = self.rate_converter(ad)
        for h in adata:

            temp_state[3][3] = temp_state[3][3]^ self.bitarray_creator(dsc)

            for k in range(self.number_of_rounds.int):
                self.F()

            temp_state = self.get_state()
            zero_string = [[self.bitarray_creator('0x0') for i in range(4)]]
            for j  in range(4):
                for k  in range(4):
                    temp_state[j][k] = temp_state[j][k] ^ (h + zero_string)[j][k]
        self.write_state(temp_state)

    def bitarray_creator(self,string):
        #if len(string) < 2 or
        if string[:2] != '0x':
            string = '0b' + string
        b = BitArray(string)
        return BitArray([0]*(32-len(b.bin)) + b)

    def binstring_creator(self,text):
        binstring = ''
        for i in text:
            binstring += i.bin
        return binstring

    def encrypt(self,message,dsc):

        message = self.bitarray_creator(bin(len(message))).bin + message

        temp_state = self.get_state()
        message = self.rate_converter(message)
        ciphertext = []
        for element in message:
            temp_state[3][3] = temp_state[3][3] ^ self.bitarray_creator(dsc)
            for k in range(self.number_of_rounds.int):
                self.F()

            temp_state = self.get_state()
            temp_cipher = []
            for j in range(3):
                for k in range(4):
                    temp_cipher += [temp_state[j][k] ^ element[j][k]]
            temp_state = [temp_cipher[0:4],temp_cipher[4:8],temp_cipher[8:12],temp_state[3]]
            ciphertext += temp_cipher

        self.write_state(temp_state)
        return self.binstring_creator(ciphertext)

    def decrypt(self,ciphertext,dsc):
        temp_state = self.get_state()
        ciphertext = self.rate_converter(ciphertext)
        message = []
        for element in ciphertext:
            temp_state[3][3] = temp_state[3][3] ^ self.bitarray_creator(dsc)
            for k in range(self.number_of_rounds.int):
                self.F()

            temp_state = self.get_state()
            temp_message = []
            for j in range(3):
                for k in range(4):
                    temp_message += [temp_state[j][k] ^ element[j][k]]


            temp_state = [element[0],element[1],element[2],temp_state[3]]

            message += temp_message

        self.write_state(temp_state)
        message = self.binstring_creator(message)
        length = int(message[0:32],2)
        message = message[32:32+length]
        return message


    def finalise(self,dsc):
        temp_state = self.get_state()
        temp_state[3][3] = temp_state[3][3] ^ self.bitarray_creator(dsc)
        for k in range(2):
            for i in range(self.number_of_rounds.int):
                self.F()

        temp_state = self.get_state()
        tag = temp_state[0]
        self.write_state(temp_state)
        return tag


    def F(self):
        temp_state = self.get_state()

        assert ((len(temp_state) == 4) and (len(temp_state[0]) == 4))

        for i in range(4):
            inputs = []
            for j in range(4):
                inputs += [temp_state[j][i]]
            output = self.G(inputs)
            for k in range(4):
                temp_state[k][i] = output[k]



        x = [0,1,2,3]
        y = [[0,1,2,3],[1,2,3,0],[2,3,0,1],[3,0,1,2]]
        for i in range(4):
            inputs = []
            for j in range(4):
                inputs += [temp_state[x[j]][y[i][j]]]
            output = self.G(inputs)
            for k in range(4):
                temp_state[x[k]][y[i][k]] = output[k]

        self.write_state(temp_state)


    def G(self,input):
        for i in range(2):
            input[0] = self.H(input[0], input[1])
            input[3] = self.rotr(input[3] ^ input[0], self.r[i*2])
            input[2] = self.H(input[2], input[3])
            input[1] = self.rotr(input[1] ^ input[2], self.r[(i*2)+1])
            return input

    def H(self, x, y):
        return (x ^ y) ^ ((x & y) << 1)

    def rotr(self, x, n):
        """Bitwise right rotate, taking into account the
		   configured word size."""
        mask = (1 << n) - 1
        mask = self.bitarray_creator(str(bin(mask)))
        return (x >> n) | ((x & mask) << (32 - n))



d = NORX(32,4,1,128)
print d.AEADEnc(['0x1293','0x128746','0x218976','0x12123'],['0x127a','0x123c'],'010101010','1111111010100101011101010101010111')

e = NORX(32,4,1,128)
print e.AEADDec(['0x1293','0x128746','0x218976','0x12123'],['0x127a','0x123c'],'010101010','100000001000101000010001001110100100111110000100010100100110110110011010011100011101110000110001011001111001101100100111101111010100111011111110101001010011011101110110010001101010010100101110100101000001101001110110111101001010101111100110100000111011111101111111111010001010111101000000111010111010001010101110011100111010100111100100110001111111011100110010100000101011111010000110',[BitArray('0xe5276417'), BitArray('0x08ada135'), BitArray('0x8ad3ebc9'), BitArray('0xaf9aa20c')])