from utils.facture import generer_facture
from config import supabase

def vendre_produit(reference,quantite_vendue,prix_vendu_carton,nom_client, return_msg=False):
    result = supabase.table("produits").select("*").eq("reference", reference).execute()
    produits = result.data  # c’est une liste de dicts

    if not produits:
        return "Produit non trouvé"  # ou message d'erreur

    produit = produits[0]  # prendre le premier élément

    
    if produit["quantite"]< quantite_vendue:
        return " Stock insuffisant "

    # Mise à jour du stock
    nouvelle_quantite = produit["quantite"]- quantite_vendue
    supabase.table("produits").update({"quantite": nouvelle_quantite}).eq("id",produit["id"]).execute()

    # Calcul
    total = quantite_vendue * prix_vendu_carton

     # Génération facture
    facture_path = generer_facture(reference, quantite_vendue, prix_vendu_carton,nom_client, total)

    # Historique de vente
    supabase.table("ventes").insert({
        "produit_id": produit["id"],
        "reference": produit["reference"],     
        "quantite_vendue": quantite_vendue,
        "prix_vendu_carton": prix_vendu_carton,
        "nom_client": nom_client,
        "total": total,
        "facture_path": facture_path
    }).execute()

    return {"message": f"✔ Vente enregistrée ({quantite_vendue} x {reference})", "facture_path": facture_path}


   