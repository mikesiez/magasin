from datetime import datetime, timedelta
import requetes_sql

date_ = datetime.strptime("2025-01-01 00:00:00", '%Y-%m-%d %H:%M:%S') # quand on initialise la base, c'est necessairement au debut du temps, donc pas besoin dutiliser la date de deroulement_jeu. Lors du jeu, l'ajout de produit est gerer la bas.

def dechargement_csv():
    #recuperation donnees csv:
    fichier = open("./donnees_initiales.csv", "r", encoding = "utf8") #'r' c'est pour reading
    liste = fichier.readlines()
    fichier.close()

    #decomposition et ajout dans base de produits initiales
    for produit_str in liste[1:]:
        decomp = produit_str.split(";")
        nom = decomp[0]
        stock = int(decomp[1])
        date_preemption = datetime.strptime(decomp[2], '%Y-%m-%d %H:%M:%S')
        date_entree = datetime.strptime(decomp[3], '%Y-%m-%d %H:%M:%S')
        id_categorie = int(decomp[4])

        for i in range(stock):
            prod_id,temps_de_vie,prix_vente = requetes_sql.selection_requetes("Produit","produit_id,temps_de_vie,prix_vente",f'WHERE "produit_nom" = "{nom}"')[0]
            date_preemption = date_ + timedelta(days=temps_de_vie)
            statut_id = requetes_sql.selection_requetes("Statut","statut_id",f'WHERE "libelle_statut" = "S"')[0][0]

            requetes_sql.insertion_requetes("Exemplaire",
            '"produit_id","statut_id","date_entree","date_preemption","prix_vente_modifier"',
            f'{prod_id},"{statut_id}","{date_}","{date_preemption}",{prix_vente}')

dechargement_csv()