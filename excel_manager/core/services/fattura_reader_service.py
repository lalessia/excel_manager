import pandas as pd

def estrai_dati_fattura(file_path: str) -> dict:
    """
    Estrae e prepara i dati di fatturazione a partire da un file Excel.

    La funzione legge un file Excel contenente il resoconto di una prenotazione,
    seleziona le colonne rilevanti per la fattura, normalizza i formati delle date
    e restituisce i dati in una struttura tabellare pronta per la generazione PDF.

    Args:
        file_path (str): Percorso del file Excel (.xlsx) da cui estrarre i dati.

    Returns:
        list[list]: Tabella dei dati di fatturazione strutturata come lista di liste.
                    La prima riga contiene l'intestazione delle colonne.
    """
    df = pd.read_excel(file_path)
    
    # Selezioni le colonne che servono dal file resoconto.xlsx
    cols_to_keep = [
        'Check in',
        'Check-out',
        'Notti',
        'Addebiti',
        'servizio',
        'Importo extra',
        'Altri addebiti',
        'tot_tassa_sogg',
        'affitto',
        'ritenuta'
    ]

    df_clean = df[cols_to_keep].copy()
    
    # 👉 Conversione colonne date in datetime
    df_clean['Check in'] = pd.to_datetime(df_clean['Check in'], dayfirst=True)
    df_clean['Check-out'] = pd.to_datetime(df_clean['Check-out'], dayfirst=True)
    # 👉 Formattazione DD/MM/YY
    df_clean['Check in'] = df_clean['Check in'].dt.strftime('%d/%m/%y')
    df_clean['Check-out'] = df_clean['Check-out'].dt.strftime('%d/%m/%y')

    # 👉 Conversione in lista di liste
    detail = df_clean.values.tolist()

    # 👉 Header aggiornato
    header = [
        'CK in',
        'CK out',
        'Notti',
        'Addebiti',
        'Servizio',
        'Extra',
        'Pulizie',
        'Tax Sogg.',
        'Affitto',
        'Rit.'
    ]

    detail.insert(0, header)

    return detail