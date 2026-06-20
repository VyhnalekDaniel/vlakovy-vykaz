from copy import deepcopy
from datetime import datetime
from os import environ
import json
import re

from flask import Flask, Response, flash, redirect, render_template, request, session, url_for

from vypocet import DATABAZE, HIERARCHIE_BLOKOVANI, ziskej_klic_vozidla

app = Flask(__name__)
app.secret_key = environ.get("SECRET_KEY", "dev-key-vlakovy-vykaz")

# ------------------------------------------------------------
# Nastavení aplikace
# ------------------------------------------------------------

REZIMY_BRZDENI = [
    "G", "P", "P+Mg", "P+E", "P+E 160", "R", "R+Mg", "R+E", "R+E 160"
]

VYKONAL_MOZNOSTI = [
    "Strojvedoucí", "Posunovač", "Vozmistr", "Obsluha vlaku", "Výpravčí", "Jiný ŽDP"
]

# Předvolené poznámky ke zprávě o brzdění.
# Na stránce ZOB se zobrazí jako checkboxy a lze jich vybrat více najednou.
POZNAMKY_ZOB_MOZNOSTI = [
    "V soupravě jsou pouze vozidla s označením CODS",
    "V soupravě jsou pouze vozidla s označením LAT",
    "V soupravě jsou pouze vozidla s označením TB S",
    "V soupravě jsou pouze vozidla s označením SSOD*",
    "V soupravě jsou vozidla s označením TB 0",
    "Jízda dovolena dle rychlostního profilu: PASS 1",
    "Jízda dovolena dle rychlostního profilu: PASS 2",
    "Jízda dovolena dle rychlostního profilu: PASS 3",
    "Jízda dovolena dle rychlostního profilu: TILT 6",
    "V soupravě jsou vozidla s ovládáním nástupních dveří viz Výkaz vozidel",
    "V soupravě je k službě pohotové HV",
    "Pochybnost o správném účinku průběžné brzdy",
    "Centrální napájení vlaku U = 1 kV",
    "Na AC 25 kV centrální napájení vlaku U = 1,5 kV",
    "Z ..... do ..... vlak se zavěšeným postrkem",
    "Z ..... do ..... vlak s vloženou lokomotivou",
    "Ve vlaku jsou zařazena nešuntující vozidla",
    "Počet ŽKV s brzdou stupňovitě neodbrzďovatelnou: <číslo>",
    "Přemostění záchranné brzdy činné",
    "Soupravu celoročně napájet (CZE, vozy s označením „ee“ nebo „z“)",
    "V soupravě vozidla s označením n, y",
    "V soupravě jsou pouze vozidla s označením „o. Zub“",
    "V soupravě jsou pouze vozidla s označením „a“",
]

# Databázi vlaků doděláme později. Struktura je připravená.
DATABAZE_VLAKU = {
     "92665": {
         "druh": "Sp",
         "cislo": "92665",
         "vychozi_stanice": "Pňovany",
         "konecna_stanice": "Plzeň hl.n.",
         "odjezd": "12:31",
     },
    
    "365": {
         "druh": "Ex",
         "cislo": "365",
         "vychozi_stanice": "Zámrsk",
         "konecna_stanice": "Letohrad",
         "odjezd": "12:31",
     },
}

# Tahák úplných čísel vozidel. Pouze pomůcka, výpočet v něm nehledá.
TAHAK_CISEL_VOZIDEL = {
    # "Řada 845": ["9454 16 51 203-2", "9454 16 50 203-3"],
}

# ------------------------------------------------------------
# Dokumentace uložená v relaci prohlížeče
# ------------------------------------------------------------

