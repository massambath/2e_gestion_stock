from config import supabase

def ajouter_produit(reference,nom,categorie,prix_carton,quantite):
    supabase.table("produits").insert({
        "reference": reference,
        "nom": nom,
        "categorie": categorie,
        "prix_unitaire": prix_carton,
        "quantite": quantite
    }).execute()


def afficher_produits(return_df=False):
    data = supabase.table("produits").select("*").execute()
    return data.data 

 
