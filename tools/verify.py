"""Verify generated routes, metadata, local links and video delivery contracts."""
import json
import re
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET
from audit import ROOT, Page

errors, titles, descriptions, video_sources = [], [], [], set()
config=json.loads((ROOT/'data/site.json').read_text())


class Assets(HTMLParser):
    def __init__(self, path, html):
        super().__init__()
        self.path=path
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        for key in ('src','href','poster','data-src'):
            url=a.get(key,'')
            parsed=urlsplit(url)
            if not url or parsed.scheme or parsed.netloc or url.startswith('#'): continue
            target = (ROOT/parsed.path.lstrip('/') if parsed.path.startswith('/') else self.path.parent/unquote(parsed.path)).resolve()
            if not target.is_relative_to(ROOT): errors.append(f'{self.path}: path escapes site: {url}')
            elif not target.exists(): errors.append(f'{self.path}: missing {url}')
        if tag == 'video':
            if 'autoplay' in a or a.get('preload') != 'none' or not all(k in a for k in ('muted','playsinline','poster','data-lazy-video')):
                errors.append(f'{self.path}: invalid video policy')
            if 'src' in a or not a.get('data-src'): errors.append(f'{self.path}: eager video source')
            video_sources.add(Path(a.get('data-src','')).name)
        if tag == 'source' and a.get('type')=='video/mp4':
            if 'src' in a or not a.get('data-src'): errors.append(f'{self.path}: eager video source')
            video_sources.add(Path(a.get('data-src','')).name)
        if tag == 'img' and not urlsplit(a.get('src','')).netloc \
                and not all(k in a for k in ('alt','width','height','loading')):
            # внешние пиксели счётчиков размеров не имеют — правило про сдвиг вёрстки
            # касается только картинок самого сайта
            errors.append(f'{self.path}: missing image attributes')


pages=sorted(ROOT.rglob('*.html'))
for path in pages:
    html=path.read_text(); page=Page(html)
    route='/' + path.relative_to(ROOT).as_posix().removesuffix('index.html')
    titles.append(page.title); descriptions.append(page.meta.get('description',''))
    if len([h for h,t in page.headings if h=='h1']) != 1: errors.append(f'{route}: expected one H1')
    if page.canonical != config['production_origin']+route: errors.append(f'{route}: wrong canonical')
    for key in ('description','og:title','og:description','og:url','twitter:card','robots'):
        if not page.meta.get(key): errors.append(f'{route}: missing {key}')
    if config['environment']=='preview' and page.meta.get('robots')!='noindex,follow': errors.append(f'{route}: indexable preview')
    for data in re.findall(r'<script type="application/ld\+json">(.*?)</script>',html):
        try: json.loads(data)
        except ValueError: errors.append(f'{route}: invalid JSON-LD')
    Assets(path,html)
for label,values in [('title',titles),('description',descriptions)]:
    if any(v>1 for v in Counter(values).values()): errors.append(f'Duplicate {label}')
if video_sources != {p.name for p in (ROOT/'assets/videos').glob('*.mp4')}: errors.append('Not all video files referenced')
sitemap=ET.parse(ROOT/'sitemap.xml')
locations=[x.text for x in sitemap.iter() if x.tag.endswith('}loc')]
# indexable_routes может быть списком маршрутов или строкой 'all' — открыт весь сайт
_allowed=config['indexable_routes']
if config['environment']!='production':
    expected=[]
elif _allowed=='all':
    expected=[config['production_origin']+'/'+x.relative_to(ROOT).as_posix().removesuffix('index.html') for x in pages]
else:
    expected=[config['production_origin']+r for r in _allowed]
if sorted(locations)!=sorted(expected): errors.append('Sitemap contains unapproved routes')
if errors: raise SystemExit('\n'.join(errors))
print(f'PASS: {len(pages)} pages, {len(video_sources)} videos; metadata, links, images, schema and indexation policy')
