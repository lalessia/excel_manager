'''
Classe che gestisce la home
'''

import tkinter as tk
from tkinter import Menu, messagebox
import sys

from gui.components.helper_popup import show_guide_export, show_guide_pdf  # Assicurati che il path sia corretto
from gui.windows.settings_extras_window import show_extras_settings

global_root = None

def restore_home():
    global_root.destroy()
    sys.exit()
    '''
    alternativa: 
    global global_root
    global_root.deiconify()
    '''
def restore_home():
    global_root.deiconify()
    global_root.focus_force()

    
def on_closing():
    """
    Funzione eseguita alla chiusura della finestra principale.
    Termina completamente l'applicazione.
    """
    if messagebox.askokcancel("Uscita", "Vuoi davvero uscire dall'applicazione?"):
        global_root.destroy()
        sys.exit()  # ✅ Termina l'app
    
def show_home(on_elabora_callback, on_pdf_callback):
    global global_root
    global_root = tk.Tk()
    global_root.title("Mati Excel Manager – Home")
    global_root.geometry("500x350")
    global_root.resizable(False, False)
    # ✅ Chiude correttamente tutto alla "X"
    global_root.protocol("WM_DELETE_WINDOW", on_closing)
    # -------- Menù --------
    menubar = Menu(global_root)

    # File
    file_menu = Menu(menubar, tearoff=0)
    file_menu.add_command(label="Esci", command=global_root.quit)
    menubar.add_cascade(label="File", menu=file_menu)
    
    # Settings
    settings_menu = Menu(menubar, tearoff=0)
    settings_menu.add_command(
        label="Gestione Extra",
        command=lambda: (
            global_root.withdraw(),
            show_extras_settings(
                parent=global_root,
                on_close_callback=restore_home
            )
        )
    )
    menubar.add_cascade(label="Settings", menu=settings_menu)

    # Guida
    guida_menu = Menu(menubar, tearoff=0)
    guida_menu.add_command(
        label="Elaborazione Excel",
        command=lambda: (global_root.withdraw(), show_guide_export(parent=global_root, on_close_callback=restore_home))
    )
    guida_menu.add_command(
        label="Generazione PDF",
        command=lambda: (global_root.withdraw(), show_guide_pdf(parent=global_root, on_close_callback=restore_home))
    )
    menubar.add_cascade(label="Guida", menu=guida_menu)

    global_root.config(menu=menubar)

    # -------- Titolo e descrizione --------
    title = tk.Label(global_root, text="Benvenutə in Mati Excel Manager", font=("Helvetica", 18, "bold"))
    title.pack(pady=20)

    description = tk.Label(
        global_root,
        text="Scegli una delle funzionalità disponibili:",
        font=("Helvetica", 12)
    )
    description.pack(pady=10)

    # -------- Bottone Elaborazione --------
    elabora_button = tk.Button(
        global_root,
        text="Elaborazione file Excel",
        font=("Helvetica", 12),
        width=30,
        height=2,
        command=lambda: (global_root.withdraw(), on_elabora_callback())
    )
    elabora_button.pack(pady=30)
    
    # Bottone 2 – Esportazione PDF
    btn_pdf = tk.Button(
        global_root, 
        text="Esportazione rendiconto.pdf", 
        font=("Helvetica", 12),
        width=30,
        height=2,
        command=lambda: (global_root.withdraw(), on_pdf_callback())
    )
    btn_pdf.pack(pady=10)

    # Footer (opzionale)
    footer = tk.Label(
        global_root,
        text="© 2025 Mati Tool - by Alessia Profeta",
        font=("Helvetica", 9),
        fg="gray"
    )
    footer.pack(side="bottom", pady=10)

    global_root.mainloop()
