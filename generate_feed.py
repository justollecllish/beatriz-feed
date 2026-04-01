import requests
import re
from datetime import datetime

url = "https://qoshe.com/yazar/beatriz-mej-a-mori/700683"
headers = {"User-Agent": "Mozilla/5.0"}

response = requests.get(url, headers=headers)
html = response.text

pattern = r'(beatriz-mej[^"]+)"[^>]*>\s*<h1[^>]*>([^<]+)</h1>.*?<i[^>]*>(\d{2}\.\d{2}\.\d{4})</i>'
matches = re.findall(pattern, html, re.DOTALL)

rss = '''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>
<title>Beatriz Mejía Mori - Expreso</title>
<link>https://www.expreso.com.pe/columnista/beatriz-mejia-mori/</link>
<description>Últimas columnas de Beatriz Mejía Mori</description>
'''

for slug, titulo, fecha in matches[:10]:
    url_art = f"https://qoshe.com/{slug}"
    d, m, y = fecha.split(".")
    rss += f'''<item>
<title>{titulo}</title>
<link>{url_art}</link>
<guid>{url_art}</guid>
<pubDate>{d} {m} {y} 00:00:00 +0000</pubDate>
</item>
'''

rss += '</channel></rss>'

with open("feed.xml", "w", encoding="utf-8") as f:
    f.write(rss)

print(f"Feed generado con {len(matches)} artículos")
