import pandas as pd

def estrai_dati_fattura(file_path: str) -> dict:
    """
    Legge il file Excel e restituisce un dict con i dati necessari alla fattura.
    """
    print("DEBUG file_path: ", file_path)
    df = pd.read_excel(file_path)
    
    # Estrai i dati della prima (o unica) prenotazione
  
    dati = {
        "check_in": df.loc[0, "Check in"],
        "check_out": df.loc[0, "Check-out"],
        "notti": df.loc[0, "Notti"],
        "importo_ricevuto": df.loc[0, "Addebiti"],
    }

    return dati


'''
        "Servizio": df.loc[0, "Totale"]
        "Extra": df.loc[0, "Importo extra"],
        "Pulizie": df.loc[0, "Costi pulizia"],
        "Tassa": df.loc[0, "Tassa di soggiorno"],
        "Affitto": df.loc[0, "Affitto"],
        "Ritenuta": df.loc[0, "Ritenuta affitto"]

[2 rows x 21 columns]
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 2 entries, 0 to 1
Data columns (total 21 columns):
 #   Column             Non-Null Count  Dtype
---  ------             --------------  -----
 0   ID                 2 non-null      int64
 1   Numero             2 non-null      object
 2   Check in           2 non-null      object
 3   Check-out          2 non-null      object
 4   Notti              2 non-null      int64
 5   Ospiti             2 non-null      int64
 6   Canale             2 non-null      object
 7   Addebiti           2 non-null      float64
 8   Altri addebiti     2 non-null      float64
 9   Importo extra      2 non-null      int64
 10  Descrizione extra  1 non-null      object
 11  Pulizie            2 non-null      int64
 12  Senza Iva          2 non-null      float64
 13  TT con CC          2 non-null      int64
 14  Comm. Lorda        2 non-null      float64
 15  Tot tassa sogg     2 non-null      int64
 16  Comm_netta         2 non-null      float64
 17  IVA comm           2 non-null      float64
 18  Iva Pulizie        2 non-null      float64
 19  Servizio           2 non-null      float64
 20  Netto Affitto      2 non-null      float64
dtypes: float64(9), int64(7), object(5)
memory usage: 468.0+ bytes
Dataframe:  None
'''