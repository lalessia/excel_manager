import tkinter as tk
from tkinter import filedialog, messagebox
from gui.components.data_table import show_dataframe_table
from core.io.excel_reader import load_xlsx, extract_clean_data
#from core.data_extractor import estrai_colonne_rilevanti
from gui.components.extras_editor import show_extras_editor
from gui.windows.home_window import restore_home
import os

def show_elabora_excel_window():
    window = tk.Toplevel()
    window.title("Elaborazione File Excel")
    window.geometry("600x400")
    window.resizable(False, False)

    label = tk.Label(window, text="Seleziona la cartella 'estratti_crm'", font=("Helvetica", 12))
    label.pack(pady=20)

    selected_path_var = tk.StringVar()

    def seleziona_file():
        file_path = filedialog.askopenfilename(
            title="Seleziona file Excel",
            filetypes=[("File Excel", "*.xlsx")]
        )
        if file_path:
            selected_path_var.set(file_path)
            path_label.config(
                text=f"File selezionato:\n{file_path}",
                fg="green"
            )
        else:
            path_label.config(text="Nessun file selezionato", fg="red")

    def avvia_elaborazione():
        try:
            file_path = selected_path_var.get()

            if not file_path:
                messagebox.showwarning("Attenzione", "Seleziona prima un file Excel.")
                return

            df_full = load_xlsx(file_path)
            df_ridotto = extract_clean_data(df_full)

            show_extras_editor(df_ridotto, on_done_callback=mostra_riepilogo)

        except Exception as e:
            messagebox.showerror(
                "Errore",
                f"Errore durante l'elaborazione:\n{e}"
        )
            
    def mostra_riepilogo(df_finale):
        # Qui mostriamo il dataframe finale
        input_file = selected_path_var.get()
        base_folder = os.path.dirname(input_file)
        show_dataframe_table(df_finale, base_folder)
        #show_dataframe_table(df_finale, selected_path_var.get())

    tk.Button(window, text="📄 Seleziona file Excel", command=seleziona_file, width=25).pack(pady=10)

    path_label = tk.Label(window, text="Nessun file selezionato", font=("Helvetica", 10), fg="red")
    path_label.pack()

    tk.Button(window, text="✅ Avvia elaborazione", command=avvia_elaborazione, width=25).pack(pady=20)

    # Pulsante per chiudere
    # tk.Button(window, text="❌ Chiudi", command=window.destroy).pack(pady=10)
    tk.Button(window, text="🏠 Torna alla Home", width=25, command=lambda: (window.destroy(), restore_home())).pack(pady=10)

