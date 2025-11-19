from database.db_setup import get_connection

def ajouter_produit(nom,categorie,prix_carton,quantite):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO produits (nom,categorie,prix_unitaire,quantite)
    VALUES(?,?,?,?)               
    """,(nom,categorie,prix_carton,quantite))
    conn.commit()
    conn.close()
    print(f"Produit '{nom}' ajouté avec succès.")


def afficher_produits():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produits")
    produits = cursor.fetchall()
    conn.close()

    print("\n Liste des produits : ")
    for p in produits :
        print(f"{p[0]} | {p[1]} | {p[2]} | {p[3]} CFA | Stock: {p[4]}")
