from copy import deepcopy
from os import environ

from flask import Flask, flash, redirect, render_template, request, session, url_for

from vypocet import DATABAZE, HIERARCHIE_BLOKOVANI, ocisti_cislo, ziskej_klic_vozidla

app = Flask(__name__)
app.secret_key = environ.get("SECRET_KEY", "dev-secret-change-me")

REZIMY = ["G", "P", "R", "R+Mg"]
STAVY_HDV = ["činné", "dopravované"]

DEFAULT_INFO_VLAKU = {
    "vlak": "",
    "datum_odjezdu": "",
    "vychozi_stanice": "",
    "konecna_stanice": "",
    "poznamky": "",
    "zkouska_brzdy": "",
    "misto_zkousky": "",
    "rezim_brzdy_vlaku": "",
    "potrebna_procenta": 0,
    "skutecna_procenta": 0,
    "chybejici_procenta": 0,
    "vedouci_hdv": "",
    "podpis_strojvedouciho": "",
}


def get_state():
    if "info_vlaku" not in session:
        session["info_vlaku"] = deepcopy(DEFAULT_INFO_VLAKU)
    if "seznam_vozidel" not in session:
        session["seznam_vozidel"] = []
    if "zadana_cisla" not in session:
        session["zadana_cisla"] = []
    return session["info_vlaku"], session["seznam_vozidel"], session["zadana_cisla"]


def save_state(info_vlaku, seznam_vozidel, zadana_cisla):
    session["info_vlaku"] = info_vlaku
    session["seznam_vozidel"] = seznam_vozidel
    session["zadana_cisla"] = zadana_cisla
    session.modified = True


def norm_rezim(value):
    rezim = (value or "P").strip().upper()
    if rezim == "R+MG":
        return "R+Mg"
    return rezim


def to_float(value, default=0):
    try:
        return float(str(value).replace(",", "."))
    except (TypeError, ValueError):
        return default


def vyber_brzdici_vahu(vozidlo):
    return vozidlo.get("brzdici_vaha", 0)


def spocitej_skupinu(vozidla):
    return {
        "pocet": len(vozidla),
        "hmotnost": sum(v["hmotnost"] for v in vozidla),
        "delka": sum(v["delka"] for v in vozidla),
        "pocet_naprav": sum(v["pocet_naprav"] for v in vozidla),
        "brzdici_vaha": sum(vyber_brzdici_vahu(v) for v in vozidla),
        "kotoucove_brzdy": sum(1 for v in vozidla if v.get("kotoucove_brzdy", 0) == 1),
        "nekovove_spaliky": sum(1 for v in vozidla if v.get("nekovove_spaliky", 0) == 1),
        "G": sum(1 for v in vozidla if v.get("rezim_brzdeni") == "G"),
        "P": sum(1 for v in vozidla if v.get("rezim_brzdeni") == "P"),
        "R": sum(1 for v in vozidla if v.get("rezim_brzdeni") == "R"),
        "R+Mg": sum(1 for v in vozidla if v.get("rezim_brzdeni") == "R+Mg"),
    }


def vytvor_vypocet(seznam_vozidel):
    cinna_hdv = []
    dopravovana_hdv = []
    vozy = []

    for vozidlo in seznam_vozidel:
        if vozidlo["typ"] == "HDV" and vozidlo["stav"] == "činné":
            cinna_hdv.append(vozidlo)
        elif vozidlo["typ"] == "HDV" and vozidlo["stav"] == "dopravované":
            dopravovana_hdv.append(vozidlo)
        elif vozidlo["typ"] == "VOZ":
            vozy.append(vozidlo)

    souprava = dopravovana_hdv + vozy
    vlak = cinna_hdv + dopravovana_hdv + vozy
    max_rychlost = min((v["max_rychlost"] for v in vlak), default=0)

    return {
        "cinna_hdv": spocitej_skupinu(cinna_hdv),
        "dopravovana_hdv": spocitej_skupinu(dopravovana_hdv),
        "vozy": spocitej_skupinu(vozy),
        "souprava": spocitej_skupinu(souprava),
        "vlak": spocitej_skupinu(vlak),
        "max_rychlost": max_rychlost,
    }


