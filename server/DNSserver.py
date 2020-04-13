import pandas as pd
from server import server
import sys
sys.path.append("..")

from FRP import FRPSend,FRPRcv


def dns(client):
    # Peut planter si le message contient des caractères spéciaux
    msg = FRPRcv(client)
    print("recieved")
    url = msg['url'].decode()
    data = {"server" : dnsTable["server"][dnsTable.url == url][0],
            "directory": dnsTable["directory"][dnsTable.url == url][0]}
    FRPSend(client,data)
    print("send")

        
dnsTable = pd.read_csv("dns.csv")

server(23486,dns)
