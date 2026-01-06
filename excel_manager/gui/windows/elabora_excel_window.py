import tkinter as tk
from tkinter import filedialog, messagebox
from gui.components.data_table import show_dataframe_table
from core.io.excel_reader import load_xlsx_from_folder, extract_clean_data
#from core.data_extractor import estrai_colonne_rilevanti
from gui.components.extras_editor import show_extras_editor
from gui.windows.home_window import restore_home

def show_elabora_excel_window():
    window = tk.Toplevel()
    window.title("Elaborazione File Excel")
    window.geometry("600x400")
    window.resizable(False, False)

    label = tk.Label(window, text="Seleziona la cartella 'estratti_crm'", font=("Helvetica", 12))
    label.pack(pady=20)

    selected_path_var = tk.StringVar()

    def seleziona_cartella():
        folder = filedialog.askdirectory(title="Seleziona cartella 'estratti_crm'")
        if folder:
            selected_path_var.set(folder)
            path_label.config(text=f"Cartella selezionata:\n{folder}", fg="green")
        else:
            path_label.config(text="Nessuna cartella selezionata", fg="red")

    def avvia_elaborazione():
        folder = selected_path_var.get()
        if not folder:
            messagebox.showwarning("Attenzione", "Seleziona prima una cartella.")
            return
        try:
            df_full = load_xlsx_from_folder(folder)
            df_ridotto = extract_clean_data(df_full)

            # GUI per inserimento extra
            show_extras_editor(df_ridotto, on_done_callback=mostra_riepilogo)
        except Exception as e:
            messagebox.showerror("Errore", f"Errore durante l'elaborazione:\n{e}")
            return
            
    def mostra_riepilogo(df_finale):
        # Qui mostriamo il dataframe finale
        show_dataframe_table(df_finale, selected_path_var.get())

    tk.Button(window, text="📁 Seleziona cartella", command=seleziona_cartella, width=25).pack(pady=10)

    path_label = tk.Label(window, text="Nessuna cartella selezionata", font=("Helvetica", 10), fg="red")
    path_label.pack()

    tk.Button(window, text="✅ Avvia elaborazione", command=avvia_elaborazione, width=25).pack(pady=20)

    # Pulsante per chiudere
    # tk.Button(window, text="❌ Chiudi", command=window.destroy).pack(pady=10)
    tk.Button(window, text="🏠 Torna alla Home", width=25, command=lambda: (window.destroy(), restore_home())).pack(pady=10)

