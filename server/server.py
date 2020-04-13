# -*- coding: utf-8 -*-
import socket
import select

#Server : système des gestion d'un serveur executant la fonction task pour chaque client connecté

def server(port, task):

    connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connexion_principale.bind(('', port))
    connexion_principale.listen(5)
    print("Le serveur écoute à présent sur le port {}".format(port))
    
    
    serveur_lance = True
    clients_connectes = []
    while serveur_lance:
        #On regarde si de nouveaux clients veulent se connecter
        connexions_demandees, wlist, xlist = select.select([connexion_principale],
            [], [], 0.05)
        
        for connexion in connexions_demandees: 
            connexion_avec_client, infos_connexion = connexion.accept()
            # On ajoute le socket connecté à la liste des clients
            clients_connectes.append(connexion_avec_client)
    
        clients_a_lire = []
        try:
            clients_a_lire, wlist, xlist = select.select(clients_connectes, #On récupère la liste des clients ayant envoyé une requette
                    [], [], 0.05)
        except select.error:
            pass
        else:
            # On parcourt la liste des clients à lire
            for client in clients_a_lire:
                # Client est de type socket
                try:
                    t = task(client) 
                    if t: #Si t est terminée, on suprime le client
                        clients_connectes.remove(client) 
                except ConnectionAbortedError: #Si le client n'est plus connecté, on l'enlève de la liste
                    client.close()
                    clients_connectes.remove(client) 
                    
    
    print("Fermeture des connexions")
    for client in clients_connectes:
        client.close()
    
    connexion_principale.close()

