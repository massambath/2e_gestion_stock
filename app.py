import streamlit as st
import pandas as pd
import os
from models.produit import afficher_produits, ajouter_produit
from models.vente import vendre_produit
from database.db_setup import init_db , get_connection
init_db()

st.set_page_config(page_title="Gestion de Stock",page_icon="📦")

st.title(" Application de gestion de stock")
st.write("Interface simple pour gérer les produits et enregistrer les ventes")

#------------Onglets---------
onglet = st.sidebar.radio("Navigation", ["Liste des produits", "Ajouter un produit","Enregistrer une vente","Historique"])

#--------Liste des produits----

if onglet == "Liste des produits":
    st.subheader("Liste actuelle des produits")

    data = afficher_produits(return_df=True)  #On ajoute cette option dans produit.py
    st.dataframe(data, use_container_width=True)

#-----Ajouter un produit-------
elif onglet == "Ajouter un produit":
    st.subheader("Ajouter un produit")

    reference = st.text_input("Référence du produit")
    nom = st.text_input("Nom du produit")
    categorie = st.text_input("Catégorie")
    prix = st.number_input("Prix carton", min_value=0.0)
    quantite = st.number_input("Quantite",min_value=0)

    if st.button("Ajouter"):
        if nom.strip() == "":
            st.error("Veuillez entre un nom")
        else:
            ajouter_produit(reference,nom,categorie,prix,quantite)
            st.success(f"Produit '{reference}' ajouté!")

#-----Vente--------------

elif onglet == "Enregistrer une vente":
    st.subheader("Vendre un produit")

    reference= st.text_input("reference du produit vendu")
    quantite_vendue =st.number_input("Quantité vendue", min_value=1)
    prix_vendu_carton = st.number_input("Prix vendu (carton)", min_value=0.0)
    nom_client = st.text_input("Nom du client")

    if st.button("Valider la vente"):
        result = vendre_produit(reference, quantite_vendue, prix_vendu_carton,nom_client, return_msg=True)
        
        if isinstance(result, dict):
            st.success(result["message"])
        else:
            st.error(result)

        # Si une facture est générée , affficher un bouton de téléchargement
        if "facture_path" in result:
            with open(result["facture_path"], "rb") as f:
                st.download_button(
                    label =" Télécharger la facture",
                    data = f,
                    file_name = result["facture_path"].split("/")[-1],
                    mime="application/pdf"
                )
#-----Onglet-------------

elif onglet=="Historique":
    st.title("Historique des ventes")
    conn = get_connection()

    df = pd.read_sql_query("SELECT * FROM ventes order by date_vente desc",conn)
    conn.close()
    
    #Affichage des ventes 
    for index ,row in df.iterrows():
        st.write(f"Référence: {row['reference']} | Client: {row.get('nom_client','')} | Quantité: {row['quantite_vendue']} | Prix: {row['prix_vendu_carton']} | Total: {row['total']} | Date: {row['date_vente']}")
        
        # bouton de téléchargement facture
        if row['facture_path'] and os.path.exists(row['facture_path']):
            with open(row['facture_path'], 'rb') as f:
                st.download_button(
                    label ='Télécharger la facture',
                    data= f,
                    file_name= os.path.basename(row['facture_path']),
                    mime="application/pdf",
                    key = f"download_{index}"

                )
    df_affichage = df.drop(columns=["facture_path"])

    st.dataframe(df_affichage, use_container_width=True)

   