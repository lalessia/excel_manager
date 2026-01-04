import pandas as pd

def estrai_dati_fattura(file_path: str) -> dict:
    """
    Legge il file Excel e restituisce un dict con i dati necessari alla fattura.
    """
    df = pd.read_excel(file_path)
    
    # Selezioni le colonne che servono dal file resoconto.xlsx
    cols_to_keep = [
        'Check in',
        'Check-out',
        'Notti',
        'Addebiti',
        'Importo extra',
        'Pulizie',
        'Tot tassa sogg',
        'Comm_netta'
    ]

    df_clean = df[cols_to_keep].copy()
    
    # 👉 Conversione colonne date in datetime
    df_clean['Check in'] = pd.to_datetime(df_clean['Check in'], dayfirst=True)
    df_clean['Check-out'] = pd.to_datetime(df_clean['Check-out'], dayfirst=True)
    # 👉 Formattazione DD/MM/YY
    df_clean['Check in'] = df_clean['Check in'].dt.strftime('%d/%m/%y')
    df_clean['Check-out'] = df_clean['Check-out'].dt.strftime('%d/%m/%y')
    
    # 🔥 Arrotondo subito a 2 decimali le colonne numeriche base
    df_clean["Addebiti"] = df_clean["Addebiti"].round(2)
    df_clean["Importo extra"] = df_clean["Importo extra"].round(2)
    df_clean["Pulizie"] = (df_clean["Pulizie"] * 1.22).round(2)
    df_clean["Tot tassa sogg"] = df_clean["Tot tassa sogg"].round(2)
    df_clean['Affitto'] = round(df_clean['Addebiti'] - df_clean['Pulizie'] - df_clean['Comm_netta']*1.22 - df_clean['Tot tassa sogg'], 2)
    df_clean['Ritenuta'] = round(df_clean['Affitto'] * 0.21, 2)

    # 🔥 Calcolo della colonna Servizio + arrotondamento
    df_clean["Servizio"] = (
        (df_clean["Addebiti"] * 0.20) +
        (df_clean["Importo extra"] * 100 / 122)
    ).apply(lambda x: round(x * 1.22, 2))

    # 👉 Nuovo ordine colonne
    new_order = [
        'Check in',
        'Check-out',
        'Notti',
        'Addebiti',
        'Servizio',
        'Importo extra',
        'Pulizie',
        'Tot tassa sogg',
        'Affitto',
        'Ritenuta'
    ]

    df_clean = df_clean[new_order]

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