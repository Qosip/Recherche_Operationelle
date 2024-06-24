from utils import read_excel_data

# Chemin vers le fichier Excel
file_path = "Tableau_donnees_sac_a_dos_Velo.xlsx"  # Remplacez par le chemin correct

# Lire les données du fichier Excel
objects = read_excel_data(file_path)

# Nombre total d'objets
total_objects = len(objects)

# Nombre total d'organisations de sac à dos, y compris le sac à dos vide
total_combinations = 2 ** total_objects

print(f"Nombre total d'organisations de sac à dos: {total_combinations}")
