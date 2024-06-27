import pandas as pd
import os

# Obtenir le chemin absolu du répertoire du script Python
script_directory = os.path.dirname(os.path.abspath(__file__))

# Définir le chemin complet vers le fichier Excel
file_path = os.path.join(script_directory, "a.xlsx")

# Lire le fichier Excel
marchandises_df = pd.read_excel(file_path)

# Afficher un aperçu des données pour vérifier que le chargement a été effectué correctement
print("Aperçu des données du fichier Excel :")
print(marchandises_df.head())

# Dimensions du conteneur (en mètres)
longueur_conteneur = 11.583
largeur_conteneur = 2.294

# Extraire les dimensions et désignations des marchandises
lengths = marchandises_df['Longueur']
widths = marchandises_df['Largeur']
designations = marchandises_df['Désignation']

# Combiner les informations pertinentes dans une seule liste de tuples (désignation, longueur, largeur)
cargo_items = list(zip(designations, lengths, widths))

# Afficher les marchandises avant le placement
print("\n== Détails des marchandises à placer ==")
for i, (designation, longueur, largeur) in enumerate(cargo_items, start=1):
    print(f"Marchandise {i}: Désignation = {designation}, Longueur = {longueur} m, Largeur = {largeur} m")


def remplissage_2d_FF(objets):
    nb_conteneurs = 0
    dim_non_occupé = 0
    nb_objet = 0
    dimension_occupé = 0
    conteneurs = []
    
    for objet_actuel in objets:
        placement = False
        
        for i in range(nb_conteneurs):
            for j in range(1, len(conteneurs[i])):
                if objet_actuel[2] <= conteneurs[i][j][0] and not placement:
                    conteneurs[i][j][0] -= objet_actuel[2]
                    conteneurs[i][j][1].append(objet_actuel[0])
                    placement = True
                    nb_objet += 1
                    dimension_occupé += objet_actuel[2] * objet_actuel[1]
                    
            if not placement and objet_actuel[1] <= conteneurs[i][0]:
                conteneurs[i].append([largeur_conteneur - objet_actuel[2], [objet_actuel[0]]])
                conteneurs[i][0] -= objet_actuel[1]
                placement = True
                nb_objet += 1
                dimension_occupé += objet_actuel[2] * objet_actuel[1]
                    
        if not placement:
            for i in range(nb_conteneurs):
                for j in range(1, len(conteneurs[i])):
                    if objet_actuel[1] <= conteneurs[i][j][0] and objet_actuel[2] <= conteneurs[i][j][1]:
                        conteneurs[i][j][0] -= objet_actuel[1]
                        conteneurs[i][j][2].append(objet_actuel[0])
                        placement = True
                        nb_objet += 1
                        dimension_occupé += objet_actuel[2] * objet_actuel[1]
                
                if not placement and objet_actuel[2] <= conteneurs[i][0] and objet_actuel[1] < largeur_conteneur:
                    conteneurs[i].append([largeur_conteneur - objet_actuel[1], objet_actuel[2], [objet_actuel[0]]])
                    conteneurs[i][0] -= objet_actuel[2]
                    placement = True
                    nb_objet += 1
                    dimension_occupé += objet_actuel[2] * objet_actuel[1]
    
        if not placement:
            conteneurs.append([longueur_conteneur - objet_actuel[1], [largeur_conteneur - objet_actuel[2], [objet_actuel[0]]]])
            nb_conteneurs += 1
            nb_objet += 1
            dimension_occupé += objet_actuel[2] * objet_actuel[1]
         
    dim_non_occupé = nb_conteneurs * largeur_conteneur * longueur_conteneur - dimension_occupé
    
    return nb_conteneurs, round(dim_non_occupé, 3)

def remplissage_2d_FFD(objets):
    # Trier les objets par surface (longueur * largeur) décroissante
    objets_trie = sorted(objets, key=lambda x: x[1] * x[2], reverse=True)
    return remplissage_2d_FF(objets_trie)  # Réutiliser la logique de FF après tri


# Appel des fonctions pour remplir les conteneurs en 2D Online (FF) et Offline (FFD)
ff_conteneurs, ff_non_occupé = remplissage_2d_FF(cargo_items)
ffd_conteneurs, ffd_non_occupé = remplissage_2d_FFD(cargo_items)

# Afficher les résultats pour la méthode Online (FF)
print("\n== Résultats pour la méthode Online (FF) ==")
print(f"Il y a {ff_conteneurs} conteneurs et une surface inutilisée de {ff_non_occupé} m².")

# Afficher les résultats pour la méthode Offline (FFD)
print("\n== Résultats pour la méthode Offline (FFD) ==")
print(f"Il y a {ffd_conteneurs} conteneurs et une surface inutilisée de {ffd_non_occupé} m².")
