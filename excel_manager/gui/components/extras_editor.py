import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd

from core.processing.data_cleaner import DataCleaner
from core.services.extras_repository import get_all_extras


def show_extras_editor(df, on_done_callback):
    # ======================================================
    # FINESTRA PRINCIPALE
    # ======================================================
    window = tk.Toplevel()
    window.title("Aggiungi Extra per Prenotazione")
    window.geometry("1000x400")
    window.resizable(True, True)

    frame = tk.Frame(window)
    frame.pack(fill="both", expand=True)

    # ======================================================
    # TREEVIEW PRINCIPALE CON SCROLLBAR
    # ======================================================
    tree = ttk.Treeview(frame, show="headings")
    tree.grid(row=0, column=0, sticky="nsew")

    scrollbar_y = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    scrollbar_y.grid(row=0, column=1, sticky="ns")

    scrollbar_x = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
    scrollbar_x.grid(row=1, column=0, sticky="ew")

    tree.configure(
        yscrollcommand=scrollbar_y.set,
        xscrollcommand=scrollbar_x.set
    )

    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    # ======================================================
    # COLONNA "PAGAMENTO CARTA"
    # ======================================================
    if "Pagamento carta" not in df.columns:
        df["Pagamento carta"] = False

    cols = df.columns.tolist()
    tree["columns"] = cols

    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor="center")

    # Popolamento treeview
    for _, row in df.iterrows():
        values = list(row)
        idx_pagamento = df.columns.get_loc("Pagamento carta")
        values[idx_pagamento] = "☑" if row["Pagamento carta"] else "☐"
        tree.insert("", "end", values=values)

    # ======================================================
    # TOGGLE CHECKBOX PAGAMENTO CARTA
    # ======================================================
    def on_tree_click(event):
        region = tree.identify("region", event.x, event.y)
        if region != "cell":
            return

        column = tree.identify_column(event.x)
        row_id = tree.identify_row(event.y)

        col_index = int(column.replace("#", "")) - 1
        col_name = df.columns[col_index]

        if col_name != "Pagamento carta":
            return

        row_index = tree.index(row_id)
        new_value = not df.at[row_index, "Pagamento carta"]
        df.at[row_index, "Pagamento carta"] = new_value

        values = list(df.iloc[row_index])
        values[col_index] = "☑" if new_value else "☐"
        tree.item(row_id, values=values)

    tree.bind("<Button-1>", on_tree_click)

    # ======================================================
    # MODIFICA RIGA → POPUP EXTRA
    # ======================================================
    def modifica_riga():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Selezione", "Seleziona una riga da modificare")
            return

        idx = tree.index(selected[0])
        riga = df.iloc[idx]

        popup = tk.Toplevel(window)
        popup.title(f"Aggiungi extra – ID {riga['ID']}")
        popup.geometry("420x480")
        popup.resizable(False, False)

        # --------------------------------------------------
        # RECUPERO EXTRA DAL DB
        # --------------------------------------------------
        extras_db = get_all_extras()  # [(id, nome, prezzo)]
        extras_map = {nome: prezzo for _, nome, prezzo in extras_db}
        extra_disponibili = set(extras_map.keys())
        extra_selezionati = []

        # --------------------------------------------------
        # SELEZIONE EXTRA
        # --------------------------------------------------
        tk.Label(popup, text="Extra:").pack(pady=(10, 0))

        extra_var = tk.StringVar()
        combo = ttk.Combobox(
            popup,
            textvariable=extra_var,
            values=sorted(extra_disponibili),
            state="readonly"
        )
        combo.pack()

        tk.Label(popup, text="Quantità:").pack(pady=(10, 0))
        qty_var = tk.IntVar(value=1)
        tk.Entry(popup, textvariable=qty_var, width=10).pack()

        # --------------------------------------------------
        # RIEPILOGO EXTRA AGGIUNTI
        # --------------------------------------------------
        tk.Label(popup, text="Riepilogo extra aggiunti").pack(pady=(20, 5))

        riepilogo = ttk.Treeview(
            popup,
            columns=("extra", "qty", "totale"),
            show="headings",
            height=6
        )
        riepilogo.heading("extra", text="Extra")
        riepilogo.heading("qty", text="Qty")
        riepilogo.heading("totale", text="Totale €")

        riepilogo.column("extra", width=180)
        riepilogo.column("qty", width=50, anchor="center")
        riepilogo.column("totale", width=80, anchor="e")

        riepilogo.pack()

        totale_var = tk.StringVar(value="Totale: € 0.00")
        tk.Label(
            popup,
            textvariable=totale_var,
            font=("Arial", 10, "bold")
        ).pack(pady=(5, 10))

        # --------------------------------------------------
        # FUNZIONI DI SUPPORTO UI
        # --------------------------------------------------
        def aggiorna_combo_extra():
            combo["values"] = sorted(extra_disponibili)
            extra_var.set("")

        def aggiorna_riepilogo():
            riepilogo.delete(*riepilogo.get_children())
            totale = 0

            for e in extra_selezionati:
                subtot = e["prezzo"] * e["qty"]
                totale += subtot
                riepilogo.insert(
                    "",
                    "end",
                    values=(e["nome"], e["qty"], f"{subtot:.2f}")
                )

            totale_var.set(f"Totale: € {totale:.2f}")

        # --------------------------------------------------
        # RIMOZIONE EXTRA (DOPPIO CLICK)
        # --------------------------------------------------
        def rimuovi_extra(event):
            selected = riepilogo.selection()
            if not selected:
                return

            item = riepilogo.item(selected[0])
            nome = item["values"][0]

            for e in extra_selezionati:
                if e["nome"] == nome:
                    extra_selezionati.remove(e)
                    break

            extra_disponibili.add(nome)

            aggiorna_riepilogo()
            aggiorna_combo_extra()

        # 👉 BIND CORRETTO
        riepilogo.bind("<Double-1>", rimuovi_extra)

        # --------------------------------------------------
        # AGGIUNTA EXTRA
        # --------------------------------------------------
        def aggiungi_extra():
            nome = extra_var.get()
            qty = qty_var.get()

            if not nome or qty <= 0:
                messagebox.showwarning("Errore", "Seleziona un extra e una quantità valida")
                return

            extra_selezionati.append({
                "nome": nome,
                "prezzo": extras_map[nome],
                "qty": qty
            })

            extra_disponibili.remove(nome)
            aggiorna_riepilogo()
            aggiorna_combo_extra()

        tk.Button(popup, text="➕ Aggiungi extra", command=aggiungi_extra).pack(pady=5)

        # --------------------------------------------------
        # CONFERMA FINALE
        # --------------------------------------------------
        def conferma():
            if extra_selezionati:
                totale = sum(e["prezzo"] * e["qty"] for e in extra_selezionati)
                descrizione = ", ".join(
                    f"{e['nome']}({e['prezzo']}*{e['qty']})"
                    for e in extra_selezionati
                )

                df.at[idx, "Importo extra"] = totale
                df.at[idx, "Descrizione extra"] = descrizione
                tree.item(selected[0], values=list(df.iloc[idx]))

            popup.destroy()

        tk.Button(popup, text="✅ Conferma", command=conferma).pack(pady=10)

    # ======================================================
    # CONFERMA MODIFICHE GLOBALI
    # ======================================================
    def conferma_modifiche():
        cleaner = DataCleaner(df)
        cleaned_df = cleaner.clean()
        on_done_callback(cleaned_df)
        window.destroy()

    tk.Button(window, text="✏️ Modifica selezione", command=modifica_riga).pack(pady=10)
    tk.Button(window, text="✅ Procedi al riepilogo", command=conferma_modifiche).pack(pady=5)
    tk.Button(window, text="🏠 Torna indietro", command=window.destroy).pack(pady=5)
