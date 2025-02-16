import sqlite3

def selection_requetes(tableau, champs, filtres): 
    requete = (f"SELECT {champs} FROM {tableau} {str()} {filtres}")
    connexion = sqlite3.connect("BDD_en_cours_jeu.db") ; curseur = connexion.cursor()
    curseur.execute(requete) ; lignes = curseur.fetchall()
    curseur.close() ; connexion.commit() ; connexion.close()
    return lignes

def insertion_requetes(tableau, champs, valeurs): 
    requete = (f"INSERT INTO {tableau} ({champs}) VALUES({valeurs})")
    connexion = sqlite3.connect("BDD_en_cours_jeu.db") ; curseur = connexion.cursor()
    curseur.execute(requete) ; 
    curseur.close() ; connexion.commit() ; connexion.close()
    
def update_requetes(tableau, valeurs, conditions):
    requete = (f"UPDATE {tableau} SET {valeurs} WHERE {conditions}")
    connexion = sqlite3.connect("BDD_en_cours_jeu.db") ; curseur = connexion.cursor()
    curseur.execute(requete) ; 
    curseur.close() ; connexion.commit() ; connexion.close()