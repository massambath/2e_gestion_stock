from database.db_setup import get_connection

def ajouter_produit(reference,nom,categorie,prix_carton,quantite):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO produits (reference,nom,categorie,prix_unitaire,quantite)
    VALUES(?,?,?,?,?)               
    """,(reference,nom,categorie,prix_carton,quantite))
    conn.commit()
    conn.close()
    print(f"Produit '{nom}' ajouté avec succès.")


def afficher_produits(return_df=False):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produits")
    produits = cursor.fetchall()
    conn.close()

    if return_df :
        import pandas as pd
        df = pd.DataFrame(produits,columns=["id","reference","nom", "categorie", "prix_unitaire", "quantite"])
        return df
    return produits

 
    #print("\n Liste des produits : ")
    #for p in produits :
    #    print(f"{p[0]} | {p[1]} | {p[2]} | {p[3]} CFA | Stock: {p[4]}")
