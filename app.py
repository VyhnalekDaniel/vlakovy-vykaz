from copy import deepcopy
from os import environ

from flask import Flask, flash, redirect, render_template, request, session, url_for

from vypocet import DATABAZE, HIERARCHIE_BLOKOVANI, ocisti_cislo, ziskej_klic_vozidla


app = Flask(__name__)
app.secret_key = environ.get("SECRET_KEY", "dev-key-vlakovy-vykaz")


# ============================================================
# NASTAVENÍ
# ============================================================

REZIMY_BRZDENI = [
    "G",
    "P",
    "P+Mg",
    "P+E",
    "P+E 160",
    "R",
    "R+Mg",
    "R+E",
    "R+E 160",
]

VYKONAL_MOZNOSTI = [
    "Strojvedoucí",
    "Posunovač",
    "Vozmistr",
    "Obsluha vlaku",
    "Výpravčí",
    "Jiný ŽDP",
]

# Sem si později dopíšeš vlastní poznámky ke zprávě o brzdění.
# Můžeš jich zaškrtnout víc najednou.
POZNAMKY_ZOB_MOZNOSTI = [
    # "Příklad poznámky ke zprávě o brzdění",
    # "Další poznámka",
]

# Databázi vlaků zatím necháváme jednoduchou.
# Později ji můžeme přesunout do vlastní databáze.
DATABAZE_VLAKU = {
    # "92665": {
    #     "druh": "Sp",
    #     "cislo": "92665",
    #     "vychozi_stanice": "Pňovany",
    #     "konecna_stanice": "Plzeň hl.n.",
    #     "odjezd": "12:31",
    # },
}

# Tahák úplných čísel vozidel.
# Systém v tom nehledá pro výpočet, je to jen pomůcka.
TAHAK_CISEL_VOZIDEL = {
    # "Řada 845": [
    #     "9454 16 51 203-2",
    #     "9454 16 50 203-3",
    # ],
}


# ============================================================
# PRÁCE S DOKUMENTACÍ V SESSION
# ============================================================

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
            "potrebna_procenta": 0,
            "rezim_brzdy_vlaku": "",
            "doprovod": "",
            "poznamky": "",
            "poznamky_vybrane": [],
        },
        "jzb": {
            "vykonana": "NE",
            "kde": "",
            "kdy": "",
            "kym": "",
            "kym_jiny": "",
        },
        "uzb": {
            "vykonana": "NE",
            "kde": "",
            "kdy": "",
            "kym": "",
            "kym_jiny": "",
        },
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


# ============================================================
# POMOCNÉ FUNKCE
# ============================================================

def normalizuj_rezim(rezim):
    rezim = (rezim or "").strip()

    if rezim.upper() == "R+MG":
        return "R+Mg"

    if rezim.upper() == "P+MG":
        return "P+Mg"

    return rezim


def dostupne_rezimy_vozidla(vozidlo):
    dostupne = []

    for rezim in REZIMY_BRZDENI:
        hodnota = vozidlo.get(rezim, 0)

        if hodnota and hodnota > 0:
            dostupne.append(f"{rezim} ({hodnota})")

    return dostupne


def najdi_vozidlo_v_databazi(cislo, typ):
    typ = typ.upper().strip()

    if typ not in ["HDV", "VOZ"]:
        return None, "Typ musí být HDV nebo VOZ."

    klic = ziskej_klic_vozidla(cislo, typ)

    if not klic:
        return None, "Z čísla vozidla se nepodařilo získat klíč."

    if typ == "HDV":
        cast = DATABAZE.get("HDV", {})
    else:
        cast = DATABAZE.get("VOZY", {})

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
    if not vozidla:
        return "nezjištěno"

    nejvyssi_systemy = []

    for vozidlo in vozidla:
        system = nejvyssi_system_vozidla(vozidlo)

        if system in HIERARCHIE_BLOKOVANI:
            nejvyssi_systemy.append(system)

    if not nejvyssi_systemy:
        return "nezjištěno"

    return min(nejvyssi_systemy, key=lambda s: HIERARCHIE_BLOKOVANI.index(s))


