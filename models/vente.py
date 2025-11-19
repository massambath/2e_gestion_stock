from database.db_setup import get_connection
from utils.facture import generer_facture

def vendre_produit(nom,quantite_vendue,prix_vendu,prix_vendu_carton):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT quantite FROM produits WHERE nom= ?", (nom,))
    result = cursor.fetchone()

    if result :
        quantite_dispo = result[0]
        if quantite_dispo >= quantite_vendue:
            nouvelle_quantite = quantite_dispo - quantite_vendue
            cursor.execute("UPDATE produits SET quantite= ? WHERE nom = ?", (nouvelle_quantite,nom))
            
            total = quantite_vendue * prix_vendu_carton
            cursor.execute("""
                INSERT INTO VENTES (nom,quantite_vendue,prix_vendue_carton,total)
                VALUES (?,?,?,?)
                           """,(nom, quantite_vendue,prix_vendu_carton,total))
            
            conn.commit()
            print(f" Vente de {quantite_vendue} {nom} pour {total} CFA")
            generer_facture(nom,quantite_vendue,prix_vendu_carton,total)
        else:
            print("Stock insuffisant")
    else:
        print("Produit non trouvé")

    conn.close()
    