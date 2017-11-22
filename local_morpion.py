# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 17:02:22 2017

@author: A463351
"""

import tkinter as tk
from tkinter import messagebox
import random

class main:
    
    def __init__(self):
        self.game = [[0,0,0],[0,0,0],[0,0,0]]
        self.player = random.randint(0,1)
        menubar = tk.Menu(fen)
        menu1 = tk.Menu(menubar, tearoff=0)
        menu1.add_command(label="Nouvelle partie", command=self.alert)
        menu1.add_separator()
        menu1.add_command(label="Quitter", command=fen.destroy)
        menubar.add_cascade(label="Jeu", menu=menu1)

        menu2 = tk.Menu(menubar, tearoff=0)
        menu2.add_command(label="Infos", command=self.infos)
        menubar.add_cascade(label="Aide", menu=menu2)
        fen.config(menu=menubar)
        
        self.canvas = tk.Canvas(fen, width=240, height=240)
        self.canvas.focus_set()
        self.canvas.create_line(0, 80, 240, 80)
        self.canvas.create_line(0, 160, 240, 160)
        self.canvas.create_line(80, 0, 80, 240)
        self.canvas.create_line(160, 0, 160, 240)
        self.draw = False
        if self.player == 0:
            self.color = "red"
        else:
            self.color = "blue"
        self.player_turn = tk.Label(fen, text="Au tour du joueur {}".format(self.player + 1), fg=self.color)
        self.player_turn.pack()
        self.canvas.pack(padx=40, pady=10)
        self.play()
    
    def replay(self, event):
        self.alert()
        
    def play(self):
        self.canvas.bind('<Button-1>', self.motion)   
        self.canvas.bind('<Control-n>', self.replay)
        
    def alert(self):
        self.canvas.delete(tk.ALL)
        self.game = [[0,0,0],[0,0,0],[0,0,0]]
        self.player = random.randint(0,100) % 2
        if self.player == 0:
            self.color = "red"
        else:
            self.color = "blue"
        self.draw = False
        self.canvas.create_line(0, 80, 240, 80)
        self.canvas.create_line(0, 160, 240, 160)
        self.canvas.create_line(80, 0, 80, 240)
        self.canvas.create_line(160, 0, 160, 240)        
        self.player_turn.configure(text="Au tour du joueur {}".format(self.player + 1), fg=self.color)
        self.player_turn.pack()
        self.canvas.pack(padx=40, pady=10)
        self.play()
        
    def infos(self):
        messagebox.showinfo("A propos", "Corentin M.")
       

    def draw_circle(self, l, c):
        self.canvas.create_oval((c * 80) + 10, (l * 80) + 10, (c * 80) + 70, (l * 80) + 70, outline="red", width=3)
    
    
    def draw_cross(self, l, c):
        self.canvas.create_line((c * 80) + 10, (l * 80) + 10, (c * 80) + 70, (l * 80) + 70, fill="blue", width=3)
        self.canvas.create_line((c * 80) + 70, (l * 80) + 10, (c * 80) + 10, (l * 80) + 70, fill="blue", width=3)


    def end(self):
        self.draw = True
        self.player_turn.pack()
        self.canvas.unbind("<ButtonPress-1>")
    
    
    def check_win(self):
        
        for i in range(3):
            if sum(self.game[i]) == 3:
                self.player_turn['text']=("VICTOIRE du joueur {}".format(1))
                self.player_turn['fg']=("red")
                self.end()
            if sum(self.game[i]) == 12:
                self.player_turn['text']=("VICTOIRE du joueur {}".format(2))
                self.player_turn['fg']=("blue")
                self.end()
                
        self.emag=[[row[i] for row in self.game] for i in range(3)]
        for i in range(3):
            if sum(self.emag[i]) == 3:
                self.player_turn['text']=("VICTOIRE du joueur {}".format(1))
                self.player_turn['fg']=("red")
                self.end()
            if sum(self.emag[i]) == 12:
                self.player_turn['text']=("VICTOIRE du joueur {}".format(2))
                self.player_turn['fg']=("blue")
                self.end()
                
        if self.game[0][0] == self.game[1][1] == self.game[2][2] == 1:
            self.player_turn['text']=("VICTOIRE du joueur {}".format(1))
            self.player_turn['fg']=("red")
            self.end()
        if self.game[0][0] == self.game[1][1] == self.game[2][2] == 4:
            self.player_turn['text']=("VICTOIRE du joueur {}".format(2))
            self.player_turn['fg']=("blue")
            self.end()
        if self.game[0][2] == self.game[1][1] == self.game[2][0] == 1:
            self.player_turn['text']=("VICTOIRE du joueur {}".format(1))
            self.player_turn['fg']=("red")
            self.end()
        if self.game[0][2] == self.game[1][1] == self.game[2][0] == 4:
            self.player_turn['text']=("VICTOIRE du joueur {}".format(2))
            self.player_turn['fg']=("blue")
            self.end()

        zero = 0
        for liste in self.game:
            if not 0 in liste:
                zero += 1
        if zero == 3 and self.draw == False:
            self.player_turn['text']=("C'est une egalite !!")
            self.player_turn['fg']=("green")
            self.end()
       
        
    def motion(self, event):
        x, y = event.x, event.y
        for l in range(3):
            for c in range(3):
                if (x < 80 * (c + 1) and x > 0 + (80 * c )
                and y > 0 + (80 * l) and y < 80 * (l + 1)
                and self.game[l][c] == 0):
                    if self.player == 0:
                        self.draw_circle(l, c)
                        self.game[l][c] = 1
                        self.player = 1
                        self.color = "blue"
                    elif self.player == 1:
                        self.draw_cross(l, c)
                        self.game[l][c] = 4
                        self.player = 0
                        self.color= "red"
        self.player_turn['text']=("Au tour du joueur {}".format(self.player + 1))
        self.player_turn['fg']=(self.color)
        self.check_win()
        
fen = tk.Tk()
fen.title("Morpion")
main()
fen.mainloop()  