def aktualizuj_brzdici_procenta(info_vlaku, seznam_vozidel):
    vypocet = vytvor_vypocet(seznam_vozidel)
    celkova_hmotnost = vypocet["vlak"]["hmotnost"]
    brzdici_vaha = vypocet["vlak"]["brzdici_vaha"]
    skutecna = 0 if celkova_hmotnost == 0 else (brzdici_vaha / celkova_hmotnost) * 100
    potrebna = to_float(info_vlaku.get("potrebna_procenta"), 0)
    chybejici = max(0, potrebna - skutecna)
    info_vlaku["skutecna_procenta"] = skutecna
    info_vlaku["chybejici_procenta"] = chybejici
    return info_vlaku


def rychlost_podle_brzd(info_vlaku, seznam_vozidel):
    info_vlaku = aktualizuj_brzdici_procenta(info_vlaku, seznam_vozidel)
    vypocet = vytvor_vypocet(seznam_vozidel)
    return max(0, int(vypocet["max_rychlost"] - info_vlaku["chybejici_procenta"]))


def nejvyssi_system_vozidla(vozidlo):
    systemy = vozidlo.get("system_blokovani", [])
    if isinstance(systemy, str):
        systemy = [systemy]
    platne = [s for s in systemy if s in HIERARCHIE_BLOKOVANI]
    if not platne:
        return "nezjištěno"
    return max(platne, key=lambda s: HIERARCHIE_BLOKOVANI.index(s))


def vyhodnot_system_blokovani(seznam_vozidel):
    nejvyssi_systemy = []
    for vozidlo in seznam_vozidel:
        system = nejvyssi_system_vozidla(vozidlo)
        if system in HIERARCHIE_BLOKOVANI:
            nejvyssi_systemy.append(system)
    if not nejvyssi_systemy:
        return "nezjištěno"
    return min(nejvyssi_systemy, key=lambda s: HIERARCHIE_BLOKOVANI.index(s))


def vyhodnot_nbu(seznam_vozidel):
    if not seznam_vozidel:
        return "NBU neaktivní"
    return "NBU aktivní" if all(v.get("NBU", 0) == 1 for v in seznam_vozidel) else "NBU neaktivní"


def najdi_vedouci_hdv(seznam_vozidel):
    for vozidlo in seznam_vozidel:
        if vozidlo["typ"] == "HDV" and vozidlo["stav"] == "činné":
            return vozidlo["zadane_cislo"]
    return ""


def vytvor_vykaz(info_vlaku, seznam_vozidel):
    info_vlaku = aktualizuj_brzdici_procenta(info_vlaku, seznam_vozidel)
    vypocet = vytvor_vypocet(seznam_vozidel)
    return {
        "info": info_vlaku,
        "vozidla": seznam_vozidel,
        "vypocet": vypocet,
        "rychlost_podle_brzd": rychlost_podle_brzd(info_vlaku, seznam_vozidel),
        "nbu": vyhodnot_nbu(seznam_vozidel),
        "system_blokovani": vyhodnot_system_blokovani(seznam_vozidel),
    }


