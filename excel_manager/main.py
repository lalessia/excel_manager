'''
from gui.home_window import show_home
from gui.helper_popup import show_guide_export, show_guide_pdf
from gui.folder_selector import select_estratti_folder
from gui.data_table import show_dataframe_table
from core.data_loader import load_xlsx_from_folder


def main():
    def elabora_excel():
        show_guide_export(on_close_callback=seleziona_cartella)
        
    def estrai_pdf():
        show_guide_pdf(on_close_callback=seleziona_cartella)

    def seleziona_cartella():
        folder = select_estratti_folder()
        if folder:
            try:
                df = load_xlsx_from_folder(folder)
                show_dataframe_table(df, folder)
            except Exception as e:
                print(f"Errore: {e}")
        else:
            print("Nessuna cartella selezionata")
    
    show_home(on_elabora_callback=elabora_excel, on_pdf_callback=estrai_pdf)

if __name__ == "__main__":
    main()
'''

from gui.home_window import show_home
from gui.elabora_excel_window import show_elabora_excel_window  # nuova GUI
from gui.pdf_export_window import show_pdf_export_window        # in futuro
from core.data_cleared import DataCleaner


def main():
    show_home(
        on_elabora_callback=show_elabora_excel_window,
        on_pdf_callback=show_pdf_export_window  # Placeholder
    )

if __name__ == "__main__":
    main()