{% extends "base.html" %}
{% block title %}Databáze{% endblock %}
{% block content %}
<div class="card"><h1>Databáze</h1><p class="muted">Výpočetní databáze vozidel, databáze vlaků a tahák čísel.</p></div>
<div class="card"><h2>Databáze vlaků</h2>{% for cislo, v in vlaky.items() %}<p>{{ cislo }} - {{ v.druh }} | {{ v.vychozi_stanice }} → {{ v.konecna_stanice }}</p>{% else %}<p>Databáze vlaků je zatím prázdná.</p>{% endfor %}</div>
<div class="card"><h2>Tahák čísel vozidel</h2>{% for rada, cisla in tahak.items() %}<h3>{{ rada }}</h3><ul>{% for c in cisla %}<li>{{ c }}</li>{% endfor %}</ul>{% endfor %}</div>
<div class="card"><h2>Výpočetní databáze vozidel</h2>{% for typ, cast in databaze.items() %}<h3>{{ typ }}</h3>{% for klic, v in cast.items() %}<p><strong>{{ klic }}</strong> - {{ v.nazev }} | G {{ v.G }} | P {{ v.P }} | R {{ v.R }} | R+Mg {{ v['R+Mg'] }}</p>{% endfor %}{% endfor %}</div>
{% endblock %}
