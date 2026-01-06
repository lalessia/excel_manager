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
    "Altri addebiti",
    "Da pagare",
]


def load_xlsx_from_folder(folder_path):
    """
    Carica il primo file Excel presente in una cartella.

    La funzione cerca un file .xlsx all'interno della cartella indicata,
    lo legge in un DataFrame Pandas e verifica la presenza delle colonne
    minime richieste.

    Args:
        folder_path (str | Path): Percorso della cartella contenente
                                  il file Excel esportato dal CRM.

    Returns:
        pandas.DataFrame: DataFrame contenente solo le colonne richieste.

    Raises:
        FileNotFoundError: Se non viene trovato alcun file .xlsx.
        ValueError: Se il file Excel non contiene tutte le colonne attese.
    """
    folder = Path(folder_path)
    print(f"[DEBUG] Cerco file .xlsx in: {folder.resolve()}")

    xlsx_files = list(folder.glob("*.xlsx"))
    if not xlsx_files:
        raise FileNotFoundError(
            "Nessun file .xlsx trovato nella cartella selezionata."
        )

    file_path = xlsx_files[0]
    print(f"[DEBUG] Caricamento file: {file_path.name}")

    df = pd.read_excel(file_path)

    # Verifica presenza colonne obbligatorie
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

    print("[DEBUG] DataFrame inizializzato per processing")
    print(df_cleaned.info())

    return df_cleaned