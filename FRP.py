# -*- coding: utf-8 -*-
#Protoles FRP (Friend request protocol)
import socket
import pickle

HEADERSIZE = 10

#Connection à un serveur
def FRPConect(ip,port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    return s

#Envoie de données data par un socket s
def FRPSend(s,data):
    msg = pickle.dumps(data)
    msg = bytes(f"{len(msg):<{HEADERSIZE}}", 'utf-8')+msg
    s.send(msg)
    return msg    

#Receptions de données par un socket s
def FRPRcv(s):
    full_msg = b''
    new_msg = True
    while True:
        msg = s.recv(1024)
        if msg != '' and msg != b'':
            if new_msg:
                msglen = int(msg[:HEADERSIZE])
                new_msg = False    

            full_msg += msg


            if len(full_msg)-HEADERSIZE == msglen:
                loaded = pickle.loads(full_msg[HEADERSIZE:])
                break
    return loaded
