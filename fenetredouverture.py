'''
Created on 2013-12-09

@author: maximeblouin
'''
#! /usr/bin/env python
# -*- coding:Utf-8 -*-
from tkinter import *
import webbrowser

site = '''http://fr.wikipedia.org/wiki/Règles_du_jeu_d'échecs'''

root = Tk()
frame = Frame(root)
frame.pack()

def OuvrirLien():
    webbrowser.open_new(site)

button = Button(frame, text="CLICK", command=OuvrirLien)

button.pack()
root.mainloop()

class FenetreDeSetup:

    def __init__(self):
        self.root = Tk()
        self.root.title("Bienvenu a notre jeu d'échec!")
        self.frame = Frame(self.root)
        self.frame.pack()
        
        self.instructionMessage = StringVar()
        Label(self.frame, textvariable=self.instructionMessage).grid(row=0)
        self.instructionMessage.set("Veuiller entrer les options de départ")

        Label(self.frame, text="Noms").grid(row=1,column=1)
        
        Label(self.frame, text="Jouer 1 (Blanc)").grid(row=2,column=0)
        self.entry_nomjoueur1 = Entry(self.frame)
        self.entry_nomjoueur1.grid(row=2,column=1)
        
        Label(self.frame, text="Joueur 2 (Noir)").grid(row=3,column=0)
        self.entry_nomjoueur2 = Entry(self.frame)
        self.entry_nomjoueur2.grid(row=3,column=1)            

        b = Button(self.frame, text="Commençer la partie!", command=self.validation)
        b.grid(row=4,column=1)

    def validation(self):
        self.nomjoueur1 = self.entry_nomjoueur1.get()
        self.couleurjoueur1 = "blanc"
        self.nomjoueur2 = self.entry_nomjoueur2.get()
        self.couleurjoueur2 = "noir"
        
        if self.nomjoueur1 != "" and self.nomjoueur2 != "":
            self.frame.destroy()
        else:
                        #Insérons un nom de joueur par défaut si rien n'est entré par l'utilisateur
                        if self.nomjoueur1 == "":
                                self.entry_nomjoueur1.insert(ANCHOR,"Joueur1")
                        elif self.nomjoueur2=="":
                                self.entry_nomjoueur2.insert(ANCHOR,"Joueur2")
                                


    def ParametreDeDepart(self):
        self.root.wait_window(self.frame)
        self.root.destroy()
        return (self.nomjoueur1, self.couleurjoueur1, 
                self.nomjoueur2, self.couleurjoueur2)



if __name__ == "__main__":        

    d = FenetreDeSetup()
    x = d.GetParametreDeDepart()
    print(x)
