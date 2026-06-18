# ============================================================
# VÝKAZ VOZIDEL - JEDEN SOUBOR
# ============================================================

# ------------------------------------------------------------
# HIERARCHIE SYSTÉMŮ BLOKOVÁNÍ
# ------------------------------------------------------------

# Od nejslabšího po nejsilnější
HIERARCHIE_BLOKOVANI = ["TB5", "TB0", "SSOD", "TBS", "LAT", "CODS"]


# ------------------------------------------------------------
# DATABÁZE VOZIDEL
# ------------------------------------------------------------

DATABAZE = {
    "HDV": {
        "371": {
            "typ": "HDV",
            "nazev": "Lokomotiva řady 371",
            "hmotnost": 84,
            "delka": 16.8,
            "pocet_naprav": 4,
            "G": 38,
            "P": 107,
            "R": 0,
            "R+Mg": 0,
            "kotoucove_brzdy": 0,
            "nekovove_spaliky": 1,
            "NBU": 0,
            "system_blokovani": ["TB5"],
            "max_rychlost": 160
        },

        "362": {
            "typ": "HDV",
            "nazev": "Lokomotiva řady 362",
            "hmotnost": 86,
            "delka": 16.8,
            "pocet_naprav": 4,
            "G": 24,
            "P": 44,
            "R": 0,
            "R+Mg": 0,
            "kotoucove_brzdy": 0,
            "nekovove_spaliky": 1,
            "NBU": 0,
            "system_blokovani": ["TB5", "TB0", "SSOD"],
            "max_rychlost": 140
        },

        "810": {
            "typ": "HDV",
            "nazev": "Motorový vůz řady 810",
            "hmotnost": 24,
            "delka": 13.97,
            "pocet_naprav": 4,
            "G": 0,
            "P": 27,
            "R": 0,
            "R+Mg": 0,
            "kotoucove_brzdy": 0,
            "nekovove_spaliky": 1,
            "NBU": 0,
            "system_blokovani": ["CODS"],
            "max_rychlost": 80
        },

        "811": {
            "typ": "HDV",
            "nazev": "Motorový vůz řady 811",
            "hmotnost": 24,
            "delka": 13.97,
            "pocet_naprav": 4,
            "G": 0,
            "P": 27,
            "R": 0,
            "R+Mg": 0,
            "kotoucove_brzdy": 0,
            "nekovove_spaliky": 1,
            "NBU": 0,
            "system_blokovani": ["CODS"],
            "max_rychlost": 80
        },

        "845": {
            "typ": "HDV",
            "nazev": "Motorový vůz řady 845",
            "hmotnost": 45,
            "delka": 22.70,
            "pocet_naprav": 4,
            "G": 0,
            "P": 0,
            "R": 64,
            "R+Mg": 81,
            "kotoucove_brzdy": 0,
            "nekovove_spaliky": 1,
            "NBU": 0,
            "system_blokovani": ["CODS"],
            "max_rychlost": 120
        },

        "742": {
            "typ": "HDV",
            "nazev": "Lokomotiva řady 742",
            "hmotnost": 64,
            "delka": 14.42,
            "pocet_naprav": 4,
            "G": 30,
            "P": 42,
            "R": 0,
            "R+Mg": 0,
            "kotoucove_brzdy": 0,
            "nekovove_spaliky": 1,
            "NBU": 0,
            "system_blokovani": ["TB5"],
            "max_rychlost": 90
        },

        "750": {
            "typ": "HDV",
            "nazev": "Lokomotiva řady 750",
            "hmotnost": 74,
            "delka": 16.50,
            "pocet_naprav": 4,
            "G": 35,
            "P": 50,
            "R": 0,
            "R+Mg": 0,
            "kotoucove_brzdy": 0,
            "nekovove_spaliky": 1,
            "NBU": 0,
            "system_blokovani": ["TB5"],
            "max_rychlost": 100
        },

        "162": {
            "typ": "HDV",
            "nazev": "Lokomotiva řady 162",
            "hmotnost": 85,
            "delka": 16.80,
            "pocet_naprav": 4,
            "G": 24,
            "P": 44,
            "R": 0,
            "R+Mg": 0,
            "kotoucove_brzdy": 0,
            "nekovove_spaliky": 1,
            "NBU": 0,
            "system_blokovani": ["TB5", "TB0", "SSOD"],
            "max_rychlost": 120
        },

        "843": {
            "typ": "HDV",
            "nazev": "Motorový vůz řady 843",
            "hmotnost": 62,
            "delka": 14.42,
            "pocet_naprav": 4,
            "G": 0,
            "P": 65,
            "R": 0,
            "R+Mg": 0,
            "kotoucove_brzdy": 0,
            "nekovove_spaliky": 1,
            "NBU": 0,
            "system_blokovani": ["CODS"],
            "max_rychlost": 110
        }
    },

    "VOZY": {
        "1991": {
            "typ": "VOZ",
            "nazev": "Vůz Amz138",
            "hmotnost": 55,
            "delka": 26.4,
            "pocet_naprav": 4,
            "G": 0,
            "P": 60,
            "R": 76,
            "R+Mg": 117,
            "kotoucove_brzdy": 1,
            "nekovove_spaliky": 0,
            "NBU": 1,
            "system_blokovani": ["TB5", "TB0", "TBS"],
            "max_rychlost": 200
        },

        "2190": {
            "typ": "VOZ",
            "nazev": "Vůz Bmz226",
            "hmotnost": 53,
            "delka": 26.4,
            "pocet_naprav": 4,
            "G": 0,
            "P": 51,
            "R": 70,
            "R+Mg": 111,
            "kotoucove_brzdy": 1,
            "nekovove_spaliky": 0,
            "NBU": 1,
            "system_blokovani": ["TB5", "TB0", "TBS"],
            "max_rychlost": 200
        },

        "945": {
            "typ": "VOZ",
            "nazev": "Vůz 945",
            "hmotnost": 33,
            "delka": 22.7,
            "pocet_naprav": 4,
            "G": 0,
            "P": 0,
            "R": 48,
            "R+Mg": 60,
            "kotoucove_brzdy": 1,
            "nekovove_spaliky": 0,
            "NBU": 0,
            "system_blokovani": ["CODS"],
            "max_rychlost": 120
        },

        "2244": {
            "typ": "VOZ",
            "nazev": "Vůz Bdmtee275",
            "hmotnost": 48,
            "delka": 26.4,
            "pocet_naprav": 4,
            "G": 0,
            "P": 41,
            "R": 59,
            "R+Mg": 0,
            "kotoucove_brzdy": 1,
            "nekovove_spaliky": 0,
            "NBU": 0,
            "system_blokovani": ["TB5", "SSOD"],
            "max_rychlost": 160
        },

        "9329": {
            "typ": "VOZ",
            "nazev": "Vůz BDtax782",
            "hmotnost": 20,
            "delka": 13.97,
            "pocet_naprav": 4,
            "G": 0,
            "P": 21,
            "R": 0,
            "R+Mg": 0,
            "kotoucove_brzdy": 0,
            "nekovove_spaliky": 1,
            "NBU": 0,
            "system_blokovani": ["TB5"],
            "max_rychlost": 80
        }
    }
}


