# Importation des modules nécessaires
from flask import Flask

def create_app():
    app = Flask(__name__)
    app.secret_key = "your_secret_key_here"
    
    # Importation des vues (après la création de l'app pour éviter les imports circulaires)
    from archilog.views import app as views_app
    
    # Retourner l'application Flask
    return views_app