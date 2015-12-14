__author__ = 'Durt'
def geef_fl_benaderd(x, begin, eind, bits=7):
    if bits==2:
        print'aantal bits moet groter dan 2 zijn'
        return
    if eind<x or begin>x or eind<=begin:
        print 'fout met het interval'
        return
    #print ((2**(bits))-2)
    intervalgrootte=(float(eind)-float(begin))/((2**(bits))-2)
    #print intervalgrootte
    count=2
    cur_bound=begin+(intervalgrootte)
    while x>cur_bound:
        #print x
        count+=1
        cur_bound+=intervalgrootte
        #print cur_bound
    print 'count', count
    return count,cur_bound-intervalgrootte/2

def maak_benadering_weer(x, begin, einde, bits=7):
    intervalgrootte=float(einde-begin)/((2**(bits))-2)
    count=2
    result=begin+intervalgrootte/2
    #print 'begin while'
    while x>count:
        result += intervalgrootte
        #print result
        count += 1
    return result

#x=geef_fl_benaderd(23.5, -12, 23.5)
#print maak_benadering_weer(x[0], -12, 23.5)
#print x
