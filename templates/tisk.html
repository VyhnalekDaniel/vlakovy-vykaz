{% extends "base.html" %}
{% block title %}Tisk{% endblock %}
{% block content %}
<div class="card printcard">
  <h1>Výkaz vozidel a zpráva o brzdění</h1>
  <p><strong>Vlak:</strong> {{ doc.vlak.druh }} {{ doc.vlak.cislo }} | {{ doc.vlak.vychozi_stanice }} → {{ doc.vlak.konecna_stanice }}</p>
  <p><strong>Datum:</strong> {{ doc.vlak.datum }} <strong>Odjezd:</strong> {{ doc.vlak.odjezd }}</p>
  <p><strong>Sepsal:</strong> {{ doc.vlak.sepsal }} | <strong>Sepsáno v:</strong> {{ doc.vlak.sepsano_v }}</p>
  <h2>Vozidla</h2>
  <ol>{% for v in vozidla %}<li>{{ v.zadane_cislo }} | {{ v.nazev }} | {{ v.stav }} | {{ v.rezim_brzdeni }} | brz. váha {{ v.brzdici_vaha }}</li>{% endfor %}</ol>
  <h2>Souhrn</h2>
  <p>Hmotnost {{ '%.1f'|format(vypocet.vlak.hmotnost) }} t, délka {{ '%.2f'|format(vypocet.vlak.delka) }} m, nápravy {{ vypocet.vlak.pocet_naprav }}, brzdicí váha {{ vypocet.vlak.brzdici_vaha }}</p>
  <p>Skutečná % {{ '%.2f'|format(vypocet.skutecna_procenta) }}, potřebná % {{ '%.2f'|format(vypocet.potrebna_procenta) }}, chybějící % {{ '%.2f'|format(vypocet.chybejici_procenta) }}</p>
  <p>Rychlost: {{ vypocet.rychlost_podle_brzd }} km/h | {{ vypocet.nbu }} | blokování {{ vypocet.system_blokovani }}</p>
  <h2>JZB / ÚZB</h2>
  <p>JZB: {{ doc.jzb.vykonana }} | {{ doc.jzb.kde }} | {{ doc.jzb.kdy }} | {{ doc.jzb.kym }} {{ doc.jzb.kym_jiny }}</p>
  <p>ÚZB: {{ doc.uzb.vykonana }} | {{ doc.uzb.kde }} | {{ doc.uzb.kdy }} | {{ doc.uzb.kym }} {{ doc.uzb.kym_jiny }}</p>
</div>
<div class="buttons no-print"><button class="btn" onclick="window.print()">Tisk / uložit jako PDF</button><a class="btn secondary" href="{{ url_for('rekapitulace') }}">Zpět</a></div>
{% endblock %}
