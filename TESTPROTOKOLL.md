# Testprotokoll IT ServiceDesk

| Nr. | Testfall | Erwartetes Ergebnis | Tatsächliches Ergebnis |
|---|---|---|---|
| T1 | Startseite aufrufen | HTTP 200, Startseite wird angezeigt | |
| T2 | Registrierung mit gültigen Daten | Benutzer wird erstellt und zur Login-Seite weitergeleitet | |
| T3 | Login mit gültigen Daten | Benutzer wird angemeldet und Dashboard angezeigt | |
| T4 | Ticket erstellen | Ticket wird gespeichert und im Dashboard angezeigt | |
| T5 | Ticketstatus ändern | Status wird gespeichert und Dashboard-Zähler aktualisiert | |
| T6 | Ticket nach Status filtern | Nur Tickets mit ausgewähltem Status werden angezeigt | |
| T7 | API Health-Check | HTTP 200 und {"status":"ok"} | |
| T8 | API ohne Bearer Token | HTTP 401 | |
| T9 | API Token mit gültigem Login | HTTP 200 und 64 Zeichen langer Bearer Token | |
| T10 | Tickets über API abrufen | HTTP 200 und eigene Tickets als JSON | |
