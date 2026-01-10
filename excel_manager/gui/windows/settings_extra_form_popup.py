import tkinter as tk
from tkinter import messagebox


def show_extra_form(
    parent,
    on_save_callback,
    extra_data=None
):
    """
    Popup per Nuovo / Modifica Extra

    :param parent: finestra padre
    :param on_save_callback: funzione chiamata al salvataggio
    :param extra_data: dict {'nome': str, 'prezzo': float} oppure None
    """

    is_edit = extra_data is not None

    window = tk.Toplevel(parent)
    window.title("Modifica Extra" if is_edit else "Nuovo Extra")
    window.geometry("360x260")
    window.resizable(False, False)
    window.grab_set()  # blocca la finestra padre

    # -------- Titolo --------
    title = tk.Label(
        window,
        text="Modifica Extra" if is_edit else "Nuovo Extra",
        font=("Helvetica", 14, "bold")
    )
    title.pack(pady=15)

    # -------- Form --------
    form_frame = tk.Frame(window)
    form_frame.pack(padx=20, pady=10)

    tk.Label(form_frame, text="Nome extra").grid(row=0, column=0, sticky="w")
    nome_var = tk.StringVar(value=extra_data["nome"] if is_edit else "")
    nome_entry = tk.Entry(form_frame, textvariable=nome_var, width=30)
    nome_entry.grid(row=1, column=0, pady=5)

    tk.Label(form_frame, text="Prezzo (€)").grid(row=2, column=0, sticky="w")
    prezzo_var = tk.StringVar(
        value=str(extra_data["prezzo"]) if is_edit else ""
    )
    prezzo_entry = tk.Entry(form_frame, textvariable=prezzo_var, width=30)
    prezzo_entry.grid(row=3, column=0, pady=5)

    nome_entry.focus()

    # -------- Azioni --------
    def salva():
        nome = nome_var.get().strip()
        prezzo_raw = prezzo_var.get().strip()

        if not nome:
            messagebox.showwarning("Errore", "Il nome dell'extra è obbligatorio.")
            return

        try:
            prezzo = float(prezzo_raw)
            if prezzo < 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning(
                "Errore",
                "Il prezzo deve essere un numero maggiore o uguale a 0."
            )
            return

        on_save_callback({
            "nome": nome,
            "prezzo": prezzo
        })

        window.destroy()

    def annulla():
        window.destroy()

    buttons_frame = tk.Frame(window)
    buttons_frame.pack(pady=15)

    btn_save = tk.Button(
        buttons_frame,
        text="💾 Salva",
        width=12,
        command=salva
    )
    btn_cancel = tk.Button(
        buttons_frame,
        text="Annulla",
        width=12,
        command=annulla
    )

    btn_save.pack(side="left", padx=5)
    btn_cancel.pack(side="left", padx=5)
