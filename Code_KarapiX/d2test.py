import pandas as pd
import os
import json

# Obtenir le chemin absolu du répertoire du script Python
script_directory = os.path.dirname(os.path.abspath(__file__))

# Définir le chemin complet vers le fichier Excel
file_path = os.path.join(script_directory, "a.xlsx")

# Lire le fichier Excel
marchandises_df = pd.read_excel(file_path)

# Afficher un aperçu des données pour vérifier que le chargement a été effectué correctement
print(marchandises_df.head())

# Dimensions du conteneur (en mètres)
longueur_conteneur = 11.583
largeur_conteneur = 2.294

# Extraire les dimensions et désignations des marchandises dans l'ordre du fichier Excel
designations = marchandises_df['Désignation']
lengths = marchandises_df['Longueur']
widths = marchandises_df['Largeur']

# Combiner les informations pertinentes dans une seule liste de tuples (désignation, longueur, largeur)
cargo_items = list(zip(designations, lengths, widths))

# Fonction pour remplir les conteneurs en 2D Online (First Fit)
def remplissage_2d_FF(objets):
    nb_conteneurs = 0
    surface_occupee = 0
    conteneurs = []

    json_structure = {}

    for objet_actuel in objets:
        designation, longueur, largeur = objet_actuel
        placement = False
        
        for conteneur in conteneurs:
            for rangee in conteneur['rangees']:
                # Vérifier si l'objet peut être placé dans cette rangée (en termes de largeur)
                if largeur <= rangee['largeur_disponible']:
                    # Placer l'objet dans cette rangée
                    rangee['largeur_disponible'] -= largeur
                    rangee['objets'].append({
                        "longueur": longueur,
                        "largeur": largeur,
                        "designation": designation
                    })
                    placement = True
                    surface_occupee += longueur * largeur
                    break
            
            # Si l'objet n'a pas été placé dans une rangée existante, vérifier la longueur disponible dans le conteneur
            if not placement and longueur <= conteneur['longueur_disponible']:
                conteneur['rangees'].append({
                    "largeur_disponible": largeur_conteneur - largeur,
                    "objets": [{
                        "longueur": longueur,
                        "largeur": largeur,
                        "designation": designation
                    }]
                })
                conteneur['longueur_disponible'] -= longueur
                placement = True
                surface_occupee += longueur * largeur
                break

        # Si l'objet n'a pas été placé, ajouter un nouveau conteneur
        if not placement:
            nb_conteneurs += 1
            conteneur = {
                "longueur_disponible": longueur_conteneur - longueur,
                "rangees": [{
                    "largeur_disponible": largeur_conteneur - largeur,
                    "objets": [{
                        "longueur": longueur,
                        "largeur": largeur,
                        "designation": designation
                    }]
                }]
            }
            conteneurs.append(conteneur)
            surface_occupee += longueur * largeur

    # Préparer la structure JSON
    for i, conteneur in enumerate(conteneurs):
        wagon_name = f"Wagon {i + 1}"
        wagon_structure = {}
        for j, rangee in enumerate(conteneur['rangees']):
            rangee_structure = {}
            for k, objet in enumerate(rangee['objets']):
                objet_structure = {
                    "longueur": objet["longueur"],
                    "largeur": objet["largeur"],
                    "designation": objet["designation"]
                }
                rangee_structure[f"Objet {k + 1}"] = objet_structure
            wagon_structure[f"Rangee {j + 1}"] = rangee_structure
        json_structure[wagon_name] = wagon_structure

    # Calculer la surface non occupée
    surface_non_occupee = nb_conteneurs * longueur_conteneur * largeur_conteneur - surface_occupee
    print(f"Il y a {nb_conteneurs} conteneurs et une surface inutilisée de {round(surface_non_occupee, 3)} m².")

    return json_structure, nb_conteneurs, round(surface_non_occupee, 3)

# Fonction pour remplir les conteneurs en 2D Offline (First Fit Decreasing)
def remplissage_2d_FFD(objets):
    # Trier les objets par surface (longueur * largeur) décroissante
    objets_tries = sorted(objets, key=lambda x: x[1] * x[2], reverse=True)
    return remplissage_2d_FF(objets_tries)  # Réutiliser la logique de FF après tri

# Appel des fonctions pour remplir les conteneurs en 2D Online (FF) et Offline (FFD)
ff_structure, ff_conteneurs, ff_non_occupee = remplissage_2d_FF(cargo_items)
ffd_structure, ffd_conteneurs, ffd_non_occupee = remplissage_2d_FFD(cargo_items)

# Afficher les résultats pour la méthode Online (FF)
print("\n== Résultats pour la méthode Online (FF) ==")
for wagon, details in ff_structure.items():
    print(f"\n{wagon}:")
    for rangee, objets in details.items():
        print(f"  {rangee}:")
        for objet, caracteristiques in objets.items():
            print(f"    {objet}: {caracteristiques}")

# Afficher les résultats pour la méthode Offline (FFD)
print("\n== Résultats pour la méthode Offline (FFD) ==")
for wagon, details in ffd_structure.items():
    print(f"\n{wagon}:")
    for rangee, objets in details.items():
        print(f"  {rangee}:")
        for objet, caracteristiques in objets.items():
            print(f"    {objet}: {caracteristiques}")

# Créer la structure JSON finale
output_data = {
    "d2": {
        "Online_FF": {
            "structure": ff_structure,
            "nombre_wagons": ff_conteneurs,
            "dimension_non_occupee": f"{ff_non_occupee} m²"
        },
        "Offline_FFD": {
            "structure": ffd_structure,
            "nombre_wagons": ffd_conteneurs,
            "dimension_non_occupee": f"{ffd_non_occupee} m²"
        }
    }
}

# Définir le chemin pour le fichier JSON
json_file_path = os.path.join(script_directory, "wagon_assignments_d2.json")

# Écrire les données dans le fichier JSON avec encodage UTF-8
with open(json_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(output_data, json_file, ensure_ascii=False, indent=4)

print(f"\nLes données des wagons ont été exportées dans le fichier {json_file_path}")
