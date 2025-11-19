import sqlite3
import os

DB_PATH = os.path.join("data","stock.db")

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    #table produits
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS produits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        categorie TEXT,
        prix_unitaire REAL NOT NULL,
        quantite INTEGER NOT NULL)
                   
                   """)
    
    #table ventes
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ventes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        quantite_vendue INTEGER NOT NULL,
        prix_vendu_carton REAL NOT NULL,
        total REAL NOT NULL,
        data_vente TIMESTRAMP DEFAULT CURRENT_TIMESTAMP
        )

""")
    conn.commit()
    conn.close()