# ------------------------------------------------------------
# PAMĚŤ PROGRAMU
# ------------------------------------------------------------

seznam_vozidel = []
zadana_cisla = set()

info_vlaku = {
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
}


# ------------------------------------------------------------
# POMOCNÉ FUNKCE
# ------------------------------------------------------------

def ocisti_cislo(cislo):
    """
    Odstraní pomlčky a mezery.
    """
    return cislo.replace("-", "").replace(" ", "")


def ziskej_klic_vozidla(cislo, typ):
    """
    HDV:
    - najde 54
    - přeskočí jedno číslo za 54
    - vezme další 3 číslice

    Příklad:
    95545811111-4
    95 54 5 811 1114
          ^ přeskočit
            811

    VOZ:
    - přeskočí první 4 číslice
    - vezme další 4 číslice

    Příklad:
    51542191000-0
    5154 2191 0000
         2191
    """

    cislo = ocisti_cislo(cislo)

    if typ == "HDV":
        pozice = cislo.find("54")

        if pozice == -1:
            return None

        start = pozice + 3

        if len(cislo) < start + 3:
            return None

        return cislo[start:start + 3]

    if typ == "VOZ":
        if len(cislo) < 8:
            return None

        return cislo[4:8]

    return None


def nacti_float(text):
    while True:
        hodnota = input(text).replace(",", ".")

        try:
            return float(hodnota)
        except ValueError:
            print("Musíte zadat číslo.")