def vyhodnot_nbu(vozidla):
    if not vozidla:
        return "NBU neaktivní"

    for vozidlo in vozidla:
        if vozidlo.get("NBU", 0) != 1:
            return "NBU neaktivní"

    return "NBU aktivní"


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

    cinna_hdv = []
    dopravovana_hdv = []
    vozy = []

    for vozidlo in vozidla:
        if vozidlo.get("typ") == "HDV" and vozidlo.get("stav") == "činné":
            cinna_hdv.append(vozidlo)
        elif vozidlo.get("typ") == "HDV" and vozidlo.get("stav") == "dopravované":
            dopravovana_hdv.append(vozidlo)
        elif vozidlo.get("typ") == "VOZ":
            vozy.append(vozidlo)

    souprava = dopravovana_hdv + vozy
    vlak = cinna_hdv + dopravovana_hdv + vozy

    if vlak:
        max_rychlost = min(v.get("max_rychlost", 0) for v in vlak)
    else:
        max_rychlost = 0

    celkova_hmotnost = sum(v.get("hmotnost", 0) for v in vlak)
    brzdici_vaha = sum(v.get("brzdici_vaha", 0) for v in vlak)

    if celkova_hmotnost > 0:
        skutecna_procenta = (brzdici_vaha / celkova_hmotnost) * 100
    else:
        skutecna_procenta = 0

    potrebna_procenta = float(doc.get("zob", {}).get("potrebna_procenta", 0) or 0)
    chybejici_procenta = potrebna_procenta - skutecna_procenta

    if chybejici_procenta < 0:
        chybejici_procenta = 0

    rychlost_podle_brzd = max_rychlost - chybejici_procenta

    if rychlost_podle_brzd < 0:
        rychlost_podle_brzd = 0

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
    zob = doc["zob"]

    zob["potrebna_procenta"] = request.form.get("potrebna_procenta", zob.get("potrebna_procenta", 0))
    zob["rezim_brzdy_vlaku"] = request.form.get("rezim_brzdy_vlaku", zob.get("rezim_brzdy_vlaku", ""))
    zob["doprovod"] = request.form.get("doprovod", zob.get("doprovod", ""))
    zob["poznamky"] = request.form.get("poznamky", zob.get("poznamky", ""))

    vybrane = request.form.getlist("poznamky_zob")
    zob["poznamky_vybrane"] = vybrane

    doc["zob"] = zob


# ============================================================
# ROUTES
# ============================================================

@app.route("/")
def index():
    return render_template("index.html")


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
            flash("Vlak nebyl nalezen v databázi. Můžete ho zadat jako libovolný vlak.")
            return redirect(url_for("libovolny_vlak", cislo=cislo))

        novy_vlak = {
            "druh": vlak.get("druh", ""),
            "cislo": vlak.get("cislo", cislo),
            "datum": request.form.get("datum", ""),
            "odjezd": vlak.get("odjezd", ""),
            "vychozi_stanice": vlak.get("vychozi_stanice", ""),
            "konecna_stanice": vlak.get("konecna_stanice", ""),
            "sepsano_v": vlak.get("vychozi_stanice", ""),
            "sepsal": request.form.get("sepsal", ""),
            "poznamky": "",
            "zdroj": "JŘ",
        }

        if doc.get("vozidla") and doc["vlak"].get("cislo") != cislo:
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

        if doc.get("vozidla") and doc["vlak"].get("cislo") != novy_vlak["cislo"]:
            session["pending_vlak"] = novy_vlak
            return redirect(url_for("potvrdit_zmenu_vlaku"))

        doc["vlak"] = novy_vlak
        save_doc(doc)
        return redirect(url_for("vykaz_vozidel"))

    cislo = request.args.get("cislo", "")
    return render_template("libovolny_vlak.html", cislo=cislo)


@app.route("/potvrdit-zmenu-vlaku", methods=["GET", "POST"])
def potvrdit_zmenu_vlaku():
    doc = get_doc()
    pending = session.get("pending_vlak")

    if not pending:
        return redirect(url_for("vlakova_dokumentace"))

    if request.method == "POST":
        akce = request.form.get("akce")

        doc["vlak"] = pending

        if akce == "vymazat":
            doc["vozidla"] = []

        save_doc(doc)
        session.pop("pending_vlak", None)

        return redirect(url_for("vykaz_vozidel"))

    return render_template("potvrdit_zmenu_vlaku.html", vlak=pending, pocet_vozidel=len(doc.get("vozidla", [])))


