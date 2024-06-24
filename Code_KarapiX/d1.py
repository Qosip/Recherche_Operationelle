import pandas as pd
import os
import time
import json

# Obtenir le chemin absolu du répertoire du script Python
script_directory = os.path.dirname(os.path.abspath(__file__))

# Définir le chemin complet vers le fichier Excel a.xlsx
file_path = os.path.join(script_directory, "a.xlsx")

# Lire le fichier Excel
marchandises_df = pd.read_excel(file_path)

# Afficher un aperçu des données pour vérifier que le chargement a été effectué correctement
print(marchandises_df.head())

# Dimensions du conteneur (en mètres)
container_length = 11.583

# Extraire les longueurs, largeurs, hauteurs et désignations des marchandises
lengths = marchandises_df['Longueur']
widths = marchandises_df['Largeur']
heights = marchandises_df['Hauteur']
designations = marchandises_df['Désignation']

# Combiner les informations dans une seule liste de tuples
cargo_items = list(zip(lengths, widths, heights, designations))

# Fonction d'optimisation pour d=1 Offline avec FFD
def d1_ffd(cargo_items, container_length):
    # Trier les marchandises par longueur décroissante
    sorted_items = sorted(cargo_items, key=lambda x: x[0], reverse=True)
    wagons = []
    assignments = []  # Pour garder la trace des marchandises dans chaque wagon
    
    for length, width, height, designation in sorted_items:
        # Trouver le premier wagon où la marchandise peut entrer
        placed = False
        for i in range(len(wagons)):
            if wagons[i] + length <= container_length:
                wagons[i] += length
                assignments[i].append((length, width, height, designation))
                placed = True
                break
        # Si aucune place n'est trouvée, ajouter un nouveau wagon
        if not placed:
            wagons.append(length)
            assignments.append([(length, width, height, designation)])
    
    # Calculer la dimension non occupée
    used_space = sum(wagons)
    unused_space = container_length * len(wagons) - used_space
    
    return len(wagons), unused_space, assignments

# Fonction d'optimisation pour d=1 Online avec FF
def d1_ff(cargo_items, container_length):
    wagons = []
    assignments = []  # Pour garder la trace des marchandises dans chaque wagon
    
    for length, width, height, designation in cargo_items:
        # Trouver le premier wagon où la marchandise peut entrer
        placed = False
        for i in range(len(wagons)):
            if wagons[i] + length <= container_length:
                wagons[i] += length
                assignments[i].append((length, width, height, designation))
                placed = True
                break
        # Si aucune place n'est trouvée, ajouter un nouveau wagon
        if not placed:
            wagons.append(length)
            assignments.append([(length, width, height, designation)])
    
    # Calculer la dimension non occupée
    used_space = sum(wagons)
    unused_space = container_length * len(wagons) - used_space
    
    return len(wagons), unused_space, assignments

# Calculer le nombre de wagons nécessaires pour d=1 Offline (FFD) et Online (FF)
d1_offline_wagons, d1_offline_unused, d1_offline_assignments = d1_ffd(cargo_items, container_length)
d1_online_wagons, d1_online_unused, d1_online_assignments = d1_ff(cargo_items, container_length)

# Afficher les résultats pour d=1 Offline (FFD)
print(f"Nombre de wagons nécessaires (d=1 Offline avec FFD): {d1_offline_wagons}")
print(f"Dimension non occupée pour d=1 Offline avec FFD: {d1_offline_unused:.2f} mètres carrés")
print("Combinaisons des marchandises dans les wagons (Offline avec FFD):")
for i, wagon in enumerate(d1_offline_assignments):
    print(f"Wagon {i + 1}: {wagon}")

# Afficher les résultats pour d=1 Online (FF)
print(f"Nombre de wagons nécessaires (d=1 Online avec FF): {d1_online_wagons}")
print(f"Dimension non occupée pour d=1 Online avec FF: {d1_online_unused:.2f} mètres carrés")
print("Combinaisons des marchandises dans les wagons (Online avec FF):")
for i, wagon in enumerate(d1_online_assignments):
    print(f"Wagon {i + 1}: {wagon}")

# Créer une structure JSON selon le format demandé
def create_json_structure(assignments):
    json_data = {}
    for wagon_index, wagon in enumerate(assignments):
        wagon_key = f"wagon {wagon_index + 1}"
        json_data[wagon_key] = {}
        for obj_index, (length, width, height, designation) in enumerate(wagon):
            object_key = f"objet {obj_index + 1}"
            json_data[wagon_key][object_key] = {
                "longueur": length,
                "largeur": width,
                "hauteur": height,
                "designation": designation
            }
    return json_data

# Créer la structure JSON finale pour les wagons
output_data = {
    "d1": {
        "Offline_FFD": create_json_structure(d1_offline_assignments),
        "Online_FF": create_json_structure(d1_online_assignments)
    }
}

# Définir le chemin pour le fichier JSON
json_file_path = os.path.join(script_directory, "wagon_assignments.json")

# Écrire les données dans le fichier JSON
with open(json_file_path, 'w') as json_file:
    json.dump(output_data, json_file, indent=4)

print(f"Les données des wagons ont été exportées dans le fichier {json_file_path}")
