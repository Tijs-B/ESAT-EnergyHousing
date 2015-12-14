from bitstring import *

class NORX():
    def __init__(self,wordlength = 32,number_of_rounds = 4,parallellism = 1,tagsize =128):
        """
        Creates a NORX instance given the correct wordlength,number_of_rounds,parallellism and tagsize.
        In this implementation only NORX(32,x,1,128) can be created with x a natural number
        """
        if wordlength != 32:
            print 'The wordlength must be 32.'
            assert False
        if parallellism != 1:
            print 'The parallellism degree must be 1.'
            assert False
        if tagsize != 128:
            print 'The tagsize must be four times the wordlength, i.e. 128 bits.'
            assert False


        self.__r_list = [8,11,16,31]
        u = [
            [ '0x243f6a88', '0x0', '0x0', '0x85a308d3' ],
            [ '0x0', '0x0', '0x0', '0x0' ],
            [ '0x13198a2e', '0x03707344', '0x254f537a', '0x38531d48' ],
            [ '0x839c6e83', '0xf97a3ae5', '0x8c91d88c', '0x11eafb59' ]]

        self.__state_matrix = [[self.bitarray_creator(u[i][k]) for k in range(4)] for i in range(4)]


        self.__wordlength = self.bitarray_creator(str(hex(wordlength)))
        self.__number_of_rounds = self.bitarray_creator(str(hex(number_of_rounds)))
        self.__parallellism = self.bitarray_creator(str(hex(parallellism)))
        self.__tagsize = self.bitarray_creator(str(hex(tagsize)))

    def AEADEnc(self, key = None, nonce = None, header = None, message = None, trailer = '0101001101110100011001010110011001101011011001010111001100100000011100110111010001110010011000010110011001100110011001010010000001101011011011110111001101110100'):
        """
        This is the high level encryption method that generates a ciphertext and a tag given the correct inputs.
        :param key: a list of length four with strings of hexadecimal numbers as elements,
        e.g. ['0x1c89','0x1a89','0x1989','0x1129'].
        :param nonce: a list of length two with strings ofr hexqdecimql numbers as elements,
        e.g. ['0x1c89','0x1a89'].
        :param header: a binary string, e.g. '010111'.
        :param message: a binary string, e.g. '010111'.
        :param trailer: a binary string, e.g. '010111'.
        :return: a tuple of ciphertext and tag, e.g. ('0011010','0110')
        """

        if not isinstance(header,basestring) \
                or not isinstance(message,basestring) or not isinstance(trailer,basestring):
            print "An error has occurred due to invalid input."
            assert False

        self.initialize(key, nonce)
        self.absorb(header, '0x1')
        ciphertext = self.encrypt(message, '0x2')
        self.absorb(trailer,'0x4')
        tag = self.binstring_creator(self.finalise('0x8'))

        return ciphertext, tag


    def AEADDec(self, key = None, nonce = None, header = None, ciphertext = None, tag1 = None, trailer = '0101001101110100011001010110011001101011011001010111001100100000011100110111010001110010011000010110011001100110011001010010000001101011011011110111001101110100'):
        """
        This is the high level decryption function which generates a decrypted message given the correct inputs.
        :param key: a list of length two with strings ofr hexadecimal numbers as elements,
        e.g. ['0x1c89','0x1a89','0x1a89','0x1a89'].
        :param nonce: a list of length two with strings ofr hexadecimal numbers as elements,
        e.g. ['0x1c89','0x1a89'].
        :param header: a binary string, e.g. '010111'.
        :param ciphertext:a binary string of length 384 or a multiple of 384.
        :param tag1: a binary string of length 128.
        :param trailer: a binary string, e.g. '010111'.
        :return:
        """

        if not isinstance(header,basestring) or not isinstance(ciphertext,basestring) \
                or not isinstance(trailer,basestring) or not isinstance(tag1,basestring):
            print "An error has occurred due to invalid input."
            assert False

        self.initialize(key, nonce)
        self.absorb(header, '0x1')
        message = self.decrypt(ciphertext, '0x2')
        self.absorb(trailer,'0x4')
        tag2 = self.binstring_creator(self.finalise('0x8'))

        if tag1 == tag2:
            return message
        else:
            assert(False)

    def get_state(self):
        """
        Fetches the current state of the encryption matrix.
        """
        return map(list,self.__state_matrix)

    def write_state(self,state):
        """
        Overwrites the state of the encryption matrix, given a matrix
        """
        self.__state_matrix  = state


    def initialize(self, key, nonce):
        """
        Initializes the matrix given a key and nonce of the correct shape.
        """
        temp_state  = self.get_state()

        if not isinstance(key,list) or not (len(key) == 4):
            print 'Key type or length is invalid.'
            assert False
        for i in key:
            if i[:2] != '0x':
                print 'Key input is invalid.'
                assert False
        if not isinstance(nonce,list) or  not (len(nonce) == 2) or not ((k[:2] == '0x') for k in nonce):
            print 'Nonce type or length is invalid.'
            assert False

        temp_state[0][1] = self.bitarray_creator(nonce[0])
        temp_state[0][2] = self.bitarray_creator(nonce[1])
        for i in range(4):
            temp_state[1][i] = self.bitarray_creator(key[i])
        temp_state[3][0] ^= self.__wordlength
        temp_state[3][1] ^= self.__number_of_rounds
        temp_state[3][2] ^= self.__parallellism
        temp_state[3][3] ^= self.__tagsize

        self.write_state(temp_state)

    def rate_converter(self,bitstring):
        """
        Turns the given bitstring into a workable object for the algorithm.
        A brief overview:
            - Pads the bitstring to a multiple of 384.
            - Splits the bitstring into bitarray objects of binary length 32.
            - Creates a 3x4 matrix with the words as elements.
        """

        remainder = 384 - len(bitstring)%384

        if remainder != 384:
            bitstring += '1' + (remainder-2)*'0' + '1'

        bitlist = [self.bitarray_creator(bitstring[i:i+32]) for i in range(0, len(bitstring), 32)]
        u = [bitlist[i:i+12] for i in range(0,len(bitlist),12)]
        return [[u[j][l:l+4] for l in range(0,9,4)] for j in range(len(u))]



    def absorb(self,ad,dsc):
        """
        Absorbs the header or trailer into the encryption matrix as part of the NORX algorithm.
        """
        adata = self.rate_converter(ad)
        temp_state = self.get_state()

        for h in adata:

            temp_state[3][3] = temp_state[3][3]^ self.bitarray_creator(dsc)
            for k in range(self.__number_of_rounds.int):
                temp_state = self.F(temp_state)

            zero_string = [[self.bitarray_creator('0x0') for i in range(4)]]
            for j  in range(4):
                for k  in range(4):
                    temp_state[j][k] = temp_state[j][k] ^ (h + zero_string)[j][k]

        self.write_state(temp_state)

    def bitarray_creator(self,string):
        """
        Creates a bitarray object of length 32 in binary given a hexadecimal number or a bitstring.
        """
        if string[:2] != '0x':
            string = '0b' + string
        b = BitArray(string)
        return BitArray([0]*(32-len(b.bin)) + b)

    def binstring_creator(self,text):
        """
        Creates a bitstring given a list of bitarray objects.
        """
        binstring = ''
        for i in text:
            binstring += i.bin
        return binstring

    def encrypt(self,message,dsc):
        """
        Absorbs the message into the encryption matrix and generates the ciphertext, as part of a the NORX algorithm.
        """
        temp_state = self.get_state()
        message = self.bitarray_creator(bin(len(message))).bin + message
        message = self.rate_converter(message)
        ciphertext = []
        for element in message:

            temp_state[3][3] = temp_state[3][3] ^ self.bitarray_creator(dsc)

            for k in range(self.__number_of_rounds.int):
                temp_state = self.F(temp_state)

            temp_cipher = []
            for j in range(3):
                for k in range(4):
                    temp_cipher += [temp_state[j][k] ^ element[j][k]]
            temp_state = [temp_cipher[0:4],temp_cipher[4:8],temp_cipher[8:12],temp_state[3]]
            ciphertext += temp_cipher

        self.write_state(temp_state)
        return self.binstring_creator(ciphertext)

    def decrypt(self,ciphertext,dsc):
        """
        Absorbs the ciphertext into the encryption matrix and generates the original message,
        as part of a the NORX algorithm.
        """
        temp_state = self.get_state()
        ciphertext = self.rate_converter(ciphertext)
        message = []
        for element in ciphertext:
            temp_state[3][3] = temp_state[3][3] ^ self.bitarray_creator(dsc)
            for k in range(self.__number_of_rounds.int):
                temp_state = self.F(temp_state)

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
        """
        Generates the tag, as part of the NORX algorithm.
        """
        temp_state = self.get_state()
        temp_state[3][3] = temp_state[3][3] ^ self.bitarray_creator(dsc)
        for k in range(2):
            for i in range(self.__number_of_rounds.int):
                temp_state = self.F(temp_state)

        tag = temp_state[0]
        self.write_state(temp_state)
        return tag


    def F(self,temp_state):
        """
        Applies several transformations on the encryption matrix, as part of the NORX algorithm.
        """
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

        return temp_state


    def G(self,input):
        """
        Applies several transformations on a list of bitarray objects, as part of the NORX algorithm.
        """
        for i in range(2):
            input[0] = self.H(input[0], input[1])
            input[3] = self.rotr(input[3] ^ input[0], self.__r_list[i*2])
            input[2] = self.H(input[2], input[3])
            input[1] = self.rotr(input[1] ^ input[2], self.__r_list[(i*2)+1])
            return input

    def H(self, x, y):
        """
        A fundamental bitwise operation of the NORX algorithm. Returns a bitarray object given two bitarray objects.
        """
        return (x ^ y) ^ ((x & y) << 1)

    def rotr(self, x, n):
        """
        Bitwise right rotate, as part of the NORX algorithm.
        """
        mask = (1 << n) - 1
        mask = self.bitarray_creator(str(bin(mask)))
        return (x >> n) | ((x & mask) << (32 - n))
