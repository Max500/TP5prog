'''
Created on 2013-11-28

@author: maximeblouin
'''
#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import Tkinter
import Tkinter as tk
from Tkinter import * 
import webbrowser


#Site web des reglements du jeu
site = '''http://fr.wikipedia.org/wiki/Règles_du_jeu_d'échecs'''

root = Tk()
frame = Frame(root)
frame.pack()

def OuvrirLien():
    webbrowser.open_new(site)
    
class Damier(tk.Frame):
    
    '''
    Classe permettant l'affichage d'un damier
    '''

    def __init__(self, parent,size):
        '''size est la taille d'un cote d'une case en pixel.'''
        # Definition du damier
        self.rows = 8
        self.columns = 8
        self.size = size
        self.color1 = "white"
        self.color2 = "gray"

        self.pieces = {}
        # Calcul de la taille du dessin
        canvas_width = self.columns * self.size
        canvas_height = self.rows * self.size

        # Initialisation du menu 
        menubar = Menu(root)

        filemenu = Menu(menubar, tearoff = 0)
        filemenu.add_command(label="Nouvelle Partie", command=root.quit)
        filemenu.add_command(label="Charger", command=root.quit)
        filemenu.add_separator()
        filemenu.add_command(label="Enregistrer", command=root.quit)
        filemenu.add_separator()
        filemenu.add_command(label="Quitter", command=root.quit)
        menubar.add_cascade(label="Fichier", menu=filemenu)

        helpmenu = Menu(menubar, tearoff = 0)
        helpmenu.add_command(label="A propos", command=root.quit)
        menubar.add_cascade(label="Aide", menu=helpmenu, command=OuvrirLien)
        
        root.config(menu=menubar)


        # Initialisation de la fenetre parente contenant le canvas
        tk.Frame.__init__(self, parent)


        # Initialise la boite d'entree de commande et son label
        self.lab_commande=tk.Label(self,text="Commande/Deplacement:",anchor=tk.W)
        self.lab_commande.grid(row=1,column=0,stick=tk.W)
        self.entre_commande=tk.Entry(self)
        self.entre_commande.grid(row=1,column=1, columnspan=4, sticky=tk.W+E)

        # Initialisation du label de messages d'erreurs en bas de la fenetre
        self.lab_erreur=tk.Label(self,text="Messages d'Erreur: ",anchor=tk.W)
        self.lab_erreur.grid(row=2, column=0, sticky=tk.W)
        self.lab_erreur2=tk.Label(self,text="aucune erreur", anchor=tk.W, bg="white")     
        self.lab_erreur2.grid(row=2, column=1, columnspan=4, sticky=tk.W+E) 

        # Initialise la fenetre de texte pour les coups joues avec son label
        self.lab_coups=tk.Label(self,text="Coups joues:",anchor=tk.N)
        self.lab_coups.grid(row=0,column=5, sticky=tk.W)
        self.liste=tk.Label(self,text="a venir", anchor=tk.N+W, bg="white")
        self.liste.grid(row=0,column=5, columnspan=2, padx=5, pady=5, sticky=tk.W+E+N+S)
        
        # Création de l'affichage
        self.affichage = Text(self.root, height=100, width=100, wrap=WORD, state="disabled")
        self.affichage.grid(row=5, columnspan=3, sticky=NSEW)
        self.affichage["font"] = ("Courier New", 10)
        self.affichage["fg"] = "black"
        # Initialise le scrollbar du canvas
        self.scrollbar=Scrollbar(self.lab_coups, bg='gray', orient=VERTICAL,troughcolor='black')
        # association du deplacement de la glissiere des scrollbar avec la position visible dans le widget canvas.              
        self.scrollbar.config(command=self.affichage.yview)
        self.affichage.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.grid(row=5, column=2, sticky=NSEW)
        
        # Initialise les 4 boutons sous la fenetre des "Coups joues"
        ## Nouveau
        self.bou_nouveau=tk.Button(self,text="Nouveau",anchor=tk.CENTER,fg="blue",width=20)
        self.bou_nouveau.grid(row=1,column=5, sticky=tk.W)
        ## Charger
        self.bou_charger1=tk.Button(self,text="Charger",anchor=tk.CENTER,fg="dark green",width=20)
        self.bou_charger1.grid(row=1,column=6, sticky=tk.E)
        ## Enregistrer
        self.bou_enregistrer1=tk.Button(self,text="Enregistrer",anchor=tk.CENTER,fg="blue",width=20)
        self.bou_enregistrer1.grid(row=2,column=5, sticky=tk.W)
        ## Quitter
        self.bou_quitter = tk.Button(self, text="Quitter", command=root.quit,anchor=tk.CENTER,fg="dark green",width=20)
        self.bou_quitter.grid(row=2,column=6, sticky=tk.E)

        # Initialisation du canvas
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0,width=canvas_width, height=canvas_height, background="white")
        # "Grid" le tout.
        self.canvas.grid(row=0,columnspan=4,padx=2, pady=2)
        self.grid(row=0,columnspan=4,padx=4, pady=4)

        # Fais en sorte que le redimensionnement de la fenetre redimensionne le damier
        self.canvas.bind("<Configure>", self.refresh)
        self.root.mainloop()
       
        self.button.pack()
        self.bou_quitter.pack()
        self.bou_enregistrer.pack()
        self.bou_charger1.pack()
        self.bou_nouveau.pack()

    def addpiece(self, name, row=0, column=0):
        '''Ajoute une piece sur le damier'''
        # Caracteres unicode des pieces
        dic_pieces = {'TB': '\u2656','CB': '\u2658','FB': '\u2657','KB': '\u2654','QB': '\u2655','PB': '\u2659',
                      'TN': '\u265C','CN': '\u265E','FN': '\u265D','KN': '\u265A','QN': '\u265B','PN': '\u265F',}
        tempfont = ('Helvetica',self.size//2)
        text = dic_pieces[name[0:2]]
        # On "dessine" le nom
        self.canvas.create_text(row, column, text=text, tags=(name, "piece"),font=tempfont)
        # On place la piece pour le rafraichissement
        self.pieces[name] = (row, column)
        self.placepiece(name, row, column)

    def placepiece(self, name, row, column):
        '''Place une piece a la position donnee row/column'''
        x0 = (column * self.size) + int(self.size / 2)
        y0 = (row * self.size) + int(self.size / 2)
        self.canvas.coords(name, x0, y0)

    def refresh(self, event):
        '''Redessine le damier lorsque la fenetre est redimensionnee'''
        # Calcul de la nouvelle taille du damier
        xsize = int((event.width - 1) / self.columns)
        ysize = int((event.height - 1) / self.rows)
        self.size = min(xsize, ysize)
        # On efface les cases
        self.canvas.delete("case")
        # On les redessine
        color = self.color2
        for row in range(self.rows):
            color = self.color1 if color == self.color2 else self.color2
            for col in range(self.columns):
                x1 = (col * self.size)
                y1 = (row * self.size)
                x2 = x1 + self.size
                y2 = y1 + self.size
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color, tags="case")
                color = self.color1 if color == self.color2 else self.color2
        # On redessine les pieces
        for name in self.pieces:
            self.placepiece(name, self.pieces[name][0], self.pieces[name][1])
        # On mets les pieces au dessus des cases
        self.canvas.tag_raise("piece")
        self.canvas.tag_lower("case")


