import pandas as pd
import os
import time
import json

# Fonctions d'optimisation pour d=3
def d3_offline_ffd(lengths, widths, heights, designations, container_length, container_width, container_height):
    # Trier les marchandises par volume décroissant
    sorted_goods = sorted(zip(lengths, widths, heights, designations), key=lambda x: x[0] * x[1] * x[2], reverse=True)
    wagons = []
    assignments = []
    current_volume = 0
    container_volume = container_length * container_width * container_height
    
    for length, width, height, designation in sorted_goods:
        volume = length * width * height
        placed = False
        for wagon in wagons:
            if wagon['volume'] + volume <= container_volume:
                wagon['volume'] += volume
                wagon['goods'].append((length, width, height, designation))
                placed = True
                break
        
        if not placed:
            new_wagon = {'volume': volume, 'goods': [(length, width, height, designation)]}
            wagons.append(new_wagon)
    
    return len(wagons), wagons

def d3_online(lengths, widths, heights, designations, container_length, container_width, container_height):
    wagons = []
    current_volume = 0
    container_volume = container_length * container_width * container_height
    
    for length, width, height, designation in zip(lengths, widths, heights, designations):
        volume = length * width * height
        placed = False
        for wagon in wagons:
            if wagon['volume'] + volume <= container_volume:
                wagon['volume'] += volume
                wagon['goods'].append((length, width, height, designation))
                placed = True
                break
        
        if not placed:
            new_wagon = {'volume': volume, 'goods': [(length, width, height, designation)]}
            wagons.append(new_wagon)
    
    return len(wagons), wagons

def display_results_d3(d3_offline_wagons, d3_online_wagons):
    print(f"Nombre de wagons nécessaires (d=3 Offline FFD): {d3_offline_wagons}")
    print(f"Nombre de wagons nécessaires (d=3 Online): {d3_online_wagons}")

# Fonction pour évaluer la complexité temporelle
def evaluate_time_complexity_d3(lengths, widths, heights, designations, container_length, container_width, container_height, offline_function, online_function):
    times_offline = []
    times_online = []
    sizes = []
    
    for size in range(100, len(lengths) + 1, 100):
        subset_lengths = lengths[:size]
        subset_widths = widths[:size]
        subset_heights = heights[:size]
        subset_designations = designations[:size]
        
        # Mesurer le temps pour la fonction offline
        start_time_offline = time.time()
        offline_function(subset_lengths, subset_widths, subset_heights, subset_designations, container_length, container_width, container_height)
        end_time_offline = time.time()
        times_offline.append(end_time_offline - start_time_offline)
        
        # Mesurer le temps pour la fonction online
        start_time_online = time.time()
        online_function(subset_lengths, subset_widths, subset_heights, subset_designations, container_length, container_width, container_height)
        end_time_online = time.time()
        times_online.append(end_time_online - start_time_online)
        
        sizes.append(size)
    
    return sizes, times_offline, times_online

# Fonction pour créer la structure JSON
def create_json_structure(assignments):
    json_data = {}
    for wagon_index, wagon in enumerate(assignments):
        wagon_key = f"wagon {wagon_index + 1}"
        json_data[wagon_key] = {}
        for obj_index, (length, width, height, designation) in enumerate(wagon['goods']):
            object_key = f"objet {obj_index + 1}"
            json_data[wagon_key][object_key] = {
                "longueur": length,
                "largeur": width,
                "hauteur": height,
                "designation": designation
            }
    return json_data

if __name__ == "__main__":
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
    container_width = 2.294
    container_height = 2.569

    # Extraire les dimensions et désignations des marchandises
    lengths = marchandises_df['Longueur']
    widths = marchandises_df['Largeur']
    heights = marchandises_df['Hauteur']
    designations = marchandises_df['Désignation']

    # Calculer le nombre de wagons nécessaires pour d=3 Offline FFI et Online
    d3_offline_wagons, d3_offline_assignments = d3_offline_ffd(lengths, widths, heights, designations, container_length, container_width, container_height)
    d3_online_wagons, d3_online_assignments = d3_online(lengths, widths, heights, designations, container_length, container_width, container_height)

    # Afficher les résultats pour d=3
    display_results_d3(d3_offline_wagons, d3_online_wagons)

    # Calculer l'espace non utilisé pour d=3
    total_volume = container_length * container_width * container_height
    used_volume_offline = sum(wagon['volume'] for wagon in d3_offline_assignments)
    unused_volume_offline = (d3_offline_wagons * total_volume) - used_volume_offline

    used_volume_online = sum(wagon['volume'] for wagon in d3_online_assignments)
    unused_volume_online = (d3_online_wagons * total_volume) - used_volume_online

    print(f"Espace non utilisé pour d=3 Offline FFD : {unused_volume_offline:.2f} m³")
    print(f"Espace non utilisé pour d=3 Online : {unused_volume_online:.2f} m³")

    # Évaluer la complexité temporelle pour d=3 Offline FFI et Online
    sizes, times_offline, times_online = evaluate_time_complexity_d3(lengths, widths, heights, designations, container_length, container_width, container_height, d3_offline_ffd, d3_online)

    # Afficher les temps de calcul pour d=3 Offline FFD et Online
    print("Temps de calcul pour d=3 Offline FFD :")
    for size, time_offline in zip(sizes, times_offline):
        print(f"Taille du subset : {size}, Temps : {time_offline:.6f} secondes")

    print("Temps de calcul pour d=3 Online :")
    for size, time_online in zip(sizes, times_online):
        print(f"Taille du subset : {size}, Temps : {time_online:.6f} secondes")

    # Créer la structure JSON finale pour les wagons
    output_data = {
        "d3": {
            "Offline_FFD": create_json_structure(d3_offline_assignments),
            "Online_FF": create_json_structure(d3_online_assignments)
        }
    }

    # Définir le chemin pour le fichier JSON
    json_file_path = os.path.join(script_directory, "wagon_assignments_d3.json")

    # Écrire les données dans le fichier JSON
    with open(json_file_path, 'w') as json_file:
        json.dump(output_data, json_file, indent=4)

    print(f"Les données des wagons ont été exportées dans le fichier {json_file_path}")
