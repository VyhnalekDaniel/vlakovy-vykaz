from flask import Flask, render_template, request
import vypocet as vk

app = Flask(__name__)


def resetuj_data():
    """Vyčistí data mezi jednotlivými výpočty, aby se uživatelé nemíchali dohromady."""
    vk.seznam_vozidel.clear()
    vk.zadana_cisla.clear()
    vk.info_vlaku.update({
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
        "podpis_strojvedouciho": ""
    })


def normalizuj_rezim(rezim):
    rezim = (rezim or "P").strip().upper()
    if rezim == "R+MG":
        return "R+Mg"
    if rezim in ["G", "P", "R"]:
        return rezim
    if rezim == "R+Mg":
        return rezim
    return "P"


def normalizuj_stav(stav):
    stav = (stav or "dopravované").strip().lower()
    if stav in ["cinne", "činné", "c"]:
        return "činné"
    return "dopravované"


def pridej_vozidlo_web(cislo, typ, rezim="P", stav="dopravované"):
    cislo = (cislo or "").strip()
    typ = (typ or "").strip().upper()

    if not cislo:
        raise ValueError("Nebylo zadáno číslo vozidla.")
    if typ not in ["HDV", "VOZ"]:
        raise ValueError("Typ musí být HDV nebo VOZ.")

    cislo_ocistene = vk.ocisti_cislo(cislo)
    if cislo_ocistene in vk.zadana_cisla:
        raise ValueError(f"Vozidlo {cislo} už bylo zadáno.")

    klic = vk.ziskej_klic_vozidla(cislo, typ)
    if klic is None:
        raise ValueError(f"Z čísla {cislo} se nepodařilo získat klíč vozidla.")

    cast_databaze = vk.DATABAZE["HDV"] if typ == "HDV" else vk.DATABAZE["VOZY"]
    if klic not in cast_databaze:
        raise ValueError(f"V databázi není vozidlo s klíčem {klic} z čísla {cislo}.")

    vozidlo = cast_databaze[klic].copy()
    vozidlo["zadane_cislo"] = cislo
    vozidlo["klic"] = klic
    vozidlo["rezim_brzdeni"] = normalizuj_rezim(rezim)
    vozidlo["brzdici_vaha"] = vozidlo.get(vozidlo["rezim_brzdeni"], 0)

    if typ == "HDV":
        vozidlo["stav"] = normalizuj_stav(stav)
    else:
        vozidlo["stav"] = "vůz"

    vk.seznam_vozidel.append(vozidlo)
    vk.zadana_cisla.add(cislo_ocistene)
    vk.aktualizuj_brzdici_procenta()
    return vozidlo


def parse_vozidla(text):
    """
    Každý řádek:
    číslo;typ;režim;stav

    Příklad:
    95545811111-4;HDV;P;činné
    51542191000-0;VOZ;R
    """
    pridana = []
    chyby = []

    for radek_cislo, raw in enumerate((text or "").splitlines(), start=1):
        radek = raw.strip()
        if not radek:
            continue

        casti = [c.strip() for c in radek.split(";")]
        while len(casti) < 4:
            casti.append("")

        cislo, typ, rezim, stav = casti[:4]

        try:
            pridana.append(pridej_vozidlo_web(cislo, typ, rezim, stav))
        except Exception as e:
            chyby.append(f"Řádek {radek_cislo}: {e}")

    return pridana, chyby


def priprav_vysledek():
    vk.aktualizuj_brzdici_procenta()
    vyp = vk.vytvor_vypocet()
    rychlost_podle_brzd = vk.vypocitej_rychlost_podle_brzd()

    vozidla = []
    for i, v in enumerate(vk.seznam_vozidel, start=1):
        systemy = v.get("system_blokovani", [])
        if isinstance(systemy, list):
            systemy_text = ", ".join(systemy)
        else:
            systemy_text = str(systemy)

        vozidla.append({
            "poradi": i,
            "cislo": v.get("zadane_cislo", ""),
            "klic": v.get("klic", ""),
            "nazev": v.get("nazev", ""),
            "typ": v.get("typ", ""),
            "stav": v.get("stav", ""),
            "rezim": v.get("rezim_brzdeni", ""),
            "brzdici_vaha": v.get("brzdici_vaha", 0),
            "hmotnost": v.get("hmotnost", 0),
            "delka": v.get("delka", 0),
            "napravy": v.get("pocet_naprav", 0),
            "nbu": v.get("NBU", 0),
            "systemy": systemy_text,
            "nejvyssi_system": vk.nejvyssi_system_vozidla(v),
        })

    return {
        "info": vk.info_vlaku.copy(),
        "souhrn": vyp,
        "vozidla": vozidla,
        "rychlost_podle_brzd": rychlost_podle_brzd,
        "nbu": vk.vyhodnot_nbu(),
        "system_blokovani": vk.vyhodnot_system_blokovani(),
        "vedouci_hdv": vk.najdi_vedouci_hdv(),
    }


@app.route("/", methods=["GET", "POST"])
def index():
    vysledek = None
    chyby = []
    form = {
        "vlak": "",
        "datum_odjezdu": "",
        "vychozi_stanice": "",
        "konecna_stanice": "",
        "poznamky": "",
        "potrebna_procenta": "100",
        "zkouska_brzdy": "JZB",
        "misto_zkousky": "",
        "rezim_brzdy_vlaku": "P",
        "podpis_strojvedouciho": "",
        "vozidla_text": "95545811111-4;HDV;P;činné\n51542191000-0;VOZ;R\n51542190000-0;VOZ;R"
    }

    if request.method == "POST":
        resetuj_data()
        for key in form:
            form[key] = request.form.get(key, form[key])

        try:
            potrebna = float(str(form["potrebna_procenta"]).replace(",", "."))
        except ValueError:
            potrebna = 0
            chyby.append("Potřebná brzdicí procenta musí být číslo.")

        vk.info_vlaku["vlak"] = form["vlak"]
        vk.info_vlaku["datum_odjezdu"] = form["datum_odjezdu"]
        vk.info_vlaku["vychozi_stanice"] = form["vychozi_stanice"]
        vk.info_vlaku["konecna_stanice"] = form["konecna_stanice"]
        vk.info_vlaku["poznamky"] = form["poznamky"]
        vk.info_vlaku["potrebna_procenta"] = potrebna
        vk.info_vlaku["zkouska_brzdy"] = form["zkouska_brzdy"]
        vk.info_vlaku["misto_zkousky"] = form["misto_zkousky"] or form["vychozi_stanice"]
        vk.info_vlaku["rezim_brzdy_vlaku"] = normalizuj_rezim(form["rezim_brzdy_vlaku"])
        vk.info_vlaku["podpis_strojvedouciho"] = form["podpis_strojvedouciho"]

        _, chyby_vozidel = parse_vozidla(form["vozidla_text"])
        chyby.extend(chyby_vozidel)

        if not chyby:
            vysledek = priprav_vysledek()

    return render_template("index.html", form=form, vysledek=vysledek, chyby=chyby)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
