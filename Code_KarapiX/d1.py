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

# Extraire les longueurs des marchandises
lengths = marchandises_df['Longueur']

# Fonction d'optimisation pour d=1 Offline avec FFD
def d1_ffd(lengths, container_length):
    # Trier les marchandises par longueur décroissante
    sorted_lengths = sorted(lengths, reverse=True)
    wagons = []
    
    for length in sorted_lengths:
        # Trouver le premier wagon où la marchandise peut entrer
        placed = False
        for i in range(len(wagons)):
            if wagons[i] + length <= container_length:
                wagons[i] += length
                placed = True
                break
        # Si aucune place n'est trouvée, ajouter un nouveau wagon
        if not placed:
            wagons.append(length)
    
    # Calculer la dimension non occupée
    used_space = sum(wagons)
    unused_space = container_length * len(wagons) - used_space
    
    return len(wagons), unused_space

# Fonction d'optimisation pour d=1 Online avec FF
def d1_ff(lengths, container_length):
    wagons = []
    
    for length in lengths:
        # Trouver le premier wagon où la marchandise peut entrer
        placed = False
        for i in range(len(wagons)):
            if wagons[i] + length <= container_length:
                wagons[i] += length
                placed = True
                break
        # Si aucune place n'est trouvée, ajouter un nouveau wagon
        if not placed:
            wagons.append(length)
    
    # Calculer la dimension non occupée
    used_space = sum(wagons)
    unused_space = container_length * len(wagons) - used_space
    
    return len(wagons), unused_space

# Calculer le nombre de wagons nécessaires pour d=1 Offline (FFD) et Online (FF)
d1_offline_wagons, d1_offline_unused = d1_ffd(lengths, container_length)
d1_online_wagons, d1_online_unused = d1_ff(lengths, container_length)

print(f"Nombre de wagons nécessaires (d=1 Offline avec FFD): {d1_offline_wagons}")
print(f"Dimension non occupée pour d=1 Offline avec FFD: {d1_offline_unused:.2f} mètres carrés")

print(f"Nombre de wagons nécessaires (d=1 Online avec FF): {d1_online_wagons}")
print(f"Dimension non occupée pour d=1 Online avec FF: {d1_online_unused:.2f} mètres carrés")

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

# Évaluer la complexité pour d=1 Offline (FFD)
sizes_offline, times_offline = evaluate_time_complexity(lengths, container_length, d1_ffd)
print(f"Temps de calcul pour d=1 Offline avec FFD: {times_offline[-1]:.6f} secondes")

# Évaluer la complexité pour d=1 Online (FF)
sizes_online, times_online = evaluate_time_complexity(lengths, container_length, d1_ff)
print(f"Temps de calcul pour d=1 Online avec FF: {times_online[-1]:.6f} secondes")
