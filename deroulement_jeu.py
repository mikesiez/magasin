not tested
# initialisation de base avec produits initiales:
from datetime import datetime, timedelta
import requetes_sql
import random
import pygame
import time

magasin = {}
reserve = {}

class File:
    def __init__(self):
         self.file = []
    def enfile(self, element): # Ajoute un element un fin de liste
        self.file.append(element)
    def defile(self): # Defile et retourne lelement defile
        if not self.est_vide():
            return self.file.pop(0)
    def est_vide(self):
        return self.file == []
    def __str__(self):
        return ', '.join(map(str, self.file))
 

class Pile:
    def __init__(self):
        self.pile = []
    def empile(self, element):
        self.pile.append(element)
    def depile(self):
        if not self.est_vide():
            return self.pile.pop(-1)
    def est_vide(self):
        return self.pile == []
    def __str__(self):
        return ', '.join(map(str, self.pile))

class Management:
    def Dict_reserve():
        # Transfert les produits de la DB a un dictionnaire "reserve" initialize a la ligne 8
        # liste Produits qui contient des tuples (id de lexemplaire, id de produit, id de rayon/allee)
        global reserve
        
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
    Dict_reserve()

    def transferer_vers_magasin(produit_id, rayon):
        global magasin, reserve
        
        if rayon in reserve and produit_id in reserve[rayon]:
            if rayon not in magasin:
                magasin[rayon] = {}
            
            if produit_id not in magasin[rayon]:
                magasin[rayon][produit_id] = File()
                
            for _ in range(5):  # On prend un maximum de 5 exemplaires
                if not reserve[rayon][produit_id].est_vide():
                    exemplaire_id = reserve[rayon][produit_id].depile()
                    magasin[rayon][produit_id].enfile(exemplaire_id)
                    requetes_sql.update_requetes("Exemplaire", "statut_id = 2", f"exemplaire_id = {exemplaire_id}")
                else:
                    break

# Mettre à jour tous les produits
for rayon in reserve:
        for produit_id in reserve[rayon]:
            Management.transferer_vers_magasin(produit_id,rayon)
            

#-------------------------------------------------------------------------------------------------------

def gestion_clients():
    rayon = random.choice(list(magasin.keys())) if magasin else None
    if rayon:
        produit = random.choice(list(magasin[rayon].keys())) if magasin[rayon] else None
        if produit and not magasin[rayon][produit].est_vide():
            quantite = random.randint(1, 3)
            for _ in range(quantite):
                if not magasin[rayon][produit].est_vide():
                    exemplaire_id = magasin[rayon][produit].defile()
                    requetes_sql.update_requetes("Exemplaire", "statut_id = 3", f"exemplaire_id = {exemplaire_id}")
            print(f"Un client a acheté {quantite} exemplaires de produit {produit} dans le rayon {rayon}.")

def restocker_etageres():
    for rayon, produits in magasin.items():
        for produit, file_exemplaires in produits.items():
            if file_exemplaires.est_vide():
                Management.transferer_vers_magasin(produit, rayon)
                print(f"Le produit {produit} dans le rayon {rayon} a été réapprovisionné.")


def main():
    global date
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Gestion du Magasin")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    
    running = True
    last_update_time = time.time()
    
    while running:
        screen.fill((255, 255, 255))
        date_text = font.render(f"Date: {date.strftime('%Y-%m-%d %H:%M:%S')}", True, (0, 0, 0))
        screen.blit(date_text, (50, 50))
        
        pygame.display.flip()
        clock.tick(60)  # 60 FPS
        
        current_time = time.time()
        if current_time - last_update_time >= 1:  # Chaque seconde en temps réel = 1 minute en jeu
            date += timedelta(minutes=1)
            last_update_time = current_time
            
            if date.second == 0:  # Chaque minute IRL (60s) correspond à une journée en jeu
                restocker_etageres()
        
        if random.random() < 0.7:
            gestion_clients()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    
    pygame.quit()

date = datetime.strptime("2025-01-01 00:00:00", '%Y-%m-%d %H:%M:%S')
main()
