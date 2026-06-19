{% extends "base.html" %}
{% block content %}
<section class="hero compact">
  <h1>Změna čísla vlaku</h1>
  <p>Už máš ve výkazu zadaná vozidla. Rozhodni, jestli je chceš u nového vlaku ponechat.</p>
</section>

<section class="panel warning-panel">
  <h2>Chceš ponechat vozidla ve výkazu?</h2>
  <div class="grid two">
    <div class="kv"><span>Původní vlak</span><strong>{{ stare_info.vlak or 'nezadán' }}</strong></div>
    <div class="kv"><span>Nový vlak</span><strong>{{ nove_info.vlak or 'nezadán' }}</strong></div>
    <div class="kv"><span>Počet vozidel ve výkazu</span><strong>{{ pocet }}</strong></div>
    <div class="kv"><span>Nová trasa</span><strong>{{ nove_info.vychozi_stanice or '?' }} → {{ nove_info.konecna_stanice or '?' }}</strong></div>
  </div>

  <form method="post" class="choice-buttons">
    <button class="primary" name="ponechat_vozidla" value="ANO">Ano, ponechat vozidla</button>
    <button class="danger" name="ponechat_vozidla" value="NE">Ne, vymazat výkaz vozidel</button>
  </form>
</section>
{% endblock %}
