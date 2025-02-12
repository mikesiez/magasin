# initialisation de base avec produits initiales:
from datetime import datetime, timedelta
import requetes_sql

date = datetime.strptime("2025-01-01 00:00:00", '%Y-%m-%d %H:%M:%S')

magasin = {}
reserve = {}

class File:
    def __init__(self):
         self.file = []

    def enfile(self, element): # Ajoute un element un fin de liste
        self.file.append(element)
       
    def defile(self): # Defile et retourne lelement defile
        if not est_vide(self):
            return self.file.pop(0)

    def est_vide(self):
        return self.file == []
 

class Pile:
    def __init__(self):
        self.pile = []

    def empile(self, element):
        self.pile.append(element)

    def depile(self):
        if not est_vide(self):
            return self.pile.pop(-1)

    def est_vide(self):
        return self.pile == []
    
    def __str__(self):
        return ', '.join(map(str, self.pile))

def Dict_reserve():
    # Transfert les produits de la DB a un dictionnaire "reserve" initialize a la ligne 8
    # liste Produits qui contient des tuples (id de lexemplaire, id de produit, id de rayon/allee)
    liste_exemplaires = requetes_sql.selection_requetes("Exemplaire JOIN Produit JOIN Categorie","Exemplaire.exemplaire_id, Exemplaire.produit_id, Categorie.rayon","WHERE Exemplaire.produit_id = Produit.produit_id AND Categorie.categorie_id = Produit.categorie_id")
    for exemplaire in liste_exemplaires:
        id_exemplaire = exemplaire[0]
        id_produit = exemplaire[1]
        rayon = exemplaire[2]
        
        # Si le rayon nest pas dans la reserve, on linitialize
        if rayon not in reserve:
            reserve[rayon] = {id_produit:Pile()}
        if id_produit not in reserve[rayon]:
            reserve[rayon][id_produit] = Pile()
        
        #print(rayon, exemplaire)
         # Si la pile est deja init --> on empile
        reserve[rayon][id_produit].empile(id_exemplaire)
            
    return reserve
    
reserve = Dict_reserve()
#SELECT SELECT Exemplaire.exemplaire_id, Exemplaire.produit_id, Categorie.rayon FROM Exemplaire JOIN Produit JOIN Categorie WHERE Exemplaire.produit_id = Produit.produit_id AND Categorie.categorie_id = Produit.categorie_id