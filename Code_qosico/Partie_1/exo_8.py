import openpyxl
from utils import read_excel_data  # Remplacez 'your_module' par le nom du module où se trouve votre fonction

def knapsack(L, C):
    """
    Résout le problème du sac à dos en utilisant un algorithme exact (Programmation Dynamique).

    Arguments :
    L : liste de tuples où chaque tuple représente un objet avec (poids, utilité)
    C : capacité maximale du sac à dos

    Retourne :
    (utilité maximale, liste des indices des objets choisis)
    """
    N = len(L)
    # Convertir les poids en entiers en multipliant par 100
    C = int(C * 100)
    L = [(int(weight * 100), value) for weight, value in L]

    # Initialisation de la matrice K avec des zéros
    K = [[0 for _ in range(C + 1)] for _ in range(N + 1)]

    # Remplissage de la matrice K
    for i in range(1, N + 1):
        for w in range(C + 1):
            if L[i-1][0] <= w:
                K[i][w] = max(L[i-1][1] + K[i-1][w-L[i-1][0]], K[i-1][w])
            else:
                K[i][w] = K[i-1][w]

    # Extraction de la solution optimale
    w = C
    objets_choisis = []
    for i in range(N, 0, -1):
        if K[i][w] != K[i-1][w]:
            objets_choisis.append(i-1)
            w -= L[i-1][0]

    # Retourner l'utilité maximale et la liste des objets choisis
    return K[N][C], objets_choisis

# Lire les données à partir du fichier Excel
file_path = 'Tableau_donnees_sac_a_dos_Velo.xlsx'  # Remplacez par le chemin correct vers votre fichier
objects = read_excel_data(file_path)

# Préparer les données pour l'algorithme du sac à dos
L = [(obj['masse'], obj['utilite']) for obj in objects]
C = 0.6  # Par exemple, la capacité maximale du sac à dos

# Résoudre le problème du sac à dos
utilite_maximale, objets_choisis_indices = knapsack(L, C)

# Afficher les résultats
print("Utilité maximale :", utilite_maximale)
print("Objets choisis :")
for index in objets_choisis_indices:
    print(objects[index]['name'])