def nacti_rezim_brzdeni():
    while True:
        rezim = input("Zadejte režim brzdění vozidla G/P/R/R+Mg: ").strip()

        if rezim == "":
            rezim = "P"

        rezim = rezim.upper()

        if rezim == "R+MG":
            rezim = "R+Mg"

        if rezim in ["G", "P", "R", "R+Mg"]:
            return rezim

        print("Neplatný režim. Zadejte G, P, R nebo R+Mg.")


def nacti_rezim_brzdy_vlaku():
    while True:
        rezim = input("Režim brzdy vlaku G/P/R/R+Mg: ").strip()

        if rezim == "":
            rezim = "P"

        rezim = rezim.upper()

        if rezim == "R+MG":
            rezim = "R+Mg"

        if rezim in ["G", "P", "R", "R+Mg"]:
            return rezim

        print("Neplatný režim. Zadejte G, P, R nebo R+Mg.")


def vyber_brzdici_vahu(vozidlo):
    return vozidlo.get("brzdici_vaha", 0)


# ------------------------------------------------------------
# DATA O VLAKU
# ------------------------------------------------------------

def vloz_data_vlaku():
    print("\n=== DATA O VLAKU ===")

    info_vlaku["vlak"] = input("Zadejte číslo vlaku: ")
    info_vlaku["datum_odjezdu"] = input("Zadejte datum odjezdu: ")
    info_vlaku["vychozi_stanice"] = input("Zadejte výchozí stanici: ")
    info_vlaku["konecna_stanice"] = input("Zadejte konečnou stanici: ")
    info_vlaku["poznamky"] = input("Zadejte poznámky k vlaku: ")

    print("\n=== BRZDICÍ PROCENTA ===")
    info_vlaku["potrebna_procenta"] = nacti_float("Zadejte potřebná brzdicí procenta: ")

    info_vlaku["skutecna_procenta"] = 0
    info_vlaku["chybejici_procenta"] = 0

    print("\nData vlaku byla uložena.")


# ------------------------------------------------------------
# PŘIDÁNÍ VOZIDLA
# ------------------------------------------------------------

def pridej_vozidlo():
    print("\n=== PŘIDÁNÍ VOZIDLA ===")

    cislo = input("Zadejte celé číslo vozu nebo lokomotivy: ").strip()

    if cislo == "":
        print("Nebylo zadáno žádné číslo.")
        return

    cislo_ocistene = ocisti_cislo(cislo)

    if cislo_ocistene in zadana_cisla:
        print("Toto číslo už bylo zadáno. Zadejte jiné číslo.")
        return

    typ = input("Jedná se o HDV nebo VOZ? ").strip().upper()

    if typ not in ["HDV", "VOZ"]:
        print("Chyba: zadejte pouze HDV nebo VOZ.")
        return

    klic = ziskej_klic_vozidla(cislo, typ)

    print(f"DEBUG: očištěné číslo = {cislo_ocistene}")
    print(f"DEBUG: hledaný klíč v databázi = {klic}")

    if klic is None:
        print("Nepodařilo se z čísla získat klíč vozidla.")
        return

    if typ == "HDV":
        cast_databaze = DATABAZE["HDV"]
    else:
        cast_databaze = DATABAZE["VOZY"]

    if klic not in cast_databaze:
        print(f"V databázi není vozidlo s klíčem {klic}.")
        print("Doplň ho do části DATABAZE.")
        return

    vozidlo = cast_databaze[klic].copy()
    vozidlo["zadane_cislo"] = cislo
    vozidlo["klic"] = klic

    rezim_brzdeni = nacti_rezim_brzdeni()
    vozidlo["rezim_brzdeni"] = rezim_brzdeni
    vozidlo["brzdici_vaha"] = vozidlo.get(rezim_brzdeni, 0)

    if typ == "HDV":
        stav = input("Je HDV činné nebo dopravované? ").strip().lower()

        if stav in ["cinne", "činné"]:
            stav = "činné"
        elif stav in ["dopravovane", "dopravované"]:
            stav = "dopravované"
        else:
            print("Chyba: stav HDV musí být činné nebo dopravované.")
            return

        vozidlo["stav"] = stav
    else:
        vozidlo["stav"] = "vůz"

    seznam_vozidel.append(vozidlo)
    zadana_cisla.add(cislo_ocistene)

    aktualizuj_brzdici_procenta()

    print(f"Přidáno: {vozidlo['nazev']}")
    print(f"Režim brzdění: {vozidlo['rezim_brzdeni']}")
    print(f"Brzdicí váha: {vozidlo['brzdici_vaha']}")
    print(f"Počet vozidel v seznamu: {len(seznam_vozidel)}")


