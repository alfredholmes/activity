---
name: {{ name }}
start_time: {{ start_time }}
{% if tags %}      
tags:
{% for tag in tags%}
  - {{ tag }}
{% endfor %}
{% endif %}
---

# {{ name }}
