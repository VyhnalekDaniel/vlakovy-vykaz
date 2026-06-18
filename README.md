# Vlakový výkaz - Flask verze

## Spuštění

1. Otevři příkazový řádek v této složce.
2. Nainstaluj Flask:

```bash
pip install -r requirements.txt
```

3. Spusť aplikaci:

```bash
python app.py
```

4. Otevři v prohlížeči:

```text
http://127.0.0.1:5000
```

## Zadávání vozidel

Každý řádek má tvar:

```text
číslo;typ;režim;stav
```

Příklady:

```text
95545811111-4;HDV;P;činné
51542191000-0;VOZ;R
```

U vozů se stav ignoruje. U HDV použij stav `činné` nebo `dopravované`.