def nova_dokumentace():
    return {
        "vlak": {
            "druh": "",
            "cislo": "",
            "datum": "",
            "odjezd": "",
            "vychozi_stanice": "",
            "konecna_stanice": "",
            "sepsano_v": "",
            "sepsal": "",
            "poznamky": "",
            "zdroj": "",
        },
        "vozidla": [],
        "zob": {
            "potrebna_procenta": "0",
            "rezim_brzdy_vlaku": "",
            "doprovod": "",
            "poznamky": "",
            "poznamky_vybrane": [],
        },
        "jzb": {"vykonana": "NE", "kde": "", "kdy": "", "kym": "", "kym_jiny": ""},
        "uzb": {"vykonana": "NE", "kde": "", "kdy": "", "kym": "", "kym_jiny": ""},
    }


def get_doc():
    if "doc" not in session:
        session["doc"] = nova_dokumentace()
    return session["doc"]


def save_doc(doc):
    session["doc"] = doc
    session.modified = True


def reset_doc():
    session["doc"] = nova_dokumentace()
    session.pop("pending_vlak", None)
    session.modified = True


def sloucit_s_vychozi_dokumentaci(nahrana):
    """Doplní chybějící klíče, aby šly načíst i starší uložené soubory."""
    vychozi = nova_dokumentace()

    if not isinstance(nahrana, dict):
        return vychozi

    for cast in ["vlak", "zob", "jzb", "uzb"]:
        if isinstance(nahrana.get(cast), dict):
            vychozi[cast].update(nahrana[cast])

    if isinstance(nahrana.get("vozidla"), list):
        vychozi["vozidla"] = nahrana["vozidla"]

    return vychozi


def bezpecny_nazev_souboru(text):
    text = text or "dokumentace"
    text = re.sub(r"[^0-9A-Za-zÁ-Žá-ž_-]+", "_", text)
    text = text.strip("_")
    return text or "dokumentace"


def navrhni_nazev_exportu(doc):
    vlak = doc.get("vlak", {})
    casti = [
        vlak.get("druh", ""),
        vlak.get("cislo", ""),
        vlak.get("datum", ""),
    ]
    zaklad = "_".join(bezpecny_nazev_souboru(c) for c in casti if c)
    if not zaklad:
        zaklad = "vlakova_dokumentace"
    return f"{zaklad}.json"

# ------------------------------------------------------------
# Pomocné funkce
# ------------------------------------------------------------

def normalizuj_rezim(rezim):
    rezim = (rezim or "").strip()
    mapa = {"R+MG": "R+Mg", "P+MG": "P+Mg"}
    return mapa.get(rezim.upper(), rezim)


def dostupne_rezimy_vozidla(vozidlo):
    vysledek = []
    for rezim in REZIMY_BRZDENI:
        hodnota = vozidlo.get(rezim, 0)
        if hodnota and hodnota > 0:
            vysledek.append(f"{rezim} ({hodnota})")
    return vysledek


def najdi_vozidlo_v_databazi(cislo, typ):
    typ = (typ or "").upper().strip()
    if typ not in ["HDV", "VOZ"]:
        return None, "Typ musí být HDV nebo VOZ."

    klic = ziskej_klic_vozidla(cislo, typ)
    if not klic:
        return None, "Z čísla vozidla se nepodařilo získat klíč."

    cast = DATABAZE["HDV"] if typ == "HDV" else DATABAZE["VOZY"]
    if klic not in cast:
        return None, f"V databázi není vozidlo s klíčem {klic}."

    vozidlo = deepcopy(cast[klic])
    vozidlo["zadane_cislo"] = cislo
    vozidlo["klic"] = klic
    return vozidlo, ""


def nejvyssi_system_vozidla(vozidlo):
    systemy = vozidlo.get("system_blokovani", [])
    if isinstance(systemy, str):
        systemy = [systemy]
    platne = [s for s in systemy if s in HIERARCHIE_BLOKOVANI]
    if not platne:
        return "nezjištěno"
    return max(platne, key=lambda s: HIERARCHIE_BLOKOVANI.index(s))


def vyhodnot_system_blokovani(vozidla):
    systemy = []
    for vozidlo in vozidla:
        system = nejvyssi_system_vozidla(vozidlo)
        if system in HIERARCHIE_BLOKOVANI:
            systemy.append(system)
    if not systemy:
        return "nezjištěno"
    return min(systemy, key=lambda s: HIERARCHIE_BLOKOVANI.index(s))


