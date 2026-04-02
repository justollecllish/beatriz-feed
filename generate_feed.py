import requests
import re
import xml.etree.ElementTree as ET

# ---- BEATRIZ MEJÍA MORI (qoshe) ----
def get_beatriz():
    url = "https://qoshe.com/yazar/beatriz-mej-a-mori/700683"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    html = response.text
    pattern = r'(beatriz-mej[^"]+)"[^>]*>\s*<h1[^>]*>([^<]+)</h1>.*?<i[^>]*>(\d{2}\.\d{2}\.\d{4})</i>'
    matches = re.findall(pattern, html, re.DOTALL)
    items = []
    for slug, titulo, fecha in matches[:10]:
        d, m, y = fecha.split(".")
        items.append({
            'titulo': titulo,
            'url': f"https://qoshe.com/{slug}",
            'fecha': f"{d} {m} {y} 00:00:00 +0000",
            'autor': 'Beatriz Mejía Mori'
        })
    return items

# ---- ALDO MARIÁTEGUI (lampadia) ----
def get_aldo():
    url = "https://lampadia.com/feed"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    root = ET.fromstring(response.content)
    channel = root.find('channel')
    items = []
    for item in channel.findall('item'):
        title = item.findtext('title', '')
        link = item.findtext('link', '')
        pub_date = item.findtext('pubDate', '')
        # Solo artículos de Aldo
        creator = item.findtext('{http://purl.org/dc/elements/1.1/}creator', '')
        if 'Mariátegui' in creator or 'Mariateg' in link or 'aldo' in link.lower():
            items.append({
                'titulo': title,
                'url': link,
                'fecha': pub_date,
                'autor': 'Aldo Mariátegui'
            })
    return items[:10]

# ---- GENERAR RSS COMBINADO ----
beatriz = get_beatriz()
aldo = get_aldo()
todos = beatriz + aldo

rss = '''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>
<title>Opinión Perú - Beatriz Mejía & Aldo Mariátegui</title>
<link>https://justollecllish.github.io/beatriz-feed/</link>
<description>Columnas de opinión seleccionadas</description>
'''

for a in todos:
    titulo = a['titulo'].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    rss += f'''<item>
<title>[{a["autor"]}] {titulo}</title>
<link>{a['url']}</link>
<guid>{a['url']}</guid>
<pubDate>{a['fecha']}</pubDate>
</item>
'''

rss += '</channel></rss>'

with open("feed.xml", "w", encoding="utf-8") as f:
    f.write(rss)

print(f"Feed generado: {len(beatriz)} Beatriz + {len(aldo)} Aldo = {len(todos)} total")
