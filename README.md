# Vlaková dokumentace – Flask průvodce

Toto je opravený balíček pro Render/GitHub.

## Důležité soubory

- `app.py` = Python aplikace Flask. Tento soubor NESMÍ obsahovat HTML šablonu.
- `vypocet.py` = výpočty a databáze vozidel.
- `templates/` = HTML šablony. Soubory s `{% extends ... %}` patří pouze sem.
- `static/` = CSS.
- `requirements.txt` = pouze knihovny:
  - flask
  - gunicorn
- `Procfile` = obsahuje `web: gunicorn app:app`.

## Render nastavení

Build Command:

```text
pip install -r requirements.txt
```

Start Command:

```text
gunicorn app:app
```

Do Start Command se nepíše `web:` a nepíše se `app.py : app`.

## Lokální spuštění

```bash
pip install -r requirements.txt
python app.py
```

Potom otevři:

```text
http://127.0.0.1:5000
```

## Nahrání na GitHub

Nahraj tyto položky:

- app.py
- vypocet.py
- requirements.txt
- Procfile
- README.md
- templates/
- static/
- .gitignore

Nenahrávej `__pycache__`.
