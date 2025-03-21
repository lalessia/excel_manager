import os
from excel_manager import ExcelManager
from invoice_generator import InvoiceGenerator

if __name__ == "__main__":
    # data_folder = "../data"  # La cartella principale dove sono salvati gli appartamenti
    data_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data"))
    if os.path.exists(data_folder):
        apartment_totals = ExcelManager.process_all_files(data_folder)  # Restituisce il dizionario {apartment_name: total}
        ExcelManager.update_summary(apartment_totals)  # Usa il dizionario per aggiornare summary.xlsx
        print("Operazione completata!")
        
        print("Generazione fatture...")
        invoice_gen = InvoiceGenerator()
        print('data_folder: ', data_folder)
        invoice_gen.generate_all_invoices(data_folder)
    else:
        print(f"La cartella '{data_folder}' non esiste.")
