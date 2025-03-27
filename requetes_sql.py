import sqlite3

DB_Path = "./BDD_en_cours_jeu.db" #Path for the database

def selection_requetes(tableau, champs, filtres): # Returns selected lines
    requete = f"SELECT {champs} FROM {tableau} {str()} {filtres}"
    
    with sqlite3.connect(DB_Path) as connexion:
        curseur = connexion.cursor()
        curseur.execute(requete)
        lignes = curseur.fetchall()

    return lignes

def insertion_requetes(tableau, champs, valeurs): # Inserts a new row into the table
    requete = f"INSERT INTO {tableau} ({champs}) VALUES({valeurs})"

    with sqlite3.connect(DB_Path) as connexion:
        curseur = connexion.cursor()
        curseur.execute(requete)
        connexion.commit() # Sauvegarde tout changement/modification a la base de donnees

    
def update_requetes(tableau, valeurs, conditions): # Modifies/updates current values in the table
    requete = f"UPDATE {tableau} SET {valeurs} WHERE {conditions}"

    with sqlite3.connect(DB_Path) as connexion: # Code identique a insert_requetes
        curseur = connexion.cursor()
        curseur.execute(requete)
        connexion.commit() # Sauvegarde tout changement/modification a la base de donnees