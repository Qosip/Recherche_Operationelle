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
hauteur_conteneur = 2.569  # Hauteur du conteneur

# Extraire les dimensions et désignations des marchandises dans l'ordre du fichier Excel
designations = marchandises_df['Désignation']
lengths = marchandises_df['Longueur']
widths = marchandises_df['Largeur']
heights = marchandises_df['Hauteur']  # Ajout de la hauteur

# Combiner les informations pertinentes dans une seule liste de tuples (désignation, longueur, largeur, hauteur)
cargo_items = list(zip(designations, lengths, widths, heights))

# Fonction pour remplir les conteneurs en 3D Online (FF) dans l'ordre des objets
def remplissage_3d_FF(objets):
    nb_conteneurs = 0
    volume_occupé = 0
    conteneurs = []

    json_structure = {}

    for objet_actuel in objets:
        designation, longueur, largeur, hauteur = objet_actuel
        placement = False
        
        for conteneur in conteneurs:
            for rangée in conteneur['rangées']:
                # Vérifier si l'objet peut être placé dans cette rangée (en termes de largeur, hauteur)
                if largeur <= rangée['largeur_disponible'] and hauteur <= rangée['hauteur_disponible']:
                    # Placer l'objet dans cette rangée
                    rangée['largeur_disponible'] -= largeur
                    rangée['hauteur_disponible'] -= hauteur
                    rangée['objets'].append({
                        "longueur": longueur,
                        "largeur": largeur,
                        "hauteur": hauteur,
                        "designation": designation
                    })
                    placement = True
                    volume_occupé += longueur * largeur * hauteur
                    break
            
            # Si l'objet n'a pas été placé dans une rangée existante, vérifier la longueur disponible dans le conteneur
            if not placement and longueur <= conteneur['longueur_disponible']:
                conteneur['rangées'].append({
                    "largeur_disponible": largeur_conteneur - largeur,
                    "hauteur_disponible": hauteur_conteneur - hauteur,
                    "objets": [{
                        "longueur": longueur,
                        "largeur": largeur,
                        "hauteur": hauteur,
                        "designation": designation
                    }]
                })
                conteneur['longueur_disponible'] -= longueur
                placement = True
                volume_occupé += longueur * largeur * hauteur
                break

        # Si l'objet n'a pas été placé, ajouter un nouveau conteneur
        if not placement:
            nb_conteneurs += 1
            conteneur = {
                "longueur_disponible": longueur_conteneur - longueur,
                "rangées": [{
                    "largeur_disponible": largeur_conteneur - largeur,
                    "hauteur_disponible": hauteur_conteneur - hauteur,
                    "objets": [{
                        "longueur": longueur,
                        "largeur": largeur,
                        "hauteur": hauteur,
                        "designation": designation
                    }]
                }]
            }
            conteneurs.append(conteneur)
            volume_occupé += longueur * largeur * hauteur

    # Préparer la structure JSON
    for i, conteneur in enumerate(conteneurs):
        wagon_name = f"wagon {i + 1}"
        wagon_structure = {}
        for j, rangée in enumerate(conteneur['rangées']):
            rangee_structure = {}
            for k, objet in enumerate(rangée['objets']):
                objet_structure = {
                    "longueur": objet["longueur"],
                    "largeur": objet["largeur"],
                    "hauteur": objet["hauteur"],
                    "designation": objet["designation"]
                }
                rangee_structure[f"objet {k + 1}"] = objet_structure
            wagon_structure[f"rangée {j + 1}"] = rangee_structure
        json_structure[wagon_name] = wagon_structure

    # Calculer le volume non occupé
    volume_non_occupe = nb_conteneurs * longueur_conteneur * largeur_conteneur * hauteur_conteneur - volume_occupé
    print(f"Il y a {nb_conteneurs} conteneurs et un volume inutilisé de {round(volume_non_occupe, 3)} m³.")

    return json_structure, nb_conteneurs, round(volume_non_occupe, 3)

# Fonction pour remplir les conteneurs en 3D Offline (FFD)
def remplissage_3d_FFD(objets):
    # Trier les objets par volume (longueur * largeur * hauteur) décroissant
    objets_trie = sorted(objets, key=lambda x: x[1] * x[2] * x[3], reverse=True)
    return remplissage_3d_FF(objets_trie)  # Réutiliser la logique de FF après tri

# Appel des fonctions pour remplir les conteneurs en 3D Online (FF) et Offline (FFD)
ff_structure, ff_conteneurs, ff_non_occupe = remplissage_3d_FF(cargo_items)
ffd_structure, ffd_conteneurs, ffd_non_occupe = remplissage_3d_FFD(cargo_items)

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
            "volume_non_occupe": f"{ff_non_occupe} m³"
        },
        "Offline_FFD": {
            "structure": ffd_structure,
            "nombre_wagons": ffd_conteneurs,
            "volume_non_occupe": f"{ffd_non_occupe} m³"
        }
    }
}

# Définir le chemin pour le fichier JSON
json_file_path = os.path.join(script_directory, "wagon_assignments_d2.json")

# Écrire les données dans le fichier JSON
with open(json_file_path, 'w') as json_file:
    json.dump(output_data, json_file, ensure_ascii=False, indent=4)

print(f"\nLes données des wagons ont été exportées dans le fichier {json_file_path}")
