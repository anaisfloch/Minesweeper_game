# -*- coding: utf-8 -*-
"""
Created on Fri Oct 24 09:05:11 2025

@author: afloch
"""

### Imports ###
import numpy as np
from abc import abstractmethod


### Définition d'une grille de jeu ###

class Grille():
    
    def __init__(self, difficulte):
        """Initialise la grille de jeu du démineur avec une certaine 
        taille et un nombre de bombes en fonction de la difficulté choisie.
        
        Paramètres
        ---------
        grille : array
            Matrice vide représentant la grille de jeu.
        taille :  tuple
            Longeur et largeur de la grille.
        bombe : int
            Nombre de bombes présentes dans la grille.
        difficulte : int
            Codes de difficulté :
                0 - facile, 8x8, 10 bombes
                1 - moyen, 16x16, 40 bombes
                2 - difficile, 30x16, 99 bombes
        """
        self.difficulte = difficulte
        
        # Choix de config en fonction de la difficulté
        if difficulte == 0:
            self.taille = (8,8)
            self.bombe = 10
        elif difficulte == 1:
            self.taille = (16,16)
            self.bombe = 40
        elif difficulte == 2:
            self.taille = (16,30)
            self.bombe = 99
        else:
            raise ValueError("Le code de difficulté doit être de 0 (facile), 1 (moyen) ou 2 (difficile).")
         
        # Placement des bombes    
        self.grille = np.empty(self.taille)
        nb_case = self.taille[0] * self.taille [1]
        place_bombe = np.random.choice(nb_case, self.bombe, replace = False)
        coord_bombe = []
        for i in place_bombe:
            # i+1 pour prendre en compte case 0 dans le compte des lignes
            coord_bombe.append(((i+1)//self.taille [1] - 1, i % self.taille[0]))
            
        # Remplissage de la grille
        for i in range(self.taille[0]):
            for j in range(self.taille[1]):
                if (i,j) in coord_bombe:
                    self.grille[i, j] = CaseBombe((i,j), self)
                else :
                    self.grille[i, j] = CaseVide((i,j), self)
                    
        def afficher(self):
            for i in range(self.taille[0]):
                ligne = []
                for j in range(self.taille[1]):
                    c = self.grille[i,j]
                    if c.drapeau == 1 :
                        ligne.append("*")
                    elif not c.decouverte:
                        ligne.append("_")
                    elif isinstance(c, CaseBombe):
                        ligne.append("BOUM")
                    elif c.nbr_bombes_voisines > 0:
                        ligne.append(str(c.nbr_bombes_voisines))
                    else:
                        ligne.append("0")
                print(" ".join(ligne))
            print()          
         
        

### Définition d'une case de jeu ###

class Case():
    
    def __init__(self, position, grille, drapeau = 0):
        """Initialise une case de la grille de jeu du démineur dans un 
        certain état et une position particulière.
        
        Paramètres
        ---------
        position : tuple
            Coordonnées de la case dans la grille de jeu.
        grille : array
            Matrice à laquelle la case est rattachée.
        drapeau : int
            Indique la présence ou non d'un drapeau sur la case. Par défaut 
            égal à 0'
        """
        self.drapeau = drapeau
        self.grille = grille
        self.position = position
        self.decouverte = False
    
    @abstractmethod
    def decouvrir(case):
        pass
    
    @abstractmethod
    def drapeau(self, position):
        pass


class CaseBombe(Case):
    
    def __init__(self, position, grille, drapeau = 0):
        super().__init__(position, grille, drapeau = 0)
        
    def decouvrir(self, position):
        #terminer la partie sauf s'il y a déjà un drapeau = True 
        if self.drapeau == 1:
            print(f"Case {self.position} marquée, ne peut être découverte")
        else: 
            print(f"MACRON EXPLOSION (perdu nullos)")
            self.grille.afficher()
            exit()
            
    def drapeau(self, position):
        #ajouter un drapeau sur la case, set drapeau = True
        self.drapeau = 1 - self.drapeau
        
    
class CaseVide(Case):
    
    def __init__(self, position, grille, drapeau = 0):
        super().__init__(position, grille, drapeau = 0)
        self.nbr_bombes_voisines = self.get_nbr_bomb()
        
    def decouvrir(self, position):
        if self.drapeau == 1 or self.decouverte :
            print(f"Cette case ne peut être découverte")
        else: 
            self.decouverte = True
            x, y = self.position
            if self.nbr_bombes_voisines > 0:
                print(f"Case {self.position} : {self.nbr_bombes_voisines} bombes voisines.")
            else :
                print(f"Case {self.position} vide : Découverte automatique des cases voisines.")
                for i in range(x-1, x+2):
                    for j in range(y-1, y+2):
                        if (0 <= i <= self.grille.taille[0]) and (0 <= j <= self.grille.taille[1]) and (i,j) != (x,y):
                            self.grille.grille[i,j].decouvrir
    
    def drapeau(self, position, drapeau = 0):
        #ajouter un drapeau sur la case, set drapeau = True
        self.drapeau = 1 - self.drapeau
    
    def get_nbr_bomb(self):
        #return le nombre de bombes environnantes
        x, y = self.position
        voisins = [
            (i,j)
            for i in range(x-1, x+2)
            for j in range(y-1, y+2)
            if (0 <= i <= self.grille.taille[0]) and (0 <= j <= self.grille.taille[1]) and (i,j) != (x,y)
        ]
        return sum(isinstance(self.grille.grille[i,j], CaseBombe) for i, j in voisins)
    
    
