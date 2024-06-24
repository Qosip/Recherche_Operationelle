import pandas as pd

# Charger les données depuis le fichier Excel
file_path = "/mnt/data/Données marchandises.xlsx"

# Lire le fichier Excel
marchandises_df = pd.read_excel(file_path)

# Afficher un aperçu des données
marchandises_df.head()

# Charger les données
import pandas as pd

file_path = "/mnt/data/Données marchandises.xlsx"

# Lire le fichier Excel
marchandises_df = pd.read_excel(file_path)

# Dimensions du conteneur (en mètres)
container_length = 11.583

# Extraire les longueurs des marchandises
lengths = marchandises_df['Longueur']


# Fonction pour d=1 Offline
def d1_offline(lengths, container_length):
    # Trier les marchandises par longueur décroissante
    sorted_lengths = sorted(lengths, reverse=True)

    wagons = 0
    current_length = 0

    for length in sorted_lengths:
        if current_length + length <= container_length:
            current_length += length
        else:
            wagons += 1
            current_length = length

    # Ajouter le dernier wagon utilisé
    if current_length > 0:
        wagons += 1

    return wagons


# Fonction pour d=1 Online
def d1_online(lengths, container_length):
    wagons = 0
    current_length = 0

    for length in lengths:
        if current_length + length <= container_length:
            current_length += length
        else:
            wagons += 1
            current_length = length

    # Ajouter le dernier wagon utilisé
    if current_length > 0:
        wagons += 1

    return wagons


# Calculer le nombre de wagons nécessaires pour d=1 Offline et Online
d1_offline_wagons = d1_offline(lengths, container_length)
d1_online_wagons = d1_online(lengths, container_length)

d1_offline_wagons, d1_online_wagons

import time


# Fonction pour évaluer la complexité temporelle
def evaluate_time_complexity(lengths, container_length, function):
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


# Évaluer la complexité pour d=1 Offline et Online
sizes_offline, times_offline = evaluate_time_complexity(lengths, container_length, d1_offline)
sizes_online, times_online = evaluate_time_complexity(lengths, container_length, d1_online)

sizes_offline, times_offline, sizes_online, times_online

import matplotlib.pyplot as plt

# Tracer les temps de calcul
plt.figure(figsize=(12, 6))
plt.plot(sizes_offline, times_offline, label='d=1 Offline')
plt.plot(sizes_online, times_online, label='d=1 Online')
plt.xlabel('Nombre de marchandises')
plt.ylabel('Temps de calcul (secondes)')
plt.title('Complexité temporelle pour d=1')
plt.legend()
plt.grid(True)
plt.show()
