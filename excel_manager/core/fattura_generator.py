import math
import os
from fpdf import FPDF

class FatturaPDF(FPDF):
    def header(self):
        # --- LOGO ---
        logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "img", "logo.png")

        if os.path.exists(logo_path):
            self.image(logo_path, x=10, y=30, w=400)
        else:
            self.set_font("Arial", "", 12)
            self.text(10, 15, "[Logo mancante]")

        # Spazio sotto il logo
        self.ln(40)

    def footer(self):
        # Numero pagina
        self.set_y(-15)
        self.set_font("Arial", "", 9)
        self.set_text_color(120)
        self.cell(0, 10, f"Pagina {self.page_no()}", align="C")


def genera_pdf_fattura(header: dict, detail: list, output_path: str):

    # normalizzo i valori: None / NaN -> "", gli altri diventano str()
    def safe_str(val):
        if val is None:
            return ""
        # handle numpy.nan / float('nan')
        try:
            if isinstance(val, float) and math.isnan(val):
                return ""
        except Exception:
            pass
        return str(val)

    pdf = FatturaPDF()
    pdf.add_page()

    font_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "fonts")
    font_normal = os.path.join(font_dir, "DejaVuSerif.ttf")
    font_bold = os.path.join(font_dir, "DejaVuSerif-Bold.ttf")

    if os.path.exists(font_normal):
        pdf.add_font("DejaVu", "", font_normal, uni=True)
        if os.path.exists(font_bold):
            pdf.add_font("DejaVu", "B", font_bold, uni=True)
        pdf.set_font("DejaVu", "", 14)
    else:
        pdf.set_font("Arial", "", 14)

    # 👉 DATA A DESTRA
    pdf.set_font("DejaVu", size=12)
    pdf.cell(0, 6, f"Data: {header['data']}", ln=True, align="R")
    pdf.ln(25)

    # 👉 TABELLA DETTAGLI
    pdf.set_font("DejaVu", size=10)

    # costruisco TABLE_DATA come tuple di tuple di stringhe
    TABLE_DATA = tuple(tuple(safe_str(cell) for cell in row) for row in detail)

    with pdf.table() as table:
        for data_row in TABLE_DATA:
            row = table.row()
            for datum in data_row:
                row.cell(datum, border="TOP", align="C")
    # --- SALVA PDF ---
    pdf.output(output_path)
