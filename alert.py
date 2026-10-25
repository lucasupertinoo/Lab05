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

        # Verifica se la finestra di dialogo è attualmente aperta (open == True)
        if self._alert_dialog.open:
            # SE È APERTA: aggiorna la pagina per riflettere eventuali modifiche apportate ai controlli interni del dialogo
            self._page.update()
        else:
            # SE NON È APERTA: mostra ufficialmente il dialogo sullo schermo
            self._page.show_dialog(self._alert_dialog)

    def close(self, e):
        # Metodo chiamato a seguito di un evento (es. il click su un pulsante "Chiudi" o "Annulla")
        # Chiude e rimuove dallo schermo la finestra di dialogo attiva più recente
        self._page.pop_dialog()