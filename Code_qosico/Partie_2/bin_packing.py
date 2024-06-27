import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import random
import time
import json
import itertools
global longueur_conteneur
global largeur_conteneur
global hauteur_conteneur
longueur_conteneur=11.583
largeur_conteneur=2.294
hauteur_conteneur=2.569

fichier=open("donnees_part_2.csv",'r')
liste_données=[]
objets=[]

for line in fichier:
    liste_données.append(line.strip().split(';'))
for i in range (1,len(liste_données)):
    objets.append([liste_données[i][1]
                  ,float(liste_données[i][2].replace(',','.'))
                  ,float(liste_données[i][3].replace(',','.'))
                  ,float(liste_données[i][4].replace(',','.'))])


def bin_packing_Offline(objets):
    objets_triés=objets[:]
    objets_triés.sort(key=lambda x: x[1]*x[2], reverse=True)
    return bin_packing_Online(objets_triés)


def plot_box(ax, x, y, z, dx, dy, dz, color, label):
    # Affiche un coli dans les coordonnées données
    xx = [x, x, x + dx, x + dx, x]
    yy = [y, y + dy, y + dy, y, y]
    args = {'alpha': 0.8, 'color': color}

    ax.plot3D(xx, yy, [z], **args)
    ax.plot3D(xx, yy, [z + dz], **args)
    ax.plot3D([x, x], [y, y], [z, z + dz], **args)
    ax.plot3D([x, x], [y + dy, y + dy], [z, z + dz], **args)
    ax.plot3D([x + dx, x + dx], [y, y], [z, z + dz], **args)
    ax.plot3D([x + dx, x + dx], [y + dy, y + dy], [z, z + dz], **args)

    ax.text(x + dx / 2, y + dy / 2, z + dz / 2, label, color=color)  # on met le nom de l'objet au milieu du coli
def peut_renter_dans(coli, espace_dispo):
    # Vérifie si un colis peut entrer dans un espace disponible et si oui retourne les 3 espaces libres qu'il crée
    # sinon retourne None pour être utilisé comme condition d'un if
    longueur_coli, largeur_coli, hauteur_coli = coli
    longueur_dispo, largeur_dispo, hauteur_dispo = espace_dispo[0]
    x, y, z = espace_dispo[1]
    nv_espace_dispo = []

    if (longueur_coli <= longueur_dispo and largeur_coli <= largeur_dispo and hauteur_coli <= hauteur_dispo):
        nv_espace_dispo.append(
            ((longueur_dispo - longueur_coli, largeur_dispo, hauteur_dispo), (x + longueur_coli, y, z)))
        nv_espace_dispo.append(((longueur_coli, largeur_dispo - largeur_coli, hauteur_dispo), (x, y + largeur_coli, z)))
        nv_espace_dispo.append(((longueur_coli, largeur_coli, hauteur_dispo - hauteur_coli), (x, y, z + hauteur_coli)))
        return nv_espace_dispo
    else:
        return None
def bin_packing_Online(objets):
    conteneurs = []  # liste qui contient nos conteneurs/wagons
    for i in range(len(objets)):
        objet_actuel = objets[i]
        x = objet_actuel[1]
        y = objet_actuel[2]
        z = objet_actuel[3]
        enzo_le_demenageur = False  # variable qui permet de savoir si on a placé le coli ou non

        for conteneur_actuel in conteneurs:
            for p in range(len(conteneur_actuel[1])):
                espace_libre = conteneur_actuel[1][p]
                for coli in (itertools.permutations([x, y, z])):  # (x, y, z), (z, x, y), (y, x, z)
                    nv_espace_dispo = peut_renter_dans(coli, espace_libre)
                    if nv_espace_dispo and not enzo_le_demenageur:
                        enzo_le_demenageur = True
                        conteneur_actuel[1].pop(p)
                        conteneur_actuel[0].append((objet_actuel, espace_libre[1]))
                        conteneur_actuel[1].extend(nv_espace_dispo)
                        objet_actuel[1] = coli[0]
                        objet_actuel[2] = coli[1]
                        objet_actuel[3] = coli[2]
                        break
                if enzo_le_demenageur:
                    break
        if not enzo_le_demenageur:
            coli = (x, y, z)
            conteneurs.append([[(objet_actuel, (0, 0, 0))], peut_renter_dans(coli, (
            (longueur_conteneur, largeur_conteneur, hauteur_conteneur), (0, 0, 0)))])

    return conteneurs


def plot_3d(conteneur):
    # fonction pour afficher le contenu d'un conteneur en 3d
    fig = plt.figure(figsize=(20, 15))
    ax = fig.add_subplot(111, projection='3d')
    col = 0
    colors = ['r', 'g', 'b', 'y', 'c', 'm']
    plot_box(ax, 0, 0, 0, longueur_conteneur, largeur_conteneur, hauteur_conteneur, "black",
             None)  # on met la bordure du conteneur
    for obj in conteneur[0]:
        # pour chaque objet, on récupère son nom, sa taille et ses coordonnées
        name, longueur, largeur, hauteur = obj[0][0], obj[0][1], obj[0][2], obj[0][3]
        x, y, z = obj[1]
        plot_box(ax, x, y, z, longueur, largeur, hauteur, colors[col], name)
        col = (col + 1) % 5  # pour changer la couleur entre les colis

    # on met les axes de même longueur pour que on garde la forme de contener
    ax.set_xlim([0, longueur_conteneur])
    ax.set_ylim([0, longueur_conteneur])
    ax.set_zlim([0, longueur_conteneur])

    plt.show()

def export_to_json(conteneurs, file_path):
    wagons = {}
    for i, conteneur in enumerate(conteneurs):
        wagon_key = f"wagon {i + 1}"
        wagons[wagon_key] = {}
        for j, (objet, position) in enumerate(conteneur[0]):
            objet_key = f"objet {j + 1}"
            wagons[wagon_key][objet_key] = {
                "longueur": objet[1],
                "largeur": objet[2],
                "hauteur": objet[3],
                "designation": objet[0]
            }
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(wagons, f, ensure_ascii=False, indent=4)

# Exécuter l'algorithme de bin packing
conteneurs = bin_packing_Offline(objets)

# Exporter les résultats en JSON
output_file_path = "resultats_wagons.json"
export_to_json(conteneurs, output_file_path)