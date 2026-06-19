from copy import deepcopy
from os import environ

from flask import Flask, flash, redirect, render_template, request, session, url_for

from vypocet import (
    DATABAZE,
    DATABAZE_VLAKU,
    TAHAK_CISEL_VOZIDEL,
    REZIMY_BRZDENI,
    najdi_vlak,
    otoc_jednotku,
    otoc_vlak,
    prazdna_dokumentace,
    presun_vozidlo,
    pridej_vozidlo,
    skutecna_brzdici_procenta,
    vytvor_vypocet,
    vypocitej_rychlost_podle_brzd,
    vyhodnot_nbu,
    vyhodnot_system_blokovani,
)

app = Flask(__name__)
app.secret_key = environ.get("SECRET_KEY", "vlakovy_web_dev_secret")

KDO_VYKONAL_MOZNOSTI = [
    "Strojvedoucí",
    "Posunovač",
    "Vozmistr",
    "Obsluha vlaku",
    "Výpravčí",
    "Jiný ŽDP",
]

POZNAMKY_ZOB_MOZNOSTI = [
    # Sem si později dopiš vlastní přednastavené poznámky, například:
    # "Vlak brzděn v režimu P.",
]


def get_doc():
    if "dokumentace" not in session:
        session["dokumentace"] = prazdna_dokumentace()
    return session["dokumentace"]


def save_doc(doc):
    session["dokumentace"] = doc
    session.modified = True


def vlak_z_formulare(zdroj):
    return {
        "cislo": request.form.get("cislo", "").strip(),
        "druh": request.form.get("druh", "").strip(),
        "datum": request.form.get("datum", "").strip(),
        "vychozi_stanice": request.form.get("vychozi_stanice", "").strip(),
        "konecna_stanice": request.form.get("konecna_stanice", "").strip(),
        "sepsano_v": request.form.get("sepsano_v", "").strip(),
        "sepsal": request.form.get("sepsal", "").strip(),
        "poznamky": request.form.get("poznamky", "").strip(),
        "zdroj": zdroj,
    }


def uloz_nebo_potvrd_vlak(novy_vlak):
    doc = get_doc()
    stary_cislo = doc.get("vlak", {}).get("cislo", "")
    meni_se_vlak = stary_cislo and novy_vlak.get("cislo") and stary_cislo != novy_vlak.get("cislo")
    ma_vozidla = len(doc.get("vozidla", [])) > 0
    if meni_se_vlak and ma_vozidla:
        session["pending_vlak"] = novy_vlak
        session.modified = True
        return redirect(url_for("potvrdit_zmenu_vlaku"))
    doc["vlak"] = novy_vlak
    save_doc(doc)
    return redirect(url_for("vykaz_vozidel"))


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/nova-dokumentace")
def nova_dokumentace():
    session["dokumentace"] = prazdna_dokumentace()
    session.pop("pending_vlak", None)
    flash("Založena nová vlaková dokumentace.", "ok")
    return redirect(url_for("vlakova_dokumentace"))


@app.route("/vlakova-dokumentace")
def vlakova_dokumentace():
    return render_template("vlakova_dokumentace.html")


@app.route("/vlak-z-jr", methods=["GET", "POST"])
def vlak_z_jr():
    nalezeny = None
    hledano = ""
    if request.method == "POST":
        action = request.form.get("action")
        if action == "hledat":
            hledano = request.form.get("cislo", "").strip()
            nalezeny = najdi_vlak(hledano)
            if not nalezeny:
                flash("Vlak nebyl nalezen v databázi. Můžeš ho přidat ručně.", "warn")
        elif action == "ulozit":
            cislo = request.form.get("cislo", "").strip()
            data = najdi_vlak(cislo)
            if not data:
                flash("Vlak už není v databázi nalezen. Zadej ho ručně.", "error")
                return redirect(url_for("libovolny_vlak", cislo=cislo))
            novy_vlak = vlak_z_formulare("JŘ")
            return uloz_nebo_potvrd_vlak(novy_vlak)
    return render_template("vlak_z_jr.html", nalezeny=nalezeny, hledano=hledano)