def vyhodnot_nbu(vozidla):
    if not vozidla:
        return "NBU neaktivní"
    return "NBU aktivní" if all(v.get("NBU", 0) == 1 for v in vozidla) else "NBU neaktivní"


def spocitej_skupinu(vozidla):
    return {
        "pocet": len(vozidla),
        "hmotnost": sum(v.get("hmotnost", 0) for v in vozidla),
        "delka": sum(v.get("delka", 0) for v in vozidla),
        "pocet_naprav": sum(v.get("pocet_naprav", 0) for v in vozidla),
        "brzdici_vaha": sum(v.get("brzdici_vaha", 0) for v in vozidla),
        "kotoucove_brzdy": sum(1 for v in vozidla if v.get("kotoucove_brzdy", 0) == 1),
        "nekovove_spaliky": sum(1 for v in vozidla if v.get("nekovove_spaliky", 0) == 1),
        "G": sum(1 for v in vozidla if v.get("rezim_brzdeni") == "G"),
        "P": sum(1 for v in vozidla if v.get("rezim_brzdeni") == "P"),
        "R": sum(1 for v in vozidla if v.get("rezim_brzdeni") == "R"),
        "R+Mg": sum(1 for v in vozidla if v.get("rezim_brzdeni") == "R+Mg"),
    }


def vytvor_vypocet(doc):
    vozidla = doc.get("vozidla", [])
    cinna_hdv = [v for v in vozidla if v.get("typ") == "HDV" and v.get("stav") == "činné"]
    dopravovana_hdv = [v for v in vozidla if v.get("typ") == "HDV" and v.get("stav") == "dopravované"]
    vozy = [v for v in vozidla if v.get("typ") == "VOZ"]
    souprava = dopravovana_hdv + vozy
    vlak = cinna_hdv + dopravovana_hdv + vozy

    max_rychlost = min((v.get("max_rychlost", 0) for v in vlak), default=0)
    celkova_hmotnost = sum(v.get("hmotnost", 0) for v in vlak)
    brzdici_vaha = sum(v.get("brzdici_vaha", 0) for v in vlak)
    skutecna_procenta = (brzdici_vaha / celkova_hmotnost * 100) if celkova_hmotnost else 0

    try:
        potrebna_procenta = float(str(doc.get("zob", {}).get("potrebna_procenta", 0)).replace(",", "."))
    except ValueError:
        potrebna_procenta = 0

    chybejici_procenta = max(0, potrebna_procenta - skutecna_procenta)
    rychlost_podle_brzd = max(0, max_rychlost - chybejici_procenta)

    return {
        "cinna_hdv": spocitej_skupinu(cinna_hdv),
        "dopravovana_hdv": spocitej_skupinu(dopravovana_hdv),
        "vozy": spocitej_skupinu(vozy),
        "souprava": spocitej_skupinu(souprava),
        "vlak": spocitej_skupinu(vlak),
        "max_rychlost": max_rychlost,
        "skutecna_procenta": skutecna_procenta,
        "potrebna_procenta": potrebna_procenta,
        "chybejici_procenta": chybejici_procenta,
        "rychlost_podle_brzd": int(rychlost_podle_brzd),
        "nbu": vyhodnot_nbu(vlak),
        "system_blokovani": vyhodnot_system_blokovani(vlak),
    }


def uloz_zob_z_formulare(doc):
    doc["zob"] = {
        "potrebna_procenta": request.form.get("potrebna_procenta", doc["zob"].get("potrebna_procenta", "0")),
        "rezim_brzdy_vlaku": request.form.get("rezim_brzdy_vlaku", doc["zob"].get("rezim_brzdy_vlaku", "")),
        "doprovod": request.form.get("doprovod", doc["zob"].get("doprovod", "")),
        "poznamky": request.form.get("poznamky", doc["zob"].get("poznamky", "")),
        "poznamky_vybrane": request.form.getlist("poznamky_zob"),
    }

