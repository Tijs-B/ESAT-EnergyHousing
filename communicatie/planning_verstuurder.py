__author__ = 'Kevin'

from Server_Test import *
from benader_x import *

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

    return make_binary(ontvanger, 2)+make_binary(zender,2)+make_binary(toestel,5)+ \
            make_binary(status,7)





#intervallen_toestellen = {"5":[20,25]}
#Key: pin toestel
#1ste positie value: beginwaarde interval
#2de positie: eindewaarde interval





def verstuur(planning):
#Verstuurt een voor een de gegevens door van de planning uit de database.
# Deze planning bestaat uit een lijst met daarin nog eens lijsten.
# Deze lijsten bevatten drie elementen
# de ontvanger, het toestel en de waarde.

    boodschap_huis_1 = ""
    boodschap_huis_2 = ""
    for i in range(0,len(planning)):

        ontvanger = planning[i][0]
        toestel = planning[i][2]
        waarde = planning[i][1]

        #Als de waarde een 0 een 1 of een 2 is, moet er enkel iets af of aan gezet worden

        #if waarde == 0 or waarde == 1 or waarde == 2:

        if ontvanger == 0:
            boodschap_huis_1 += str(Make_message(ontvanger,toestel,waarde))[4:]
        elif ontvanger == 1:
            boodschap_huis_2 += str(Make_message(ontvanger,toestel,waarde))[4:]



        # Anders zal er een waarde worden doorgezonden
        # Er wordt een benadering gemaakt van de waarde
        # Het deelinterval waar deze waarde in ligt (geheel getal)
        # zal worden verzonden. Met deze informatie kan in het huis
        # een benaderende waarde worden geconstrueerd

        #else:

            #interval = intervallen_toestellen[str(toestel)]
            #benaderd = geef_fl_benaderd(waarde, interval[0] , interval[1], bits=7)[0]
            #boodschap = str(Make_message(ontvanger,toestel,benaderd))

            #S.send(boodschap)

    boodschap_huis_1 = "0100" + boodschap_huis_1
    boodschap_huis_2 = "1000" + boodschap_huis_2

    S.send(boodschap_huis_1)
    S.send(boodschap_huis_2)


#planning = [[1,2,2],[0,2,2],[1,6,1],[0,6,0],[1,7,1],[1,5,24]]
#verstuur(planning)