@app.route("/libovolny-vlak", methods=["GET", "POST"])
def libovolny_vlak():
    doc = get_doc()
    if request.method == "POST":
        return uloz_nebo_potvrd_vlak(vlak_z_formulare("ručně"))
    vychozi = deepcopy(doc.get("vlak", {}))
    if request.args.get("cislo"):
        vychozi["cislo"] = request.args.get("cislo")
    return render_template("libovolny_vlak.html", vlak=vychozi)


@app.route("/potvrdit-zmenu-vlaku", methods=["GET", "POST"])
def potvrdit_zmenu_vlaku():
    pending = session.get("pending_vlak")
    if not pending:
        return redirect(url_for("vlakova_dokumentace"))
    if request.method == "POST":
        doc = get_doc()
        doc["vlak"] = pending
        if request.form.get("vozidla") == "smazat":
            doc["vozidla"] = []
            flash("Vlak byl změněn a výkaz vozidel byl vymazán.", "ok")
        else:
            flash("Vlak byl změněn a vozidla zůstala ve výkazu.", "ok")
        save_doc(doc)
        session.pop("pending_vlak", None)
        return redirect(url_for("vykaz_vozidel"))
    return render_template("potvrdit_zmenu_vlaku.html", pending=pending, doc=get_doc())


@app.route("/vykaz-vozidel")
def vykaz_vozidel():
    doc = get_doc()
    vypocet = vytvor_vypocet(doc)
    return render_template("vykaz_vozidel.html", doc=doc, vypocet=vypocet)


@app.route("/pridat-vozidlo", methods=["GET", "POST"])
def pridat_vozidlo_route():
    doc = get_doc()
    if request.method == "POST":
        ok, zprava = pridej_vozidlo(
            doc,
            request.form.get("cislo"),
            request.form.get("typ"),
            request.form.get("rezim_brzdeni"),
            request.form.get("stav"),
        )
        if ok:
            save_doc(doc)
            flash(zprava, "ok")
            return redirect(url_for("vykaz_vozidel"))
        flash(zprava, "error")
    return render_template("pridat_vozidlo.html", rezimy=REZIMY_BRZDENI)


@app.route("/vozidlo/<int:index>/smazat", methods=["POST"])
def smazat_vozidlo(index):
    doc = get_doc()
    if 0 <= index < len(doc.get("vozidla", [])):
        cislo = doc["vozidla"][index].get("zadane_cislo")
        doc["vozidla"].pop(index)
        save_doc(doc)
        flash(f"Vozidlo {cislo} bylo odstraněno.", "ok")
    return redirect(url_for("vykaz_vozidel"))


@app.route("/vozidlo/<int:index>/nahoru", methods=["POST"])
def vozidlo_nahoru(index):
    doc = get_doc()
    presun_vozidlo(doc, index, index - 1)
    save_doc(doc)
    return redirect(url_for("vykaz_vozidel"))


@app.route("/vozidlo/<int:index>/dolu", methods=["POST"])
def vozidlo_dolu(index):
    doc = get_doc()
    presun_vozidlo(doc, index, index + 1)
    save_doc(doc)
    return redirect(url_for("vykaz_vozidel"))


@app.route("/vozidlo/<int:index>/presunout", methods=["POST"])
def vozidlo_presunout(index):
    doc = get_doc()
    try:
        nova_pozice = int(request.form.get("nova_pozice", "1")) - 1
    except ValueError:
        nova_pozice = index
    presun_vozidlo(doc, index, nova_pozice)
    save_doc(doc)
    return redirect(url_for("vykaz_vozidel"))