# ------------------------------------------------------------
# VÝPOČTY
# ------------------------------------------------------------

def spocitej_skupinu(vozidla):
    return {
        "pocet": len(vozidla),
        "hmotnost": sum(v["hmotnost"] for v in vozidla),
        "delka": sum(v["delka"] for v in vozidla),
        "pocet_naprav": sum(v["pocet_naprav"] for v in vozidla),
        "brzdici_vaha": sum(vyber_brzdici_vahu(v) for v in vozidla),

        "kotoucove_brzdy": sum(
            1 for v in vozidla if v.get("kotoucove_brzdy", 0) == 1
        ),

        "nekovove_spaliky": sum(
            1 for v in vozidla if v.get("nekovove_spaliky", 0) == 1
        ),

        "G": sum(1 for v in vozidla if v.get("rezim_brzdeni") == "G"),
        "P": sum(1 for v in vozidla if v.get("rezim_brzdeni") == "P"),
        "R": sum(1 for v in vozidla if v.get("rezim_brzdeni") == "R"),
        "R+Mg": sum(1 for v in vozidla if v.get("rezim_brzdeni") == "R+Mg"),
    }


def vytvor_vypocet():
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

    if len(vlak) > 0:
        max_rychlost = min(v["max_rychlost"] for v in vlak)
    else:
        max_rychlost = 0

    return {
        "cinna_hdv": spocitej_skupinu(cinna_hdv),
        "dopravovana_hdv": spocitej_skupinu(dopravovana_hdv),
        "vozy": spocitej_skupinu(vozy),
        "souprava": spocitej_skupinu(souprava),
        "vlak": spocitej_skupinu(vlak),
        "max_rychlost": max_rychlost
    }


def vypocitej_brzdici_procenta():
    vypocet = vytvor_vypocet()

    celkova_hmotnost = vypocet["vlak"]["hmotnost"]
    brzdici_vaha = vypocet["vlak"]["brzdici_vaha"]

    if celkova_hmotnost == 0:
        return 0

    return (brzdici_vaha / celkova_hmotnost) * 100


def aktualizuj_brzdici_procenta():
    skutecna = vypocitej_brzdici_procenta()
    potrebna = info_vlaku["potrebna_procenta"]

    chybejici = potrebna - skutecna

    if chybejici < 0:
        chybejici = 0

    info_vlaku["skutecna_procenta"] = skutecna
    info_vlaku["chybejici_procenta"] = chybejici


def vypocitej_rychlost_podle_brzd():
    """
    Pokud chybí brzdicí procenta, sníží maximální rychlost.
    1 chybějící procento = -1 km/h.

    Výsledek nikdy neklesne pod 0 km/h.
    """

    aktualizuj_brzdici_procenta()

    vypocet = vytvor_vypocet()

    max_rychlost = vypocet["max_rychlost"]
    chybejici = info_vlaku["chybejici_procenta"]

    upravena_rychlost = max_rychlost - chybejici

    if upravena_rychlost < 0:
        upravena_rychlost = 0

    return int(upravena_rychlost)


def najdi_vedouci_hdv():
    for vozidlo in seznam_vozidel:
        if vozidlo["typ"] == "HDV" and vozidlo["stav"] == "činné":
            return vozidlo["zadane_cislo"]

    return ""


# ------------------------------------------------------------
# NBU A SYSTÉM BLOKOVÁNÍ
# ------------------------------------------------------------

def vyhodnot_nbu():
    """
    Pokud mají všechna vozidla NBU = 1, vrátí NBU aktivní.
    Jinak vrátí NBU neaktivní.
    """

    if len(seznam_vozidel) == 0:
        return "NBU neaktivní"

    for vozidlo in seznam_vozidel:
        if vozidlo.get("NBU", 0) != 1:
            return "NBU neaktivní"

    return "NBU aktivní"


