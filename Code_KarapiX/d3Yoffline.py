import pandas as pd
import os
import time
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import json

# Définition des dimensions du conteneur
CONTAINER_LENGTH = 11.5
CONTAINER_WIDTH = 2.2
CONTAINER_HEIGHT = 2.5

# Classe pour représenter une marchandise
class Marchandise:
    def __init__(self, num_objet, designation, length, width, height):
        self.num_objet = num_objet
        self.designation = designation
        self.length = length
        self.width = width
        self.height = height
        self.position = None  # Coordonnées x, y, z dans le conteneur

# Classe pour représenter un conteneur
class Conteneur:
    def __init__(self, wagon):
        self.wagon = wagon
        self.contents = []  # Liste des marchandises
        # Création d'une grille 3D représentant le conteneur
        self.grid = [[[False for _ in range(math.ceil(CONTAINER_HEIGHT * 10))] for _ in range(math.ceil(CONTAINER_WIDTH * 10))] for _ in range(math.ceil(CONTAINER_LENGTH * 10))]

    def peut_placer(self, marchandise):
        # Essayer de placer la marchandise dans la grille
        for x in range(math.ceil(CONTAINER_LENGTH * 10) - math.ceil(marchandise.length * 10) + 1):
            for y in range(math.ceil(CONTAINER_WIDTH * 10) - math.ceil(marchandise.width * 10) + 1):
                for z in range(math.ceil(CONTAINER_HEIGHT * 10) - math.ceil(marchandise.height * 10) + 1):
                    if self.est_libre(x, y, z, marchandise):
                        return (x / 10.0, y / 10.0, z / 10.0)  # Convertir les indices en float pour la position
        return None

    def est_libre(self, x, y, z, marchandise):
        # Vérifie si l'espace nécessaire pour la marchandise est libre
        for dx in range(math.ceil(marchandise.length * 10)):
            for dy in range(math.ceil(marchandise.width * 10)):
                for dz in range(math.ceil(marchandise.height * 10)):
                    if self.grid[x + dx][y + dy][z + dz]:
                        return False
        return True

    def place_marchandise(self, marchandise, position):
        # Place la marchandise dans la grille
        x, y, z = position
        for dx in range(math.ceil(marchandise.length * 10)):
            for dy in range(math.ceil(marchandise.width * 10)):
                for dz in range(math.ceil(marchandise.height * 10)):
                    self.grid[int(x * 10) + dx][int(y * 10) + dy][int(z * 10) + dz] = True
        marchandise.position = position
        self.contents.append(marchandise)

    def get_dimensions(self):
        return CONTAINER_LENGTH, CONTAINER_WIDTH, CONTAINER_HEIGHT

    def get_contents_with_positions(self):
        contents_info = []
        for marchandise in self.contents:
            contents_info.append({
                'num_objet': marchandise.num_objet,
                'longueur': marchandise.length,
                'largeur': marchandise.width,
                'hauteur': marchandise.height,
                'designation': marchandise.designation,
                'position': {
                    'x': marchandise.position[0],
                    'y': marchandise.position[1],
                    'z': marchandise.position[2]
                }
            })
        return contents_info

# Fonction pour lire les marchandises depuis un fichier Excel et les trier par volume
def lire_marchandises(filepath):
    df = pd.read_excel(filepath)

    marchandises = []
    for index, row in df.iterrows():
        num_objet = row['Numéro ']
        designation = row['Désignation']
        length = row['Longueur']
        width = row['Largeur']
        height = row['Hauteur']
        marchandises.append(Marchandise(num_objet, designation, length, width, height))
    
    # Tri des marchandises par volume (length * width * height)
    marchandises.sort(key=lambda m: m.length * m.width * m.height, reverse=True)
    
    return marchandises

# Fonction pour charger les marchandises triées dans les conteneurs
def charger_marchandises(marchandises):
    conteneurs = []
    wagon_id = 1

    start_time = time.time()  # Début de la mesure du temps pour le chargement des marchandises

    for marchandise in marchandises:
        place = False
        for conteneur in conteneurs:
            position = conteneur.peut_placer(marchandise)
            if position:
                conteneur.place_marchandise(marchandise, position)
                place = True
                break
        
        if not place:
            # Crée un nouveau conteneur si la marchandise ne peut pas être placée
            nouveau_conteneur = Conteneur(wagon_id)
            wagon_id += 1
            position = nouveau_conteneur.peut_placer(marchandise)
            nouveau_conteneur.place_marchandise(marchandise, position)
            conteneurs.append(nouveau_conteneur)

    end_time = time.time()  # Fin de la mesure du temps pour le chargement des marchandises
    print(f"Temps d'exécution pour charger les marchandises: {end_time - start_time:.4f} secondes")
    
    return conteneurs

