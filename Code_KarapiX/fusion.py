import os
import json

# Obtenir le chemin absolu du répertoire du script Python
script_directory = os.path.dirname(os.path.abspath(__file__))

# Définir les chemins complets vers les fichiers JSON à fusionner
json_files = [
    "wagon_assignments_d1.json",
    "wagon_assignments_d2.json",
    "wagon_assignments_d3.json"
]

# Lire et fusionner les contenus des fichiers JSON
combined_data = {}

for file_name in json_files:
    file_path = os.path.join(script_directory, file_name)
    if os.path.exists(file_path):
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            combined_data.update(data)

# Définir le chemin pour le fichier JSON fusionné
combined_json_file_path = os.path.join(script_directory, "wagon_assignments.json")

# Écrire les données fusionnées dans le fichier JSON
with open(combined_json_file_path, 'w') as combined_json_file:
    json.dump(combined_data, combined_json_file, indent=4)

print(f"Les données des fichiers JSON ont été fusionnées et exportées dans le fichier {combined_json_file_path}")