@app.route("/vykaz-vozidel")
def vykaz_vozidel():
    doc = get_doc()
    vypocet = vytvor_vypocet(doc)

    return render_template(
        "vykaz_vozidel.html",
        doc=doc,
        vypocet=vypocet,
        vozidla=doc.get("vozidla", []),
    )


@app.route("/pridat-vozidlo", methods=["GET", "POST"])
def pridat_vozidlo():
    doc = get_doc()

    if request.method == "POST":
        cislo = request.form.get("cislo", "").strip()
        typ = request.form.get("typ", "").strip().upper()
        rezim = normalizuj_rezim(request.form.get("rezim_brzdeni", ""))
        stav = request.form.get("stav", "").strip()

        if not cislo:
            flash("Zadejte číslo vozidla.")
            return redirect(url_for("pridat_vozidlo"))

        vozidlo, chyba = najdi_vozidlo_v_databazi(cislo, typ)

        if chyba:
            flash(chyba)
            return redirect(url_for("pridat_vozidlo"))

        brzdici_vaha = vozidlo.get(rezim, 0)

        if brzdici_vaha <= 0:
            dostupne = dostupne_rezimy_vozidla(vozidlo)
            if dostupne:
                flash(
                    f"Vybraný režim {rezim} má u vozidla {vozidlo['nazev']} brzdicí hmotnost 0. "
                    f"Dostupné režimy: {', '.join(dostupne)}."
                )
            else:
                flash(
                    f"Vybraný režim {rezim} má u vozidla {vozidlo['nazev']} brzdicí hmotnost 0. "
                    f"Pro toto vozidlo nejsou v databázi dostupné žádné nenulové režimy."
                )
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

        flash(f"Přidáno vozidlo: {vozidlo['zadane_cislo']}")
        return redirect(url_for("vykaz_vozidel"))

    return render_template("pridat_vozidlo.html", rezimy=REZIMY_BRZDENI)


@app.route("/odstranit-vozidlo/<int:index>", methods=["POST"])
def odstranit_vozidlo(index):
    doc = get_doc()
    vozidla = doc.get("vozidla", [])

    if 0 <= index < len(vozidla):
        odebrane = vozidla.pop(index)
        save_doc(doc)
        flash(f"Odstraněno vozidlo: {odebrane.get('zadane_cislo', '')}")

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

    index_vozu = 0

    for i in range(len(doc["vozidla"])):
        if doc["vozidla"][i].get("typ") == "VOZ":
            doc["vozidla"][i] = vozy[index_vozu]
            index_vozu += 1

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

    return render_template(
        "zob.html",
        doc=doc,
        rezimy=REZIMY_BRZDENI,
        poznamky_moznosti=POZNAMKY_ZOB_MOZNOSTI,
    )


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

    return render_template(
        "zkouska.html",
        typ=klic,
        nazev=nazev,
        data=doc.get(klic, {}),
        vykonal_moznosti=VYKONAL_MOZNOSTI,
    )


@app.route("/rekapitulace")
def rekapitulace():
    doc = get_doc()
    vypocet = vytvor_vypocet(doc)

    return render_template(
        "rekapitulace.html",
        doc=doc,
        vypocet=vypocet,
        vozidla=doc.get("vozidla", []),
    )


@app.route("/tisk")
def tisk():
    doc = get_doc()
    vypocet = vytvor_vypocet(doc)

    return render_template(
        "tisk.html",
        doc=doc,
        vypocet=vypocet,
        vozidla=doc.get("vozidla", []),
    )


@app.route("/databaze")
def databaze():
    return render_template(
        "databaze.html",
        databaze=DATABAZE,
        vlaky=DATABAZE_VLAKU,
        tahak=TAHAK_CISEL_VOZIDEL,
    )


@app.route("/konec")
def konec():
    reset_doc()
    flash("Dokumentace byla ukončena.")
    return redirect(url_for("index"))


# ============================================================
# LOKÁLNÍ SPUŠTĚNÍ
# ============================================================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