# Fonction principale
def main():
    script_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_directory, "a.xlsx")

    start_reading_time = time.time()
    marchandises = lire_marchandises(file_path)
    end_reading_time = time.time()
    print(f"Temps d'exécution pour lire les marchandises: {end_reading_time - start_reading_time:.4f} secondes")

    print("Marchandises lues depuis le fichier Excel et triées par volume décroissant:")
    for marchandise in marchandises:
        print(f"Numéro d'objet: {marchandise.num_objet}, Désignation: {marchandise.designation}, Length: {marchandise.length}, Width: {marchandise.width}, Height: {marchandise.height}")

    start_loading_time = time.time()
    conteneurs = charger_marchandises(marchandises)
    end_loading_time = time.time()
    print(f"Temps d'exécution pour charger les marchandises dans les conteneurs: {end_loading_time - start_loading_time:.4f} secondes")

    print("\nNombre total de wagons utilisés:", len(conteneurs))
    
    # Générer la structure JSON à partir des conteneurs chargés
    json_data = generer_structure_json(conteneurs)

    # Écrire le JSON dans un fichier
    json_file_path = os.path.join(script_directory, "d3offline.json")
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(json_data, json_file, indent=4)  # Utilisation de json.dump pour écrire la structure JSON

    print(f"\nStructure JSON des conteneurs écrite dans {json_file_path}")

    # Affichage 3D des conteneurs
    #for conteneur in conteneurs:
         #plot_conteneur_3d(conteneur)

# Fonction pour afficher un conteneur en 3D
def plot_conteneur_3d(conteneur):
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')

    conteneur_length, conteneur_width, conteneur_height = conteneur.get_dimensions()

    for marchandise in conteneur.contents:
        position = marchandise.position
        dimensions = (marchandise.length, marchandise.width, marchandise.height)
        plot_item(ax, position, dimensions, (0.4, 0.4, 0.4))

    ax.set_xlim(0, conteneur_length)
    ax.set_ylim(0, conteneur_width)
    ax.set_zlim(0, conteneur_height)

    ax.set_xlabel('Longueur')
    ax.set_ylabel('Largeur')
    ax.set_zlabel('Hauteur')
    ax.set_title(f'Wagon {conteneur.wagon}')

    plt.show()

# Fonction pour tracer une marchandise dans un conteneur
def plot_item(ax, position, dimensions, color):
    x, y, z = position
    dx, dy, dz = dimensions
    vertices = [
        [x, y, z],
        [x + dx, y, z],
        [x + dx, y + dy, z],
        [x, y + dy, z],
        [x, y, z + dz],
        [x + dx, y, z + dz],
        [x + dx, y + dy, z + dz],
        [x, y + dy, z + dz]
    ]
    faces = [
        [vertices[0], vertices[1], vertices[2], vertices[3]],
        [vertices[4], vertices[5], vertices[6], vertices[7]],
        [vertices[0], vertices[1], vertices[5], vertices[4]],
        [vertices[2], vertices[3], vertices[7], vertices[6]],
        [vertices[1], vertices[2], vertices[6], vertices[5]],
        [vertices[4], vertices[7], vertices[3], vertices[0]]
    ]
    poly3d = Poly3DCollection(faces, facecolors=color, linewidths=1, edgecolors='r', alpha=.25)
    ax.add_collection3d(poly3d)

# Fonction pour générer le JSON à partir des conteneurs chargés
def generer_structure_json(conteneurs):
    structure = {}
    
    for conteneur in conteneurs:
        wagon_key = f"wagon {conteneur.wagon}"
        structure[wagon_key] = {}
        
        for idx, marchandise in enumerate(conteneur.contents):
            objet_key = f"objet {idx + 1}"
            position_objet = {
                "x": marchandise.position[0],
                "y": marchandise.position[1],
                "z": marchandise.position[2]
            }
            structure[wagon_key][objet_key] = {
                "longueur": marchandise.length,
                "largeur": marchandise.width,
                "hauteur": marchandise.height,
                "designation": marchandise.designation,
                "position": position_objet
            }
    
    return structure

# Exécution de la fonction principale
if __name__ == "__main__":
    overall_start_time = time.time()
    main()
    overall_end_time = time.time()
    print(f"Temps d'exécution total du script: {overall_end_time - overall_start_time:.4f} secondes")