def addNouveauJeu(board):
        # Le blancs
        board.addpiece("TB1", 0, 0)
        board.addpiece("CB1", 0, 1)
        board.addpiece("FB1", 0, 2)
        board.addpiece("KB", 0, 3)
        board.addpiece("QB", 0, 4)
        board.addpiece("FB2", 0, 5)
        board.addpiece("CB2", 0, 6)
        board.addpiece("TB2", 0, 7)
        board.addpiece("PB1", 1, 0)
        board.addpiece("PB2", 1, 1)
        board.addpiece("PB3", 1, 2)
        board.addpiece("PB4", 1, 3)
        board.addpiece("PB5", 1, 4)
        board.addpiece("PB6", 1, 5)
        board.addpiece("PB7", 1, 6)
        board.addpiece("PB8", 1, 7)
        # Les noirs
        board.addpiece("TN1", 7, 0)
        board.addpiece("CN1", 7, 1)
        board.addpiece("FN1", 7, 2)
        board.addpiece("KN", 7, 3)
        board.addpiece("QN", 7, 4)
        board.addpiece("FN2", 7, 5)
        board.addpiece("CN2", 7, 6)
        board.addpiece("TN2", 7, 7)
        board.addpiece("PN1", 6, 0)
        board.addpiece("PN2", 6, 1)
        board.addpiece("PN3", 6, 2)
        board.addpiece("PN4", 6, 3)
        board.addpiece("PN5", 6, 4)
        board.addpiece("PN6", 6, 5)
        board.addpiece("PN7", 6, 6)
        board.addpiece("PN8", 6, 7)

if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(0,0)
    root.title("Jeu d'echecs")
    board = Damier(root,64)
    addNouveauJeu(board)
    root.mainloop()