@app.route("/otocit-vlak", methods=["POST"])
def otocit_vlak_route():
    doc = get_doc()
    otoc_vlak(doc)
    save_doc(doc)
    flash("Vlak byl otočen. Otočily se pouze vozy, HDV zůstala na svých pozicích.", "ok")
    return redirect(url_for("vykaz_vozidel"))


@app.route("/otocit-jednotku", methods=["POST"])
def otocit_jednotku_route():
    doc = get_doc()
    otoc_jednotku(doc)
    save_doc(doc)
    flash("Jednotka byla otočena.", "ok")
    return redirect(url_for("vykaz_vozidel"))


def uloz_zob_z_formulare(doc):
    zob = doc.setdefault("zob", {})
    try:
        zob["potrebna_procenta"] = float((request.form.get("potrebna_procenta") or "0").replace(",", "."))
    except ValueError:
        zob["potrebna_procenta"] = 0
    zob["rezim_brzdy_vlaku"] = request.form.get("rezim_brzdy_vlaku", "P")
    zob["doprovod"] = request.form.get("doprovod", "").strip()
    zob["poznamky"] = request.form.get("poznamky", "").strip()
    zob["poznamky_vyber"] = request.form.getlist("poznamky_vyber")
    save_doc(doc)


@app.route("/zob", methods=["GET", "POST"])
def zob():
    doc = get_doc()
    if request.method == "POST":
        uloz_zob_z_formulare(doc)
        action = request.form.get("action")
        if action == "jzb":
            return redirect(url_for("zkouska_brzdy", typ="jzb"))
        if action == "uzb":
            return redirect(url_for("zkouska_brzdy", typ="uzb"))
        if action == "rekapitulace":
            return redirect(url_for("rekapitulace"))
        flash("Zpráva o brzdění byla uložena.", "ok")
    return render_template("zob.html", doc=doc, rezimy=REZIMY_BRZDENI, poznamky_moznosti=POZNAMKY_ZOB_MOZNOSTI)


@app.route("/zkouska/<typ>", methods=["GET", "POST"])
def zkouska_brzdy(typ):
    if typ not in ["jzb", "uzb"]:
        return redirect(url_for("zob"))
    doc = get_doc()
    if request.method == "POST":
        doc[typ] = {
            "vykonana": request.form.get("vykonana", "ne"),
            "kde": request.form.get("kde", "").strip(),
            "kdy": request.form.get("kdy", "").strip(),
            "kym": request.form.get("kym", "").strip(),
            "kym_jiny": request.form.get("kym_jiny", "").strip(),
        }
        save_doc(doc)
        flash(f"{typ.upper()} byla uložena.", "ok")
        return redirect(url_for("zob"))
    return render_template("zkouska.html", typ=typ, data=doc.get(typ, {}), moznosti=KDO_VYKONAL_MOZNOSTI)


@app.route("/rekapitulace")
def rekapitulace():
    doc = get_doc()
    vypocet = vytvor_vypocet(doc)
    rychlost, chybi, skutecna = vypocitej_rychlost_podle_brzd(doc)
    return render_template("rekapitulace.html", doc=doc, vypocet=vypocet, rychlost=rychlost, chybi=chybi, skutecna=skutecna, nbu=vyhodnot_nbu(doc), blokovani=vyhodnot_system_blokovani(doc))


@app.route("/tisk")
def tisk():
    doc = get_doc()
    vypocet = vytvor_vypocet(doc)
    rychlost, chybi, skutecna = vypocitej_rychlost_podle_brzd(doc)
    return render_template("tisk.html", doc=doc, vypocet=vypocet, rychlost=rychlost, chybi=chybi, skutecna=skutecna, nbu=vyhodnot_nbu(doc), blokovani=vyhodnot_system_blokovani(doc))


@app.route("/databaze")
def databaze():
    return render_template("databaze.html", databaze=DATABAZE, vlaky=DATABAZE_VLAKU, tahak=TAHAK_CISEL_VOZIDEL)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(environ.get("PORT", 5000)), debug=True)
