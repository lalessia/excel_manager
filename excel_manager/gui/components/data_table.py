'''
Gestione della tabella e dei dettagli prima del salvataggio
'''
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from pathlib import Path
import os


def show_dataframe_table(df: pd.DataFrame, save_folder: str, parent=None):
    def salva_file():
        try:
            base_path = Path(save_folder)
            preprocessing_dir = base_path / "preprocessing"

            # Crea la cartella se non esiste
            preprocessing_dir.mkdir(parents=True, exist_ok=True)

            filepath = preprocessing_dir / "resoconto_mensile.xlsx"

            df.to_excel(filepath, index=False)

            messagebox.showinfo(
                "Successo",
                f"File salvato in:\n{filepath}"
            )
            table_window.destroy()

        except Exception as e:
            messagebox.showerror(
                "Errore",
                f"Impossibile salvare il file:\n{e}"
            )

    
    def torna_alla_modifica():
        table_window.destroy()
        if on_edit_callback:
            on_edit_callback(df)
            
    table_window = tk.Tk()
    table_window.title("Riepilogo Dati - Resoconto")
    table_window.geometry("800x500")

    # Titolo
    label = tk.Label(table_window, text="Riepilogo dati elaborati", font=("Helvetica", 14, "bold"))
    label.pack(pady=10)

    # Tabella
    frame = ttk.Frame(table_window)
    frame.pack(fill="both", expand=True)

    tree = ttk.Treeview(frame, columns=list(df.columns), show="headings")
    for col in df.columns:
        tree.heading(col, text=col)
        tree.column(col, width=120)

    for _, row in df.iterrows():
        tree.insert("", "end", values=list(row))

    scrollbar_y = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    scrollbar_x = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
    tree.configure(yscroll=scrollbar_y.set, xscroll=scrollbar_x.set)

    tree.pack(side="left", fill="both", expand=True)
    scrollbar_y.pack(side="right", fill="y")
    scrollbar_x.pack(side="bottom", fill="x")

    # Bottone Salva
    btn_salva = tk.Button(table_window, text="💾 Salva Resoconto", font=("Helvetica", 12), command=salva_file)
    btn_salva.pack(pady=15)
    
    # 👇 Questo va messo prima dei bottoni
    button_frame = tk.Frame(table_window)
    button_frame.pack(pady=15)
    
    btn_torna = tk.Button(button_frame, text="↩️ Torna alla modifica", font=("Helvetica", 12), command=torna_alla_modifica)
    btn_torna.pack(side="left", padx=10)

    table_window.mainloop()
