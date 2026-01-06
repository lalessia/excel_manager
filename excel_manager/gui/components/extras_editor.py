import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pandas as pd
from core.processing.data_cleaner import DataCleaner


def show_extras_editor(df, on_done_callback):
    window = tk.Toplevel()
    window.title("Modifica Extra per Prenotazione")
    window.geometry("1000x400")
    window.resizable(True, True)

    frame = tk.Frame(window)
    frame.pack(fill="both", expand=True)

    tree = ttk.Treeview(frame, show="headings")
    tree.pack(side="left", fill="both", expand=True)

    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    scrollbar.pack(side="right", fill="y")
    tree.configure(yscrollcommand=scrollbar.set)

    cols = df.columns.tolist()
    tree["columns"] = cols

    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor="center")

    for _, row in df.iterrows():
        tree.insert("", "end", values=list(row))

    # dizionario per modifiche extra
    modifiche_extra = {}

    def modifica_riga():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Selezione", "Seleziona una riga da modificare")
            return

        idx = tree.index(selected[0])
        riga = df.iloc[idx]

        popup = tk.Toplevel(window)
        popup.title(f"Aggiungi extra – ID {riga['ID']}")
        popup.geometry("300x200")

        tk.Label(popup, text="Importo extra:").pack(pady=5)
        extra_var = tk.DoubleVar(value=riga.get("Importo extra", 0))
        tk.Entry(popup, textvariable=extra_var).pack()

        tk.Label(popup, text="Descrizione extra:").pack(pady=5)
        descr_var = tk.StringVar(value=riga.get("Descrizione extra", ""))
        tk.Entry(popup, textvariable=descr_var).pack()

        def conferma():
            df.at[idx, "Importo extra"] = extra_var.get()
            df.at[idx, "Descrizione extra"] = descr_var.get()

            # aggiorna la riga visivamente
            tree.item(selected[0], values=list(df.iloc[idx]))
            popup.destroy()

        tk.Button(popup, text="Conferma", command=conferma).pack(pady=10)
    '''
    def conferma_modifiche():
        on_done_callback(df)
        window.destroy()
    '''
            
    def conferma_modifiche():
        print("[DEBUG] Conferma modifiche cliccato")
        cleaner = DataCleaner(df)
        cleaned_df = cleaner.clean()
        on_done_callback(cleaned_df)
        window.destroy()

    tk.Button(window, text="✏️ Modifica selezione", command=modifica_riga).pack(pady=10)
    tk.Button(window, text="✅ Procedi al riepilogo", command=conferma_modifiche).pack(pady=5)
    # 👇 Nuovo bottone "Torna alla home"
    tk.Button(window, text="🏠 Torna indietro", command=window.destroy).pack(pady=5)