import pandas as pd
import os
import json

# Obtenir le chemin absolu du répertoire du script Python
script_directory = os.path.dirname(os.path.abspath(__file__))

# Définir le chemin complet vers le fichier Excel a.xlsx
file_path = os.path.join(script_directory, "a.xlsx")

# Lire le fichier Excel
marchandises_df = pd.read_excel(file_path)

# Afficher un aperçu des données pour vérifier que le chargement a été effectué correctement
print(marchandises_df.head())

# Dimensions du conteneur (en mètres) - pour d=2, la longueur et la largeur sont pertinentes
container_length = 11.583
container_width = 2.294

# Extraire les longueurs, largeurs et désignations des marchandises
lengths = marchandises_df['Longueur']
widths = marchandises_df['Largeur']
designations = marchandises_df['Désignation']

# Combiner les informations pertinentes dans une seule liste de tuples (longueur, largeur, désignation)
cargo_items = list(zip(lengths, widths, designations))

# Fonction d'optimisation pour d=2 Offline avec FFD
def d2_ffd(cargo_items, container_length, container_width):
    # Trier les marchandises par surface décroissante
    sorted_items = sorted(cargo_items, key=lambda x: x[0] * x[1], reverse=True)
    wagons = []
    assignments = []  # Pour garder la trace des marchandises dans chaque wagon
    
    for length, width, designation in sorted_items:
        placed = False
        for i in range(len(wagons)):
            if wagons[i] + length * width <= container_length * container_width:
                wagons[i] += length * width
                assignments[i].append((length, width, designation))
                placed = True
                break
        if not placed:
            wagons.append(length * width)
            assignments.append([(length, width, designation)])
    
    # Calculer la surface non occupée
    used_space = sum(wagons)
    unused_space = container_length * container_width * len(wagons) - used_space
    
    return len(wagons), unused_space, assignments

# Fonction d'optimisation pour d=2 Online avec FF
def d2_ff(cargo_items, container_length, container_width):
    wagons = []
    assignments = []  # Pour garder la trace des marchandises dans chaque wagon
    
    for length, width, designation in cargo_items:
        placed = False
        for i in range(len(wagons)):
            if wagons[i] + length * width <= container_length * container_width:
                wagons[i] += length * width
                assignments[i].append((length, width, designation))
                placed = True
                break
        if not placed:
            wagons.append(length * width)
            assignments.append([(length, width, designation)])
    
    # Calculer la surface non occupée
    used_space = sum(wagons)
    unused_space = container_length * container_width * len(wagons) - used_space
    
    return len(wagons), unused_space, assignments

# Calculer le nombre de wagons nécessaires pour d=2 Offline (FFD) et Online (FF)
d2_offline_wagons, d2_offline_unused, d2_offline_assignments = d2_ffd(cargo_items, container_length, container_width)
d2_online_wagons, d2_online_unused, d2_online_assignments = d2_ff(cargo_items, container_length, container_width)

# Afficher les résultats pour d=2 Offline (FFD)
print(f"Nombre de wagons nécessaires (d=2 Offline avec FFD): {d2_offline_wagons}")
print(f"Surface non occupée pour d=2 Offline avec FFD: {d2_offline_unused:.2f} mètres carrés")
print("Combinaisons des marchandises dans les wagons (Offline avec FFD):")
for i, wagon in enumerate(d2_offline_assignments):
    print(f"Wagon {i + 1}: {wagon}")

# Afficher les résultats pour d=2 Online (FF)
print(f"Nombre de wagons nécessaires (d=2 Online avec FF): {d2_online_wagons}")
print(f"Surface non occupée pour d=2 Online avec FF: {d2_online_unused:.2f} mètres carrés")
print("Combinaisons des marchandises dans les wagons (Online avec FF):")
for i, wagon in enumerate(d2_online_assignments):
    print(f"Wagon {i + 1}: {wagon}")

# Créer une structure JSON selon le format demandé
def create_json_structure(assignments):
    json_data = {}
    for wagon_index, wagon in enumerate(assignments):
        wagon_key = f"wagon {wagon_index + 1}"
        json_data[wagon_key] = {}
        for obj_index, (length, width, designation) in enumerate(wagon):
            object_key = f"objet {obj_index + 1}"
            json_data[wagon_key][object_key] = {
                "longueur": length,
                "largeur": width,
                "designation": designation
            }
    return json_data

# Créer la structure JSON finale pour les wagons
output_data = {
    "d2": {
        "Offline_FFD": create_json_structure(d2_offline_assignments),
        "Online_FF": create_json_structure(d2_online_assignments)
    }
}

# Définir le chemin pour le fichier JSON
json_file_path = os.path.join(script_directory, "wagon_assignments_d2.json")

# Écrire les données dans le fichier JSON
with open(json_file_path, 'w') as json_file:
    json.dump(output_data, json_file, indent=4)

print(f"Les données des wagons ont été exportées dans le fichier {json_file_path}")