def nejvyssi_system_vozidla(vozidlo):
    """
    Zjistí nejvyšší systém blokování, který dané vozidlo umí.

    Například:
    ["TB5", "TB0", "SSOD", "TBS"] -> TBS
    ["TB5", "TB0"] -> TB0
    """

    systemy = vozidlo.get("system_blokovani", [])

    if isinstance(systemy, str):
        systemy = [systemy]

    platne_systemy = []

    for system in systemy:
        if system in HIERARCHIE_BLOKOVANI:
            platne_systemy.append(system)

    if len(platne_systemy) == 0:
        return "nezjištěno"

    nejvyssi_index = max(
        HIERARCHIE_BLOKOVANI.index(system)
        for system in platne_systemy
    )

    return HIERARCHIE_BLOKOVANI[nejvyssi_index]


def vyhodnot_system_blokovani():
    """
    Pro každé vozidlo zjistí jeho nejvyšší dostupný systém.
    Potom pro celý vlak vybere nejslabší z těchto nejvyšších systémů.

    Hierarchie:
    TB5 < TB0 < SSOD < TBS < LAT < CODS

    Příklad:
    Vozidlo 1 max TBS
    Vozidlo 2 max TB0
    Vozidlo 3 max TBS

    Výsledek vlaku = TB0
    """

    if len(seznam_vozidel) == 0:
        return "nezjištěno"

    nejvyssi_systemy_vozidel = []

    for vozidlo in seznam_vozidel:
        system = nejvyssi_system_vozidla(vozidlo)

        if system in HIERARCHIE_BLOKOVANI:
            nejvyssi_systemy_vozidel.append(system)

    if len(nejvyssi_systemy_vozidel) == 0:
        return "nezjištěno"

    nejmensi_index = min(
        HIERARCHIE_BLOKOVANI.index(system)
        for system in nejvyssi_systemy_vozidel
    )

    return HIERARCHIE_BLOKOVANI[nejmensi_index]


# ------------------------------------------------------------
# ZKOUŠKA BRZDY
# ------------------------------------------------------------

def automaticka_jzb():
    if len(seznam_vozidel) == 0:
        print("Nejdřív musíš zadat vozidla.")
        return

    misto = input("Kde byla JZB vykonána: ").strip()

    if misto == "":
        misto = info_vlaku["vychozi_stanice"]

    rezim = nacti_rezim_brzdy_vlaku()

    info_vlaku["zkouska_brzdy"] = "JZB"
    info_vlaku["misto_zkousky"] = misto
    info_vlaku["rezim_brzdy_vlaku"] = rezim

    aktualizuj_brzdici_procenta()

    vedouci = najdi_vedouci_hdv()

    if vedouci != "":
        info_vlaku["vedouci_hdv"] = vedouci

    print("\nJZB byla automaticky vytvořena.")
    print(f"Místo zkoušky: {info_vlaku['misto_zkousky']}")
    print(f"Režim brzdy vlaku: {info_vlaku['rezim_brzdy_vlaku']}")
    print(f"Potřebná brzdicí procenta: {info_vlaku['potrebna_procenta']:.2f} %")
    print(f"Skutečná brzdicí procenta: {info_vlaku['skutecna_procenta']:.2f} %")
    print(f"Chybějící brzdicí procenta: {info_vlaku['chybejici_procenta']:.2f} %")
    print(f"Rychlost po odečtení chybějících brzdicích procent: {vypocitej_rychlost_podle_brzd()} km/h")
    print(f"Vedoucí HDV: {info_vlaku['vedouci_hdv']}")


