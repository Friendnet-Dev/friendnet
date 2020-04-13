# -*- coding: utf-8 -*-

import socket
import pickle

HEADERSIZE = 10


def FRP(ip,port,data):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    
    full_msg = b''
    new_msg = True
    msg = pickle.dumps(data)
    msg = bytes(f"{len(msg):<{HEADERSIZE}}", 'utf-8')+msg
    s.send(msg)
    while True:
        msg = s.recv(16)
        
        if new_msg:
            msglen = int(msg[:HEADERSIZE])
            new_msg = False    

        full_msg += msg


        if len(full_msg)-HEADERSIZE == msglen:
            loaded = pickle.loads(full_msg[HEADERSIZE:])
            break
    return loaded

def DNS(url):
    return FRP("jupitershost.hopto.org",12800,{'url' : url.encode()})
    
def get(url,directory):
    
    return FRP("jupitershost.hopto.org",12801,)
