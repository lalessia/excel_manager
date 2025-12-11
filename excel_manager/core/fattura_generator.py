import os
from fpdf import FPDF

class FatturaPDF(FPDF):
    def header(self):
        # --- LOGO ---

        logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "img", "logo.png")

        print('logo_path: ', logo_path)

        if os.path.exists(logo_path):
            self.image(logo_path, x=10, y=30, w=400)
        else:
            self.set_font("Arial", "", 12)
            self.text(10, 15, "[Logo mancante]")

        # Spazio sotto il logo
        self.ln(20)

    def footer(self):
        # Numero pagina
        self.set_y(-15)
        self.set_font("Arial", "", 9)
        self.set_text_color(120)
        self.cell(0, 10, f"Pagina {self.page_no()}", align="C")


def genera_pdf_fattura(header: dict, detail: list, output_path: str):
    print("Creazione PDF minimal...")

    # Percorso font
    # font_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "fonts", "DejaVuSerif.ttf")

    font_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "fonts",
        "DejaVuSerif.ttf"
    )

    pdf = FatturaPDF()
    pdf.add_page()

    # Uso font unicode solo se esiste
    if os.path.exists(font_path):
        pdf.add_font("DejaVu", "", font_path, uni=True)
        pdf.set_font("DejaVu", "", 14)
        print('Il font settato è DejaVuSans.ttf')
    else:
        pdf.set_font("Arial", "", 14)
        print('Il font settato è Arial')

    # --- CONTENUTO MINIMALE ---
    pdf.cell(0, 10, f"Fattura n. {header.get('numero', '')}", ln=True)
    pdf.cell(0, 10, f"Data: {header.get('data', '')}", ln=True)

    # --- SALVA PDF ---
    pdf.output(output_path)

    print(f"PDF creato: {output_path}")
