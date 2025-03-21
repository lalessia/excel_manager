from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import openpyxl
import os

class InvoiceGenerator:
    def __init__(self, output_folder="invoices"):
        self.output_folder = output_folder
        os.makedirs(output_folder, exist_ok=True)  # Crea la cartella se non esiste

    def generate_invoice(self, excel_file):
        """Legge i dati dal file Excel e genera un PDF della fattura."""
        workbook = openpyxl.load_workbook(excel_file)
        sheet = workbook.active
        
        # Estrai dati dalla fattura
        apartment_name = sheet["C2"].value  # Nome dell'appartamento
        total_amount = sheet["C11"].value   # Totale da fatturare
        invoice_number = f"INV-{apartment_name}-{sheet['A1'].value}"  # Numero fattura
        
        if not apartment_name or not total_amount:
            print(f"Errore: dati mancanti in {excel_file}")
            return

        # Creazione PDF
        invoice_file = os.path.join(self.output_folder, f"{invoice_number}.pdf")
        c = canvas.Canvas(invoice_file, pagesize=A4)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(100, 800, "Fattura")  # Titolo
        c.setFont("Helvetica", 12)
        c.drawString(100, 770, f"Numero Fattura: {invoice_number}")
        c.drawString(100, 750, f"Appartamento: {apartment_name}")
        c.drawString(100, 730, f"Totale: € {total_amount}")

        c.save()
        print(f"Fattura generata: {invoice_file}")

    def generate_all_invoices(self, data_folder):
        """Genera fatture per tutti i file Excel nelle sottocartelle di `data_folder`."""
        for apartment_name in os.listdir(data_folder):
            apartment_path = os.path.join(data_folder, apartment_name)

            # Ignora la cartella 'summary_apartment'
            if not os.path.isdir(apartment_path) or apartment_name == "summary_apartment":
                continue
            
            for file_name in os.listdir(apartment_path):
                if file_name.endswith(".xlsx") and not file_name.startswith("~$"):  # Evita file temporanei
                    excel_file = os.path.join(apartment_path, file_name)
                    self.generate_invoice(excel_file)
