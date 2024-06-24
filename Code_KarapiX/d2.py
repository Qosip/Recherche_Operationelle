import pandas as pd
import os
import time

# Obtenir le chemin absolu du répertoire du script Python
script_directory = os.path.dirname(os.path.abspath(__file__))

# Définir le chemin complet vers le fichier Excel a.xlsx
file_path = os.path.join(script_directory, "a.xlsx")

# Lire le fichier Excel
marchandises_df = pd.read_excel(file_path)

# Afficher un aperçu des données pour vérifier que le chargement a été effectué correctement
print(marchandises_df.head())

# Dimensions du conteneur (en mètres)
container_length = 11.583
container_width = 2.294

# Extraire les dimensions des marchandises sous forme de liste de tuples (longueur, largeur)
rectangles = [(row['Longueur'], row['Largeur']) for index, row in marchandises_df.iterrows()]

# Fonction d'optimisation pour d=2 Offline avec FFDH
def d2_ffdh(rectangles, container_length, container_width):
    start_time = time.time()  # Mesure du temps de début
    
    # Trier les rectangles par aire décroissante
    rectangles = sorted(rectangles, key=lambda rect: rect[0] * rect[1], reverse=True)
    wagons = []
    
    for rect in rectangles:
        placed = False
        for wagon in wagons:
            if can_place(wagon, rect, container_length, container_width):
                place_in_wagon(wagon, rect)
                placed = True
                break
        if not placed:
            new_wagon = [(0, 0, rect[0], rect[1])]  # (x, y, length, width)
            wagons.append(new_wagon)
    
    end_time = time.time()  # Mesure du temps de fin
    temps_execution = end_time - start_time  # Calcul du temps d'exécution
    
    surface_totale_utilisee = sum(l * w for wagon in wagons for x, y, l, w in wagon)
    surface_totale_conteneur = container_length * container_width
    surface_inutilisee = surface_totale_conteneur - surface_totale_utilisee
    
    return wagons, temps_execution, surface_inutilisee

# Fonction auxiliaire pour vérifier si le rectangle peut être placé dans le wagon
def can_place(wagon, rect, container_length, container_width):
    for x, y, l, w in wagon:
        # Check if we can place it to the right
        if x + l + rect[0] <= container_length and y + rect[1] <= container_width:
            return True
        # Check if we can place it below
        if x + rect[0] <= container_length and y + w + rect[1] <= container_width:
            return True
    return False

# Fonction auxiliaire pour placer le rectangle dans le wagon
def place_in_wagon(wagon, rect):
    for i, (x, y, l, w) in enumerate(wagon):
        # Try to place to the right
        if x + l + rect[0] <= container_length and y + rect[1] <= container_width:
            wagon.append((x + l, y, rect[0], rect[1]))
            return
        # Try to place below
        if x + rect[0] <= container_length and y + w + rect[1] <= container_width:
            wagon.append((x, y + w, rect[0], rect[1]))
            return
    # If no placement was found (shouldn't reach here due to check before calling)
    wagon.append((0, 0, rect[0], rect[1]))

# Calculer le nombre de wagons nécessaires pour d=2 Offline (FFDH) et mesurer le temps d'exécution
wagons_offline, temps_execution_offline, surface_inutilisee_offline = d2_ffdh(rectangles, container_length, container_width)

# Affichage des résultats pour la version offline
print("Version Offline (FFDH)")
print(f"Liste des wagons : {wagons_offline}")
print(f"Nombre de wagons : {len(wagons_offline)}")
print(f"Temps d'exécution : {temps_execution_offline:.6f} secondes")
print(f"Surface inutilisée : {surface_inutilisee_offline:.2f} m²")


import pandas as pd
import os
import time

# Obtenir le chemin absolu du répertoire du script Python
script_directory = os.path.dirname(os.path.abspath(__file__))

# Définir le chemin complet vers le fichier Excel a.xlsx
file_path = os.path.join(script_directory, "a.xlsx")

# Lire le fichier Excel
marchandises_df = pd.read_excel(file_path)

# Afficher un aperçu des données pour vérifier que le chargement a été effectué correctement
print(marchandises_df.head())

# Dimensions du conteneur (en mètres)
container_length = 11.583
container_width = 2.294

# Extraire les dimensions des marchandises sous forme de liste de tuples (longueur, largeur)
rectangles = [(row['Longueur'], row['Largeur']) for index, row in marchandises_df.iterrows()]

# Fonction d'optimisation pour d=2 Online avec FFDH
def d2_online_ffdh(rectangles, container_length, container_width):
    start_time = time.time()  # Mesure du temps de début
    
    wagons = [[]]  # Liste des wagons initiaux
    for rect in rectangles:
        placed = False
        for wagon in wagons:
            if can_place(wagon, rect, container_length, container_width):
                place_in_wagon(wagon, rect)
                placed = True
                break
        if not placed:
            new_wagon = [(0, 0, rect[0], rect[1])]  # (x, y, length, width)
            wagons.append(new_wagon)
    
    end_time = time.time()  # Mesure du temps de fin
    temps_execution = end_time - start_time  # Calcul du temps d'exécution
    
    surface_totale_utilisee = sum(l * w for wagon in wagons for x, y, l, w in wagon)
    surface_totale_conteneur = container_length * container_width
    surface_inutilisee = surface_totale_conteneur - surface_totale_utilisee
    
    return wagons, temps_execution, surface_inutilisee

# Calculer le nombre de wagons nécessaires pour d=2 Online (FFDH) et mesurer le temps d'exécution
wagons_online, temps_execution_online, surface_inutilisee_online = d2_online_ffdh(rectangles, container_length, container_width)

# Affichage des résultats pour la version online
print("\nVersion Online (FFDH)")
print(f"Liste des wagons : {wagons_online}")
print(f"Nombre de wagons : {len(wagons_online)}")
print(f"Temps d'exécution : {temps_execution_online:.6f} secondes")
print(f"Surface inutilisée : {surface_inutilisee_online:.2f} m²")
