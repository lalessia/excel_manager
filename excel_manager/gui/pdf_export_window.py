import tkinter as tk
from gui.home_window import restore_home

def show_pdf_export_window():
    window = tk.Toplevel()
    window.title("Esportazione PDF - Work in Progress")
    window.geometry("500x300")
    window.resizable(False, False)

    label = tk.Label(
        window,
        text="🚧 Funzionalità in sviluppo 🚧\n\nQui in futuro potrai esportare i dati in formato PDF.",
        font=("Helvetica", 12),
        justify="center"
    )
    label.pack(pady=50)

    btn_close = tk.Button(
        window,
        text="🔙 Torna alla Home",
        font=("Helvetica", 11),
        width=25,
        height=2,
        command=lambda: (window.destroy(), restore_home())
    )
    btn_close.pack(pady=20)
