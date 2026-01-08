# core/io/excel_reader.py

"""
Modulo excel_reader

Responsabile della lettura dei file Excel (.xlsx) esportati dal CRM
e della prima selezione/normalizzazione delle colonne necessarie
al processo di elaborazione.

Questo modulo NON applica regole di business complesse:
si limita a validare la struttura del file e a preparare i dati
per il layer di processing.
"""

import pandas as pd
from pathlib import Path


# Colonne minime attese nel file Excel di origine
COLUMNS_TO_KEEP = [
    "ID",
    "Numero",
    "Check in",
    "Check-out",
    "Notti",
    "Ospiti",
    "Canale",
    "Addebiti",
    "Commissioni",
    "Altri addebiti",
    "Da pagare",
]


def load_xlsx(file_path):
    """
    Carica un file Excel specifico (.xlsx).

    Args:
        file_path (str | Path): Percorso del file Excel.

    Returns:
        pandas.DataFrame: DataFrame contenente solo le colonne richieste.
    """
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError("Il file selezionato non esiste.")

    if file_path.suffix != ".xlsx":
        raise ValueError("Il file selezionato non è un file .xlsx.")

    df = pd.read_excel(file_path)

    missing_cols = [col for col in COLUMNS_TO_KEEP if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Colonne mancanti nel file: {missing_cols}")

    return df[COLUMNS_TO_KEEP].copy()


def extract_clean_data(df_full):
    """
    Prepara un DataFrame di lavoro a partire dai dati letti.

    Questa funzione crea una copia del DataFrame originale e
    aggiunge le colonne necessarie alle fasi successive
    (es. inserimento manuale di extra).

    Args:
        df_full (pandas.DataFrame): DataFrame caricato dal file Excel.

    Returns:
        pandas.DataFrame: DataFrame pronto per il layer di processing.
    """
    df_cleaned = df_full[COLUMNS_TO_KEEP].copy()

    # Colonne inizializzate per input manuale successivo
    df_cleaned["Importo extra"] = 0.0
    df_cleaned["Descrizione extra"] = ""

    return df_cleaned