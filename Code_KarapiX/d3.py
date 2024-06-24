import pandas as pd
import os
import time

# Fonctions d'optimisation pour d=3
def d3_offline_ffd(lengths, widths, heights, container_length, container_width, container_height):
    sorted_goods = sorted(zip(lengths, widths, heights), key=lambda x: x[0] * x[1] * x[2])
    wagons = 0
    current_volume = 0
    container_volume = container_length * container_width * container_height

    for length, width, height in sorted_goods:
        volume = length * width * height
        if current_volume + volume <= container_volume:
            current_volume += volume
        else:
            wagons += 1
            current_volume = volume

    if current_volume > 0:
        wagons += 1

    return wagons

def d3_online(lengths, widths, heights, container_length, container_width, container_height):
    wagons = 0
    current_volume = 0
    container_volume = container_length * container_width * container_height

    for length, width, height in zip(lengths, widths, heights):
        volume = length * width * height
        if current_volume + volume <= container_volume:
            current_volume += volume
        else:
            wagons += 1
            current_volume = volume

    if current_volume > 0:
        wagons += 1

    return wagons

def display_results_d3(d3_offline_wagons, d3_online_wagons):
    print(f"Nombre de wagons nécessaires (d=3 Offline FFD): {d3_offline_wagons}")
    print(f"Nombre de wagons nécessaires (d=3 Online): {d3_online_wagons}")

def evaluate_time_complexity_d3(lengths, widths, heights, container_length, container_width, container_height, offline_function, online_function):
    times_offline = []
    times_online = []
    sizes = []
    
    for size in range(100, len(lengths) + 1, 100):
        subset_lengths = lengths[:size]
        subset_widths = widths[:size]
        subset_heights = heights[:size]
        
        # Measure time for offline function
        start_time_offline = time.time()
        offline_function(subset_lengths, subset_widths, subset_heights, container_length, container_width, container_height)
        end_time_offline = time.time()
        times_offline.append(end_time_offline - start_time_offline)
        
        # Measure time for online function
        start_time_online = time.time()
        online_function(subset_lengths, subset_widths, subset_heights, container_length, container_width, container_height)
        end_time_online = time.time()
        times_online.append(end_time_online - start_time_online)
        
        sizes.append(size)
    
    return sizes, times_offline, times_online

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

    # Extraire les dimensions des marchandises
    lengths = marchandises_df['Longueur']
    widths = marchandises_df['Largeur']
    heights = marchandises_df['Hauteur']

    # Calculer le nombre de wagons nécessaires pour d=3 Offline FFI et Online
    d3_offline_wagons = d3_offline_ffd(lengths, widths, heights, container_length, container_width, container_height)
    d3_online_wagons = d3_online(lengths, widths, heights, container_length, container_width, container_height)

    # Afficher les résultats pour d=3
    display_results_d3(d3_offline_wagons, d3_online_wagons)

    # Calculer l'espace non utilisé pour d=3
    total_volume = container_length * container_width * container_height
    used_volume = d3_offline_wagons * total_volume
    unused_volume = total_volume - used_volume

    print(f"Espace non utilisé pour d=3 : {unused_volume:.2f} m³")

    # Évaluer la complexité temporelle pour d=3 Offline FFI et Online
    sizes, times_offline, times_online = evaluate_time_complexity_d3(lengths, widths, heights, container_length, container_width, container_height, d3_offline_ffd, d3_online)

    # Afficher les temps de calcul pour d=3 Offline FFI et Online
    print("Temps de calcul pour d=3 Offline FFD :")
    for size, time_offline in zip(sizes, times_offline):
        print(f"Taille du subset : {size}, Temps : {time_offline:.6f} secondes")

    print("Temps de calcul pour d=3 Online :")
    for size, time_online in zip(sizes, times_online):
        print(f"Taille du subset : {size}, Temps : {time_online:.6f} secondes")
