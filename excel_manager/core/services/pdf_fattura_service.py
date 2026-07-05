import math
import os
import sys
from fpdf import FPDF


def resource_path(relative_path: str) -> str:
    """
    Restituisce il percorso assoluto di una risorsa, compatibile con PyInstaller.

    Durante l'esecuzione come file eseguibile, PyInstaller utilizza una directory
    temporanea (_MEIPASS). Questa funzione garantisce il corretto accesso
    a font, immagini e altre risorse statiche sia in sviluppo che in produzione.

    Args:
        relative_path (str): Percorso relativo della risorsa.

    Returns:
        str: Percorso assoluto della risorsa.
    """
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


class FatturaPDF(FPDF):
    """
    Estensione della classe FPDF per la generazione di fatture personalizzate.

    Gestisce:
    - caricamento dei font
    - intestazione con logo e data
    - piè di pagina con numerazione delle pagine
    """

    def __init__(self, data_fattura: str = "", *args, **kwargs):
        """
        Inizializza il documento PDF della fattura.

        Args:
            data_fattura (str): Data della fattura da visualizzare nell'intestazione.
        """
        super().__init__(*args, **kwargs)
        self.data_fattura = data_fattura

        font_dir = resource_path("fonts")

        font_normal = os.path.join(font_dir, "DejaVuSerif.ttf")
        font_bold = os.path.join(font_dir, "DejaVuSerif-Bold.ttf")

        if os.path.exists(font_normal):
            self.add_font("DejaVu", "", font_normal, uni=True)
            if os.path.exists(font_bold):
                self.add_font("DejaVu", "B", font_bold, uni=True)
            self.default_font = "DejaVu"
        else:
            # Fallback nel caso i font non siano disponibili
            self.default_font = "Arial"

    def header(self):
        """
        Disegna l'intestazione del PDF.

        Include:
        - logo aziendale (se presente)
        - data della fattura
        """
        self.set_font(self.default_font, size=12)

        logo_path = resource_path("img/logo.png")

        if os.path.exists(logo_path):
            self.image(logo_path, x=10, y=30, w=400)
        else:
            self.set_font("Arial", "", 10)
            self.text(10, 15, "[Logo mancante]")

        self.set_font(self.default_font, size=12)
        self.set_xy(0, 10)
        self.cell(0, 8, f"Data: {self.data_fattura}", align="R")

        self.ln(50)

    def footer(self):
        """
        Disegna il piè di pagina del PDF con la numerazione delle pagine.
        """
        self.set_y(-15)
        self.set_font("Arial", "", 9)
        self.set_text_color(120)
        self.cell(0, 10, f"Pagina {self.page_no()}", align="C")


def genera_pdf_fattura(header: dict, detail: list, output_path: str) -> None:
    """
    Genera il PDF della fattura a partire dai dati forniti.

    La funzione:
    - crea il documento PDF
    - renderizza la tabella dei dettagli
    - calcola i totali (affitto, ritenuta, bonifico)
    - salva il file PDF nel percorso indicato

    Args:
        header (dict): Dizionario contenente i dati di intestazione della fattura
                       (es. data).
        detail (list): Lista di liste contenente i dati tabellari della fattura,
                       inclusa l'intestazione come prima riga.
        output_path (str): Percorso di output del file PDF.
    """

    def safe_str(val) -> str:
        """
        Converte un valore in stringa gestendo None e NaN.

        Args:
            val: Valore da convertire.

        Returns:
            str: Valore convertito in stringa sicura.
        """
        if val is None:
            return ""
        try:
            if isinstance(val, float) and math.isnan(val):
                return ""
        except Exception:
            pass
        return str(val)

    pdf = FatturaPDF(data_fattura=header["data"])
    pdf.add_page()
    pdf.set_font(pdf.default_font, size=10)

    # Preparazione dati tabella
    table_data = tuple(tuple(safe_str(cell) for cell in row) for row in detail)

    with pdf.table() as table:
        for data_row in table_data:
            row = table.row()
            for datum in data_row:
                row.cell(datum, border="TOP", align="C")

    # Esclusione header per i calcoli
    righe_dati = detail[1:]

    tot_affitto = sum(row[8] for row in righe_dati)
    tot_ritenuta = sum(row[9] for row in righe_dati)
    tot_bonifico = round(tot_affitto - tot_ritenuta, 2)

    # Sezione totali
    pdf.ln(10)
    pdf.set_font(pdf.default_font, "B", 10)

    label_w = 50
    value_w = 40

    pdf.cell(label_w, 8, "Totale Affitto", border=1)
    pdf.set_font(pdf.default_font, "", 10)
    pdf.cell(value_w, 8, f"{tot_affitto:.2f} €", border=1, ln=True, align="R")

    pdf.set_font(pdf.default_font, "B", 10)
    pdf.cell(label_w, 8, "Totale Ritenuta", border=1)
    pdf.set_font(pdf.default_font, "", 10)
    pdf.cell(value_w, 8, f"{tot_ritenuta:.2f} €", border=1, ln=True, align="R")

    pdf.set_font(pdf.default_font, "B", 11)
    pdf.cell(label_w, 9, "Totale Bonifico", border=1)
    pdf.cell(value_w, 9, f"{tot_bonifico:.2f} €", border=1, ln=True, align="R")

    pdf.output(output_path)
