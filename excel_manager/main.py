from gui.windows.home_window import show_home
from gui.windows.elabora_excel_window import show_elabora_excel_window  # nuova GUI
from gui.windows.pdf_export_window import show_pdf_export_window        # in futuro

def main():
    show_home(
        on_elabora_callback=show_elabora_excel_window,
        on_pdf_callback=show_pdf_export_window  # Placeholder
    )

if __name__ == "__main__":
    main()