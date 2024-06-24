# Algorithme Papier : Force Brute pour le Sac à Dos

## Description de l'algorithme
1. Générer toutes les combinaisons possibles des objets.
2. Pour chaque combinaison :
   - Calculer la masse totale.
   - Calculer l'utilité totale.
   - Si la masse totale est inférieure ou égale à la capacité \( C \) et l'utilité totale est la meilleure trouvée jusqu'à présent, enregistrer cette combinaison comme la meilleure.
3. Retourner la meilleure combinaison trouvée.

## Compter les opérations
1. **Générer toutes les combinaisons possibles des objets** : \( 2^n \) combinaisons pour \( n \) objets.
2. **Calculer la masse totale et l'utilité totale pour chaque combinaison** :
   - Comparaisons : \( 2^n \) (pour chaque combinaison, vérifier la masse totale et l'utilité totale)
   - Additions : \( n \) par combinaison (somme des masses et utilités des objets dans chaque combinaison)
3. **Enregistrer la meilleure combinaison** :
   - Comparaison : \( 2^n \) (vérifier si l'utilité totale est la meilleure)

## Algorithme en Pseudocode
```
 Algorithm KnapsackBruteForce(objects, C)
    best_value <- 0
    best_combination <- []

    for each combination in PowerSet(objects)
        total_mass <- 0
        total_value <- 0
        for each object in combination
            total_mass <- total_mass + object.mass
            total_value <- total_value + object.value
        end for
        if total_mass <= C and total_value  best_value
            best_value <- total_value
            best_combination <- combination
        end if
    end for

    return best_combination, best_value
 end Algorithm
```

## Compteur d'Opérations

Pour une combinaison donnée :
- Comparaison pour vérifier si la masse totale est inférieure ou égale à \( C \) : 1
- Comparaison pour vérifier si l'utilité totale est meilleure que la meilleure trouvée : 1
- \( n \) additions pour calculer la masse totale
- \( n \) additions pour calculer l'utilité totale

Pour \( 2^n \) combinaisons :
- Comparaisons : \( 2^n \times 2 = 2^{n+1} \)
- Additions : \( 2^n \times n \times 2 = 2^n \times 2n = 2^{n+1} \times n \)

## Algorithme en Python

Pour illustrer cela en Python, voici le script qui implémente cet algorithme et compte les opérations :

 from itertools import chain, combinations
 from utils import read_excel_data

 # Chemin vers le fichier Excel
 file_path = "Tableau_donnees_sac_a_dos.xlsx"

 # Lire les données du fichier Excel
 objects = read_excel_data(file_path)
```
 def knapsack_bruteforce(objects, C):
    best_value = 0
    best_combination = []
    for r in range(1, len(objects) + 1):
        for combination in combinations(objects, r):
            total_mass = sum(obj["masse"] for obj in combination)
            total_value = sum(obj["utilite"] for obj in combination)
            if total_mass <= C and total_value  best_value:
                best_value = total_value
                best_combination = combination

    return best_combination, best_value
```