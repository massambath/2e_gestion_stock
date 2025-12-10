import sqlite3
import os

# Chemin absolu vers le dossier du fichier db_setup.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# Chemin correct vers data/stock.db même dans Streamlit
DB_PATH = os.path.join(BASE_DIR, "..", "data", "stock.db")

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    ## table produits
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS produits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        reference TEXT NOT NULL,
        nom TEXT NOT NULL,
        categorie TEXT,
        prix_unitaire REAL NOT NULL,
        quantite INTEGER NOT NULL,
        date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    # table ventes


# Puis recréer la table avec nom_client
    cursor.execute("""
CREATE TABLE IF NOT EXISTS ventes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    reference TEXT NOT NULL,
    nom_client TEXT,                  
    quantite_vendue INTEGER NOT NULL,
    prix_vendu_carton REAL NOT NULL,
    total REAL NOT NULL,
    date_vente TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    facture_path TEXT
)
""")
    conn.commit()
    conn.close()
