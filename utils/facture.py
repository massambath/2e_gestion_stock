import datetime
import os

def generer_facture(nom,quantite,prix_carton,total):
    dossier_factures = "factures"
    os.makedirs(dossier_factures,exist_ok=True)

    date = datetime.datetime.now.strftime("%Y%m%d_%H%M%S")
    fichier = os.path.join(dossier_factures, f"facture_{nom}_{date}.txt")
    with open(fichier, "w", encoding="utf-8") as f:
        f.write("=== Facture ====\n")
        f.write(f"Produit : {nom}\n")
        f.write(f"Quantite : {quantite}\n")
        f.write(f"Prix carton: {prix_carton} CFA\n")
        f.write(f"Total : {total} CFA\n")
        f.write(f"Date : {datetime.datetime.now()}\n")
    print(f" Facture générée : {fichier}")