def automaticka_uzb():
    if len(seznam_vozidel) == 0:
        print("Nejdřív musíš zadat vozidla.")
        return

    misto = input("Kde byla ÚZB vykonána: ").strip()

    if misto == "":
        misto = info_vlaku["vychozi_stanice"]

    rezim = nacti_rezim_brzdy_vlaku()

    info_vlaku["zkouska_brzdy"] = "ÚZB"
    info_vlaku["misto_zkousky"] = misto
    info_vlaku["rezim_brzdy_vlaku"] = rezim

    aktualizuj_brzdici_procenta()

    vedouci = najdi_vedouci_hdv()

    if vedouci != "":
        info_vlaku["vedouci_hdv"] = vedouci

    print("\nÚZB byla automaticky vytvořena.")
    print(f"Místo zkoušky: {info_vlaku['misto_zkousky']}")
    print(f"Režim brzdy vlaku: {info_vlaku['rezim_brzdy_vlaku']}")
    print(f"Potřebná brzdicí procenta: {info_vlaku['potrebna_procenta']:.2f} %")
    print(f"Skutečná brzdicí procenta: {info_vlaku['skutecna_procenta']:.2f} %")
    print(f"Chybějící brzdicí procenta: {info_vlaku['chybejici_procenta']:.2f} %")
    print(f"Rychlost po odečtení chybějících brzdicích procent: {vypocitej_rychlost_podle_brzd()} km/h")
    print(f"Vedoucí HDV: {info_vlaku['vedouci_hdv']}")


def automaticka_zkouska_brzdy():
    print("\n=== AUTOMATICKÁ ZKOUŠKA BRZDY ===")
    print("1 - Vytvořit JZB")
    print("2 - Vytvořit ÚZB")
    print("0 - Zpět")

    volba = input("Zadejte volbu: ").strip()

    if volba == "1":
        automaticka_jzb()
    elif volba == "2":
        automaticka_uzb()
    elif volba == "0":
        return
    else:
        print("Neplatná volba.")


# ------------------------------------------------------------
# TABULKY A VÝKAZ
# ------------------------------------------------------------

def vypis_radek_souhrnu(nazev, data):
    print(
        f"{nazev:<22}"
        f"{data['pocet']:>7}"
        f"{data['hmotnost']:>12.1f}"
        f"{data['delka']:>12.2f}"
        f"{data['pocet_naprav']:>10}"
        f"{data['brzdici_vaha']:>14}"
        f"{data['kotoucove_brzdy']:>11}"
        f"{data['nekovove_spaliky']:>11}"
        f"{data['G']:>6}"
        f"{data['P']:>6}"
        f"{data['R']:>6}"
        f"{data['R+Mg']:>8}"
    )


def vypis_souhrn(vypocet):
    print("\n--- SOUHRN ---")

    print(
        f"{'Skupina':<22}"
        f"{'Počet':>7}"
        f"{'Hmotnost':>12}"
        f"{'Délka':>12}"
        f"{'Nápravy':>10}"
        f"{'Brzd. váha':>14}"
        f"{'Kotouč.':>11}"
        f"{'Špalíky':>11}"
        f"{'G':>6}"
        f"{'P':>6}"
        f"{'R':>6}"
        f"{'R+Mg':>8}"
    )

    print("-" * 125)

    vypis_radek_souhrnu("Činná HDV", vypocet["cinna_hdv"])
    vypis_radek_souhrnu("Dopravovaná HDV", vypocet["dopravovana_hdv"])
    vypis_radek_souhrnu("Vozy celkem", vypocet["vozy"])
    vypis_radek_souhrnu("Souprava celkem", vypocet["souprava"])
    vypis_radek_souhrnu("Vlak celkem", vypocet["vlak"])


