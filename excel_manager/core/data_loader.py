import pandas as pd
from pathlib import Path

# Colonne da estrarre
COLUMNS_TO_KEEP = [
    "ID",
    "Numero",
    "Check in",
    "Check-out",
    "Canale",
    "Addebiti",
    "Addebito soggiorno",
    "Addebito tassa di soggiorno",
    "Altri addebiti",
    "Da pagare"
]

def load_xlsx_from_folder(folder_path):
    folder = Path(folder_path)
    xlsx_files = list(folder.glob("*.xlsx"))

    if not xlsx_files:
        raise FileNotFoundError("Nessun file .xlsx trovato nella cartella selezionata.")

    file_path = xlsx_files[0]
    print(f"Caricamento file: {file_path.name}")

    df = pd.read_excel(file_path)

    # Verifica colonne presenti
    missing_cols = [col for col in COLUMNS_TO_KEEP if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Colonne mancanti nel file: {missing_cols}")

    df_filtered = df[COLUMNS_TO_KEEP].copy()
    return df_filtered