def pridej_vozidlo_do_stavu(seznam_vozidel, zadana_cisla, cislo, typ, rezim_brzdeni, stav):
    cislo = (cislo or "").strip()
    if not cislo:
        raise ValueError("Nebylo zadáno žádné číslo vozidla.")

    cislo_ocistene = ocisti_cislo(cislo)
    if cislo_ocistene in zadana_cisla:
        raise ValueError("Toto číslo už bylo zadáno. Zadejte jiné číslo.")

    typ = (typ or "").strip().upper()
    if typ not in ["HDV", "VOZ"]:
        raise ValueError("Typ musí být HDV nebo VOZ.")

    klic = ziskej_klic_vozidla(cislo, typ)
    if klic is None:
        raise ValueError("Nepodařilo se z čísla získat klíč vozidla.")

    cast_databaze = DATABAZE["HDV"] if typ == "HDV" else DATABAZE["VOZY"]
    if klic not in cast_databaze:
        raise ValueError(f"V databázi není vozidlo s klíčem {klic}.")

    rezim_brzdeni = norm_rezim(rezim_brzdeni)
    if rezim_brzdeni not in REZIMY:
        raise ValueError("Režim brzdění musí být G, P, R nebo R+Mg.")

    vozidlo = deepcopy(cast_databaze[klic])
    vozidlo["zadane_cislo"] = cislo
    vozidlo["klic"] = klic
    vozidlo["rezim_brzdeni"] = rezim_brzdeni
    vozidlo["brzdici_vaha"] = vozidlo.get(rezim_brzdeni, 0)

    if typ == "HDV":
        stav = (stav or "činné").strip().lower()
        if stav in ["cinne", "činné"]:
            stav = "činné"
        elif stav in ["dopravovane", "dopravované"]:
            stav = "dopravované"
        else:
            raise ValueError("Stav HDV musí být činné nebo dopravované.")
        vozidlo["stav"] = stav
    else:
        vozidlo["stav"] = "vůz"

    seznam_vozidel.append(vozidlo)
    zadana_cisla.append(cislo_ocistene)
    return vozidlo


@app.route("/")
def menu():
    info_vlaku, seznam_vozidel, _ = get_state()
    info_vlaku = aktualizuj_brzdici_procenta(info_vlaku, seznam_vozidel)
    save_state(info_vlaku, seznam_vozidel, session["zadana_cisla"])
    return render_template("menu.html", info=info_vlaku, pocet=len(seznam_vozidel))


@app.route("/data-vlaku", methods=["GET", "POST"])
def data_vlaku():
    info_vlaku, seznam_vozidel, zadana_cisla = get_state()
    if request.method == "POST":
        for key in ["vlak", "datum_odjezdu", "vychozi_stanice", "konecna_stanice", "poznamky", "podpis_strojvedouciho"]:
            info_vlaku[key] = request.form.get(key, "")
        info_vlaku["potrebna_procenta"] = to_float(request.form.get("potrebna_procenta"), 0)
        aktualizuj_brzdici_procenta(info_vlaku, seznam_vozidel)
        save_state(info_vlaku, seznam_vozidel, zadana_cisla)
        flash("Data vlaku byla uložena.", "success")
        return redirect(url_for("menu"))
    return render_template("data_vlaku.html", info=info_vlaku)


@app.route("/pridat-vozidlo", methods=["GET", "POST"])
def pridat_vozidlo():
    info_vlaku, seznam_vozidel, zadana_cisla = get_state()
    if request.method == "POST":
        try:
            vozidlo = pridej_vozidlo_do_stavu(
                seznam_vozidel,
                zadana_cisla,
                request.form.get("cislo"),
                request.form.get("typ"),
                request.form.get("rezim_brzdeni"),
                request.form.get("stav"),
            )
            aktualizuj_brzdici_procenta(info_vlaku, seznam_vozidel)
            save_state(info_vlaku, seznam_vozidel, zadana_cisla)
            flash(f"Přidáno: {vozidlo['nazev']} | brzdicí váha {vozidlo['brzdici_vaha']}", "success")
            return redirect(url_for("pridat_vozidlo"))
        except ValueError as e:
            flash(str(e), "error")
    return render_template("pridat_vozidlo.html", rezimy=REZIMY, stavy=STAVY_HDV)


@app.route("/vykaz")
def vykaz():
    info_vlaku, seznam_vozidel, zadana_cisla = get_state()
    if not seznam_vozidel:
        flash("Nejsou zadána žádná vozidla. Nejdřív použij volbu 2.", "error")
        return redirect(url_for("menu"))
    data = vytvor_vykaz(info_vlaku, seznam_vozidel)
    save_state(info_vlaku, seznam_vozidel, zadana_cisla)
    return render_template("vykaz.html", data=data)


