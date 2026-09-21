"""Read-only HTML/asset audit; standard library only."""
import csv
import json
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit

ROOT = Path(__file__).resolve().parents[1]


class Page(HTMLParser):
    def __init__(self, html):
        super().__init__(convert_charrefs=True)
        self.title = ''
        self.headings = []
        self.meta = {}
        self.links = []
        self.images = []
        self.videos = []
        self.canonical = ''
        self.text = []
        self.active = None
        self.skip = 0
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ('script', 'style'): self.skip += 1
        if tag == 'title' or tag in ('h1', 'h2', 'h3'):
            self.active = [tag, '']
        if tag == 'meta': self.meta[a.get('name', a.get('property', ''))] = a.get('content', '')
        if tag == 'link' and a.get('rel') == 'canonical': self.canonical = a.get('href', '')
        if tag == 'a' and a.get('href'): self.links.append(a['href'])
        if tag == 'img': self.images.append(a)
        if tag == 'video':
            self.videos.append(a)
            if a.get('poster'): self.images.append({'src': a['poster'], 'role': 'poster'})
        if a.get('data-preview'): self.images.append({'src': a['data-preview'], 'role': 'hover-preview'})

    def handle_endtag(self, tag):
        if tag in ('script', 'style'): self.skip = max(0, self.skip-1)
        if self.active and self.active[0] == tag:
            if tag == 'title': self.title = self.active[1].strip()
            else: self.headings.append(self.active)
            self.active = None

    def handle_data(self, text):
        if self.active: self.active[1] += text
        if not self.skip and text.strip(): self.text.append(text.strip())


def local_audit(label):
    out = ROOT / 'docs' / 'audit'
    out.mkdir(parents=True, exist_ok=True)
    rows, assets = [], []
    for path in sorted(ROOT.rglob('*.html')):
        if any(p.startswith('.') for p in path.relative_to(ROOT).parts): continue
        page = Page(path.read_text())
        route = '/' + path.relative_to(ROOT).as_posix().removesuffix('index.html')
        rows.append({'url': route, 'title': page.title, 'description': page.meta.get('description',''),
                     'h1': ' | '.join(t for h,t in page.headings if h == 'h1'),
                     'h1_count': sum(h == 'h1' for h,t in page.headings), 'canonical': page.canonical,
                     'robots': page.meta.get('robots',''), 'images': len(page.images), 'videos': len(page.videos)})
        for img in page.images:
            assets.append({'image': urljoin(route, img.get('src','')), 'page': route,
                           'role': img.get('role','img'), 'alt': img.get('alt','')})
    for name, data in [('pages',rows),('assets',assets)]:
        with (out/f'{label}-{name}.csv').open('w') as f:
            w=csv.DictWriter(f,fieldnames=list(data[0]));w.writeheader();w.writerows(data)
    summary = {'pages':len(rows), 'images':dict(Counter(a['image'] for a in assets)),
               'without_canonical':sum(not p['canonical'] for p in rows),
               'h1_errors':sum(p['h1_count'] != 1 for p in rows)}
    (out/f'{label}-summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(summary,ensure_ascii=False,indent=2))


if __name__ == '__main__':
    import sys
    local_audit(sys.argv[1] if len(sys.argv)>1 else 'current')
