from utils import read_excel_data

# Chemin vers le fichier Excel
file_path = "Tableau_donnees_sac_a_dos_Velo.xlsx"  # Remplacez par le chemin correct

# Lire les données du fichier Excel
objects = read_excel_data(file_path)


def knapsack_dp(objects, max_masse):
    n = len(objects)
    max_weight = int(max_masse * 100)
    dp = [0] * (max_weight + 1)
    keep = [[0] * (max_weight + 1) for _ in range(n)]

    for i in range(n):
        weight = int(objects[i]["masse"] * 100)
        value = objects[i]["utilite"]
        for j in range(max_weight, weight - 1, -1):
            if dp[j] < dp[j - weight] + value:
                dp[j] = dp[j - weight] + value
                keep[i][j] = 1

    best_value = max(dp)
    best_combination = []
    w = dp.index(best_value)

    for i in range(n - 1, -1, -1):
        if keep[i][w] == 1:
            best_combination.append(objects[i])
            w -= int(objects[i]["masse"] * 100)

    return best_combination, best_value


# Résoudre le problème pour C = 0.6
C = 0.6
best_combination, best_value = knapsack_dp(objects, C)

print(f"Meilleure combinaison pour C = {C}:")
for obj in best_combination:
    print(f"{obj['name']} - Masse: {obj['masse']} - Utilité: {obj['utilite']}")
print(f"Utilité totale: {best_value}")