@app.route("/odstranit", methods=["GET", "POST"])
def odstranit():
    info_vlaku, seznam_vozidel, zadana_cisla = get_state()
    if request.method == "POST":
        try:
            pozice = int(request.form.get("pozice", 0))
            if pozice < 1 or pozice > len(seznam_vozidel):
                raise ValueError("Neplatná pozice.")
            vozidlo = seznam_vozidel.pop(pozice - 1)
            cislo = ocisti_cislo(vozidlo["zadane_cislo"])
            if cislo in zadana_cisla:
                zadana_cisla.remove(cislo)
            aktualizuj_brzdici_procenta(info_vlaku, seznam_vozidel)
            save_state(info_vlaku, seznam_vozidel, zadana_cisla)
            flash(f"Odstraněno vozidlo: {vozidlo['zadane_cislo']}", "success")
            return redirect(url_for("seznam"))
        except ValueError as e:
            flash(str(e), "error")
    return render_template("odstranit.html", vozidla=seznam_vozidel)


@app.route("/otoc-jednotku", methods=["POST"])
def otoc_jednotku():
    info_vlaku, seznam_vozidel, zadana_cisla = get_state()
    seznam_vozidel.reverse()
    save_state(info_vlaku, seznam_vozidel, zadana_cisla)
    flash("Jednotka byla otočena.", "success")
    return redirect(url_for("seznam"))


@app.route("/otoc-vlak", methods=["POST"])
def otoc_vlak():
    info_vlaku, seznam_vozidel, zadana_cisla = get_state()
    vozy = [v for v in seznam_vozidel if v["typ"] == "VOZ"]
    if not vozy:
        flash("Ve vlaku nejsou žádné vozy k otočení.", "error")
        return redirect(url_for("seznam"))
    vozy.reverse()
    index_vozu = 0
    for i, vozidlo in enumerate(seznam_vozidel):
        if vozidlo["typ"] == "VOZ":
            seznam_vozidel[i] = vozy[index_vozu]
            index_vozu += 1
    save_state(info_vlaku, seznam_vozidel, zadana_cisla)
    flash("Vlak byl otočen. Otočily se pouze vozy, HDV zůstala na původních pozicích.", "success")
    return redirect(url_for("seznam"))


@app.route("/seznam")
def seznam():
    _, seznam_vozidel, _ = get_state()
    return render_template("seznam.html", vozidla=seznam_vozidel, podrobne=False)


@app.route("/seznam-podrobne")
def seznam_podrobne():
    _, seznam_vozidel, _ = get_state()
    return render_template("seznam.html", vozidla=seznam_vozidel, podrobne=True, nejvyssi_system_vozidla=nejvyssi_system_vozidla)


@app.route("/databaze")
def databaze():
    return render_template("databaze.html", databaze=DATABAZE)


@app.route("/smazat", methods=["POST"])
def smazat():
    info_vlaku, _, _ = get_state()
    info_vlaku = aktualizuj_brzdici_procenta(info_vlaku, [])
    save_state(info_vlaku, [], [])
    flash("Seznam vozidel byl smazán.", "success")
    return redirect(url_for("menu"))


@app.route("/zkouska", methods=["GET", "POST"])
def zkouska():
    info_vlaku, seznam_vozidel, zadana_cisla = get_state()
    if request.method == "POST":
        if not seznam_vozidel:
            flash("Nejdřív musíš zadat vozidla.", "error")
            return redirect(url_for("zkouska"))
        typ = request.form.get("zkouska_brzdy", "JZB")
        misto = request.form.get("misto_zkousky", "").strip() or info_vlaku.get("vychozi_stanice", "")
        rezim = norm_rezim(request.form.get("rezim_brzdy_vlaku"))
        info_vlaku["zkouska_brzdy"] = typ
        info_vlaku["misto_zkousky"] = misto
        info_vlaku["rezim_brzdy_vlaku"] = rezim
        info_vlaku["vedouci_hdv"] = najdi_vedouci_hdv(seznam_vozidel)
        aktualizuj_brzdici_procenta(info_vlaku, seznam_vozidel)
        save_state(info_vlaku, seznam_vozidel, zadana_cisla)
        flash(f"{typ} byla automaticky vytvořena.", "success")
        return redirect(url_for("vykaz"))
    return render_template("zkouska.html", info=info_vlaku, rezimy=REZIMY)


@app.route("/konec", methods=["POST"])
def konec():
    session.clear()
    flash("Relace byla ukončena a data byla vymazána.", "success")
    return redirect(url_for("menu"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
