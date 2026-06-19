{% extends "base.html" %}
{% block content %}
{% if tisk %}<script>window.addEventListener('load', () => setTimeout(() => window.print(), 300));</script>{% endif %}
<section class="hero print-title">
  <h1>Rekapitulace vlakové dokumentace</h1>
  <p><strong>{{ data.info.vlak }}</strong> — {{ data.info.vychozi_stanice }} → {{ data.info.konecna_stanice }}</p>
</section>

<section class="panel">
  <h2>Záhlaví</h2>
  <div class="grid two">
    <div class="kv"><span>Vlak</span><strong>{{ data.info.vlak }}</strong></div>
    <div class="kv"><span>Odjezd</span><strong>{{ data.info.datum_odjezdu }} {{ data.info.cas_odjezdu }}</strong></div>
    <div class="kv"><span>Sepsáno v</span><strong>{{ data.info.sepsano_v }}</strong></div>
    <div class="kv"><span>Sepsal</span><strong>{{ data.info.sepsal }}</strong></div>
  </div>
</section>

<section class="panel table-wrap">
  <h2>Vozidla</h2>
  <table>
    <thead><tr><th>#</th><th>Číslo</th><th>Název</th><th>Stav</th><th>Režim</th><th>Brzd. váha</th></tr></thead>
    <tbody>{% for v in data.vozidla %}<tr><td>{{ loop.index }}</td><td>{{ v.zadane_cislo }}</td><td>{{ v.nazev }}</td><td>{{ v.stav }}</td><td>{{ v.rezim_brzdeni }}</td><td>{{ v.brzdici_vaha }}</td></tr>{% endfor %}</tbody>
  </table>
</section>

<section class="panel">
  <h2>Zpráva o brzdění</h2>
  <div class="grid two">
    <div class="kv"><span>Režim brzdy vlaku</span><strong>{{ data.info.rezim_brzdy_vlaku }}</strong></div>
    <div class="kv"><span>Doprovod</span><strong>{{ data.info.doprovod }}</strong></div>
    <div class="kv"><span>Potřebná brzdicí procenta</span><strong>{{ '%.2f'|format(data.info.potrebna_procenta) }} %</strong></div>
    <div class="kv"><span>Skutečná brzdicí procenta</span><strong>{{ '%.2f'|format(data.info.skutecna_procenta) }} %</strong></div>
    <div class="kv"><span>Chybějící brzdicí procenta</span><strong>{{ '%.2f'|format(data.info.chybejici_procenta) }} %</strong></div>
    <div class="kv"><span>Rychlost podle brzd</span><strong>{{ data.rychlost_podle_brzd }} km/h</strong></div>
    <div class="kv"><span>NBU</span><strong>{{ data.nbu }}</strong></div>
    <div class="kv"><span>Systém blokování</span><strong>{{ data.system_blokovani }}</strong></div>
  </div>
  {% if data.info.poznamky_zob_vyber or data.info.poznamky_zob %}
  <h3>Poznámky ke zprávě o brzdění</h3>
  {% if data.info.poznamky_zob_vyber %}
  <ul>
    {% for p in data.info.poznamky_zob_vyber %}<li>{{ p }}</li>{% endfor %}
  </ul>
  {% endif %}
  {% if data.info.poznamky_zob %}<p>{{ data.info.poznamky_zob }}</p>{% endif %}
  {% endif %}
</section>

<section class="panel">
  <h2>JZB / ÚZB</h2>
  <div class="grid two">
    <div class="kv"><span>JZB</span><strong>{{ data.info.jzb_vykonana }}</strong></div>
    <div class="kv"><span>JZB kde/kdy/kým</span><strong>{{ data.info.jzb_kde }} {{ data.info.jzb_kdy }} {{ data.info.jzb_kym }}</strong></div>
    <div class="kv"><span>ÚZB</span><strong>{{ data.info.uzb_vykonana }}</strong></div>
    <div class="kv"><span>ÚZB kde/kdy/kým</span><strong>{{ data.info.uzb_kde }} {{ data.info.uzb_kdy }} {{ data.info.uzb_kym }}</strong></div>
  </div>
</section>

{% if not tisk %}
<section class="panel no-print">
  <h2>Další krok</h2>
  <div class="menu-grid small-grid">
    <a class="menu-card" href="{{ url_for('tisk') }}"><span>PDF</span>Vytisknout / uložit jako PDF</a>
    <a class="menu-card" href="{{ url_for('zob') }}"><span>←</span>Upravit ZOB</a>
    <a class="menu-card" href="{{ url_for('vykaz_vozidel') }}"><span>VV</span>Zpět do výkazu vozidel</a>
    <a class="menu-card" href="{{ url_for('menu') }}"><span>🏠</span>Zpět do hlavního menu</a>
  </div>
</section>
{% endif %}
{% endblock %}