# ------------------------------------------------------------
# Stránky
# ------------------------------------------------------------

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/ulozit-dokumentaci")
def ulozit_dokumentaci():
    doc = get_doc()
    export = {
        "format": "vlakovy-vykaz-json",
        "verze": 1,
        "ulozeno": datetime.now().isoformat(timespec="seconds"),
        "dokumentace": doc,
    }
    data = json.dumps(export, ensure_ascii=False, indent=2)
    filename = navrhni_nazev_exportu(doc)
    return Response(
        data,
        mimetype="application/json; charset=utf-8",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


@app.route("/nacist-dokumentaci", methods=["GET", "POST"])
def nacist_dokumentaci():
    if request.method == "POST":
        soubor = request.files.get("soubor")

        if not soubor or soubor.filename == "":
            flash("Vyberte soubor s uloženou dokumentací.")
            return redirect(url_for("nacist_dokumentaci"))

        try:
            obsah = soubor.read().decode("utf-8")
            data = json.loads(obsah)
        except Exception:
            flash("Soubor se nepodařilo načíst. Zkontrolujte, že jde o uloženou dokumentaci ve formátu JSON.")
            return redirect(url_for("nacist_dokumentaci"))

        if isinstance(data, dict) and "dokumentace" in data:
            doc = data["dokumentace"]
        else:
            # Zpětná kompatibilita: kdyby byl uložen přímo obsah dokumentace bez obalu.
            doc = data

        doc = sloucit_s_vychozi_dokumentaci(doc)
        save_doc(doc)
        flash("Dokumentace byla načtena.")
        return redirect(url_for("vykaz_vozidel"))

    return render_template("nacist_dokumentaci.html")


@app.route("/nova-dokumentace")
def nova_dokumentace_route():
    reset_doc()
    flash("Byla založena nová vlaková dokumentace.")
    return redirect(url_for("vlakova_dokumentace"))


@app.route("/vlakova-dokumentace")
def vlakova_dokumentace():
    return render_template("vlakova_dokumentace.html")


@app.route("/vlak-z-jr", methods=["GET", "POST"])
def vlak_z_jr():
    doc = get_doc()
    if request.method == "POST":
        cislo = request.form.get("cislo", "").strip()
        vlak = DATABAZE_VLAKU.get(cislo)
        if not vlak:
            flash("Vlak nebyl nalezen v databázi. Zadejte ho ručně jako libovolný vlak.")
            return redirect(url_for("libovolny_vlak", cislo=cislo))
        novy_vlak = {
            "druh": vlak.get("druh", ""), "cislo": vlak.get("cislo", cislo),
            "datum": request.form.get("datum", ""), "odjezd": vlak.get("odjezd", ""),
            "vychozi_stanice": vlak.get("vychozi_stanice", ""),
            "konecna_stanice": vlak.get("konecna_stanice", ""),
            "sepsano_v": vlak.get("vychozi_stanice", ""), "sepsal": request.form.get("sepsal", ""),
            "poznamky": "", "zdroj": "JŘ",
        }
        if doc.get("vozidla") and doc.get("vlak", {}).get("cislo") != cislo:
            session["pending_vlak"] = novy_vlak
            return redirect(url_for("potvrdit_zmenu_vlaku"))
        doc["vlak"] = novy_vlak
        save_doc(doc)
        return redirect(url_for("vykaz_vozidel"))
    return render_template("vlak_z_jr.html")


@app.route("/libovolny-vlak", methods=["GET", "POST"])
def libovolny_vlak():
    doc = get_doc()
    if request.method == "POST":
        novy_vlak = {
            "druh": request.form.get("druh", "").strip(),
            "cislo": request.form.get("cislo", "").strip(),
            "datum": request.form.get("datum", "").strip(),
            "odjezd": request.form.get("odjezd", "").strip(),
            "vychozi_stanice": request.form.get("vychozi_stanice", "").strip(),
            "konecna_stanice": request.form.get("konecna_stanice", "").strip(),
            "sepsano_v": request.form.get("sepsano_v", "").strip(),
            "sepsal": request.form.get("sepsal", "").strip(),
            "poznamky": request.form.get("poznamky", "").strip(),
            "zdroj": "ručně",
        }
        if doc.get("vozidla") and doc.get("vlak", {}).get("cislo") != novy_vlak["cislo"]:
            session["pending_vlak"] = novy_vlak
            return redirect(url_for("potvrdit_zmenu_vlaku"))
        doc["vlak"] = novy_vlak
        save_doc(doc)
        return redirect(url_for("vykaz_vozidel"))
    return render_template("libovolny_vlak.html", cislo=request.args.get("cislo", ""))


@app.route("/potvrdit-zmenu-vlaku", methods=["GET", "POST"])
def potvrdit_zmenu_vlaku():
    doc = get_doc()
    pending = session.get("pending_vlak")
    if not pending:
        return redirect(url_for("vlakova_dokumentace"))
    if request.method == "POST":
        doc["vlak"] = pending
        if request.form.get("akce") == "vymazat":
            doc["vozidla"] = []
        save_doc(doc)
        session.pop("pending_vlak", None)
        return redirect(url_for("vykaz_vozidel"))
    return render_template("potvrdit_zmenu_vlaku.html", vlak=pending, pocet_vozidel=len(doc.get("vozidla", [])))


@app.route("/vykaz-vozidel")
def vykaz_vozidel():
    doc = get_doc()
    return render_template("vykaz_vozidel.html", doc=doc, vozidla=doc.get("vozidla", []), vypocet=vytvor_vypocet(doc))


@app.route("/pridat-vozidlo", methods=["GET", "POST"])
def pridat_vozidlo():
    doc = get_doc()
    if request.method == "POST":
        cislo = request.form.get("cislo", "").strip()
        typ = request.form.get("typ", "").strip().upper()
        rezim = normalizuj_rezim(request.form.get("rezim_brzdeni", ""))
        stav = request.form.get("stav", "").strip()

        vozidlo, chyba = najdi_vozidlo_v_databazi(cislo, typ)
        if chyba:
            flash(chyba)
            return redirect(url_for("pridat_vozidlo"))

        brzdici_vaha = vozidlo.get(rezim, 0)
        if brzdici_vaha <= 0:
            dostupne = dostupne_rezimy_vozidla(vozidlo)
            flash(f"Vybraný režim {rezim} má brzdicí hmotnost 0. Dostupné režimy: {', '.join(dostupne) if dostupne else 'žádné'}.")
            return redirect(url_for("pridat_vozidlo"))

        vozidlo["rezim_brzdeni"] = rezim
        vozidlo["brzdici_vaha"] = brzdici_vaha
        if typ == "HDV":
            if stav not in ["činné", "dopravované"]:
                flash("U HDV vyberte stav činné nebo dopravované.")
                return redirect(url_for("pridat_vozidlo"))
            vozidlo["stav"] = stav
        else:
            vozidlo["stav"] = "vůz"
        doc["vozidla"].append(vozidlo)
        save_doc(doc)
        flash(f"Přidáno vozidlo: {cislo}")
        return redirect(url_for("vykaz_vozidel"))
    return render_template("pridat_vozidlo.html", rezimy=REZIMY_BRZDENI)


@app.route("/odstranit-vozidlo/<int:index>", methods=["POST"])
def odstranit_vozidlo(index):
    doc = get_doc()
    if 0 <= index < len(doc.get("vozidla", [])):
        doc["vozidla"].pop(index)
        save_doc(doc)
    return redirect(url_for("vykaz_vozidel"))


@app.route("/posun-vozidlo/<int:index>/<smer>", methods=["POST"])
def posun_vozidlo(index, smer):
    doc = get_doc()
    vozidla = doc.get("vozidla", [])
    if smer == "nahoru" and index > 0:
        vozidla[index - 1], vozidla[index] = vozidla[index], vozidla[index - 1]
    elif smer == "dolu" and index < len(vozidla) - 1:
        vozidla[index + 1], vozidla[index] = vozidla[index], vozidla[index + 1]
    save_doc(doc)
    return redirect(url_for("vykaz_vozidel"))


@app.route("/presun-vozidlo", methods=["POST"])
def presun_vozidlo():
    doc = get_doc()
    vozidla = doc.get("vozidla", [])
    try:
        index = int(request.form.get("index", "-1"))
        nova_pozice = int(request.form.get("nova_pozice", "0")) - 1
    except ValueError:
        flash("Pozice musí být číslo.")
        return redirect(url_for("vykaz_vozidel"))
    if 0 <= index < len(vozidla) and 0 <= nova_pozice < len(vozidla):
        vozidlo = vozidla.pop(index)
        vozidla.insert(nova_pozice, vozidlo)
        save_doc(doc)
    return redirect(url_for("vykaz_vozidel"))


@app.route("/otoc-vlak", methods=["POST"])
def otoc_vlak():
    doc = get_doc()
    doc["vozidla"].reverse()
    save_doc(doc)
    flash("Vlak byl otočen.")
    return redirect(url_for("vykaz_vozidel"))


@app.route("/otoc-jednotku", methods=["POST"])
def otoc_jednotku():
    doc = get_doc()
    vozy = [v for v in doc["vozidla"] if v.get("typ") == "VOZ"]
    vozy.reverse()
    idx = 0
    for i, vozidlo in enumerate(doc["vozidla"]):
        if vozidlo.get("typ") == "VOZ":
            doc["vozidla"][i] = vozy[idx]
            idx += 1
    save_doc(doc)
    flash("Jednotka byla otočena.")
    return redirect(url_for("vykaz_vozidel"))


@app.route("/zob", methods=["GET", "POST"])
def zob():
    doc = get_doc()
    if request.method == "POST":
        uloz_zob_z_formulare(doc)
        save_doc(doc)
        akce = request.form.get("akce")
        if akce == "jzb":
            return redirect(url_for("jzb"))
        if akce == "uzb":
            return redirect(url_for("uzb"))
        return redirect(url_for("rekapitulace"))
    return render_template("zob.html", doc=doc, rezimy=REZIMY_BRZDENI, poznamky_moznosti=POZNAMKY_ZOB_MOZNOSTI)


@app.route("/jzb", methods=["GET", "POST"])
def jzb():
    return zkouska_brzdy("jzb", "JZB")


@app.route("/uzb", methods=["GET", "POST"])
def uzb():
    return zkouska_brzdy("uzb", "ÚZB")


def zkouska_brzdy(klic, nazev):
    doc = get_doc()
    if request.method == "POST":
        doc[klic] = {
            "vykonana": request.form.get("vykonana", "NE"),
            "kde": request.form.get("kde", "").strip(),
            "kdy": request.form.get("kdy", "").strip(),
            "kym": request.form.get("kym", "").strip(),
            "kym_jiny": request.form.get("kym_jiny", "").strip(),
        }
        save_doc(doc)
        return redirect(url_for("zob"))
    return render_template("zkouska.html", typ=klic, nazev=nazev, data=doc.get(klic, {}), vykonal_moznosti=VYKONAL_MOZNOSTI)


@app.route("/rekapitulace")
def rekapitulace():
    doc = get_doc()
    return render_template("rekapitulace.html", doc=doc, vozidla=doc.get("vozidla", []), vypocet=vytvor_vypocet(doc))


@app.route("/tisk")
def tisk():
    doc = get_doc()
    return render_template("tisk.html", doc=doc, vozidla=doc.get("vozidla", []), vypocet=vytvor_vypocet(doc))


@app.route("/databaze")
def databaze():
    return render_template("databaze.html", databaze=DATABAZE, vlaky=DATABAZE_VLAKU, tahak=TAHAK_CISEL_VOZIDEL)


@app.route("/konec")
def konec():
    reset_doc()
    flash("Dokumentace byla ukončena.")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
