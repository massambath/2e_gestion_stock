import streamlit as st
import pandas as pd
import os
from models.produit import afficher_produits, ajouter_produit  # Pour compatibilité, mais tu peux migrer entièrement vers supabase
from models.vente import vendre_produit
from config import supabase  # ton client Supabase
from postgrest.exceptions import APIError

st.set_page_config(page_title="Gestion de Stock", page_icon="📦")

st.title("📦 Application de gestion de stock")
st.write("Interface simple pour gérer les produits et enregistrer les ventes")

#------------Onglets---------
onglet = st.sidebar.radio("Navigation", ["Liste des produits", "Ajouter un produit","Enregistrer une vente","Historique"])

#--------Liste des produits----
if onglet == "Liste des produits":
    st.subheader("Liste actuelle des produits")
    # Récupérer les produits depuis Supabase
    data = pd.DataFrame(supabase.table("produits").select("*").execute().data)
    st.dataframe(data, width='stretch')

#-----Ajouter un produit-------
elif onglet == "Ajouter un produit":
    st.subheader("Ajouter un produit")

    reference = st.text_input("Référence du produit")
    nom = st.text_input("Nom du produit")
    categorie = st.text_input("Catégorie")
    prix = st.number_input("Prix carton", min_value=0.0)
    quantite = st.number_input("Quantité", min_value=0)
    
    if st.button("Ajouter"):
        if nom.strip() == "":
            st.error("Veuillez entrer un nom")
        else:
            try:
                supabase.table("produits").insert({
                "reference": reference,
                "nom": nom,
                "categorie": categorie,
                "prix_unitaire": prix,
                "quantite": quantite
            }).execute()
                st.success(f"Produit '{reference}' ajouté!")
            except APIError:
                st.error(f"❌ Impossible d’ajouter : le produit avec la référence '{reference}' existe déjà.")

#-----Vente--------------
elif onglet == "Enregistrer une vente":
    st.subheader("Vendre un produit")

    reference = st.text_input("Référence du produit vendu")
    quantite_vendue = st.number_input("Quantité vendue", min_value=1)
    prix_vendu_carton = st.number_input("Prix vendu (carton)", min_value=0.0)
    nom_client = st.text_input("Nom du client")

    if st.button("Valider la vente"):
        result = vendre_produit(reference, quantite_vendue, prix_vendu_carton, nom_client, return_msg=True)
        
        if isinstance(result, dict):
            st.success(result["message"])
        else:
            st.error(result)

        # Bouton de téléchargement facture si générée
        if "facture_path" in result:
            with open(result["facture_path"], "rb") as f:
                st.download_button(
                    label ="Télécharger la facture",
                    data=f,
                    file_name=os.path.basename(result["facture_path"]),
                    mime="application/pdf"
                )

#-----Historique des ventes-------------
elif onglet == "Historique":
    st.subheader("Historique des ventes")
    
    # Récupération des ventes depuis Supabase
    ventes = supabase.table("ventes").select("*").order("date_vente", desc=True).execute().data
    df = pd.DataFrame(ventes)

    if df.empty:
        st.info("Aucune vente enregistrée.")
    else:
        # Affichage ligne par ligne
        for index, row in df.iterrows():
            row_dict = row.to_dict()  # convertir la Series en dict pour utiliser .get()
            st.write(
                f"Référence: {row_dict.get('reference','')} | "
                f"Client: {row_dict.get('nom_client','')} | "
                f"Quantité: {row_dict.get('quantite_vendue','')} | "
                f"Prix: {row_dict.get('prix_vendu_carton','')} | "
                f"Total: {row_dict.get('total','')} | "
                f"Date: {row_dict.get('date_vente','')}"
            )
            
            # Bouton téléchargement facture
            facture_path = row_dict.get('facture_path')
            if facture_path and os.path.exists(facture_path):
                with open(facture_path, 'rb') as f:
                    st.download_button(
                        label='Télécharger la facture',
                        data=f,
                        file_name=os.path.basename(facture_path),
                        mime="application/pdf",
                        key=f"download_{index}"
                    )

        # Tableau résumé sans chemin facture
        df_affichage = df.drop(columns=["facture_path"], errors='ignore')
        st.dataframe(df_affichage, width='stretch')

