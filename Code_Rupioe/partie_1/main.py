# Imports :
import pulp
import time
import pandas as pd


## Partie 1 :


# Question 1 :
# Execution in a Python environment
N_values = [1, 2, 10, 23]

# Calculating the number of combinations for each N
combinations = {N: 2**N for N in N_values}

print("Question 1",combinations)



# Question 2 :

# Nombre total de combinaisons pour 23 objets
N = 23
total_combinations = 2**N

print("Question 2:",total_combinations)



# Question 3 :

# Liste d'objets avec poids et utilités
objets = [
    {"poids": 0.1, "utilite": 10},
    {"poids": 0.2, "utilite": 20},
    {"poids": 0.3, "utilite": 30},
    {"poids": 0.4, "utilite": 40}
]

# Capacité maximale du sac à dos
C = 0.6

# Création du problème de maximisation
prob = pulp.LpProblem("Maximisation_de_l_utilite", pulp.LpMaximize)

# Variables de décision : prendre[o] vaut 1 si l'objet o est dans le sac, 0 sinon
prendre = pulp.LpVariable.dicts("prendre", range(len(objets)), cat='Binary')

# Fonction objectif : maximiser la somme des utilités des objets dans le sac
prob += pulp.lpSum([objets[o]["utilite"] * prendre[o] for o in range(len(objets))])

# Contrainte de poids : la somme des poids des objets dans le sac ne doit pas dépasser C
prob += pulp.lpSum([objets[o]["poids"] * prendre[o] for o in range(len(objets))]) <= C

# Résolution du problème
prob.solve()

# Extraction des résultats
resultats = [pulp.value(prendre[o]) for o in range(len(objets))]
utilite_totale = pulp.value(prob.objective)

print("Question 3 :",resultats, utilite_totale)



# Question 4 :
print("Question 4 : Algorithme sur papier :")
print("")
print("    Initialiser une variable somme à 0.")
print("    Pour chaque entier ii allant de 1 à NN:")
print("        Ajouter ii à somme.")
print("    Retourner somme.")

print("Le nombre d'opérations de l'algorithme est NN additions et NN incrémentations, donc 2N2N opérations.")




# Question 5 :

# Fonction pour calculer la somme des N premiers entiers
def somme_des_premiers_entiers(N):
    somme = 0
    for i in range(1, N + 1):
        somme += i
    return somme

# Fonction pour mesurer le temps de calcul
def mesure_temps(N):
    start_time = time.time()
    somme_des_premiers_entiers(N)
    end_time = time.time()
    return end_time - start_time

print("Question 5 :")

# Tester pour différentes valeurs de N
N_values = [10, 100, 1000, 10000, 100000]
temps_de_calcul = {N: mesure_temps(N) for N in N_values}

# Créer un DataFrame pour les temps de calcul
df_temps_de_calcul = pd.DataFrame(list(temps_de_calcul.items()), columns=['N', 'Temps (s)'])
print("Temps de Calcul :")
print(df_temps_de_calcul)

# Calcul de la durée moyenne par opération
durée_par_opération = {N: temps_de_calcul[N] / (2 * N) for N in N_values}

# Créer un DataFrame pour la durée par opération
df_durée_par_opération = pd.DataFrame(list(durée_par_opération.items()), columns=['N', 'Durée par opération (s)'])
print("\nDurée par Opération :")
print(df_durée_par_opération)




# Question 6 :
# Durée moyenne par opération (approximée à partir des résultats précédents)
T_moyen = sum(durée_par_opération.values()) / len(durée_par_opération)

# Nombre total de combinaisons pour 23 objets
total_combinations = 2**23

# Temps total nécessaire pour tester toutes les combinaisons
temps_total = T_moyen * total_combinations

print("Question 6 : ",temps_total)


# Question 7 :
# Papier
# Partie 7 : Algorithme exact pour la résolution du problème du sac à dos (A)

print("Un algorithme exact pour résoudre le problème du sac à dos peut être réalisé en utilisant une approche de programmation dynamique. Voici l'algorithme sur papier :")

