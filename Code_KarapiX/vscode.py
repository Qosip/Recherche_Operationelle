import pandas as pd
import os
import time

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

# Fonctions pour d=1 Offline et Online
def d1_offline(lengths, container_length):
    sorted_lengths = sorted(lengths, reverse=True)
    wagons = 0
    current_length = 0

    for length in sorted_lengths:
        if current_length + length <= container_length:
            current_length += length
        else:
            wagons += 1
            current_length = length

    if current_length > 0:
        wagons += 1

    return wagons

def d1_online(lengths, container_length):
    wagons = 0
    current_length = 0

    for length in lengths:
        if current_length + length <= container_length:
            current_length += length
        else:
            wagons += 1
            current_length = length

    if current_length > 0:
        wagons += 1

    return wagons

# Fonctions pour d=2 Offline (FFI) et Online
def d2_offline_ffi(lengths, widths, container_length, container_width):
    sorted_goods = sorted(zip(lengths, widths), key=lambda x: x[0] * x[1])
    wagons = 0
    current_length = 0
    current_width = 0

    for length, width in sorted_goods:
        if current_length + length <= container_length and current_width + width <= container_width:
            current_length += length
            current_width += width
        else:
            wagons += 1
            current_length = length
            current_width = width

    if current_length > 0 or current_width > 0:
        wagons += 1

    return wagons

def d2_online(lengths, widths, container_length, container_width):
    wagons = 0
    current_length = 0
    current_width = 0

    for length, width in zip(lengths, widths):
        if current_length + length <= container_length and current_width + width <= container_width:
            current_length += length
            current_width += width
        else:
            wagons += 1
            current_length = length
            current_width = width

    if current_length > 0 or current_width > 0:
        wagons += 1

    return wagons

# Fonctions pour d=3 Offline (FFI) et Online
def d3_offline_ffi(lengths, widths, heights, container_length, container_width, container_height):
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

# Calculer le nombre de wagons nécessaires pour chaque cas
d1_offline_wagons = d1_offline(lengths, container_length)
d1_online_wagons = d1_online(lengths, container_length)

print(f"Nombre de wagons nécessaires (d=1 Offline): {d1_offline_wagons}")
print(f"Nombre de wagons nécessaires (d=1 Online): {d1_online_wagons}")

d2_offline_wagons = d2_offline_ffi(lengths, widths, container_length, container_width)
d2_online_wagons = d2_online(lengths, widths, container_length, container_width)

print(f"Nombre de wagons nécessaires (d=2 Offline FFI): {d2_offline_wagons}")
print(f"Nombre de wagons nécessaires (d=2 Online): {d2_online_wagons}")

d3_offline_wagons = d3_offline_ffi(lengths, widths, heights, container_length, container_width, container_height)
d3_online_wagons = d3_online(lengths, widths, heights, container_length, container_width, container_height)

print(f"Nombre de wagons nécessaires (d=3 Offline FFI): {d3_offline_wagons}")
print(f"Nombre de wagons nécessaires (d=3 Online): {d3_online_wagons}")

# Fonction pour évaluer la complexité temporelle
def evaluate_time_complexity_d1(lengths, container_length, function):
    times = []
    sizes = []
    for size in range(100, len(lengths) + 1, 100):
        subset = lengths[:size]
        start_time = time.time()
        function(subset, container_length)
        end_time = time.time()
        times.append(end_time - start_time)
        sizes.append(size)
    return sizes, times

def evaluate_time_complexity_d2(lengths, widths, container_length, container_width, function):
    times = []
    sizes = []
    for size in range(100, len(lengths) + 1, 100):
        subset_lengths = lengths[:size]
        subset_widths = widths[:size]
        start_time = time.time()
        function(subset_lengths, subset_widths, container_length, container_width)
        end_time = time.time()
        times.append(end_time - start_time)
        sizes.append(size)
    return sizes, times

def evaluate_time_complexity_d3(lengths, widths, heights, container_length, container_width, container_height, function):
    times = []
    sizes = []
    for size in range(100, len(lengths) + 1, 100):
        subset_lengths = lengths[:size]
        subset_widths = widths[:size]
        subset_heights = heights[:size]
        start_time = time.time()
        function(subset_lengths, subset_widths, subset_heights, container_length, container_width, container_height)
        end_time = time.time()
        times.append(end_time - start_time)
        sizes.append(size)
    return sizes, times

# Évaluer la complexité pour chaque cas
sizes_offline_d1, times_offline_d1 = evaluate_time_complexity_d1(lengths, container_length, d1_offline)
sizes_online_d1, times_online_d1 = evaluate_time_complexity_d1(lengths, container_length, d1_online)

sizes_offline_d2, times_offline_d2 = evaluate_time_complexity_d2(lengths, widths, container_length, container_width, d2_offline_ffi)
sizes_online_d2, times_online_d2 = evaluate_time_complexity_d2(lengths, widths, container_length, container_width, d2_online)

sizes_offline_d3, times_offline_d3 = evaluate_time_complexity_d3(lengths, widths, heights, container_length, container_width, container_height, d3_offline_ffi)
sizes_online_d3, times_online_d3 = evaluate_time_complexity_d3(lengths, widths, heights, container_length, container_width, container_height, d3_online)

# Afficher les temps de calcul
print(f"Temps de calcul pour d=1 Offline: {times_offline_d1[-1]:.6f} secondes")
print(f"Temps de calcul pour d=1 Online: {times_online_d1[-1]:.6f} secondes")

print(f"Temps de calcul pour d=2 Offline FFI: {times_offline_d2[-1]:.6f} secondes")
print(f"Temps de calcul pour d=2 Online: {times_online_d2[-1]:.6f} secondes")

print(f"Temps de calcul pour d=3 Offline FFI: {times_offline_d3[-1]:.6f} secondes")
print(f"Temps de calcul pour d=3 Online: {times_online_d3[-1]:.6f} secondes")