def vykaz_vozidel():
    if len(seznam_vozidel) == 0:
        print("\nNejsou zadána žádná vozidla. Nejdřív použij volbu 2.")
        return

    aktualizuj_brzdici_procenta()

    vypocet = vytvor_vypocet()
    rychlost_podle_brzd = vypocitej_rychlost_podle_brzd()

    print("\n===================================================")
    print("                  VÝKAZ VOZIDEL")
    print("===================================================")

    print(f"Číslo vlaku: {info_vlaku['vlak']}")
    print(f"Datum odjezdu: {info_vlaku['datum_odjezdu']}")
    print(f"Výchozí stanice: {info_vlaku['vychozi_stanice']}")
    print(f"Konečná stanice: {info_vlaku['konecna_stanice']}")
    print(f"Poznámky: {info_vlaku['poznamky']}")

    print("\n--- SEZNAM VOZIDEL ---")

    for i, vozidlo in enumerate(seznam_vozidel, start=1):
        print(f"{i}. {vozidlo['zadane_cislo']}")

    vypis_souhrn(vypocet)

    print("\n--- VÝPOČET VLAKU ---")
    print(f"Celková délka vlaku: {vypocet['vlak']['delka']:.2f} m")
    print(f"Celkový počet náprav vlaku: {vypocet['vlak']['pocet_naprav']}")
    print(f"Celková hmotnost vlaku: {vypocet['vlak']['hmotnost']} t")
    print(f"Celková brzdicí váha: {vypocet['vlak']['brzdici_vaha']}")
    print(f"Skutečná brzdicí procenta: {info_vlaku['skutecna_procenta']:.2f} %")
    print(f"Potřebná brzdicí procenta: {info_vlaku['potrebna_procenta']:.2f} %")
    print(f"Chybějící brzdicí procenta: {info_vlaku['chybejici_procenta']:.2f} %")
    print(f"Maximální rychlost vlaku podle vozidel: {vypocet['max_rychlost']} km/h")
    print(f"Rychlost po odečtení chybějících brzdicích procent: {rychlost_podle_brzd} km/h")

    print("\n--- POZNÁMKY K VLAKU ---")
    print(vyhodnot_nbu())
    print(f"Systém blokování vlaku: {vyhodnot_system_blokovani()}")

    print("\n--- ZKOUŠKA BRZDY ---")
    print(f"Zkouška brzdy: {info_vlaku['zkouska_brzdy']}")
    print(f"Místo zkoušky: {info_vlaku['misto_zkousky']}")
    print(f"Režim brzdy vlaku: {info_vlaku['rezim_brzdy_vlaku']}")
    print(f"Číslo vedoucího HDV: {info_vlaku['vedouci_hdv']}")
    print(f"Podpis strojvedoucího: {info_vlaku['podpis_strojvedouciho']}")


# ------------------------------------------------------------
# ÚPRAVY SEZNAMU VOZIDEL
# ------------------------------------------------------------

def zobraz_zadana_vozidla():
    if len(seznam_vozidel) == 0:
        print("Zatím nejsou zadána žádná vozidla.")
        return

    print("\n--- ZADANÁ VOZIDLA ---")

    for i, vozidlo in enumerate(seznam_vozidel, start=1):
        print(f"{i}. {vozidlo['zadane_cislo']}")


def zobraz_zadana_vozidla_podrobne():
    if len(seznam_vozidel) == 0:
        print("Zatím nejsou zadána žádná vozidla.")
        return

    print("\n--- ZADANÁ VOZIDLA PODROBNĚ ---")

    for i, vozidlo in enumerate(seznam_vozidel, start=1):
        systemy = vozidlo.get("system_blokovani", [])

        if isinstance(systemy, list):
            systemy_text = ", ".join(systemy)
        else:
            systemy_text = str(systemy)

        print(
            f"{i}. {vozidlo['zadane_cislo']} | "
            f"klíč {vozidlo['klic']} | "
            f"{vozidlo['nazev']} | "
            f"{vozidlo['typ']} | "
            f"{vozidlo['stav']} | "
            f"režim {vozidlo['rezim_brzdeni']} | "
            f"brzdicí váha {vozidlo['brzdici_vaha']} | "
            f"{vozidlo['hmotnost']} t | "
            f"{vozidlo['delka']} m | "
            f"{vozidlo['pocet_naprav']} náprav | "
            f"NBU {vozidlo.get('NBU', 0)} | "
            f"systémy {systemy_text} | "
            f"nejvyšší {nejvyssi_system_vozidla(vozidlo)}"
        )


def odstran_vozidlo_podle_pozice():
    if len(seznam_vozidel) == 0:
        print("Seznam vozidel je prázdný.")
        return

    print("\n--- ODSTRANĚNÍ VOZIDLA ---")

    zobraz_zadana_vozidla()

    try:
        pozice = int(input("Zadejte pozici vozidla, které chcete odstranit: "))
    except ValueError:
        print("Musíte zadat číslo pozice.")
        return

    if pozice < 1 or pozice > len(seznam_vozidel):
        print("Neplatná pozice.")
        return

    odebrane_vozidlo = seznam_vozidel.pop(pozice - 1)
    cislo_ocistene = ocisti_cislo(odebrane_vozidlo["zadane_cislo"])

    if cislo_ocistene in zadana_cisla:
        zadana_cisla.remove(cislo_ocistene)

    aktualizuj_brzdici_procenta()

    print(f"Odstraněno vozidlo: {odebrane_vozidlo['zadane_cislo']}")


