## Question 7: Rédiger un algorithme papier pour la résolution exacte du problème du sac à dos. On l’appellera A.

### Algorithme A : Résolution exacte du problème du sac à dos

1. **Initialisation**
   - Soit `L` la liste des objets, chaque objet `o` ayant un poids `poidso` et une utilité `utiliteo`.
   - Soit `C` la capacité maximale du sac à dos.
   - Créer une matrice `K` de dimensions `(N+1) x (C+1)` où `N` est le nombre d'objets.
   - Initialiser `K[i][w] = 0` pour tout `i` dans `[0, N]` et `w` dans `[0, C]`.

2. **Remplissage de la matrice**
   - Pour chaque objet `i` de `1` à `N`:
     - Pour chaque capacité `w` de `0` à `C`:
       - Si `poidso[i-1] <= w`:
         - `K[i][w] = max(utiliteo[i-1] + K[i-1][w-poidso[i-1]], K[i-1][w])`
       - Sinon:
         - `K[i][w] = K[i-1][w]`

3. **Extraction de la solution optimale**
   - La valeur optimale est `K[N][C]`.
   - Pour retrouver les objets choisis:
     - Initialiser `w = C` et créer une liste `objets_choisis`.
     - Pour `i` de `N` à `1`:
       - Si `K[i][w] != K[i-1][w]`:
         - Ajouter l'objet `i-1` à la liste `objets_choisis`.
         - Mettre à jour `w = w - poidso[i-1]`.

4. **Résultat**
   - La liste `objets_choisis` contient les indices des objets à mettre dans le sac à dos.
   - La valeur totale de l'utilité maximale est `K[N][C]`.

 ```python
def knapsack(L, C):
     N = len(L)
     K = [[0 for _ in range(C + 1)] for _ in range(N + 1)]
     
     for i in range(1, N + 1):
         for w in range(C + 1):
             if L[i-1][0] <= w:
                 K[i][w] = max(L[i-1][1] + K[i-1][w-L[i-1][0]], K[i-1][w])
             else:
                 K[i][w] = K[i-1][w]
     
     w = C
     objets_choisis = []
     for i in range(N, 0, -1):
         if K[i][w] != K[i-1][w]:
             objets_choisis.append(i-1)
             w -= L[i-1][0]
     
     return K[N][C], objets_choisis
 ```

### Explication
- **Initialisation**: La matrice `K` est initialisée avec des zéros, représentant les utilités maximales pour différentes capacités et objets.
- **Remplissage de la matrice**: La matrice est remplie en utilisant une approche dynamique. Chaque cellule `K[i][w]` représente la valeur maximale de l'utilité que l'on peut obtenir en utilisant les premiers `i` objets avec une capacité maximale `w`.
- **Extraction de la solution optimale**: Une fois la matrice remplie, nous pouvons retrouver les objets choisis en retraçant nos pas dans la matrice `K`.
- **Résultat**: La fonction retourne la valeur maximale de l'utilité et les indices des objets choisis pour atteindre cette utilité.
