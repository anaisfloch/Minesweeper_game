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
         
        # Création d'un tableau objet    
        self.grille = np.empty(self.taille, dtype = object)
        
        # Grille préalable
        nb_case = self.taille[0] * self.taille [1]
        place_bombe = np.random.choice(nb_case, self.bombe, replace = False)
        colonnes = self.taille[1]
        grille_test = np.zeros(self.taille, dtype = bool)
        for i in place_bombe:
            l = i // colonnes
            c = i % colonnes
            grille_test[l,c] = True        
        
        # Création des cases
        for i in range(self.taille[0]):
            for j in range(self.taille[1]):
                if grille_test[i,j]:
                    self.grille[i, j] = CaseBombe((i,j), self)
                else :
                    self.grille[i, j] = CaseVide((i,j), self, voisins_calcules = False)
                    
        # Calcul des bombes voisines
        for i in range(self.taille[0]):
            for j in range(self.taille[1]):
                case = self.grille[i,j]
                if isinstance(case, CaseVide):
                    case.nbr_bombes_voisines = case.get_nbr_bomb()
                    
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
                    elif isinstance(c, CaseVide) and c.nbr_bombes_voisines > 0:
                        ligne.append(str(c.nbr_bombes_voisines))
                    else:
                        ligne.append("0")
                print(" ".join(ligne))
            print()   
            
    def afficher_solution(self):
        print("Soluce")
        for i in range(self.taille[0]):
            ligne = []
            for j in range(self.taille[1]):
                c = self.grille[i,j]
                if isinstance(c, CaseBombe):
                    ligne.append("*")
                elif isinstance(c, CaseVide) and (c.nbr_bombes_voisines >= 0):
                    ligne.append(str(c.nbr_bombes_voisines))
                else:
                    ligne.append("?")
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
    def decouvrir(self):
        pass
    
    @abstractmethod
    def ajouter_drapeau(self):
        pass


class CaseBombe(Case):
    
    def __init__(self, position, grille, drapeau = 0):
        super().__init__(position, grille, drapeau)
        
    def decouvrir(self):
        #terminer la partie sauf s'il y a déjà un drapeau = True 
        if self.drapeau == 1:
            print(f"Case {self.position} marquée, ne peut être découverte")
        else: 
            print(f"MACRON EXPLOSION (perdu nullos)")
            self.decouverte = True
            self.grille.afficher()
            exit()
            
    def ajouter_drapeau(self):
        #ajouter un drapeau sur la case, set drapeau = True
        self.drapeau = 1 - self.drapeau
        
    
class CaseVide(Case):
    
    def __init__(self, position, grille, drapeau = 0, voisins_calcules = True):
        super().__init__(position, grille, drapeau)
        self.nbr_bombes_voisines = 0 if voisins_calcules else None
        if voisins_calcules:
            self.nbr_bombes_voisines = self.get_nbr_bomb()
        
    def decouvrir(self):
        if self.drapeau == 1 or self.decouverte :
            return
        self.decouverte = True
        
        # Au cas-où ça n'a pas marché avant
        if self.nbr_bombes_voisines is None:
            self.nbr_bombes_voisines = self.get_nbr_bomb()
        if self.nbr_bombes_voisines > 0:
            print(f"Case {self.position} : {self.nbr_bombes_voisines} bombes voisines.")
            
        # Découvrir les cases vides adjointes
        x, y = self.position
        for i in range(x-1, x+2):
            for j in range(y-1, y+2):
                if (0 <= i < self.grille.taille[0]) and (0 <= j < self.grille.taille[1]) and (i,j) != (x,y):
                    self.grille.grille[i,j].decouvrir()
    
    def ajouter_drapeau(self):
        #ajouter un drapeau sur la case, set drapeau = True
        self.drapeau = 1 - self.drapeau
    
    def get_nbr_bomb(self):
        #return le nombre de bombes environnantes
        x, y = self.position
        voisins = 0
        for i in range(x-1, x+2):
            for j in range(y-1, y+2):
                if (0 <= i < self.grille.taille[0]) and (0 <= j < self.grille.taille[1]) and (i,j) != (x,y):
                    if isinstance(self.grille.grille[i,j], CaseBombe):
                        voisins += 1
        return voisins
                
    
    
