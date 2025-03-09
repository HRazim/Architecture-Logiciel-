import click
import uuid
import io
from io import StringIO
from flask import Flask, render_template, request, redirect, url_for, flash

import archilog.models as models
import archilog.services as services

# Initialisation de l'application Flask
app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # Clé secrète nécessaire pour utiliser les messages flash

# Route principale pour afficher la page d'accueil
@app.route('/')
def home():
    entries = models.get_all_entries()  # Récupère toutes les entrées de la base de données
    return render_template('home.html', entries=entries)  # Affiche la page d'accueil avec les entrées

# Route pour créer une nouvelle entrée
@app.route('/create', methods=['GET', 'POST'])
def create_entry():
    if request.method == 'POST':
        name = request.form['name']
        amount = float(request.form['amount'])
        category = request.form['category'] or None

        try:
            models.create_entry(name, amount, category)  # Crée une nouvelle entrée dans la base de données
            flash('Entrée créée avec succès!', 'success')
            return redirect(url_for('home'))

        except Exception as e:
            flash(f'Erreur lors de la création: {str(e)}', 'error')

    return render_template('create.html')  # Affiche le formulaire de création

# Route pour mettre à jour une entrée existante
@app.route('/update/<uuid:id>', methods=['GET', 'POST'])
def update_entry(id):
    try:
        entry = models.get_entry(id)  # Récupère l'entrée à mettre à jour

        if request.method == 'POST':
            name = request.form['name']
            amount = float(request.form['amount'])
            category = request.form['category'] or None

            models.update_entry(id, name, amount, category)  # Met à jour l'entrée dans la base de données
            flash('Entrée mise à jour avec succès!', 'success')

            return redirect(url_for('home'))

        return render_template('update.html', entry=entry)  # Affiche le formulaire de mise à jour

    except Exception as e:
        flash(f'Erreur: {str(e)}', 'error')
        return redirect(url_for('home'))

# Route pour supprimer une entrée
@app.route('/delete/<uuid:id>')
def delete_entry(id):
    try:
        models.delete_entry(id)  # Supprime l'entrée de la base de données
        flash('Entrée supprimée avec succès!', 'success')

    except Exception as e:
        flash(f'Erreur lors de la suppression: {str(e)}', 'error')

    return redirect(url_for('home'))

# Route pour exporter les entrées en CSV
@app.route('/export-csv')
def export_csv():
    csv_content = services.export_to_csv().getvalue()  # Génère le contenu CSV

    return csv_content, 200, {
        'Content-Type': 'text/csv',
        'Content-Disposition': 'attachment; filename=entries.csv'
    }

# Route pour importer des entrées à partir d'un fichier CSV
@app.route('/import-csv', methods=['POST'])
def import_csv():
    if 'csv_file' not in request.files:
        flash('Aucun fichier sélectionné', 'error')
        return redirect(url_for('home'))

    file = request.files['csv_file']

    if file.filename == '':
        flash('Aucun fichier sélectionné', 'error')
        return redirect(url_for('home'))

    if file and file.filename.endswith('.csv'):
        try:
            stream = io.StringIO(file.stream.read().decode("UTF-8"), newline=None)
            services.import_from_csv(stream)  # Importe les données du fichier CSV
            flash('Fichier CSV importé avec succès !', 'success')

        except Exception as e:
            flash(f'Erreur lors de l\'importation : {str(e)}', 'error')

    else:
        flash('Le fichier doit être un CSV', 'error')

    return redirect(url_for('home'))

# Commandes CLI pour interagir avec l'application
@click.group()
def cli():
    pass

@cli.command()
def init_db():
    models.init_db()  # Initialise la base de données
    print("Base de données initialisée avec succès.")

@cli.command()
def run_flask():
    app.run(debug=True)  # Lance l'application Flask en mode debug

@cli.command()
@click.option("-n", "--name", prompt="Name")
@click.option("-a", "--amount", type=float, prompt="Amount")
@click.option("-c", "--category", default=None)
def create(name: str, amount: float, category: str | None):
    models.create_entry(name, amount, category)  # Crée une entrée via la CLI
    print(f"Entrée créée: {name}, {amount}, {category}")

@cli.command()
@click.option("--id", required=True, type=click.UUID)
def get(id: uuid.UUID):
    click.echo(models.get_entry(id))  # Affiche une entrée spécifique via la CLI

@cli.command()
@click.option("--as-csv", is_flag=True, help="Ouput a CSV string.")
def get_all(as_csv: bool):
    if as_csv:
        click.echo(services.export_to_csv().getvalue())  # Exporte toutes les entrées en CSV via la CLI
    else:
        click.echo(models.get_all_entries())

@cli.command()
@click.argument("csv_file", type=click.File("r"))
def import_csv(csv_file):
    services.import_from_csv(csv_file)  # Importe des entrées à partir d'un fichier CSV via la CLI
    print("Import CSV terminé.")

@cli.command()
@click.option("--id", type=click.UUID, required=True)
@click.option("-n", "--name", required=True)
@click.option("-a", "--amount", type=float, required=True)
@click.option("-c", "--category", default=None)
def update(id: uuid.UUID, name: str, amount: float, category: str | None):
    models.update_entry(id, name, amount, category)  # Met à jour une entrée via la CLI
    print(f"Entrée mise à jour: {id}, {name}, {amount}, {category}")

@cli.command()
@click.option("--id", required=True, type=click.UUID)
def delete(id: uuid.UUID):
    models.delete_entry(id)  # Supprime une entrée via la CLI
    print(f"Entrée avec ID {id} supprimée.")

# Point d'entrée principal pour lancer l'application Flask
if __name__ == '__main__':
    app.run(debug=True)
