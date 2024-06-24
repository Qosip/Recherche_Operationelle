import math
from utils import read_excel_data

# Chemin vers le fichier Excel
file_path = "Tableau_donnees_sac_a_dos_Velo.xlsx"  # Remplacez par le chemin correct

# Lire les données du fichier Excel
objects = read_excel_data(file_path)

# Nombre total d'objets
total_objects = len(objects)

# Fonction pour calculer les combinaisons
def comb(n, k):
    return math.comb(n, k)

# Calcul des combinaisons pour N = 1, 2, 10, 23
N_values = [1, 2, 10, 23]
combinations = {N: comb(total_objects, N) for N in N_values}

# Affichage des résultats
for N in N_values:
    print(f"Nombre de sacs à dos contenant {N} objets: {combinations[N]}")
