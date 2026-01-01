# core/data_cleaner.py

class DataCleaner:
    def __init__(self, df):
        self.df = df.copy()  # Per sicurezza, evitiamo modifiche in-place

    def clean(self):
        df = self.df

        # 11. "Pulizie" = "Altri addebiti" / 1.22
        df["Pulizie"] = df["Altri addebiti"] / 1.22
        df["Pulizie"] = df["Pulizie"].round(2)
        
        # 12. "Senza Iva" = "Importo extra" * 100 / 122
        df["Senza Iva"] = df["Importo extra"] * 100 / 122
        df["Senza Iva"] = df["Senza Iva"].round(2)
        
        # 13. "TT con CC" = 0 (per ora)
        df["TT con CC"] = 0

        # 14. "Comm. Lorda" = ("Addebiti" - "TT con CC") * 0.2
        df["Comm. Lorda"] = (df["Addebiti"] - df["TT con CC"]) * 0.2
        df["Comm. Lorda"] = df["Comm. Lorda"].round(2)
        
        # 15. "Tot tassa sogg" = 0 (per ora)
        df["Tot tassa sogg"] = 0

        # 16. "Comm_netta" = "Comm. Lorda" - "Tot tassa sogg" + "Senza Iva" + "TT con CC"
        df["Comm_netta"] = df["Comm. Lorda"] - df["Tot tassa sogg"] + df["Senza Iva"] + df["TT con CC"]
        df["Comm_netta"] = df["Comm_netta"].round(2) 
        
        # 17. "IVA comm" = "Comm_netta" * 0.22
        df["IVA comm"] = df["Comm_netta"] * 0.22
        df["IVA comm"] = df["IVA comm"].round(2)
        
        # 18. "Iva Pulizie" = "Pulizie" * 0.22
        df["Iva Pulizie"] = df["Pulizie"] * 0.22
        df["Iva Pulizie"] = df["Iva Pulizie"].round(2)
        
        # 19. "Servizio" = "Comm_netta" + "IVA comm"
        df["Servizio"] = df["Comm_netta"] + df["IVA comm"]
        df["Servizio"] = df["Servizio"].round(2)
               
        # 20. "Netto Affitto" = Addebiti - Pulizie - Iva Pulizie - Comm_netta - IVA comm - Tot tassa sogg
        df["Netto Affitto"] = df["Addebiti"] - df["Pulizie"] - df["Iva Pulizie"] - df["Comm_netta"] - df["IVA comm"] - df["Tot tassa sogg"]
        df["Netto Affitto"] = df["Netto Affitto"].round(2)

        return df
