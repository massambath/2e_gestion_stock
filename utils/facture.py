import datetime
import os
from reportlab.pdfgen import canvas

FACTURE_DIR = "factures"

os.makedirs(FACTURE_DIR,exist_ok=True)

def generer_facture(nom, quantite, prix_carton, total):
    date_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"facture_{nom}_{date_str}.pdf"
    filepath = os.path.join(FACTURE_DIR, filename)

    c = canvas.Canvas(filepath)
    c.setFont("Helvetica", 14)

    c.drawString(100, 750, "FACTURE")
    c.drawString(100, 700, f"Produit : {nom}")
    c.drawString(100, 680, f"Quantité vendue : {quantite}")
    c.drawString(100, 660, f"Prix du carton : {prix_carton} CFA")
    c.drawString(100, 640, f"Total : {total} CFA")
    c.drawString(100, 620, f"Date : {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

    c.save()

    return filepath