print("Créer un tableau dp où dp[i][w] représente la valeur maximale obtenue en utilisant les premiers i objets avec une capacité maximale de w.")
print("Initialiser dp[0][w] à 0 pour tous les w, car sans objets, la valeur maximale est 0.")
print("Initialiser dp[i][0] à 0 pour tous les i, car avec une capacité de 0, la valeur maximale est 0.")
print("    Pour chaque objet i de 1 à N :i")
print("        Pour chaque capacité w de 0 à C :i")
print("            Si le poids de l'objet i est supérieur à w, alors dp[i][w] = dp[i-1][w].i")
print("            Sinon, dp[i][w] = max(dp[i-1][w], dp[i-1][w - poids[i]] + utilite[i]).i")
print("    La valeur maximale est trouvée à dp[N][C].i")



# Question 8 :
def knapsack(capacity, weights, values):
    N = len(weights)
    dp = [[0 for _ in range(capacity + 1)] for _ in range(N + 1)]

    for i in range(1, N + 1):
        for w in range(capacity + 1):
            if weights[i-1] <= w:
                dp[i][w] = max(dp[i-1][w], dp[i-1][w - weights[i-1]] + values[i-1])
            else:
                dp[i][w] = dp[i-1][w]

    return dp[N][capacity], dp

print("Question 8 : ")

# Exemple d'utilisation
weights = [2, 3, 4, 5]
values = [3, 4, 5, 6]
capacities = [2, 3, 4, 5]

for C in capacities:
    max_value, dp = knapsack(C, weights, values)
    print(f"Pour C = {C}, valeur maximale: {max_value}")




# Question 9 :

def knapsack(capacity, weights, values):
    N = len(weights)
    dp = [[0 for _ in range(capacity + 1)] for _ in range(N + 1)]

    for i in range(1, N + 1):
        for w in range(capacity + 1):
            if weights[i-1] <= w:
                dp[i][w] = max(dp[i-1][w], dp[i-1][w - weights[i-1]] + values[i-1])
            else:
                dp[i][w] = dp[i-1][w]

    return dp[N][capacity], dp

def mesure_temps_knapsack(capacity, weights, values):
    start_time = time.time()
    max_value, dp = knapsack(capacity, weights, values)
    end_time = time.time()
    return max_value, dp, end_time - start_time

weights = [2, 3, 4, 5]
values = [3, 4, 5, 6]
capacities = [2, 3, 4, 5]

results = []

for C in capacities:
    max_value, dp, temps = mesure_temps_knapsack(C, weights, values)
    results.append((C, max_value, temps))

# Affichage des résultats
df_results = pd.DataFrame(results, columns=['C', 'Valeur maximale', 'Temps de calcul (s)'])
print("Question 9 : \n",df_results)



# Question 10 :
print("Partie 10 : Algorithme heuristique (B)")
print("Un algorithme heuristique classique pour le problème du sac à dos est l'algorithme glouton basé sur la densité de valeur, c'est-à-dire la valeur par unité de poids. L'idée est de trier les objets par leur densité de valeur décroissante et de les ajouter au sac à dos tant qu'il reste de la capacité.")
print("Algorithme sur papier :")
print("")
print("    Calculer la densité de valeur (utilité/poids) pour chaque objet.")
print("    Trier les objets par densité de valeur décroissante.")
print("    Initialiser la capacité restante à C et la valeur totale à 0.")
print("    Pour chaque objet dans l'ordre trié :")
print("        Si l'objet peut être ajouté au sac (poids <= capacité restante) :")
print("            Ajouter l'objet au sac.")
print("            Soustraire le poids de l'objet de la capacité restante.")
print("            Ajouter la valeur de l'objet à la valeur totale.")
print("    Retourner la valeur totale et la liste des objets dans le sac.")


# Question 11 :
def knapsack_heuristic(capacity, weights, values):
    items = list(zip(weights, values))
    # Calculer la densité de valeur et trier par ordre décroissant
    items.sort(key=lambda x: x[1] / x[0], reverse=True)
    
    total_value = 0
    remaining_capacity = capacity
    selected_items = []

    for weight, value in items:
        if weight <= remaining_capacity:
            selected_items.append((weight, value))
            remaining_capacity -= weight
            total_value += value

    return total_value, selected_items

