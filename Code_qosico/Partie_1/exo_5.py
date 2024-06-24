from utils import read_excel_data
from measure_time import measure_time

def algorithme_glouton(objets, C):
    # Trier les objets par utilité/poids décroissant
    objets_triees = sorted(objets, key=lambda x: x['utilite'] / x['masse'], reverse=True)

    sac = []
    poids_total = 0

    for objet in objets_triees:
        if poids_total + objet['masse'] <= C:
            sac.append(objet)
            poids_total += objet['masse']

    return sac

# Lire les données du fichier Excel
fichier = 'Tableau_donnees_sac_a_dos_Velo.xlsx'
objets = read_excel_data(fichier)

# Capacité maximale du sac à dos
C = 5

# Fonction à mesurer
def execute_glouton():
    algorithme_glouton(objets, C)

# Valeurs de n pour les tests
n_values = [10, 100, 1000, 10000]

# Mesurer le temps avec répétitions
times = measure_time(execute_glouton, n_values=n_values, repetitions=5)

# Calculer le nombre total d'organisations possibles
N = len(objets)
total_organisations = 2 ** N

# Utiliser le temps moyen pour la plus grande valeur de n pour estimer le temps total
avg_time_per_operation = times[n_values[-1]]

# Calculer le temps total nécessaire en secondes
total_time_seconds = total_organisations * avg_time_per_operation

# Convertir le temps total en heures, minutes et secondes
total_time_hours = total_time_seconds / 3600
total_time_minutes = (total_time_seconds % 3600) / 60
total_time_remaining_seconds = total_time_seconds % 60

# Afficher les résultats
print(f"Nombre total d'organisations possibles: {total_organisations}")
print(f"Temps moyen par opération: {avg_time_per_operation:.10f} secondes")
print(f"Temps total estimé pour tester toutes les organisations: {total_time_hours:.10f} heures, soit {total_time_minutes:.10f} minutes, soit {total_time_remaining_seconds:.10f} secondes")
