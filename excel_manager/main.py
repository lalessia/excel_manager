from gui.windows.home_window import show_home
from gui.windows.elabora_excel_window import show_elabora_excel_window
from gui.windows.pdf_export_window import show_pdf_export_window
from core.services.extras_repository import init_db
import os

# ✅ Assicurati che la cartella per il DB esista
db_dir = os.path.join(os.path.dirname(__file__), "core", "db")
os.makedirs(db_dir, exist_ok=True)

# ✅ Inizializza il DB se non esiste
init_db()

def main():
    show_home(
        on_elabora_callback=show_elabora_excel_window,
        on_pdf_callback=show_pdf_export_window
    )

if __name__ == "__main__":
    main()
