"""Bounded, read-only crawl of the original site. Never changes production."""
import csv
import hashlib
import json
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from urllib.parse import urljoin, urlsplit
from audit import ROOT, Page

BASE = 'https://remontiryemchasi.ru/'
OUT = ROOT/'docs'/'audit'
OUT.mkdir(parents=True, exist_ok=True)
STAMP = datetime.now(timezone.utc).isoformat()


def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'WatchMigrationAudit/1.0'})
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            return r.status, r.url, r.read().decode('utf-8', errors='replace')
    except urllib.error.HTTPError as e:
        return e.code, e.url, e.read().decode('utf-8',errors='replace')
    except Exception as e:
        return 0, url, str(e)


queue = [urljoin(BASE,'sitemap_index.xml')]
urls, maps = set(), []
while queue and len(maps) < 12:
    url = queue.pop(0)
    status, final, body = fetch(url)
    maps.append({'url': url, 'status': status, 'final_url': final})
    if status != 200: continue
    root=ET.fromstring(body)
    # Image sitemap entries use a different namespace and are not HTML pages.
    entries=[e.text for e in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
    if root.tag.endswith('sitemapindex'):
        queue.extend(u for u in entries if urlsplit(u).netloc == urlsplit(BASE).netloc)
    else: urls.update(entries)

rows=[]
for url in sorted(urls)[:200]:
    if urlsplit(url).netloc != urlsplit(BASE).netloc: continue
    status, final, body = fetch(url)
    page=Page(body)
    row={'url':url,'status':status,'final_url':final,'title':page.title,
         'description':page.meta.get('description',''),'h1':[t for h,t in page.headings if h=='h1'],
         'headings':page.headings,'canonical':page.canonical,'robots':page.meta.get('robots',''),
         'links':sorted(set(urljoin(final,u) for u in page.links)),
         'text': '\n'.join(page.text), 'sha256':hashlib.sha256(body.encode()).hexdigest()}
    rows.append(row)
    print(f'{len(rows)}/{len(urls)} {status} {url}',flush=True)
    time.sleep(.15)

(OUT/'legacy-content.json').write_text(json.dumps({'checked_at':STAMP,'sitemaps':maps,'discovered_urls':len(urls),'pages':rows},ensure_ascii=False,indent=2)+'\n')
with (OUT/'legacy-pages.csv').open('w') as f:
    keys=['url','status','final_url','title','description','h1','canonical','robots']
    w=csv.DictWriter(f,fieldnames=keys);w.writeheader()
    for r in rows: w.writerow({k:' | '.join(r[k]) if isinstance(r[k],list) else r[k] for k in keys})
print('Saved',len(rows),'pages',flush=True)
