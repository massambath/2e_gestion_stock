from config import supabase
from postgrest.exceptions import APIError
def ajouter_produit(reference,nom,categorie,prix_carton,quantite):
    try:
        supabase.table("produits").insert({
        "reference": reference,
        "nom": nom,
        "categorie": categorie,
        "prix_unitaire": prix_carton,
        "quantite": quantite
        }).execute()
        return f"✔ Produit {reference} ajouté avec succès."
    except APIError:
        return f"❌ Impossible d’ajouter : le produit avec la référence {reference} existe déjà."


def afficher_produits(return_df=False):
    data = supabase.table("produits").select("*").execute()
    return data.data 

 
