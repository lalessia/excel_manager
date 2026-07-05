# core/io/excel_writer.py

import pandas as pd


def write_dataframe_to_file(df_combined, resoconto_path):
    """
    Scrive un DataFrame Pandas su file Excel (.xlsx).

    Questa funzione rappresenta lo strato di output dei dati elaborati:
    riceve un DataFrame già pulito e arricchito dalle regole di business
    e lo salva su disco in formato Excel.

    Args:
        df_combined (pandas.DataFrame): DataFrame finale contenente
                                        tutti i dati elaborati.
        resoconto_path (str | Path): Percorso completo del file Excel
                                     di destinazione.

    Returns:
        None

    Raises:
        IOError: Se il file non può essere scritto sul percorso indicato.
    """
    df_combined.to_excel(resoconto_path, index=False)
    print(f"[INFO] File Excel scritto correttamente in: {resoconto_path}")