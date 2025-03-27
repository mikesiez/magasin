from datetime import datetime, timedelta
import requetes_sql
import random
import pygame
import time

magasin = {} # Les objets que le joueur puissent acheter
reserve = {} # Les objets en stock
money = 100  # Le joueur commence avec 100€

class File: # Structure de Base d'une File
    def __init__(self):
         self.file = []

    def enfile(self, element):  # Ajoute un element à la fin de la liste
        self.file.append(element)

    def defile(self):  # Défiler et retourne l'élément défiler
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


class Management: # No instances, only sub-functions
    def Dict_reserve(): # Dictionnary with keys being the isle numbers, values being sub dictionnaries, REPRESENTS WAREHOUSE
                        # Sub dictionnary contains product_id as a key, and pile for instances of the product in the warehouse as values
        global reserve
        liste_exemplaires = requetes_sql.selection_requetes("Exemplaire JOIN Produit JOIN Categorie",
                                                            "Exemplaire.exemplaire_id, Exemplaire.produit_id, Categorie.rayon",
                                                            "WHERE Exemplaire.produit_id = Produit.produit_id AND Categorie.categorie_id = Produit.categorie_id")
        for exemplaire in liste_exemplaires:
            id_exemplaire = exemplaire[0]
            id_produit = exemplaire[1]
            rayon = exemplaire[2]

            if rayon not in reserve:
                reserve[rayon] = {id_produit:Pile()}
            if id_produit not in reserve[rayon]:
                print(1)
                reserve[rayon][id_produit] = Pile()
            reserve[rayon][id_produit].empile(id_exemplaire)

    def transferer_vers_magasin(produit_id, rayon):  # Dictionnary with keys being the isle numbers, values being sub dictionnaries, REPRESENTS STOCK
                                                     # Sub dictionnary contains product_id as a key, and file for instances of the product in the stock as values
        global magasin, reserve
        if rayon in reserve and produit_id in reserve[rayon]:
            if rayon not in magasin:
                magasin[rayon] = {}
            if produit_id not in magasin[rayon]:
                magasin[rayon][produit_id] = File()
            for _ in range(5):
                if not reserve[rayon][produit_id].est_vide():
                    exemplaire_id = reserve[rayon][produit_id].depile()
                    magasin[rayon][produit_id].enfile(exemplaire_id)
                    requetes_sql.update_requetes("Exemplaire", "statut_id = 2", f"exemplaire_id = {exemplaire_id}")
                else:
                    print("Out of stock while trying to restock")
                    
    def restocker_etageres(): # Goal: restocks a specific item on the shelf in stock
        for rayon, produits in magasin.items():
            for produit, file_exemplaires in produits.items():
                if file_exemplaires.est_vide():
                    Management.transferer_vers_magasin(produit, rayon)
                    print(f"Le produit {produit} dans le rayon {rayon} a été réapprovisionné.")

                    # Need to implement buying goods for the warehouse

Management.Dict_reserve()

for rayon in reserve: # Stocks up the warehouse
        for produit_id in reserve[rayon]:
            Management.transferer_vers_magasin(produit_id, rayon)

def gestion_clients():
    global money
    if magasin and random.random() < 0.5:  # 50% chance de générer un client toutes les 3 secondes
        nombre_produits = random.randint(1, 4)
        for _ in range(nombre_produits):
            rayon = random.choice(list(magasin.keys())) # Picks a random isle
            if magasin[rayon]:
                produit = random.choice(list(magasin[rayon].keys())) # Picks a random product
                if magasin[rayon][produit] and not magasin[rayon][produit].est_vide():
                    exemplaire_id = magasin[rayon][produit].defile() # Takes the first element of the shelf

                    # Vérifie si disponible à la vente (statut_id == 1)
                    statut = requetes_sql.selection_requetes("Exemplaire", "statut_id", f"WHERE exemplaire_id = {exemplaire_id}")
                
                    # produit "vendu"
                    requetes_sql.update_requetes("Exemplaire", "statut_id = 3", f"exemplaire_id = {exemplaire_id}")

                    # prix du produit
                    prix = requetes_sql.selection_requetes("Exemplaire", "prix_vente_modifier", f"WHERE exemplaire_id = {exemplaire_id}")[0][0]

                    # Met à jour l'argent du joueur et affiche les détails de l'achat
                    money += prix
                    money = round(money, 2)
                    print(f"Un client a acheté 1 exemplaire de produit {produit} dans le rayon {rayon} pour {prix}€.")



# Pygame, UI
def main():
    global date, money
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Gestion du Magasin")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    running = True
    last_update_time = time.time()
    last_customer_time = time.time()

    while running:
        screen.fill((255, 255, 255))
        date_text = font.render(f"Date: {date.strftime('%Y-%m-%d %H:%M:%S')}", True, (0, 0, 0))
        money_text = font.render(f"Argent: {money}€", True, (0, 0, 0))
        screen.blit(date_text, (50, 50))
        screen.blit(money_text, (50, 100))
        
        pygame.display.flip()
        clock.tick(60)

        current_time = time.time()
        if current_time - last_update_time >= 1:
            date += timedelta(minutes=1)
            last_update_time = current_time
            if date.second == 0: # shelves restock every minute, which is every day in game time
                Management.restocker_etageres()

        if current_time - last_customer_time >= 3:  # 3 secondes d'intervalle pour l'apparition du client
            gestion_clients()
            last_customer_time = current_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()

date = datetime.strptime("2025-01-01 00:00:00", '%Y-%m-%d %H:%M:%S')
main()
