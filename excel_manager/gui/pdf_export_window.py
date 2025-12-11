import tkinter as tk
from tkinter import filedialog, messagebox
from gui.home_window import restore_home
from core.fattura_reader import estrai_dati_fattura   # 👈 IMPORTANTE
from core.fattura_generator import genera_pdf_fattura
import os

def show_pdf_export_window():
    print("DEBUG: sto usando il file AGGIORNATO di pdf_export_window")
    window = tk.Toplevel()
    window.title("Generazione Fattura")
    window.geometry("550x380")
    window.resizable(False, False)

    title = tk.Label(window, text="Generazione Fattura dalla prenotazione",
                     font=("Helvetica", 15, "bold"))
    title.pack(pady=15)

    selected_file_var = tk.StringVar()

    def seleziona_file_excel():
        file_path = filedialog.askopenfilename(
            title="Seleziona un file Excel",
            filetypes=[("Excel files", "*.xlsx")],
        )
        if file_path:
            selected_file_var.set(file_path)
            label_path.config(text=f"File selezionato:\n{file_path}", fg="green")
        else:
            label_path.config(text="Nessun file selezionato", fg="red")

    def genera_fattura():
        file_path = selected_file_var.get()
        if not file_path:
            messagebox.showwarning(
                "Attenzione", "Seleziona prima un file .xlsx."
            )
            return

        try:
            header = {
                'numero': '001',
                'data': '01/02/2025',
                'cliente': 'Mario Rossi',
                'indirizzo': 'Via Roma 10, Milano',
                'cf_piva': 'RSSMRA80A01F205X',
                'tot_affitto': 290,
                'tot_ritenuta': 29
            }

            # 👉 Estraggo i dati da Excel
            detail = estrai_dati_fattura(file_path)

            # --- CREAZIONE PERCORSO PDF ---
            folder = os.path.dirname(file_path)
            pdf_path = os.path.join(folder, "fattura_prenotazione.pdf")

            # 👉 Genero la fattura PDF
            print('header: ', header)
            print('type - header: ', type(header))
            print('detail: ', detail)
            print('type - detail: ', type(detail))
            print('pdf_path: ', pdf_path)
            print('type - pdf_path: ', type(pdf_path))
            genera_pdf_fattura(header, detail, pdf_path)

            messagebox.showinfo(
                "Fattura generata",
                f"Fattura creata correttamente!\n\nPercorso:\n{pdf_path}"
            )

        except Exception as e:
            messagebox.showerror("Errore", f"Errore durante la generazione PDF:\n{e}")
            return

    # bottone selezione file
    btn_select = tk.Button(window, text="📄 Seleziona file Excel",
                           font=("Helvetica", 12), width=25,
                           command=seleziona_file_excel)
    btn_select.pack(pady=10)

    label_path = tk.Label(window, text="Nessun file selezionato",
                          font=("Helvetica", 10), fg="red")
    label_path.pack(pady=5)

    btn_generate = tk.Button(window, text="🧾 Genera Fattura",
                             font=("Helvetica", 12, "bold"),
                             width=25, command=genera_fattura)
    btn_generate.pack(pady=30)

    btn_close = tk.Button(window, text="🔙 Torna alla Home",
                          font=("Helvetica", 11), width=25,
                          command=lambda: (window.destroy(), restore_home()))
    btn_close.pack(pady=10)
