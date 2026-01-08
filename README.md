# eseguibile
pyinstaller --onefile --console --name excel_manager main.py --add-data "fonts;fonts" --add-data "img;img"


# excel_manager

Ti faccio di nuovo un riepilogo di quello che vorrei io.

Chi è il mio cliente
Il mio cliente gestisce una serie di appartamenti che affitta a breve termine, su piattaforme varie (airbnb, booking.com, canali terzi, ecc..) per conto di terzi.
Per quanto riguarda la parte di scheduling e della gestione dei check-in e check-out si affida a un CRM.

L'Obiettivo adesso è costruire un applicazione stand-alone in python per la gestione contabile

Aspetto funzionale/Che tipo di app gli serve?
Nel file system locale, ho una folder (che per il momento chiameremo prenotazioni') che al suo interno ha una serie di sotto-folder ognuna chiamata col nome dell'appartamento di riferimento(per il momento chiameremo appartment1, appartmen2, ... appartmentn). 
Ogni folder ha al suo interno.

1. un'altra sotto_folder, chiamata 'estratti_crm': al cui interno di sono i file .xlsx, provenienti dal crm che permette di gestire le prenotazioni. Ogni file ha un riferimento temporale differente.
2. un file chiamato resoconto_mensile.ods: che prende i dettagli del file di gestione prenotazioni (che come detto prima stanno nella folder estratti_crm), li elabora per la contabilizzazione 

L'utente deve interagire con una GUI1 (getFolder_apartment) che permette la visualizzazione e selezione dal filesystem locale, l'utente sceglierà la folder dello specifico appartamento fino a estratti_crm.

Il sistema visualizzerà tutti i file xlsx dalla folder selezionata apartment1/estratti_crm:

prima di proseguire vede se i dati che si vogliono inserire sono già presenti nel file resoconto_mensile.ods altrimenti lancia un warning (ASAP. da vedere come gestire).

Prima di salvare tutti i all'interno di resoconto_mensile, verrà mostrato all'utente una lista di extra e costi delle pulizie da integrare (sebbene per ognuno sia predisposto un valore di default).

Una volta presi tutti i dati in pancia segue una parte di elaborazione dei dati al fine contabile per portarli puliti all'interno del file resoconto_mensile.ods.

Quando tutti gli step sono stati eseguiti avverrà il salvataggio.


# 📦 Excel Manager - Gestione Contabile Appartamenti

## 🎯 Obiettivo
Applicazione Python standalone con interfaccia grafica per la gestione contabile di appartamenti in affitto breve. L'app consente di estrarre dati da file .xlsx esportati da un CRM e importarli in un file di resoconto mensile in formato `.ods`, dopo eventuale elaborazione.

## 🧭 Funzionalità previste (stato iniziale)
1. Selezione da GUI della folder `estratti_crm` di un appartamento.
2. Lettura automatica dell'unico file `.xlsx` presente nella cartella.
3. Estrazione di 3 colonne significative (`Check-in`, `Check-out`, `Addebiti`, `Canale`).
4. Scrittura dei dati nel file `resoconto_mensile.ods` (presente nella folder padre dell'appartamento), che inizialmente ha solo l'intestazione.

## 🚧 Struttura progetto (bozza)

```
excel_manager/
├── gui/
│   ├── folder_selector.py         # GUI1: seleziona folder 'estratti_crm'
│   └── extras_editor.py           # (in futuro) GUI2: modifica extra e pulizie
├── core/
│   ├── data_loader.py             # Caricamento file .xlsx
│   ├── data_writer.py             # Scrittura su file .ods
│   └── data_validator.py          # (in futuro) Validazione duplicati
├── utils/
│   ├── logger.py                  # Logging (in futuro)
│   └── file_utils.py              # Percorsi, backup, ecc.
├── main.py                        # Entry point del programma
└── README.md                      # Questo file
```

## 📁 Esempio struttura dati utente
```
prenotazioni/
├── appartamento1/
│   ├── estratti_crm/
│   │   └── prenotazioni_gennaio.xlsx
│   └── resoconto_mensile.ods
```

## 🚀 Avvio
```bash
python main.py
```

## 💬 Dipendenze
- tkinter
- pandas
- openpyxl
- ezodf

(Installabili con `pip install pandas openpyxl ezodf`)

## 🧪 Stato di sviluppo
- [x] GUI base per scelta folder
- [x] Lettura primo file .xlsx
- [x] Estrazione colonne essenziali
- [x] Scrittura su file .ods
- [ ] Validazione duplicati
- [ ] Backup file
- [ ] Gestione extra da GUI
- [ ] Multi-appartamento
- [ ] Logging e report

