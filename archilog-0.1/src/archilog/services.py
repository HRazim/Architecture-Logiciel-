import csv
import dataclasses
import io

from archilog.models import create_entry, get_all_entries, Entry

# Fonction pour exporter les entrées en CSV
def export_to_csv() -> io.StringIO:
    
    output = io.StringIO()  # Crée un objet StringIO pour stocker le contenu CSV
    csv_writer = csv.DictWriter(
        output, fieldnames=[f.name for f in dataclasses.fields(Entry)]
    )  # Crée un écrivain CSV avec les noms de champs de la classe Entry
    
    csv_writer.writeheader()  # Écrit l'en-tête du CSV
    
    for todo in get_all_entries():
        csv_writer.writerow(dataclasses.asdict(todo))  # Écrit chaque entrée sous forme de dictionnaire
    return output  # Retourne le contenu CSV

# Fonction pour importer des entrées à partir d'un fichier CSV
def import_from_csv(csv_file: io.StringIO) -> None:
    
    csv_reader = csv.DictReader(
        csv_file, fieldnames=[f.name for f in dataclasses.fields(Entry)]
    )  # Crée un lecteur CSV avec les noms de champs de la classe Entry
    
    next(csv_reader)  # Saute la première ligne (en-tête)
    
    for row in csv_reader:
        create_entry(
            name=row["name"],
            amount=float(row["amount"]),
            category=row["category"],
        )  # Crée une entrée dans la base de données pour chaque ligne du CSV