print("Question 11 :")

# Exemple d'utilisation
weights = [2, 3, 4, 5]
values = [3, 4, 5, 6]
capacities = [2, 3, 4, 5]

for C in capacities:
    max_value, selected_items = knapsack_heuristic(C, weights, values)
    print(f"Pour C = {C}, valeur maximale (heuristique): {max_value}, objets sélectionnés: {selected_items}")




# Question 12 :
def knapsack_heuristic(capacity, weights, values):
    items = list(zip(weights, values))
    # Calculer la densité de valeur et trier par ordre décroissant
    items.sort(key=lambda x: x[1] / x[0], reverse=True)

    total_value = 0
    remaining_capacity = capacity
    selected_items = []

    for weight, value in items:
        if weight <= remaining_capacity:
            selected_items.append((weight, value))
            remaining_capacity -= weight
            total_value += value

    return total_value, selected_items

def mesure_temps_knapsack_heuristic(capacity, weights, values):
    start_time = time.time()
    max_value, selected_items = knapsack_heuristic(capacity, weights, values)
    end_time = time.time()
    return max_value, selected_items, end_time - start_time

print("Question 12")

weights = [2, 3, 4, 5]
values = [3, 4, 5, 6]
capacities = [2, 3, 4, 5]

heuristic_results = []

for C in capacities:
    max_value, selected_items, temps = mesure_temps_knapsack_heuristic(C, weights, values)
    heuristic_results.append((C, max_value, temps, selected_items))

# Affichage des résultats
df_heuristic_results = pd.DataFrame(heuristic_results, columns=['C', 'Valeur maximale (heuristique)', 'Temps de calcul (s)', 'Objets sélectionnés'])
print(df_heuristic_results)



# Question 13 :
# Comparaison des résultats
exact_results = []
heuristic_results = []

for C in capacities:
    # Résultats exacts
    max_value_exact, dp, temps_exact = mesure_temps_knapsack(C, weights, values)
    exact_results.append((C, max_value_exact, temps_exact))

    # Résultats heuristiques
    max_value_heuristic, selected_items, temps_heuristic = mesure_temps_knapsack_heuristic(C, weights, values)
    heuristic_results.append((C, max_value_heuristic, temps_heuristic))

# DataFrames pour comparaison
df_exact_results = pd.DataFrame(exact_results, columns=['C', 'Valeur maximale (exacte)', 'Temps de calcul (s) (exact)'])
df_heuristic_results = pd.DataFrame(heuristic_results, columns=['C', 'Valeur maximale (heuristique)', 'Temps de calcul (s) (heuristique)'])

# Fusion des DataFrames pour comparaison
df_comparaison = df_exact_results.merge(df_heuristic_results, on='C')
print("Question 13 : ",df_comparaison)



# Question 14 :
def knapsack_heuristic_with_time_limit(capacity, weights, values, time_limit=2):
    start_time = time.time()
    items = list(zip(weights, values))
    # Calculer la densité de valeur et trier par ordre décroissant
    items.sort(key=lambda x: x[1] / x[0], reverse=True)

    total_value = 0
    remaining_capacity = capacity
    selected_items = []

    for weight, value in items:
        if time.time() - start_time > time_limit:
            break
        if weight <= remaining_capacity:
            selected_items.append((weight, value))
            remaining_capacity -= weight
            total_value += value

    return total_value, selected_items

print("Question 14 :")

# Exemple d'utilisation avec contrainte de temps
capacities = [2, 3, 4, 5]

for C in capacities:
    start_time = time.time()
    max_value, selected_items = knapsack_heuristic_with_time_limit(C, weights, values)
    end_time = time.time()
    temps = end_time - start_time
    print(f"Pour C = {C}, valeur maximale (heuristique avec limite de temps): {max_value}, objets sélectionnés: {selected_items}, temps de calcul: {temps:.4f} s")


