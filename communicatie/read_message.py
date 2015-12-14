__author__ = 'Durt'
def read_message(message):
    ontvanger=int(message[0:2],2)
    zender=int(message[2:4],2)
    toestel=int(message[4:9],2)
    status=int(message[9:16],2)
    return {'ontvanger':ontvanger, 'zender': zender, 'toestel': toestel,'status': status}
