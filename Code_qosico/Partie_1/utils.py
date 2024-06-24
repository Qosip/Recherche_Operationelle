import openpyxl


def read_excel_data(file_path):
    """
    Lit le fichier Excel et extrait les données en ignorant les lignes invalides.
    Retourne une liste de dictionnaires contenant les objets avec leurs masses et utilités.
    """
    wb = openpyxl.load_workbook(file_path)
    sheet = wb.active

    objects = []
    for row in sheet.iter_rows(min_row=2, values_only=True):
        name, masse, utilite = row
        try:
            masse = float(str(masse).replace(',', '.'))
            utilite = float(str(utilite).replace(',', '.'))
            objects.append({
                "name": name,
                "masse": masse,
                "utilite": utilite
            })
        except ValueError:
            continue  # Ignore les lignes qui ne peuvent pas être converties en float

    return objects
