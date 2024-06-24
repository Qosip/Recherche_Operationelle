# Importation des modules nécessaires
import time
from utils import read_excel_data  # Assurez-vous que read_excel_data est correctement définie


# Définition de l'algorithme heuristique B pour le problème du sac à dos
def heuristique_sac_a_dos(L, C):
    """
    Résout le problème du sac à dos en utilisant une heuristique basée sur le rapport utilité/poids.

    Arguments :
    L : liste de tuples où chaque tuple représente un objet avec (poids, utilité)
    C : capacité maximale du sac à dos

    Retourne :
    (utilité totale, liste des indices des objets choisis)
    """
    # Calcul des rapports utilité/poids
    rapports = [(i, obj[1] / obj[0]) for i, obj in enumerate(L)]

    # Tri des objets par ordre décroissant de leur rapport utilité/poids
    rapports.sort(key=lambda x: x[1], reverse=True)

    poids_total = 0
    utilite_totale = 0
    objets_choisis = []

    # Sélection des objets
    for i, _ in rapports:
        poids, utilite = L[i]
        if poids_total + poids <= C:
            objets_choisis.append(i)
            poids_total += poids
            utilite_totale += utilite

    return utilite_totale, objets_choisis


# Fonction pour mesurer le temps d'exécution pour chaque valeur de C
def measure_execution_time(L, capacities):
    times = {}

    for C in capacities:
        start_time = time.perf_counter()
        utilite_maximale, objets_choisis_indices = heuristique_sac_a_dos(L, C)
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        times[C] = execution_time, utilite_maximale, objets_choisis_indices

    return times


# Fonction principale pour exécuter le script
def main():
    # Chemin vers votre fichier Excel
    file_path = "Tableau_donnees_sac_a_dos_Velo.xlsx"

    # Lecture des données à partir du fichier Excel en utilisant la fonction read_excel_data
    data = read_excel_data(file_path)

    # Extraction des masses et utilités sous forme de listes de tuples (masse, utilité)
    L = [(obj['masse'], obj['utilite']) for obj in data]

    # Capacités pour lesquelles nous voulons résoudre le problème du sac à dos
    capacities = [2, 3, 4, 5]

    # Mesure du temps d'exécution pour chaque valeur de C
    times = measure_execution_time(L, capacities)

    # Affichage des résultats
    for C in capacities:
        execution_time, utilite_maximale, objets_choisis_indices = times[C]
        print(f"Pour C = {C}:")
        print(f"   Utilité maximale : {utilite_maximale}")
        print(f"   Objets choisis :")
        for indice in objets_choisis_indices:
            print(f"      {data[indice]['name']}")
        print(f"   Temps d'exécution : {execution_time:.6f} secondes")
        print()


# Vérification si le script est exécuté en tant que programme principal
if __name__ == "__main__":
    main()
