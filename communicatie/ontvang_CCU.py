__author__ = 'Durt'
#from smartgrid.models import *
from read_message import*
from benader_x import *

def ontvang_CCU(bericht):

    boodschap= read_message(bericht)

    if boodschap['zender']==2:
        print maak_benadering_weer(boodschap['status'], 1, 1023)

