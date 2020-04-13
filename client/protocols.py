# -*- coding: utf-8 -*-
import sys
sys.path.append("..")


from FRP import FRPConect,FRPSend,FRPRcv

def DNS(url,token): #Protocole pour dns : envoie d'une requete avec l'ul+token et reception de l'ip+repertoire
    s = FRPConect("localhost",23486)
    FRPSend(s,{'url' : url.encode(),'token': token})
    rcv = FRPRcv(s)
    s.close()
    return rcv
        
def get(url,directory,token): 
    s = FRPConect(url,12801)
    FRPSend(s,{'directory' : directory, 'token': token})
    rcv = FRPRcv(s)
    s.close()
    return rcv
