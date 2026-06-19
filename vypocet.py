# Vlaková dokumentace – průvodce

Nová webová verze je udělaná jako postup:

1. Hlavní stránka
2. Vlaková dokumentace
3. Vlak z JŘ nebo libovolný vlak
4. Výkaz vozidel
5. Zpráva o brzdění
6. JZB / ÚZB detail
7. Rekapitulace
8. Tisk / uložení do PDF

Databáze pro trvalé ukládání dokumentací zatím není zapojená. Data se drží v aktuální relaci prohlížeče.

## Spuštění lokálně

```bash
pip install -r requirements.txt
python app.py
```

## Render

Build Command:

```bash
pip install -r requirements.txt
```

Start Command:

```bash
gunicorn app:app
```
