__author__ = 'Kevin'

from Server_Test import *
#from benader_x import *
def make_binary(numb, bits):
    ### werkt enkele met gehele getallen###

    if not isinstance(numb, int):
        return None

    result= bin(numb)
    ln=len(result)

    result= result[2:ln]
    ln=len(result)

    while ln< bits:
        result= '0'+result
        ln= ln+1

    if ln == bits:
        return result

    else:
        return None

def Make_message(ontvanger, toestel, status, zender=0):
    #ontvanger=check_name(ontvanger, adressenboek)
    #zender= check_name(zender,adressenboek)

    return make_binary(ontvanger, 2)+make_binary(zender,2)+make_binary(toestel,4)+ \
            make_binary(status,8)






def verstuur(planning):

    for i in range(0,len(planning)):

            #if planning[i][2] == 0 or planning[i][2] == 1:
        boodschap = str(Make_message(planning[i][0],planning[i][1],planning[i][2]))
        S.send(boodschap)
            #else:
                #benaderd = geef_fl_benaderd(planning[2], 15, 25, bits=8)
                #boodschap = str(Make_message(planning[i][0],planning[i][1],benaderd))
                #S.send(boodschap)



