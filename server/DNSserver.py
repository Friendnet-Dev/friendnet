import pandas as pd
from server import server
import sys
sys.path.append("..")

from FRP import FRPSend,FRPRcv

#Serveur DNS : à la recpetion d'une url, renvoie l'ip et le répertoire recupérés dans dns.csv

def dns(client):
    # Peut planter si le message contient des caractères spéciaux
    msg = FRPRcv(client)
    url = msg['url'].decode()
    data = {"server" : dnsTable["server"][dnsTable.url == url][0],
            "directory": dnsTable["directory"][dnsTable.url == url][0]}
    FRPSend(client,data)
    client.close()
    return True

        
dnsTable = pd.read_csv("dns.csv")

server(23486,dns)
