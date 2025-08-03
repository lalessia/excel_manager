import tkinter as tk
from tkinter import messagebox
import pandas as pd
from pathlib import Path
from core.data_writer import write_dataframe_to_file

def confirm_and_write(df_new, estratti_folder_path):
    estratti_path = Path(estratti_folder_path)
    resoconto_path = estratti_path.parent / "resoconto_mensile.xlsx"

    if not resoconto_path.exists():
        raise FileNotFoundError(f"Il file {resoconto_path} non esiste.")

    # GUI setup
    root = tk.Tk()
    root.withdraw()

    preview = df_new.head().to_string()
    message = f"Anteprima nuovi dati:\n\n{preview}\n\nVuoi aggiungerli al file resoconto_mensile.xlsx?"

    if messagebox.askyesno("Conferma inserimento", message):
        try:
            df_existing = pd.read_excel(resoconto_path)
            df_combined = pd.concat([df_existing, df_new], ignore_index=True)
            write_dataframe_to_file(df_combined, resoconto_path)
            messagebox.showinfo("Successo", "✅ Dati aggiunti con successo!")
        except Exception as e:
            messagebox.showerror("Errore durante scrittura", str(e))
    else:
        messagebox.showinfo("Operazione annullata", "⛔ Nessuna modifica apportata.")
