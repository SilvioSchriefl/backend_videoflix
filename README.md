# Videoflix – Backend

REST-API für **Videoflix**, eine Video-Streaming-Plattform nach dem Vorbild von Netflix.
Gebaut mit **Django** und dem **Django REST Framework** als Abschlussprojekt meiner Ausbildung
zum Entwickler bei der Developer Akademie (2023/2024).

Das passende Angular-Frontend liegt hier: [SilvioSchriefl/Videoflix](https://github.com/SilvioSchriefl/Videoflix)

## Funktionen

**Benutzerkonten**
- Registrierung mit E-Mail und Passwort, Bestätigung per Link in einer E-Mail
- Login und Logout mit Token-Authentifizierung
- „Passwort vergessen“: Reset-Link per E-Mail, Link nur einmal gültig
- Benutzerdaten ändern und Konto löschen
- Eigenes User-Modell mit E-Mail als Login-Name

**Videos**
- Videos hochladen, abrufen und löschen (nur für angemeldete Nutzer)
- Vorschaubild (Thumbnail) wird beim Upload automatisch mit FFmpeg erzeugt
- Beim Löschen eines Videos werden auch alle zugehörigen Dateien entfernt
- Persönliche Watchlist pro Nutzer
- Vorbereitet: Umwandlung in 480p im Hintergrund über eine Redis-Warteschlange (django-rq) – im Code derzeit deaktiviert

## Technik

| Bereich | Eingesetzt |
| --- | --- |
| Framework | Django 4.2, Django REST Framework |
| Datenbank | PostgreSQL |
| Authentifizierung | DRF Token Authentication |
| Hintergrundaufgaben | Redis, django-rq |
| Videoverarbeitung | FFmpeg |
| E-Mail | SMTP |
| Konfiguration | django-environ (`.env`-Datei) |

## API-Endpunkte

| Methode | Pfad | Zweck |
| --- | --- | --- |
| POST | `/register/` | Konto anlegen, Bestätigungs-Mail senden |
| GET | `/confirm-registration/<uid>/<token>/` | E-Mail-Adresse bestätigen |
| POST | `/log_in/` | Anmelden, Token erhalten |
| POST | `/logout/` | Abmelden |
| POST | `/request_reset_password/` | Reset-Link anfordern |
| GET | `/reset_pw/<uid>/<token>/` | Reset-Link prüfen |
| POST | `/set_password/` | Neues Passwort setzen |
| PATCH | `/edit_user/` | Benutzerdaten ändern |
| DELETE | `/delete_account/` | Konto löschen |
| GET / POST / PATCH | `/video/` | Eigene Videos abrufen / hochladen / bearbeiten |
| DELETE | `/video/<id>/` | Video löschen |
| GET / PATCH | `/watchlist/<user_id>/` | Watchlist abrufen / ändern |

## Lokal starten

Voraussetzungen: Python 3.11+, PostgreSQL, FFmpeg, optional Redis (für Hintergrundaufgaben).

```bash
git clone https://github.com/SilvioSchriefl/backend_videoflix.git
cd backend_videoflix
python -m venv env
source env/bin/activate        # Windows: env\Scripts\activate
pip install -r requirements.txt
pip install "psycopg[binary]"   # PostgreSQL-Treiber

cp .env.example .env           # Werte in .env eintragen
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Die API läuft dann unter `http://127.0.0.1:8000/`.

Hinweis: `requirements.txt` enthält `rq-win` für den Betrieb unter Windows. Auf Linux oder macOS
kann diese Zeile entfernt werden.

## Tests

```bash
pip install faker
python manage.py test
```
