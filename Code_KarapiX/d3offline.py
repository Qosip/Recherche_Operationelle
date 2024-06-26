import pandas as pd
import os

# Définition des dimensions du conteneur
CONTAINER_LENGTH = 11.583
CONTAINER_WIDTH = 2.294
CONTAINER_HEIGHT = 2.569

# Classe pour représenter une marchandise
class Marchandise:
    def __init__(self, id, designation, length, width, height):
        self.id = id
        self.designation = designation
        self.length = length
        self.width = width
        self.height = height
        self.position = None  # Coordonnées x, y, z dans le conteneur
        self.volume = length * width * height  # Calculer le volume

# Classe pour représenter un conteneur
class Conteneur:
    def __init__(self, id):
        self.id = id
        self.contents = []  # Liste des marchandises
        self.occupied_space = []  # Liste des espaces occupés

    def peut_placer(self, marchandise):
        # Vérifie si la marchandise peut être placée dans ce conteneur
        for x in range(int(CONTAINER_LENGTH) + 1):
            for y in range(int(CONTAINER_WIDTH) + 1):
                for z in range(int(CONTAINER_HEIGHT) + 1):
                    if self.est_libre(x, y, z, marchandise):
                        return (x, y, z)
        return None

    def est_libre(self, x, y, z, marchandise):
        # Vérifie si un espace est libre dans le conteneur
        if (x + marchandise.length <= CONTAINER_LENGTH and
            y + marchandise.width <= CONTAINER_WIDTH and
            z + marchandise.height <= CONTAINER_HEIGHT):
            for occupied in self.occupied_space:
                if not (x + marchandise.length <= occupied[0] or
                        x >= occupied[0] + occupied[3] or
                        y + marchandise.width <= occupied[1] or
                        y >= occupied[1] + occupied[4] or
                        z + marchandise.height <= occupied[2] or
                        z >= occupied[2] + occupied[5]):
                    return False
            return True
        return False

    def place_marchandise(self, marchandise, position):
        # Place la marchandise dans le conteneur
        marchandise.position = position
        self.contents.append(marchandise)
        self.occupied_space.append((*position, marchandise.length, marchandise.width, marchandise.height))

# Fonction pour lire les marchandises depuis un fichier Excel et les trier par volume décroissant
def lire_marchandises(filepath):
    df = pd.read_excel(filepath)
    df.columns = df.columns.str.strip()  # Supprimer les espaces autour des noms de colonnes

    marchandises = []
    for index, row in df.iterrows():
        id = row['Numéro']
        designation = row['Désignation']
        length = row['Longueur']
        width = row['Largeur']
        height = row['Hauteur']
        marchandises.append(Marchandise(id, designation, length, width, height))
    
    # Trier les marchandises par volume décroissant
    marchandises.sort(key=lambda m: m.volume, reverse=True)
    
    return marchandises

# Fonction pour charger les marchandises dans les conteneurs
def charger_marchandises(marchandises):
    conteneurs = []
    conteneur_id = 1

    for marchandise in marchandises:
        placé = False
        for conteneur in conteneurs:
            position = conteneur.peut_placer(marchandise)
            if position:
                conteneur.place_marchandise(marchandise, position)
                placé = True
                break
        
        if not placé:
            # Crée un nouveau conteneur si la marchandise ne peut pas être placée
            nouveau_conteneur = Conteneur(conteneur_id)
            conteneur_id += 1
            position = nouveau_conteneur.peut_placer(marchandise)
            nouveau_conteneur.place_marchandise(marchandise, position)
            conteneurs.append(nouveau_conteneur)
    
    return conteneurs

# Fonction principale
def main():
    # Obtenir le chemin absolu du répertoire du script Python
    script_directory = os.path.dirname(os.path.abspath(__file__))

    # Définir le chemin complet vers le fichier Excel
    file_path = os.path.join(script_directory, "a.xlsx")

    # Lire le fichier Excel
    marchandises = lire_marchandises(file_path)

    print("Marchandises lues depuis le fichier Excel et triées par volume décroissant:")
    for marchandise in marchandises:
        print(f"ID: {marchandise.id}, Désignation: {marchandise.designation}, Volume: {marchandise.volume}, Dimensions: ({marchandise.length}, {marchandise.width}, {marchandise.height})")

    conteneurs = charger_marchandises(marchandises)

    print("\nNombre total de conteneurs utilisés:", len(conteneurs))
    for conteneur in conteneurs:
        print(f"\nConteneur {conteneur.id}:")
        for m in conteneur.contents:
            print(f"Marchandise ID: {m.id}, Désignation: {m.designation}, Position: {m.position}, Dimensions: ({m.length}, {m.width}, {m.height})")

# Exécution de la fonction principale
if __name__ == "__main__":
    main()
