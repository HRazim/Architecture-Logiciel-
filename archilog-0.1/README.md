# Archilog

A simple project for educational purpose.

## Technologies utilisées

### SQLAlchemy Core

SQLAlchemy est un toolkit SQL et un ORM (Object-Relational Mapping) écrit en Python. Dans ce projet, nous utilisons uniquement SQLAlchemy Core (pas l'ORM) pour interagir avec la base de données SQLite.

```python
from sqlalchemy import create_engine, Table, MetaData, Column, String, Float

# Connexion à la base SQLite
engine = create_engine('sqlite:///data.db')
metadata = MetaData()

# Définition de la table 'entries'
entries = Table(
    'entries',
    metadata,
    Column('id', String, primary_key=True),
    Column('name', String, nullable=False),
    Column('amount', Float, nullable=False),
    Column('category', String, nullable=True)
)
```

Exemple d’utilisation : 

- Cette table stocke les entrées financières avec un identifiant unique, un nom, un montant et une catégorie optionnelle.

### Flask

Flask est un framework web léger pour Python, parfait pour créer rapidement une interface web. Dans Archilog, il sert à afficher les entrées et à gérer les interactions utilisateur via des formulaires.

```python
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    entries = models.get_all_entries()
    return render_template('home.html', entries=entries)
```

Exemple d’utilisation : 

- La route racine récupère toutes les entrées et les affiche via un template HTML.

### Jinja2

Jinja2, intégré à Flask, génère des pages HTML dynamiques en combinant des templates avec les données de l’application.

```html
{% if entries and entries|length > 0 %}
    <table>
        {% for entry in entries %}
            <tr>
                <td>{{ entry.id }}</td>
                <td>{{ entry.name }}</td>
            </tr>
        {% endfor %}
    </table>
{% endif %}
```

## Structure du projet

```
.
├── pyproject.toml
├── README.md
└── src
    └── archilog
        ├── __init__.py
        ├── models.py          # Modèles de données et fonctions d'accès à la BDD
        ├── services.py        # Services d'import/export CSV
        ├── static
        │   └── css
        │       └── style.css  # Styles CSS
        ├── templates
        │   ├── create.html    # Formulaire de création
        │   ├── home.html      # Page d'accueil
        │   └── update.html    # Formulaire de modification
        └── views.py           # Contrôleurs Flask
```

## Commandes disponibles

```bash
$ pdm run archilog
Usage: archilog [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  create      Créer une nouvelle entrée
  delete      Supprimer une entrée existante
  get         Récupérer une entrée par son ID
  get-all     Lister toutes les entrées (avec option CSV)
  import-csv  Importer des données depuis un fichier CSV
  init-db     Initialiser la base de données
  update      Mettre à jour une entrée existante
```

Exemples :

- pdm run archilog create : Demande les détails (nom, montant, catégorie) pour une nouvelle entrée.
- pdm run archilog get-all --as-csv : Exporte toutes les entrées au format CSV.

## Fonctionnalités

- Affichage de toutes les entrées financières
- Création, modification et suppression d'entrées
- Importation et exportation de données au format CSV
- Interface web intuitive
- Gestion des erreurs avec messages flash
- Interface en ligne de commande complète

## Installation

1. Installez les dépendances avec PDM:
   ```
   pdm add flask sqlalchemy
   ```

2. Initialisez la base de données:
   ```
   pdm run archilog init-db
   ```

## Utilisation

### Interface en ligne de commande

```bash
# Créer une entrée
pdm run archilog create
# Entrer : name="Salaire", amount=1500, category="Revenus"

# Afficher toutes les entrées
pdm run archilog get-all

# Exporter au format CSV
pdm run archilog get-all --as-csv > export.csv

# Importer depuis un CSV
pdm run archilog import-csv export.csv

# Récupérer une entrée par son ID
pdm run archilog get --id <UUID>

# Mettre à jour une entrée
pdm run archilog update --id <UUID>

# Supprimer une entrée
pdm run archilog delete --id <UUID>
```

### Interface web

Lancez l'application Flask:
```
pdm run flask --app archilog.views --debug run
```

Puis ouvrez http://localhost:5000 dans votre navigateur.

## Développement

### Modèles de données (models.py)

Le module `models.py` définit la structure de la base de données et fournit des fonctions pour :
- Initialiser la base de données
- Créer, lire, mettre à jour et supprimer des entrées
- Gérer les connexions à la base de données avec un gestionnaire de contexte

### Services (services.py)

Le module `services.py` contient des fonctions utilitaires pour :
- Exporter les données au format CSV
- Importer des données depuis un fichier CSV

### Vues (views.py)

Le module `views.py` définit:
- Les routes Flask pour l'interface web
- Les commandes CLI pour l'utilisation en ligne de commande

## Ressources

- Documentation SQLAlchemy
- Documentation Flask
- Documentation Jinja2
- Cours et exemples : [https://kathode.neocities.org](https://kathode.neocities.org)