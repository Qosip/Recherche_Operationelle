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
    def __init__(self, id, designation, length, width, height):
        self.id = id
        self.designation = designation
        self.length = length
        self.width = width
        self.height = height
        self.position = None  # Coordonnées x, y, z dans le conteneur

# Classe pour représenter un conteneur
class Conteneur:
    def __init__(self, id):
        self.id = id
        self.contents = []  # Liste des marchandises
        # Création d'une grille 3D représentant le conteneur
        self.grid = [[[False for i in range(math.ceil(CONTAINER_HEIGHT * 10))] 
                      for i in range(math.ceil(CONTAINER_WIDTH * 10))] 
                      for i in range(math.ceil(CONTAINER_LENGTH * 10))]

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

# Fonction pour lire les marchandises depuis un fichier Excel
def lire_marchandises(filepath):
    df = pd.read_excel(filepath)

    marchandises = []
    for index, row in df.iterrows():
        id = row['Numéro ']
        designation = row['Désignation']
        length = row['Longueur']
        width = row['Largeur']
        height = row['Hauteur']
        marchandises.append(Marchandise(id, designation, length, width, height))
    
    return marchandises

# Fonction pour charger les marchandises dans les conteneurs
def charger_marchandises(marchandises):
    conteneurs = []
    conteneur_id = 1

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
            nouveau_conteneur = Conteneur(conteneur_id)
            conteneur_id += 1
            position = nouveau_conteneur.peut_placer(marchandise)
            nouveau_conteneur.place_marchandise(marchandise, position)
            conteneurs.append(nouveau_conteneur)

    end_time = time.time()  # Fin de la mesure du temps pour le chargement des marchandises
    print(f"Temps d'exécution pour charger les marchandises: {end_time - start_time:.4f} secondes")
    
    return conteneurs

# Fonction pour afficher un conteneur en 3D
def plot_conteneur_3d(conteneur):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    conteneur_length, conteneur_width, conteneur_height = conteneur.get_dimensions()

    for marchandise in conteneur.contents:
        position = marchandise.position
        dimensions = (marchandise.length, marchandise.width, marchandise.height)
        plot_item(ax, position, dimensions, (0.4, 0.6, 0.8))  # Couleur bleutée pour les marchandises

    ax.set_xlim(0, conteneur_length)
    ax.set_ylim(0, conteneur_width)
    ax.set_zlim(0, conteneur_height)

    ax.set_xlabel('Longueur')
    ax.set_ylabel('Largeur')
    ax.set_zlabel('Hauteur')
    ax.set_title(f'Conteneur {conteneur.id}')

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

# Fonction pour générer la structure JSON à partir des conteneurs chargés
def generer_structure_json(conteneurs):
    structure = {}
    
    for conteneur in conteneurs:
        wagon_key = f"wagon {conteneur.id}"
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

# Fonction principale
def main():
    script_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_directory, "a.xlsx")

    start_reading_time = time.time()
    marchandises = lire_marchandises(file_path)
    end_reading_time = time.time()
    print(f"Temps d'exécution pour lire les marchandises: {end_reading_time - start_reading_time:.4f} secondes")

    print("Marchandises lues depuis le fichier Excel:")
    for marchandise in marchandises:
        print(f"ID: {marchandise.id}, Désignation: {marchandise.designation}, Length: {marchandise.length}, Width: {marchandise.width}, Height: {marchandise.height}")

    start_loading_time = time.time()
    conteneurs = charger_marchandises(marchandises)
    end_loading_time = time.time()
    print(f"Temps d'exécution pour charger les marchandises dans les conteneurs: {end_loading_time - start_loading_time:.4f} secondes")

    # Générer la structure JSON à partir des conteneurs
    structure_json = generer_structure_json(conteneurs)
    
    # Écrire la structure JSON dans un fichier
    json_file_path = os.path.join(script_directory, "d3online.json")
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(structure_json, json_file, ensure_ascii=False, indent=4)

    print(f"\nStructure JSON des conteneurs écrite dans {json_file_path}")

    print("\nNombre total de conteneurs utilisés:", len(conteneurs))
    for conteneur in conteneurs:
        print(f"\nConteneur {conteneur.id}:")
        for m in conteneur.contents:
            print(f"Marchandise ID: {m.id}, Désignation: {m.designation}, Position: {m.position}, Dimensions: ({m.length}, {m.width}, {m.height})")
        # Affichage 3D pour chaque conteneur
        #plot_conteneur_3d(conteneur)

# Exécution de la fonction principale
if __name__ == "__main__":
    overall_start_time = time.time()
    main()
    overall_end_time = time.time()
    print(f"Temps d'exécution total du script: {overall_end_time - overall_start_time:.4f} secondes")
