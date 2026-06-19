{% extends "base.html" %}
{% block content %}
<h1>{{ typ }}</h1>
<form method="post" class="panel form">
  <label>Byla {{ typ }} vykonána?
    <select name="vykonana">
      <option value="NE" {% if info[prefix + '_vykonana'] != 'ANO' %}selected{% endif %}>NE</option>
      <option value="ANO" {% if info[prefix + '_vykonana'] == 'ANO' %}selected{% endif %}>ANO</option>
    </select>
  </label>
  <label>Kde byla vykonána<input name="kde" value="{{ info[prefix + '_kde'] or info.vychozi_stanice }}"></label>
  <label>Kdy byla vykonána<input type="datetime-local" name="kdy" value="{{ info[prefix + '_kdy'] }}"></label>
  <label>Kým byla vykonána<input name="kym" value="{{ info[prefix + '_kym'] }}"></label>
  <label>Poznámka<textarea name="poznamka">{{ info[prefix + '_poznamka'] }}</textarea></label>
  <button class="primary">Uložit {{ typ }}</button>
</form>
{% endblock %}
