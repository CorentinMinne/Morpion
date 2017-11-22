# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 16:51:10 2017

@author: A463351
"""

#! /usr/bin/python3
# -*- coding: utf-8 -*-

# python 3
# (C) Fabrice SincÃ¨re

# ubuntu : OK
# win XP, 7 : OK

# localhost : OK
# rÃ©seau local : OK (firewall Ã  paramÃ©trer)
# Internet : OK (box - routeur NAT Ã  paramÃ©trer)

# fonctionne aussi avec un simple client telnet
# telnet localhost 50026

import socket, sys, threading, time, random

# variables globales

# adresse IP et port utilisÃ©s par le serveur
HOST = ""
PORT = 1111

NOMBREJOUEUR = 2
dureemax = 120 # durÃ©e max question ; en secondes
pause = 3 # pause entre deux questions  ; en secondes

dict_clients = {}  # dictionnaire des connexions clients
dict_pseudos = {}  # dictionnaire des pseudos
dict_reponses = {}  # dictionnaire des rÃ©ponses des clients
dict_scores = {} # dictionnaire des scores de la derniÃ¨re question
dict_scores_total = {}
pseudo_l = []
test = []
nb_player = 0

class ThreadClient(threading.Thread):
    '''dÃ©rivation de classe pour gÃ©rer la connexion avec un client'''
    
    def __init__(self,conn):
        threading.Thread.__init__(self)
        self.connexion = conn
        self.nom = self.getName()
        dict_clients[self.nom] = self.connexion
        test.append(self.connexion)
        dict_scores[self.nom] = 0
        dict_scores_total[self.nom] = 0
        
        print("Connexion du client", self.connexion.getpeername(),self.nom ,self.connexion)
        
        message = bytes("Vous Ãªtes connectÃ© au serveur.\n","utf-8")
        self.connexion.send(message)
        
        
    def run(self):
        global nb_player
        self.connexion.send(b"Entrer un pseudo :\n")
        pseudo = self.connexion.recv(4096)
        pseudo = pseudo.decode(encoding='UTF-8')
        nb_player += 1
        self.connexion.send(bytes("Vous etes player;{}".format(nb_player),"UTF8"))

        dict_pseudos[self.nom] = pseudo
        pseudo_l.append(pseudo)
        
        print("Pseudo du client", self.connexion.getpeername(),">", pseudo)
        
       
        while True:
            
            try:
                pass
            except:
                print("\nFin du thread",self.nom)
                self.connexion.close()

def MessagePourTous(message):
    """ message du serveur vers tous les clients"""
    for client in dict_clients:
        dict_clients[client].send(bytes(message,"utf8"))
        
        
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mySocket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
try:
    mySocket.bind((HOST, PORT))
except socket.error:
    print("La liaison du socket Ã  l'adresse choisie a Ã©chouÃ©.")
    sys.exit()
print("Serveur prÃªt (port",PORT,") en attente de clients...")
mySocket.listen(5)



while len(dict_clients) < NOMBREJOUEUR:
    try:
        connexion, adresse = mySocket.accept()
    except:
        sys.exit()
    th = ThreadClient(connexion)
    th.setDaemon(1)
    th.start()
    

while len(dict_pseudos) < NOMBREJOUEUR:
    pass


MessagePourTous("\nLa partie va commencer !\n")


class main:
    
    def __init__(self):
        self.game = [[0,0,0],[0,0,0],[0,0,0]]
        self.player = random.randint(0,1)
        self.draw = False
        if self.player == 0:
            self.color = "red"
        else:
            self.color = "blue"
        MessagePourTous("Au tour de {}".format(pseudo_l[self.player]))
        while self.draw == False:
            for client in dict_clients:
                if self.draw == False and dict_pseudos[client] == pseudo_l[self.player]:
                    reponse = dict_clients[client].recv(4096)
                    reponse = reponse.decode(encoding='UTF-8')
                    coord = reponse.split(";")
                    print ("on a recu du joeuur", " : ", coord[0], " ", coord[1])
                    self.motion(int(coord[0]), int(coord[1]))
            pass

    def end(self):
        self.draw = True
        for client in test:
            client.close()
    
    
    def check_win(self):
        print ("pseudo = ", pseudo_l[0], "   ", pseudo_l[1])
        for i in range(3):
            if sum(self.game[i]) == 3:
                MessagePourTous("VICTOIRE de {};{}".format(pseudo_l[0], 1))
                self.end()
            if sum(self.game[i]) == 12:
                MessagePourTous("VICTOIRE de {};{}".format(pseudo_l[1], 2))
                self.end()
                
        self.emag=[[row[i] for row in self.game] for i in range(3)]
        for i in range(3):
            if sum(self.emag[i]) == 3:
                MessagePourTous("VICTOIRE de {};{}".format(pseudo_l[0], 1))
                self.end()
            if sum(self.emag[i]) == 12:
                MessagePourTous("VICTOIRE de {};{}".format(pseudo_l[1], 2))
                self.end()
                
        if self.game[0][0] == self.game[1][1] == self.game[2][2] == 1:
            MessagePourTous("VICTOIRE de {};{}".format(pseudo_l[0], 1))
            self.end()
        if self.game[0][0] == self.game[1][1] == self.game[2][2] == 4:
            MessagePourTous("VICTOIRE de {};{}".format(pseudo_l[1], 2))
            self.end()
        if self.game[0][2] == self.game[1][1] == self.game[2][0] == 1:
            MessagePourTous("VICTOIRE de {};{}".format(pseudo_l[0], 1))
            self.end()
        if self.game[0][2] == self.game[1][1] == self.game[2][0] == 4:
            MessagePourTous("VICTOIRE de {};{}".format(pseudo_l[1], 2))
            self.end()

        zero = 0
        for liste in self.game:
            if not 0 in liste:
                zero += 1
        if zero == 3 and self.draw == False:
            MessagePourTous("VICTOIRE de personne")
            self.end()
       
        
    def motion(self, x, y):
        for l in range(3):
            for c in range(3):
                if (x < 80 * (c + 1) and x > 0 + (80 * c )
                and y > 0 + (80 * l) and y < 80 * (l + 1)
                and self.game[l][c] == 0):
                    if self.player == 0:
                        MessagePourTous("COORD ;{};{};{}".format(self.player + 1, c, l))
                        self.game[l][c] = 1
                        self.player = 1
                        self.color = "blue"
                    elif self.player == 1:
                        MessagePourTous("COORD ;{};{};{}".format(self.player + 1, c, l))
                        self.game[l][c] = 4
                        self.player = 0
                        self.color= "red"
        MessagePourTous("Au tour de {}".format(pseudo_l[self.player]))
        self.check_win()
        
main()     
