# core/processing/data_cleaner.py

class DataCleaner:
    """
    Classe responsabile della pulizia e trasformazione dei dati contabili
    provenienti dal file Excel.

    Incapsula tutte le regole di business necessarie a:
    - normalizzare gli importi
    - calcolare commissioni, IVA, servizi
    - determinare affitto netto e ritenute

    La classe lavora su una copia del DataFrame per evitare modifiche in-place.
    """

    def __init__(self, df):
        """
        Inizializza il DataCleaner con un DataFrame di input.

        Args:
            df (pandas.DataFrame): DataFrame contenente i dati grezzi
                                   provenienti dal file Excel.
        """
        self.df = df.copy()

    def clean(self):
        """
        Applica tutte le trasformazioni e i calcoli ai dati.

        Il metodo:
        - adegua gli addebiti in base al canale di prenotazione
        - calcola extra, pulizie, IVA
        - determina commissioni lorde e nette
        - calcola affitto netto e ritenuta

        Returns:
            pandas.DataFrame: DataFrame pulito e arricchito con
                              tutte le colonne di calcolo.
        """
        df = self.df

        # Adeguamento addebiti sottraendo l'importo già pagato
        df["Addebiti"] = df["Addebiti"] - df["Da pagare"]

        # --- Adeguamento Addebiti in base al Canale ---
        commissioni = {
            "Airbnb": 0.0,
            "Booking": 0.195,
            "VRBO": 0.15
        }

        df["Commissioni"] = (
            df["Addebiti"] * df["Canale"].map(commissioni).fillna(0) * 1.22
        ).round(2)

        df["Addebiti"] = df["Addebiti"] -df["Commissioni"]

        '''
        df["Addebiti"] = (
            df["Addebiti"]
            * (1 - df["Canale"].map(commissioni).fillna(0) * 1.22)
        ).round(2)
        '''

        # Extra senza IVA (scorporo IVA 22%)
        df["extra_senza_iva"] = (df["Importo extra"] * 100 / 122).round(2)

        # Pulizie senza IVA
        df["pulizie"] = (df["Altri addebiti"] / 1.22).round(2)

        # IVA sulle pulizie
        df["iva_pulizie"] = (df["pulizie"] * 0.22).round(2)

        # Transazioni tramite carta di credito (attualmente non valorizzate)
        df["TT_con_CC"] = 0

        # Commissione lorda
        df["comm_lorda"] = ((df["Addebiti"] - df["TT_con_CC"]) * 0.2).round(2)

        # Tassa di soggiorno (placeholder per future estensioni)
        df["tot_tassa_sogg"] = 0

        # Commissione netta
        df["comm_netta"] = (
            df["comm_lorda"]
            - df["tot_tassa_sogg"]
            + df["extra_senza_iva"]
            + df["TT_con_CC"]
        ).round(2)

        # IVA sulla commissione
        df["IVA_comm"] = (df["comm_netta"] * 0.22).round(2)

        # Servizio totale
        df["servizio"] = (df["comm_netta"] + df["IVA_comm"]).round(2)

        # Affitto netto
        df["affitto"] = (
            df["Addebiti"]
            - df["pulizie"]
            - df["iva_pulizie"]
            - df["comm_netta"]
            - df["IVA_comm"]
            - df["tot_tassa_sogg"]
        ).round(2)

        # Ritenuta d'acconto
        df["ritenuta"] = (df["affitto"] * 0.21).round(2)

        return df
