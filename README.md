# IT ServiceDesk

Webbasierte IT-Ticketverwaltung im Rahmen der Praxisarbeit
"Datenbanken und Webentwicklung".

## Funktionen

- Benutzerregistrierung und Login
- Passwort-Hashing
- Support-Tickets erstellen
- Tickets bearbeiten und löschen
- Kategorien und Prioritäten
- Ticketstatus verwalten
- Filter nach Status und Priorität
- Dashboard mit Ticketübersicht
- REST-API mit Bearer-Token-Authentifizierung
- PostgreSQL-Datenbank

## Technologien

- Python 3.11
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Flask-WTF
- Flask-Migrate
- PostgreSQL 16
- Gunicorn
- Docker Compose
- HTML / CSS

## Anwendung starten

Docker-Container starten:

    docker compose up -d --build

Status prüfen:

    docker compose ps

## Webanwendung

Die Webanwendung wird mit Gunicorn betrieben.

Aktueller Zugriff:

    http://lab4.ifalabs.org:8000

## REST-API

Health-Check:

    GET /api/health

Token anfordern:

    POST /api/token

Tickets abrufen:

    GET /api/tickets

Einzelnes Ticket:

    GET /api/tickets/<id>

Kategorien abrufen:

    GET /api/categories

Geschützte API-Endpunkte benötigen einen Bearer Token.

## Datenbank

Die Anwendung verwendet PostgreSQL 16.
Das Datenbankschema wird mit Flask-Migrate und Alembic verwaltet.

## Autor

Liridon Latifi
