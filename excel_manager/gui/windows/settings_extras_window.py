import tkinter as tk
from tkinter import ttk, messagebox

from gui.windows.settings_extra_form_popup import show_extra_form
from core.services.extras_repository import (
    get_all_extras,
    insert_extra,
    update_extra,
    delete_extra
)


def show_extras_settings(parent=None, on_close_callback=None):
    window = tk.Toplevel(parent)
    window.title("Settings – Gestione Extra")
    window.geometry("520x420")
    window.resizable(False, False)

    # --------------------------------------------------
    # Chiusura
    # --------------------------------------------------
    def on_close():
        window.destroy()
        if on_close_callback:
            on_close_callback()

    window.protocol("WM_DELETE_WINDOW", on_close)

    # --------------------------------------------------
    # Titolo
    # --------------------------------------------------
    tk.Label(
        window,
        text="Gestione Extra",
        font=("Helvetica", 16, "bold")
    ).pack(pady=15)

    # --------------------------------------------------
    # Tabella con scrollbar
    # --------------------------------------------------
    table_frame = ttk.Frame(window)
    table_frame.pack(fill="both", expand=True, padx=20, pady=(0, 10))

    tree = ttk.Treeview(
        table_frame,
        columns=("id", "nome", "prezzo"),
        show="headings"
    )

    tree.heading("id", text="ID")
    tree.heading("nome", text="Nome Extra")
    tree.heading("prezzo", text="Prezzo (€)")

    tree.column("id", width=0, stretch=False)  # ID nascosto
    tree.column("nome", width=300)
    tree.column("prezzo", width=100, anchor="center")

    tree.pack(side="left", fill="both", expand=True)

    scrollbar = ttk.Scrollbar(
        table_frame,
        orient="vertical",
        command=tree.yview
    )
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    # --------------------------------------------------
    # Caricamento dati DB
    # --------------------------------------------------
    def load_extras():
        tree.delete(*tree.get_children())
        for extra_id, nome, prezzo in get_all_extras():
            tree.insert(
                "",
                "end",
                values=(extra_id, nome, f"{prezzo:.2f}")
            )

    load_extras()

    # --------------------------------------------------
    # Azioni
    # --------------------------------------------------
    actions_frame = tk.Frame(window)
    actions_frame.pack(pady=15)

    # ---- Nuovo ----
    def nuovo_extra():
        def on_save(data):
            extra_id = insert_extra(data["nome"], data["prezzo"])
            tree.insert(
                "",
                "end",
                values=(extra_id, data["nome"], f"{data['prezzo']:.2f}")
            )

        show_extra_form(parent=window, on_save_callback=on_save)

    # ---- Modifica ----
    def modifica_extra():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Attenzione", "Seleziona un extra da modificare.")
            return

        item_id = selected[0]
        extra_id, nome, prezzo = tree.item(item_id, "values")

        if extra_id is None:
            messagebox.showerror("Errore", "ID extra non valido.")
            return

        def on_save(data):
            success = update_extra(
                int(extra_id),
                data["nome"],
                data["prezzo"]
            )
            if success:
                tree.item(
                    item_id,
                    values=(extra_id, data["nome"], f"{data['prezzo']:.2f}")
                )
            else:
                messagebox.showerror("Errore", "Aggiornamento non riuscito.")

        show_extra_form(
            parent=window,
            extra_data={
                "nome": nome,
                "prezzo": float(prezzo)
            },
            on_save_callback=on_save
        )

    # ---- Elimina ----
    def elimina_extra():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Attenzione", "Seleziona un extra da eliminare.")
            return

        if not messagebox.askyesno("Conferma", "Vuoi eliminare l'extra selezionato?"):
            return

        extra_id = tree.item(selected[0], "values")[0]

        if extra_id is None:
            messagebox.showerror("Errore", "ID extra non valido.")
            return

        if delete_extra(int(extra_id)):
            tree.delete(selected[0])
        else:
            messagebox.showerror("Errore", "Eliminazione non riuscita.")

    # --------------------------------------------------
    # Bottoni
    # --------------------------------------------------
    tk.Button(actions_frame, text="➕ Nuovo", width=12, command=nuovo_extra).pack(side="left", padx=5)
    tk.Button(actions_frame, text="✏️ Modifica", width=12, command=modifica_extra).pack(side="left", padx=5)
    tk.Button(actions_frame, text="❌ Elimina", width=12, command=elimina_extra).pack(side="left", padx=5)

    # --------------------------------------------------
    # Footer
    # --------------------------------------------------
    tk.Button(
        window,
        text="⬅️ Torna alla Home",
        width=20,
        command=on_close
    ).pack(pady=10)
