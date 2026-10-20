import flet as ft   # Importo la libreria flet

class AlertManager:
    # Gestore centralizzato per la visualizzazione di finestre di dialogo (Alert) all'interno di un'applicazione Flet.

    def __init__(self, page: ft.Page):
        self._page = page  # Memorizziamo il riferimento alla pagina principale per poter mostrare/chiudere i dialoghi
        self._alert_dialog = ft.AlertDialog(
            title=ft.Text(""),
            actions=[
                ft.TextButton("OK", on_click=self.close)
            ]
        )
        # Creiamo fin da subito l'oggetto AlertDialog riutilizzabile.
        # All'inizio ha un titolo vuoto e un singolo pulsante "OK" che richiama il metodo self.close appena clicchi grazie a "on_click".

    def show_alert(self, message: str):
        # Mostra un avviso (popup) a schermo con il messaggio specificato.
        self._alert_dialog.title.value = message  # Aggiorna il testo del titolo dell'alert dialog con il messaggio ricevuto

        # In Flet, i dialoghi (AlertDialog) devono essere inseriti nell'overlay della pagina per poter essere visualizzati sopra gli altri elementi grafici.
        # Controlliamo se non è già stato aggiunto per evitare duplicati.
        if self._alert_dialog not in self._page.overlay:
            self._page.overlay.append(self._alert_dialog)   # ".overlay.append" è un metodo

        self._alert_dialog.open = True  # Imposta la proprietà 'open' su True per rendere visibile il popup
        self._page.update() # Aggiorna la pagina per applicare le modifiche grafiche in tempo reale

    def close(self, e):
        # Chiude la finestra di dialogo dell'avviso. Viene attivato automaticamente quando l'utente clicca sul pulsante 'OK'.

        self._alert_dialog.open = False # Imposta la proprietà 'open' su False per nascondere il popup
        self._page.update() # Aggiorna la pagina per mostrare la scomparsa dell'alert
