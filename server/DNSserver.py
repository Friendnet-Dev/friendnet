import pandas as pd
from server import server
import pickle

def dns(client):
    # Peut planter si le message contient des caractères spéciaux
    msg_recu = client.recv(1024)
    msg_recu = msg_recu.decode()
    url = msg_recu
    
    data = {"server" : dnsTable["server"][dnsTable.url == "test.fds"][0],
            "directory": dnsTable["directory"][dnsTable.url == "test.fds"][0]}
    msg = pickle.dumps(data)
    msg = bytes(f"{len(msg):<{HEADERSIZE}}", 'utf-8')+msg
    client.send(msg)
        
dnsTable = pd.read_csv('dns.csv')
HEADERSIZE = 10

server(12800,dns)