import time
from utils import read_excel_data

# Algorithme B' approché
def heuristique_sac_a_dos_approche(L, C):
    # Calcul des rapports utilité/poids et tri
    rapports = sorted(((i, obj["utilite"] / obj["masse"], obj["masse"], obj["utilite"]) for i, obj in enumerate(L)),
                      key=lambda x: x[1], reverse=True)
    poids_total = 0
    utilite_totale = 0
    objets_choisis = []

    # Sélection des objets
    for i, _, poids, utilite in rapports:
        if poids_total + poids <= C:
            objets_choisis.append(i)
            poids_total += poids
            utilite_totale += utilite
    return utilite_totale, objets_choisis

# Fonction pour mesurer le temps d'exécution
def measure_execution_time(algo_func, L, C, repetitions=5):
    total_time = 0
    for _ in range(repetitions):
        start_time = time.perf_counter()
        algo_func(L, C)
        end_time = time.perf_counter()
        total_time += end_time - start_time
    return total_time / repetitions

# Fonction principale pour comparer les algorithmes
def main():
    file_path = 'Tableau_donnees_sac_a_dos_Velo.xlsx'
    capacities = [2, 3, 4, 5]

    # Lecture des données depuis le fichier Excel
    objects = read_excel_data(file_path)

    # Comparaison pour différentes capacités C
    for C in capacities:
        # Mesure du temps pour l'algorithme B' approché
        approche_time = measure_execution_time(heuristique_sac_a_dos_approche, objects, C)

        # Affichage des résultats
        print(f"Capacité C = {C}:")
        print(f"Temps d'exécution (approché B') : {approche_time:.6f} secondes")
        print()

if __name__ == "__main__":
    main()
