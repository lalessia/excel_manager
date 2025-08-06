from gui.folder_selector import select_estratti_folder
from core.data_loader import load_xlsx_from_folder
from gui.data_confirmation import confirm_and_write

def main():
    print("Avvio applicazione Excel Manager...")
    selected_folder = select_estratti_folder()

    if selected_folder:
        print(f"Folder selezionata: {selected_folder}")
        try:
            df = load_xlsx_from_folder(selected_folder)
            print("Anteprima dati:")
            print(df.head())
            confirm_and_write(df, selected_folder)
        except Exception as e:
            print(f"Errore durante il caricamento: {e}")
    else:
        print("Nessuna cartella selezionata.")


if __name__ == "__main__":
    main()
