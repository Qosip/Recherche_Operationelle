import openpyxl
import time

# Lire le fichier Excel
file_path = "Tableau_donnees_sac_a_dos_Velo.xlsx"  # Assurez-vous que le chemin du fichier est correct
wb = openpyxl.load_workbook(file_path)
sheet = wb.active

# Extraire les données
objects = []
for row in sheet.iter_rows(min_row=2, values_only=True):
    name, masse, utilite = row
    try:
        masse = float(str(masse).replace(',', '.'))
        utilite = float(str(utilite).replace(',', '.'))
        objects.append({
            "name": name,
            "masse": masse,
            "utilite": utilite
        })
    except ValueError:
        continue  # Ignore les lignes qui ne peuvent pas être converties en float

# Programmation dynamique pour le problème du sac à dos (Algorithme exact)
def knapsack_dp(objects, max_masse):
    n = len(objects)
    dp = [0] * (int(max_masse * 100) + 1)

    for obj in objects:
        masse = int(obj["masse"] * 100)
        utilite = obj["utilite"]
        for j in range(len(dp) - 1, masse - 1, -1):
            dp[j] = max(dp[j], dp[j - masse] + utilite)

    best_value = max(dp)
    best_combination = []
    w = dp.index(best_value)
    for i in range(n - 1, -1, -1):
        if w >= int(objects[i]["masse"] * 100) and dp[w] == dp[w - int(objects[i]["masse"] * 100)] + objects[i]["utilite"]:
            best_combination.append(objects[i])
            w -= int(objects[i]["masse"] * 100)

    return best_combination, best_value

# Algorithme heuristique (Glouton)
def knapsack_greedy(objects, max_masse):
    objects = sorted(objects, key=lambda x: x["utilite"] / x["masse"], reverse=True)
    total_masse = 0
    total_utilite = 0
    best_combination = []

    for obj in objects:
        if total_masse + obj["masse"] <= max_masse:
            best_combination.append(obj)
            total_masse += obj["masse"]
            total_utilite += obj["utilite"]

    return best_combination, total_utilite

# Résoudre le problème pour différentes valeurs de C et mesurer le temps de calcul
def solve_and_measure(objects, max_masse, algorithm):
    start_time = time.time()
    best_combination, best_value = algorithm(objects, max_masse)
    end_time = time.time()
    execution_time = end_time - start_time
    return best_combination, best_value, execution_time

C_values = [2, 3, 4, 5]

print("Algorithme exact (Programmation dynamique):")
for C in C_values:
    best_combination, best_value, exec_time = solve_and_measure(objects, C, knapsack_dp)
    print(f"\nPour C = {C}:")
    for obj in best_combination:
        print(f"{obj['name']} - Masse: {obj['masse']} - Utilité: {obj['utilite']}")
    print(f"Utilité totale: {best_value}")
    print(f"Temps d'exécution: {exec_time} secondes")

print("\nAlgorithme heuristique (Glouton):")
for C in C_values:
    best_combination, best_value, exec_time = solve_and_measure(objects, C, knapsack_greedy)
    print(f"\nPour C = {C}:")
    for obj in best_combination:
        print(f"{obj['name']} - Masse: {obj['masse']} - Utilité: {obj['utilite']}")
    print(f"Utilité totale: {best_value}")
    print(f"Temps d'exécution: {exec_time} secondes")
