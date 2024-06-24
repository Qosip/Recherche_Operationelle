#### Question 1
Le nombre de sacs à dos pouvant être réalisés sans contrainte de charge maximale est de 2 pour N = 1, 4 pour N = 2, 1024 pour N = 10, et 8,388,608 pour N = 23.

#### Question 2
Le nombre total de combinaisons possibles de sacs à dos, incluant le sac à dos vide, est de 8,388,608.

#### Question 3
Le solveur MILP a trouvé la solution optimale avec une valeur objective de 60, en prenant les objets [1.0, 1.0, 1.0, 0.0] et a pris 0.00 secondes.

#### Question 4
L'algorithme sur papier pour calculer la somme des N premiers entiers naturels réalise 2N opérations (N additions et N incrémentations).

#### Question 5
Le temps de calcul pour différentes valeurs de N est :

- N = 10 : 0.000002 s
- N = 100 : 0.000006 s
- N = 1000 : 0.000059 s
- N = 10000 : 0.000522 s
- N = 100000 : 0.004902 s

La durée moyenne par opération est environ 2.45e-08 secondes pour N = 100000.

#### Question 6
Le temps total nécessaire pour tester toutes les combinaisons de sacs à dos est estimé à 0.388278 secondes.

#### Question 7
Un algorithme exact pour résoudre le problème du sac à dos peut être réalisé en utilisant une approche de programmation dynamique, où la valeur maximale est trouvée à dp[N][C].

#### Question 8
Pour l'algorithme exact et différentes valeurs de C :

- C = 2 : valeur maximale = 3
- C = 3 : valeur maximale = 4
- C = 4 : valeur maximale = 5
- C = 5 : valeur maximale = 7

#### Question 9
Temps de calcul pour l'algorithme exact :

- C = 2 : 0.000005 s
- C = 3 : 0.000005 s
- C = 4 : 0.000005 s
- C = 5 : 0.000006 s

#### Partie 10
Un algorithme heuristique classique pour le problème du sac à dos est l'algorithme glouton basé sur la densité de valeur, en triant les objets par densité de valeur décroissante.

#### Question 11
Pour l'algorithme heuristique et différentes valeurs de C :

- C = 2 : valeur maximale = 3, objets sélectionnés = [(2, 3)]
- C = 3 : valeur maximale = 3, objets sélectionnés = [(2, 3)]
- C = 4 : valeur maximale = 3, objets sélectionnés = [(2, 3)]
- C = 5 : valeur maximale = 7, objets sélectionnés = [(2, 3), (3, 4)]

#### Question 12
Temps de calcul pour l'algorithme heuristique :

- C = 2 : 0.000020 s
- C = 3 : 0.000002 s
- C = 4 : 0.000002 s
- C = 5 : 0.000002 s

#### Question 13
Comparaison entre les algorithmes exact (A) et heuristique (B) montre que l'algorithme heuristique est beaucoup plus rapide mais peut ne pas toujours donner la solution optimale.

#### Question 14
Pour l'algorithme heuristique avec limite de temps (B') et différentes valeurs de C :

- C = 2 : valeur maximale = 3, objets sélectionnés = [(2, 3)], temps de calcul = 0.0000 s
- C = 3 : valeur maximale = 3, objets sélectionnés = [(2, 3)], temps de calcul = 0.0000 s
- C = 4 : valeur maximale = 3, objets sélectionnés = [(2, 3)], temps de calcul = 0.0000 s
- C = 5 : valeur maximale = 7, objets sélectionnés = [(2, 3), (3, 4)], temps de calcul = 0.0000 s

