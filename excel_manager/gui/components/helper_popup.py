'''
Classe che gestisce i popup di help
'''

import tkinter as tk
from tkinter import messagebox

def show_guide_export(parent=None, on_close_callback=None):
    def continua():
        guide_window.destroy()
        if on_close_callback:
            on_close_callback()

    guide_window = tk.Toplevel(parent)
    guide_window.title("Guida - Elaborazione File")
    guide_window.geometry("500x300")
    guide_window.resizable(False, False)

    # Titolo
    title = tk.Label(guide_window, text="📘 Guida rapida", font=("Helvetica", 16, "bold"))
    title.pack(pady=10)

    # Testo guida
    guida_testo = (
        "Per elaborare il resoconto mensile:\n\n"
        "1. Scegli una cartella che contiene il file Excel CRM\n"
        "2. Tutti i file nella cartella verranno processati\n"
        "3. Il risultato verrà salvato come 'resoconto_mensile.xlsx'\n\n"
        "Puoi modificare i dati prima del salvataggio nella schermata successiva."
    )

    label = tk.Label(guide_window, text=guida_testo, justify="left", font=("Helvetica", 11), wraplength=450)
    label.pack(pady=10)

    # Bottone per proseguire
    btn = tk.Button(guide_window, text="Continua", font=("Helvetica", 12), command=continua)
    btn.pack(pady=20)

    guide_window.mainloop()


def show_guide_pdf(parent=None, on_close_callback=None):
    def continua():
        guide_window.destroy()
        if on_close_callback:
            on_close_callback()

    guide_window = tk.Toplevel(parent)
    guide_window.title("Guida - Elaborazione File")
    guide_window.geometry("500x300")
    guide_window.resizable(False, False)

    # Titolo
    title = tk.Label(guide_window, text="📘 Guida rapida", font=("Helvetica", 16, "bold"))
    title.pack(pady=10)

    # Testo guida
    guida_testo = (
        "Per generare il pdf del resoconto mensile:\n\n"
        "1. Scegli il file Excel precedentemente elaborato\n"
        "2. Il file selezionato verrà esportato in .pdf\n"
        "3. ...\n\n"
    )

    label = tk.Label(guide_window, text=guida_testo, justify="left", font=("Helvetica", 11), wraplength=450)
    label.pack(pady=10)

    # Bottone per proseguire
    btn = tk.Button(guide_window, text="Continua", font=("Helvetica", 12), command=continua)
    btn.pack(pady=20)

    guide_window.mainloop()