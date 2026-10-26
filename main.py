import flet as ft
from alert import AlertManager
from deposito_strumenti import DepositoStrumenti
# Importo la libreria flet e le classi

FILE_STRUMENTI = "strumenti.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DAL DEPOSITO DI STRUMENTI DEL LAB03 ---
    deposito = DepositoStrumenti("Deposito Strumenti Musicali", "Alessandro Visconti")
    try:
        deposito.carica_file_strumenti(FILE_STRUMENTI)  # Carica il file
    except FileNotFoundError as e:
        alert.show_alert(f"❌ {e}")  # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile del deposito
    txt_titolo = ft.Text(value=deposito.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {deposito.get_responsabile()}",
        size=16,
        weight=ft.FontWeight.BOLD
    )   # Per ogni testo metto size e font che voglio

    # TextField per responsabile
    input_responsabile = ft.TextField(value=deposito.get_responsabile(), label="Responsabile")  # Label ci dà la scritta che appare, Value ci dà il valore che viene espresso dal bottone,
                                                                                                # deposito.get_responsabile() è il metodo definito nella classe deposito

    # ListView per mostrare la lista di strumenti aggiornata
    lista_strumenti = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    # Tutti i TextField per le info necessarie per aggiungere un nuovo strumento (tipo, marca, anno, contatore posti)
    txt_tipo = ft.TextField(label = "Tipo", width = 300)
    txt_marca = ft.TextField(label= "Marca", width = 300)
    txt_anno = ft.TextField(label= "Anno", width = 300)

    # TextField fa da "display" del contatore per il valore in euro, value="0": il contatore parte da zero,
    txt_valore = ft.TextField(value="0", label="Valore (€)", text_align=ft.TextAlign.CENTER, width=100)

    # --- FUNZIONI APP ---
    def aggiorna_lista_strumenti():
        lista_strumenti.controls.clear()
        for strumento in deposito.strumenti_ordinati_per_marca():
            stato = "✅" if strumento.disponibile else "⛔"
            lista_strumenti.controls.append(ft.Text(f"{stato} {strumento}"))

    # Creo una funzione che legge il valore attuale del contatore come intero. Serve perché l'utente potrebbe anche
    # scrivere a mano nel campo: se scrive qualcosa che non è un numero, invece di far crashare il programma ripartiamo da 0.
    def leggi_valore_contatore():
        try:
            return int(txt_valore.value)
        except ValueError:
            return 0                       # Se la conversione fallisce, considero il valore 0

    # Funzione che svuota tutti i campi dopo un inserimento riuscito
    def svuota_campi():
        txt_tipo.value = ""
        txt_marca.value = ""
        txt_anno.value = ""
        txt_valore.value = "0"             # Il contatore torna a zero

    # --- HANDLERS APP ---
    # Il toggle è definito in seguito ma, essendo qua in un metodo, non ho problemi o eccezioni di non definizione
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"

    def conferma_responsabile(e):
        deposito.set_responsabile(input_responsabile.value)
        txt_responsabile.value = f"Responsabile: {deposito.get_responsabile()}"

    # Handlers per la gestione dei pulsanti utili all'inserimento di un nuovo strumento

    # Handler del pulsante "-" del contatore.
    # Tutti gli handler ricevono il parametro "e" (l'evento del click), anche se non lo usiamo
    def decrementa_valore(e):
        valore = leggi_valore_contatore()
        if valore > 0:                     # Non permetto di scendere sotto zero (un valore negativo non ha senso)
            valore = valore - 1
        txt_valore.value = str(valore)     # Rimetto il numero nel TextField come stringa

    # Handler del pulsante "+" del contatore
    def incrementa_valore(e):
        valore = leggi_valore_contatore()
        txt_valore.value = str(valore + 1)

    # Handler del pulsante "Aggiungi strumento".
    # legge i campi, li valida, aggiunge lo strumento, svuota i campi, aggiorna la ListView
    # Ad ogni errore mostra un alert e fa "return", così il resto della funzione non viene eseguito.
    def aggiungi_strumento(e):
        # or "" evita errori nel caso in cui value sia None
        tipo = (txt_tipo.value or "").strip()
        marca = (txt_marca.value or "").strip()
        anno_testo = (txt_anno.value or "").strip()
        valore_testo = (txt_valore.value or "").strip()

        # Controllo che i campi di testo non siano vuoti
        if tipo == "" or marca == "":
            alert.show_alert("❌ Inserisci sia il tipo che la marca dello strumento.")
            return

        # Controllo che l'anno sia un numero intero: int() lancia ValueError se non lo è
        try:
            anno = int(anno_testo)
        except ValueError:
            alert.show_alert("❌ L'anno di acquisto deve essere un numero intero.")
            return

        # Controllo che l'anno sia plausibile (positivo)
        if anno <= 0:
            alert.show_alert("❌ L'anno di acquisto deve essere un numero positivo.")
            return

        # Controllo che il valore del contatore sia numerico e maggiore di zero
        try:
            valore = float(valore_testo)
        except ValueError:
            alert.show_alert("❌ Il valore dello strumento deve essere un numero.")
            return

        if valore <= 0:
            alert.show_alert("❌ Il valore dello strumento deve essere maggiore di zero.")
            return

        # Uso il metodo della classe DepositoStrumenti che genera il nuovo codice ed aggiungere l'oggetto alla lista.
        deposito.aggiungi_strumento(tipo, marca, anno, valore)
        svuota_campi()
        aggiorna_lista_strumenti()

    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.Button("Conferma", on_click=conferma_responsabile)

    # Pulsanti per la gestione dell'inserimento di un nuovo strumento

    # IconButton mostra solo un'icona, on_click collega il pulsante al suo handler
    pulsante_meno = ft.IconButton(icon=ft.Icons.REMOVE, on_click=decrementa_valore)
    pulsante_piu = ft.IconButton(icon=ft.Icons.ADD, on_click=incrementa_valore)

    #   Il contatore vero e proprio: una riga con  "[-] [valore] [+]"
    contatore_valore = ft.Row(
        controls=[pulsante_meno, txt_valore, pulsante_piu],
        alignment=ft.MainAxisAlignment.CENTER
    )

    # Pulsante che conferma l'aggiunta dello strumento. Uso ft.Button (come per "Conferma")
    pulsante_aggiungi_strumento = ft.Button("Aggiungi strumento", on_click=aggiungi_strumento)

    # --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],   # Controlli da affiancare
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 3
        # Divisore e titolo della sezione
        ft.Divider(),
        ft.Text("Aggiungi Nuovo Strumento", size=20),
        ft.Row(
            controls=[txt_tipo, txt_marca, txt_anno, contatore_valore],
            alignment=ft.MainAxisAlignment.CENTER,
            wrap=True   # se la finestra è troppo stretta, i controlli vanno a capo invece di uscire dallo schermo.
        ),
        # Riga separata per il pulsante, centrato sotto ai campi
        ft.Row(
            controls=[pulsante_aggiungi_strumento],
            alignment=ft.MainAxisAlignment.CENTER
        ),

        # Sezione 4
        ft.Divider(),
        ft.Text("Strumenti", size=20),
        lista_strumenti,
    )
    aggiorna_lista_strumenti()

ft.run(main)    # Fondamentale per far funzionare flet la funzione ft.run()