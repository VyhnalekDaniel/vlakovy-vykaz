# Vlakový výkaz

Flask webová aplikace pro vlakovou dokumentaci, výkaz vozidel a ZOB.

## Spuštění lokálně

```bash
pip install -r requirements.txt
python app.py
```

Otevři:

```text
http://127.0.0.1:5000
```

## Render

Build Command:

```text
pip install -r requirements.txt
```

Start Command:

```text
gunicorn app:app
```

## Ukládání a načítání dokumentace

- **Uložit dokumentaci** stáhne soubor `.json`.
- **Načíst dokumentaci** umožní tento `.json` soubor znovu nahrát do aplikace.
- Data se tím neukládají na server, ale k uživateli do souboru.

## Důležité soubory

- `app.py` = Flask aplikace
- `vypocet.py` = výpočetní databáze vozidel a pomocné funkce
- `templates/` = HTML šablony
- `static/style.css` = vzhled
- `requirements.txt` = Python knihovny
- `Procfile` = příkaz pro nasazení
