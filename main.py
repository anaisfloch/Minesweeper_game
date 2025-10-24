# -*- coding: utf-8 -*-
"""
Created on Fri Oct 24 14:14:08 2025

@author: afloch
"""

from grille import Grille

def jouer():
    print(" ====== MINESWEEPER ====== ")
    print("Difficultés : 0 => facile (8x8, 10 bombes), 1 => moyen (16x16, 40 bombes), 2 => difficile (30x16, 99 bombes)")
    
    while True:
        try:
            difficulte = int(input("Choisissez la difficulté :"))
            if difficulte in [0,1,2]:
                break
            else:
                print("Le code de difficulté doit être de 0 (facile), 1 (moyen) ou 2 (difficile).")
        except ValueError:
            print("Tu fais n'importe quoi recommence.")
    
    g = Grille(difficulte)
    g.afficher_solution()
    
    while True: 
        g.afficher()
        action = input("Action (d = découvrir, p = drapeau, q = quitter) : ")
        if action == 'q':
            print("Adieu.")
            break
        try:
            x = int(input("Ligne : "))
            y = int(input("Colonne : "))
        except ValueError:
            print("Entrée invalide, recommence avec des nombres.")
            
        case = g.grille[x,y]
        
        if action == "d":
            case.decouvrir()
        elif action == "p":
            case.ajouter_drapeau()
        else:
            print("Action invalide.")
        
if __name__ == "__main__":
    jouer()
