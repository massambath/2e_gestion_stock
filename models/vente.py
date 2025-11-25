from database.db_setup import get_connection
from utils.facture import generer_facture
import sqlite3

def vendre_produit(nom,quantite_vendue,prix_vendu_carton,return_msg=False):
    conn = sqlite3.connect("data/stock.db")
    cursor = conn.cursor()
    cursor.execute("SELECT quantite FROM produits WHERE nom= ?", (nom,))
    result = cursor.fetchone()

    if not result:
        msg= "Produit non trouvé"
        return msg if return_msg else print(msg)
    quantite_dispo = result[0]

    # Stock insuffisant
    if quantite_dispo < quantite_vendue:
        msg = "⚠️ Stock insuffisant."
        return msg if return_msg else print(msg)

    # Mise à jour du stock
    nouvelle_quantite = quantite_dispo - quantite_vendue
    cursor.execute(
        "UPDATE produits SET quantite = ? WHERE nom = ?",
        (nouvelle_quantite, nom)
    )

    # Calcul
    total = quantite_vendue * prix_vendu_carton

     # Génération facture
    facture_path = generer_facture(nom, quantite_vendue, prix_vendu_carton, total)

    # Historique de vente
    cursor.execute("""
        INSERT INTO ventes (nom, quantite_vendue, prix_vendu_carton, total,facture_path)
        VALUES (?, ?, ?, ?,?)
    """, (nom, quantite_vendue, prix_vendu_carton, total,facture_path))

    conn.commit()
    conn.close()

    # Génération de la facture
    facture_path = generer_facture(nom, quantite_vendue, prix_vendu_carton, total)

    if return_msg:
        return {
            "message": f"✔ Vente enregistrée ({quantite_vendue} x {nom})",
            "facture_path": facture_path
        }
    return None