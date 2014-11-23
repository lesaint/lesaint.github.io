---
layout: page
title:  All tips
image:
 feature: feature_image_green.png
---

{% capture tips_tags %}{% for post in site.categories.tips %}{{ post.tags.first }}{% unless forloop.last %},{% endunless %}{% endfor %}{% endcapture %}
{% assign tags_list = tips_tags | split:',' | sort %}

{% assign result = tags_list[1] %}
{% for item in tags_list %}
    {% unless result contains item %}
        {% capture result %}{{ result }},{{ item }}{% endcapture %}
    {% endunless %}
{% endfor %}

{% assign tags_set = result | split:',' | sort %}

<span class="entry-tags">{% for tag in tags_set %}<a href="{{ site.url }}/tips/#{{ tag }}" title="Tips for {{ tag }}">{{ tag }}</a>{% unless forloop.last %}&nbsp;&bull;&nbsp;{% endunless %}{% endfor %}</span>
{: .center}

{% for tag in tags_set %}
  <h2 id="{{ tag }}">{{ tag }}</h2>
  <ul class="post-list">
    {% for post in site.tags[tag]%}{% if post.categories.first == 'tips' %}{% if post.title != null %}<li><a href="{{ site.url }}{{ post.url }}">{{ post.title }}<span class="entry-date"><time datetime="{{ post.date | date_to_xmlschema }}">{{ post.date | date: "%B %d, %Y" }}</time></span></a></li>{% endif %}{% endif %}{% endfor %}
  </ul>
{% endfor %}
