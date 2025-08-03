import tkinter as tk
from tkinter import filedialog

def select_estratti_folder():
    root = tk.Tk()
    root.withdraw()  # Nasconde la finestra principale

    folder_path = filedialog.askdirectory(title="Seleziona la cartella 'estratti_crm'")
    
    return folder_path