def otoc_jednotku():
    """
    Otočí úplně celý seznam vozidel.
    Tedy HDV i vozy.
    """

    if len(seznam_vozidel) == 0:
        print("Seznam vozidel je prázdný.")
        return

    seznam_vozidel.reverse()

    print("Jednotka byla otočena.")
    zobraz_zadana_vozidla()


def otoc_vlak_jen_vozy():
    """
    Otočí pouze vozy.
    HDV zůstanou na svých původních pozicích.
    """

    if len(seznam_vozidel) == 0:
        print("Seznam vozidel je prázdný.")
        return

    vozy = [v for v in seznam_vozidel if v["typ"] == "VOZ"]

    if len(vozy) == 0:
        print("Ve vlaku nejsou žádné vozy k otočení.")
        return

    vozy.reverse()

    index_vozu = 0

    for i in range(len(seznam_vozidel)):
        if seznam_vozidel[i]["typ"] == "VOZ":
            seznam_vozidel[i] = vozy[index_vozu]
            index_vozu += 1

    print("Vlak byl otočen. Otočily se pouze vozy, HDV zůstala na svých pozicích.")
    zobraz_zadana_vozidla()


def smaz_seznam_vozidel():
    seznam_vozidel.clear()
    zadana_cisla.clear()
    aktualizuj_brzdici_procenta()
    print("Seznam vozidel byl smazán.")


# ------------------------------------------------------------
# DATABÁZE - VÝPIS
# ------------------------------------------------------------

def zobraz_databazi():
    print("\n=== DATABÁZE HDV ===")

    for klic, data in DATABAZE["HDV"].items():
        print(
            f"{klic} - {data['nazev']} | "
            f"G {data.get('G', 0)} | "
            f"P {data.get('P', 0)} | "
            f"R {data.get('R', 0)} | "
            f"R+Mg {data.get('R+Mg', 0)} | "
            f"NBU {data.get('NBU', 0)} | "
            f"systémy {data.get('system_blokovani', [])}"
        )

    print("\n=== DATABÁZE VOZŮ ===")

    for klic, data in DATABAZE["VOZY"].items():
        print(
            f"{klic} - {data['nazev']} | "
            f"G {data.get('G', 0)} | "
            f"P {data.get('P', 0)} | "
            f"R {data.get('R', 0)} | "
            f"R+Mg {data.get('R+Mg', 0)} | "
            f"NBU {data.get('NBU', 0)} | "
            f"systémy {data.get('system_blokovani', [])}"
        )


# ------------------------------------------------------------
# MENU
# ------------------------------------------------------------

def menu():
    while True:
        print("\n===================================================")
        print(" MENU")
        print("===================================================")
        print("1 - Vložit data o vlaku")
        print("2 - Přidat vozidlo")
        print("3 - Vypsat výkaz vozidel a výpočet vlaku")
        print("4 - Odstranit vozidlo podle pozice")
        print("5 - Otočit jednotku")
        print("6 - Otočit vlak")
        print("7 - Zobrazit zadaná vozidla")
        print("8 - Zobrazit zadaná vozidla podrobně")
        print("9 - Zobrazit databázi")
        print("10 - Smazat seznam vozidel")
        print("11 - Automaticky vytvořit JZB / ÚZB")
        print("0 - Konec")

        volba = input("Zadejte volbu: ").strip()

        if volba == "1":
            vloz_data_vlaku()

        elif volba == "2":
            pridej_vozidlo()

        elif volba == "3":
            vykaz_vozidel()

        elif volba == "4":
            odstran_vozidlo_podle_pozice()

        elif volba == "5":
            otoc_jednotku()

        elif volba == "6":
            otoc_vlak_jen_vozy()

        elif volba == "7":
            zobraz_zadana_vozidla()

        elif volba == "8":
            zobraz_zadana_vozidla_podrobne()

        elif volba == "9":
            zobraz_databazi()

        elif volba == "10":
            smaz_seznam_vozidel()

        elif volba == "11":
            automaticka_zkouska_brzdy()

        elif volba == "0":
            print("Program ukončen.")
            break

        else:
            print("Neplatná volba.")


def main():
    menu()


if __name__ == "__main__":
    main()
