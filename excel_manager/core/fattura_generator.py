from fpdf import FPDF
import os

def genera_pdf_fattura(dati: dict, output_path: str):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # 👇 Aggiungo un font UTF-8
    font_path = os.path.join(os.path.dirname(__file__), "fonts", "DejaVuSans.ttf")
    pdf.add_font("DejaVu", "", font_path, uni=True)

    pdf.set_font("DejaVu", "", 18)
    pdf.cell(0, 10, "Fattura Prenotazione", ln=True, align="C")

    pdf.ln(10)

    pdf.set_font("DejaVu", "", 12)
    pdf.cell(0, 10, "Dati soggiorno:", ln=True)

    pdf.cell(0, 8, f"Check-in: {dati['check_in']}", ln=True)
    pdf.cell(0, 8, f"Check-out: {dati['check_out']}", ln=True)
    pdf.cell(0, 8, f"Notti: {dati['notti']}", ln=True)

    pdf.ln(5)

    pdf.set_font("DejaVu", "", 12)
    pdf.cell(0, 10, "Importi:", ln=True)

    # 👇 Il simbolo € ora funziona perché la font è unicode
    pdf.cell(0, 8, f"Importo ricevuto: € {dati['importo_ricevuto']}", ln=True)

    pdf.ln(10)

    pdf.set_font("DejaVu", "", 11)
    pdf.set_text_color(100)
    pdf.multi_cell(
        0, 7,
        "Sezione costi aggiuntivi (Servizio, Extra, Pulizie, Tassa, Affitto, Ritenuta) "
        "verrà aggiunta nelle prossime versioni."
    )
    pdf.set_text_color(0)

    pdf.output(output_path)
