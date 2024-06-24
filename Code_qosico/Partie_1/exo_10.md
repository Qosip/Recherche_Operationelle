## Question 10: Rédiger un algorithme papier heuristique pour la résolution du problème du sac à dos. On l’appellera B.

### Algorithme B : Résolution heuristique du problème du sac à dos

### Heuristique : Glouton basé sur le rapport utilité/poids

1. **Initialisation**
   - Soit `L` la liste des objets, chaque objet `o` ayant un poids `poidso` et une utilité `utiliteo`.
   - Soit `C` la capacité maximale du sac à dos.
   - Créer une liste vide `objets_choisis`.
   - Initialiser `poids_total = 0` et `utilite_totale = 0`.

2. **Calcul des rapports utilité/poids**
   - Pour chaque objet `o` dans `L`:
     - Calculer le rapport `r[o] = utiliteo / poidso`.

3. **Tri des objets**
   - Trier les objets dans `L` par ordre décroissant de leur rapport `r[o]`.

4. **Sélection des objets**
   - Pour chaque objet `o` dans `L` trié:
     - Si `poids_total + poidso ≤ C`:
       - Ajouter `o` à `objets_choisis`.
       - Mettre à jour `poids_total = poids_total + poidso`.
       - Mettre à jour `utilite_totale = utilite_totale + utiliteo`.

5. **Résultat**
   - La liste `objets_choisis` contient les objets sélectionnés pour maximiser l'utilité.
   - La valeur totale de l'utilité est `utilite_totale`.

### Pseudocode

```python
**Début**:
- `rapports` ← Liste vide
- **Pour chaque** objet `obj` **dans** `L` **faire**:
  - Calculer le rapport utilité/poids pour `obj` et l'ajouter à `rapports`.

- Trier `rapports` par ordre décroissant basé sur le rapport utilité/poids.

- `poids_total` ← 0
- `utilite_totale` ← 0
- `objets_choisis` ← Liste vide

- **Pour chaque** `i` **dans** `rapports` **faire**:
  - Récupérer le poids et l'utilité de l'objet correspondant dans `L`.
  - **Si** ajouter cet objet ne dépasse pas la capacité `C` **alors**:
    - Ajouter l'indice de l'objet à `objets_choisis`.
    - Mettre à jour `poids_total` et `utilite_totale`.

- **Retourner** `utilite_totale` et `objets_choisis`.
  
**Fin de la fonction**
```