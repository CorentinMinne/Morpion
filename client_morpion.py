# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 16:52:19 2017

@author: A463351
"""


from tkinter import *
from tkinter.messagebox import *

import socket, threading, random

name = ""
start = False

class ThreadReception(threading.Thread):
    """objet thread gÃ©rant la rÃ©ception des messages"""
    def __init__(self, conn):
        threading.Thread.__init__(self)
        ref_socket[0] = conn
        self.connexion = conn
              
    def run(self):
        global start
        global name
        while True:
            try:
                message_recu = self.connexion.recv(4096)
                message_recu = message_recu.decode(encoding='UTF-8')
                print ("meassge : ", message_recu)
                if "Vous etes player;" in message_recu:
                    tab_tmp = message_recu.split(";")
                    player_nb = int(tab_tmp[1])
                if "commencer !" in message_recu:
                    start = True
                    menubar = Menu(fen)
                    menu1 = Menu(menubar, tearoff=0)
                    menu1.add_command(label="Nouvelle partie")
                    menu1.add_separator()
                    menu1.add_command(label="Quitter", command=fen.destroy)
                    menubar.add_cascade(label="Jeu", menu=menu1)
                    
                    menu2 = Menu(menubar, tearoff=0)
                    menu2.add_command(label="Infos")
                    menubar.add_cascade(label="Aide", menu=menu2)
                    fen.config(menu=menubar)
                    
                    canvas = Canvas(fen, width=240, height=240)
                    canvas.focus_set()
                    canvas.create_line(0, 80, 240, 80)
                    canvas.create_line(0, 160, 240, 160)
                    canvas.create_line(80, 0, 80, 240)
                    canvas.create_line(160, 0, 160, 240)
                    canvas.pack(padx=40, pady=10)
                    player_turn = Label(fen, text="Message", fg="black")
                    player_turn.pack()
                    canvas.bind('<Button-1>', motion)   

                print ("name = ", name)
                if start == True and name in message_recu and message_recu.startswith("Au tour"):
                    player_turn.configure(text=message_recu, fg="blue")
                elif start == True and message_recu.startswith("Au tour"):
                    player_turn.configure(text=message_recu, fg="red")

                if start == True and message_recu.startswith("COORD"):
                    coord = message_recu.split(";")
                    nb = int(coord[1])
                    c = int(coord[2])
                    l = int(coord[3])
                    if nb == player_nb:
                        canvas.create_line((c * 80) + 10, (l * 80) + 10, (c * 80) + 70, (l * 80) + 70, fill="blue", width=3)
                        canvas.create_line((c * 80) + 70, (l * 80) + 10, (c * 80) + 10, (l * 80) + 70, fill="blue", width=3)
                    else:
                        canvas.create_oval((c * 80) + 10, (l * 80) + 10, (c * 80) + 70, (l * 80) + 70, outline="red", width=3)
                if "VICTOIRE" in message_recu:
                    vic = message_recu.split(";")
                    nb = int(vic[1])
                    if nb == player_nb:
                        player_turn.configure(text=vic[0], fg="blue")
                    else:
                        player_turn.configure(text=vic[0], fg="red")
                    global CONNEXION
                    CONNEXION = False
                    self.connexion.close()
            except socket.error:
                pass
                
def envoyer_nom():
    global name
    if CONNEXION == True:
        try:
            name = MESSAGE.get()
            print ("message = ", name)
            ref_socket[0].send(bytes(name,"UTF8"))
            ButtonEnv.configure(state = DISABLED)
            
        except socket.error:
            pass

def motion(event):
    if CONNEXION == True:
        x, y = event.x, event.y
        coord = str(x) + ";" + str(y)
        ref_socket[0].send(bytes(coord,"UTF8"))
        

def ConnexionServeur():
    
    global CONNEXION

    if CONNEXION == False:
        try:
            mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            mySocket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            mySocket.connect((HOST.get(), PORT.get()))
            th_R = ThreadReception(mySocket)
            th_R.start()
            CONNEXION = True
            ButtonConnexion.configure(state = DISABLED)
            ButtonEnv.configure(state = NORMAL)
            
        except socket.error:
            showerror('Erreur','La connexion au serveur a Ã©chouÃ©.')
        
        

CONNEXION = False

ref_socket = {}

fen = Tk()
fen.title("Morpion")


canvas1 = Canvas(fen, width=240, height=240)
Label(canvas1, text = "HÃ´te").grid(row=0,column=0,padx=5,pady=5,sticky=W)
HOST = StringVar()
HOST.set('127.0.0.1')
Entry(canvas1, textvariable= HOST).grid(row=0,column=1,padx=5,pady=5)

Label(canvas1, text = "Port").grid(row=1,column=0,padx=5,pady=5,sticky=W)
PORT = IntVar()
PORT.set(1111)
Entry(canvas1, textvariable= PORT).grid(row=1,column=1,padx=5,pady=5)

Label(canvas1, text = "Pseudo").grid(row=2,column=0,padx=5,pady=5,sticky=W)
MESSAGE = StringVar()
Entry(canvas1, textvariable= MESSAGE).grid(row=2,column=1,padx=5,pady=5)

ButtonConnexion = Button(canvas1, text ='Connexion au serveur',command=ConnexionServeur)
ButtonConnexion.grid(row=0,column=2,rowspan=2,padx=5,pady=5)

ButtonEnv = Button(canvas1, text ='Envoyer',command=envoyer_nom)
ButtonEnv.grid(row=2,column=2,rowspan=2,padx=5,pady=5)
ButtonEnv.configure(state = DISABLED)

canvas1.pack()


fen.mainloop()