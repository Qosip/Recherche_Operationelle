import time
from utils import read_excel_data
from exo_8 import knapsack

def main():
    # Lire les données à partir du fichier Excel
    file_path = 'Tableau_donnees_sac_a_dos_Velo.xlsx'
    objects = read_excel_data(file_path)

    # Préparer les données pour l'algorithme du sac à dos
    L = [(obj['masse'], obj['utilite']) for obj in objects]

    # Capacités à tester
    capacities = [2, 3, 4, 5]

    # Stocker les résultats
    results = []

    for C in capacities:
        # Mesurer le temps de calcul pour chaque capacité
        start_time = time.perf_counter()
        utilite_maximale, objets_choisis_indices = knapsack(L, C)
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time

        # Stocker le résultat pour cette capacité
        result = {
            "Capacité": C,
            "Utilité maximale": utilite_maximale,
            "Objets choisis": [objects[index]['name'] for index in objets_choisis_indices],
            "Temps de calcul (s)": elapsed_time
        }
        results.append(result)

    # Afficher les résultats
    for result in results:
        print(f"Capacité: {result['Capacité']}")
        print(f"Utilité maximale: {result['Utilité maximale']}")
        print("Objets choisis:")
        for obj in result["Objets choisis"]:
            print(f"- {obj}")
        print(f"Temps de calcul: {result['Temps de calcul (s)']:.6f} secondes")
        print()

if __name__ == "__main__":
    main()
