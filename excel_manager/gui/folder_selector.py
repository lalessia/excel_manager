import tkinter as tk
from tkinter import filedialog, messagebox

def select_estratti_folder(parent=None):
    folder_path = filedialog.askdirectory(title="Seleziona la cartella con il file Excel CRM", parent=parent)

    if folder_path:
        messagebox.showinfo("Successo", "Cartella selezionata: " + folder_path, parent=parent)
        return folder_path
    else:
        messagebox.showwarning("Attenzione", "Nessuna cartella selezionata.", parent=parent)
        return None
