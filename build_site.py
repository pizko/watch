from pathlib import Path
from html import escape
import json
import re

ROOT = Path(__file__).parent
CONFIG = json.loads((ROOT / 'data/site.json').read_text())
PAGES = []
CONTACTS = CONFIG['contacts']
PHONE = CONTACTS['phone']
PHONE_HREF = 'tel:+' + CONTACTS['phone_href'].lstrip('+')
ADDRESS = CONTACTS['address']
ADDRESS_TEXT = f"{ADDRESS['street']}, {ADDRESS['locality']}"
HOURS_TEXT = CONTACTS['hours_text']
IMAGE_SIZES = {'hero-poster.webp': (1600, 900), 'watchmaker.webp': (1000, 1000),
               'detail-01.webp': (900, 1126), 'detail-02.webp': (900, 1126),
               'detail-03.webp': (900, 1126)}


def image_attributes(match):
    tag = match.group(0)
    src = re.search(r'src="([^"]+)"', tag).group(1)
    width, height = IMAGE_SIZES[Path(src).name]
    loading = 'eager' if 'hero-poster' in src else 'lazy'
    return tag[:-1] + f' width="{width}" height="{height}" loading="{loading}" decoding="async">'

services = [
    ('full-service','Полное обслуживание механизма','Разборка, очистка, смазка, сборка, регулировка и контроль работы механизма.','ОБСЛУЖИВАНИЕ МЕХАНИЗМА'),
    ('movement-repair','Ремонт механизма','Диагностика неисправности и восстановление узлов механических и кварцевых часов.','РЕМОНТ КАЛИБРА'),
    ('polishing','Полировка и восстановление корпуса','Работа с полированными и сатинированными поверхностями корпуса и браслета.','КОРПУС И ОТДЕЛКА'),
    ('glass-replacement','Замена стекла','Подбор и замена стекла с последующей проверкой посадки и состояния корпуса.','СТЕКЛО'),
    ('water-resistance','Проверка герметичности','Контроль герметичности после вмешательства и перед повседневной эксплуатацией.','ГЕРМЕТИЧНОСТЬ'),
    ('automatic-winding','Ремонт автоподзавода','Диагностика ротора и узлов автоматического подзавода.','АВТОПОДЗАВОД'),
    ('chronograph','Хронографы и сложные механизмы','Работы со сложными калибрами требуют предварительной диагностики и согласования.','СЛОЖНЫЕ МЕХАНИЗМЫ'),
    ('restoration','Реставрация','Деликатное восстановление корпуса, элементов внешнего оформления и отдельных узлов.','РЕСТАВРАЦИЯ'),
]

brands = [
    ('rolex','Rolex'),('patek-philippe','Patek Philippe'),('audemars-piguet','Audemars Piguet'),('vacheron-constantin','Vacheron Constantin'),
    ('breguet','Breguet'),('jaeger-lecoultre','Jaeger-LeCoultre'),('a-lange-soehne','A. Lange & Söhne'),('omega','Omega'),
    ('cartier','Cartier'),('blancpain','Blancpain'),('iwc','IWC Schaffhausen'),('zenith','Zenith'),('ulysse-nardin','Ulysse Nardin'),
    ('girard-perregaux','Girard-Perregaux'),('hublot','Hublot'),('panerai','Panerai'),('chopard','Chopard'),('piaget','Piaget'),
    ('franck-muller','Franck Muller'),('parmigiani','Parmigiani Fleurier'),('h-moser','H. Moser & Cie.'),('breitling','Breitling'),
    ('tag-heuer','TAG Heuer'),('tudor','Tudor'),('grand-seiko','Grand Seiko'),('longines','Longines'),('rado','Rado'),
    ('tissot','Tissot'),('maurice-lacroix','Maurice Lacroix'),('frederique-constant','Frederique Constant'),('oris','Oris')
]

faqs = [
    ('Сколько занимает диагностика?','Срок зависит от модели и характера неисправности. После первичного осмотра мастер сообщает, нужна ли углублённая диагностика и когда можно согласовать работы.'),
    ('Стоимость известна заранее?','До начала основных работ согласуются перечень вмешательств и стоимость. Если в процессе обнаруживается дополнительная неисправность, её не следует устранять без отдельного согласования.'),
    ('Можно ли обслуживать дорогие часы без официального сервиса?','Независимая мастерская не является официальным сервисным центром брендов. Возможность конкретной работы зависит от модели, состояния часов, доступности компонентов и требований владельца.'),
    ('Что происходит после ремонта?','После сборки проверяются работа механизма и те параметры, которые относятся к выполненной услуге. Для работ, затрагивающих корпус, может потребоваться дополнительный контроль герметичности.'),
    ('Нужно ли записываться заранее?','Для часов высокого класса предварительная запись удобнее: можно заранее описать модель и задачу, а мастерская подготовится к осмотру.'),
]


# ── Schema.org ─────────────────────────────────────────────────────────────
# Размечаем только то, что подтверждено: организация, адрес, телефон, график,
# услуги и вопросы-ответы. Ни цен, ни рейтингов, ни отзывов — таких данных нет.
ORIGIN = CONFIG['production_origin'].rstrip('/')
BIZ_ID = ORIGIN + '/#atelier'


def business_node():
    return {
        '@type': 'LocalBusiness',
        '@id': BIZ_ID,
        'name': 'Atelier 01 — независимая часовая мастерская',
        'description': 'Диагностика, обслуживание и восстановление швейцарских часов в Москве.',
        'url': ORIGIN + '/',
        'telephone': CONTACTS['phone'],
        'email': CONTACTS['email'],
        'image': ORIGIN + '/assets/images/hero-poster.webp',
        'address': {
            '@type': 'PostalAddress',
            'streetAddress': ADDRESS['street'],
            'addressLocality': ADDRESS['locality'],
            'postalCode': ADDRESS['postal_code'],
            'addressCountry': ADDRESS['country'],
        },
        'areaServed': {'@type': 'City', 'name': 'Москва'},
        'openingHoursSpecification': [
            {'@type': 'OpeningHoursSpecification', 'dayOfWeek': h['days'],
             'opens': h['opens'], 'closes': h['closes']} for h in CONTACTS['hours']
        ],
        'knowsAbout': [name for _, name, _, _ in services],
    }


def crumbs_node(canonical, trail):
    """trail — список (имя, маршрут); главная добавляется сама."""
    items = [('Главная', '/')] + list(trail)
    return {
        '@type': 'BreadcrumbList',
        'itemListElement': [
            {'@type': 'ListItem', 'position': i + 1, 'name': name, 'item': ORIGIN + route}
            for i, (name, route) in enumerate(items)
        ],
    }


def rel_prefix(depth:int):
    return '../' * depth

def header(prefix=''):
    return f'''<header class="site-header">
  <div class="header-inner">
    <a class="brand" href="{prefix or './'}" aria-label="На главную">
      <span class="brand-main">Atelier 01</span><span class="brand-sub">Часовая мастерская · Москва</span>
    </a>
    <nav class="main-nav" aria-label="Основная навигация">
      <a href="{prefix}services/">Услуги</a><a href="{prefix}brands/">Бренды</a><a href="{prefix}atelier/">Мастерская</a><a href="{prefix}prices/">Цены</a><a href="{prefix}contacts/">Контакты</a>
    </nav>
    <div class="header-actions"><a class="header-phone" href="{PHONE_HREF}">{PHONE}</a><a class="header-book" href="{prefix}contacts/">Записаться</a><button class="menu-toggle" aria-label="Меню" aria-expanded="false"><span></span><span></span></button></div>
  </div>
</header>
<div class="mobile-menu"><nav><a href="{prefix}services/">Услуги</a><a href="{prefix}brands/">Бренды</a><a href="{prefix}atelier/">Мастерская</a><a href="{prefix}prices/">Цены</a><a href="{prefix}contacts/">Контакты</a></nav><div class="mobile-menu-meta"><a href="{PHONE_HREF}">{PHONE}</a><span>Петровка · Москва</span></div></div>'''

def footer(prefix=''):
    FOOTER_BRANDS = ''.join(
        f'<a href="{prefix}brands/{slug}/">{escape(name)}</a>' for slug, name in brands)
    return f'''<footer class="site-footer"><div class="container"><div class="footer-grid"><div class="footer-brand">ЧАСОВАЯ<br>МАСТЕРСКАЯ</div><nav class="footer-nav"><a href="{prefix}services/">Услуги</a><a href="{prefix}brands/">Бренды</a><a href="{prefix}prices/">Цены</a><a href="{prefix}atelier/">Мастерская</a><a href="{prefix}contacts/">Контакты</a></nav><div class="footer-meta"><a href="{PHONE_HREF}">{PHONE}</a><a href="{prefix}contacts/">{ADDRESS_TEXT}</a><span>{HOURS_TEXT}</span></div></div>
<div class="footer-brands"><span class="footer-brands-title">Марки часов</span><div class="footer-brands-list">{FOOTER_BRANDS}</div></div><div class="footer-bottom"><span>© <span data-year></span> Независимая часовая мастерская</span><span>Независимая мастерская. Не является официальным сервисным центром и не аффилирована с указанными производителями.</span></div></div></footer><a class="call-fab" href="{PHONE_HREF}" aria-label="Позвонить {PHONE}"><span>Позвонить</span></a><div class="toast"></div>'''

def doc(title, description, body, depth=0, route='/', trail=None, schema_extra=None):
    prefix = rel_prefix(depth)
    canonical = CONFIG['production_origin'].rstrip('/') + route
    allowed = CONFIG['indexable_routes']
    indexable = CONFIG['environment'] == 'production' and (allowed == 'all' or route in allowed)
    robots = 'index,follow' if indexable else 'noindex,follow'
    PAGES.append((route, indexable))
    body = body.replace('<video autoplay muted loop playsinline', '<video data-lazy-video muted loop playsinline preload="none"')
    body = re.sub(r'<source src="([^"]+\.mp4)"', r'<source data-src="\1"', body)
    body = re.sub(r'<video([^>]+)><source data-src="([^"]+)" type="video/mp4"></video>',
                  r'<video\1 aria-hidden="true" data-src="\2"></video>', body)
    body = re.sub(r'<img\s[^>]+>', image_attributes, body)
    page_node = {'@type': 'WebPage', '@id': canonical, 'url': canonical,
                 'name': title, 'description': description, 'inLanguage': 'ru',
                 'isPartOf': {'@id': ORIGIN + '/#website'},
                 'about': {'@id': BIZ_ID}}
    graph = [page_node]
    if trail:
        graph.append(crumbs_node(canonical, trail))
    graph.extend(schema_extra or [])
    if route == '/':
        graph.append(business_node())
        graph.append({'@type': 'WebSite', '@id': ORIGIN + '/#website', 'url': ORIGIN + '/',
                      'name': 'Atelier 01', 'inLanguage': 'ru',
                      'publisher': {'@id': BIZ_ID}})
    schema = {'@context': 'https://schema.org', '@graph': graph}
    schema_json = json.dumps(schema, ensure_ascii=False).replace('<', '\\u003c')
    return f'''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(title)}</title><meta name="description" content="{escape(description)}"><meta name="robots" content="{robots}"><link rel="canonical" href="{escape(canonical)}"><meta name="theme-color" content="#07090b"><meta property="og:title" content="{escape(title)}"><meta property="og:description" content="{escape(description)}"><meta property="og:url" content="{escape(canonical)}"><meta property="og:type" content="website"><meta name="twitter:card" content="summary"><meta name="twitter:title" content="{escape(title)}"><meta name="twitter:description" content="{escape(description)}"><link rel="icon" href="{prefix}assets/favicon.svg" type="image/svg+xml"><script type="application/ld+json">{schema_json}</script><link rel="stylesheet" href="{prefix}assets/css/styles.css"><!-- Yandex.Metrika counter --><script type="text/javascript">(function(m,e,t,r,i,k,a){{m[i]=m[i]||function(){{(m[i].a=m[i].a||[]).push(arguments)}};m[i].l=1*new Date();for (var j = 0; j < document.scripts.length; j++) {{if (document.scripts[j].src === r) {{ return; }}}}k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)}})(window, document,'script','https://mc.yandex.ru/metrika/tag.js?id=113016242', 'ym');ym(113016242, 'init', {{ssr:true, webvisor:true, clickmap:true, ecommerce:"dataLayer", referrer: document.referrer, url: location.href, accurateTrackBounce:true, trackLinks:true}});</script><noscript><div><img src="https://mc.yandex.ru/watch/113016242" style="position:absolute; left:-9999px;" alt="" /></div></noscript><!-- /Yandex.Metrika counter --></head><body>{header(prefix)}{body}{footer(prefix)}<script src="{prefix}assets/js/main.js" defer></script></body></html>'''

def breadcrumbs(items, prefix=''):
    home_href = prefix or './'
    parts=[f'<a href="{home_href}">Главная</a>']
    for name, href in items:
        parts.append('·')
        parts.append(f'<a href="{href}">{escape(name)}</a>' if href else f'<span>{escape(name)}</span>')
    return '<div class="breadcrumbs">' + ''.join(parts) + '</div>'

def page_hero(title, label, depth=0, media='hero-poster.webp', breadcrumbs_html=''):
    p=rel_prefix(depth)
    picture = f'<div class="page-hero-media"><img src="{p}assets/images/{media}" alt=""></div>' if media else ''
    return f'''<section class="page-hero">{picture}<div class="container page-hero-content">{breadcrumbs_html}<div class="eyebrow">{escape(label)}</div><h1 class="display display-lg">{escape(title)}</h1></div></section>'''

# HOME
BRAND_DATA = {b['slug']: b for b in json.loads((ROOT/'data/brands.json').read_text())}
featured_brands = [(slug,name) for slug,name in brands if BRAND_DATA[slug]['status'] == 'listed_on_source']
service_items=''.join([f'''<a class="service-item" href="services/{slug}/" ><span class="index">{i+1:02}</span><h3>{escape(name)}</h3><div class="meta"><span>{escape(tag)}</span></div></a>''' for i,(slug,name,desc,tag) in enumerate(services)])
brand_rows=''.join([f'''<a class="brand-row" href="brands/{slug}/"><span class="brand-no">{i+1:02}</span><span class="brand-name">{escape(name)}</span><span class="brand-tag">Подробнее</span></a>''' for i,(slug,name) in enumerate(featured_brands)])
faq_html=''.join([f'''<div class="faq-item"><button class="faq-q" aria-expanded="false"><span>{escape(q)}</span><span class="faq-plus">+</span></button><div class="faq-a"><div class="faq-a-inner">{escape(a)}</div></div></div>''' for q,a in faqs])

home=f'''
<main>
<section class="hero"><div class="hero-media"><img src="assets/images/hero-poster.webp" alt=""><video autoplay muted loop playsinline poster="assets/images/hero-poster.webp"><source src="assets/videos/hero-watch.mp4" type="video/mp4"></video></div><div class="container hero-inner"><div class="hero-copy reveal"><div class="eyebrow">Независимая мастерская · Москва</div><h1 class="display display-xl">Ремонт и восстановление<br>премиальных часов.</h1><p class="hero-sub">Швейцарские и брендовые часы: диагностика, обслуживание, восстановление корпуса и механизма. Мастерская на Петровке.</p><div class="hero-actions"><a class="btn" href="contacts/">Записаться на диагностику</a></div></div><div class="hero-bottom"><div class="hero-brands"><span>Rolex</span><span>Patek Philippe</span><span>Audemars Piguet</span><span>Omega</span><span>Cartier</span></div><div class="hero-scroll">Листайте вниз</div></div></div></section>

<section class="section section-ivory"><div class="container intro-wide"><div class="eyebrow reveal">01 / Мастерская</div><h2 class="display display-lg intro-statement reveal">Механика не терпит приблизительности.</h2><div class="intro-columns reveal"><p class="lead">Часы высокого класса требуют не громких обещаний, а точной диагностики, аккуратной работы и понятного согласования каждого вмешательства.</p><p class="copy">Мы перестраиваем привычную логику «сервисного центра» вокруг самого изделия: сначала состояние часов, затем решение, затем работа и контроль результата.</p></div></div></section>

<section class="section section-dark"><div class="container craft-grid"><div class="media-frame reveal"><img src="assets/images/watchmaker.webp" alt="Работа часовщика"><video autoplay muted loop playsinline poster="assets/images/watchmaker.webp"><source src="assets/videos/watchmaker.mp4" type="video/mp4"></video><div class="media-caption"><span>РАБОТА МАСТЕРА</span><span>01</span></div></div><div class="craft-copy reveal"><div><div class="eyebrow">Ремесло и точность</div><h2 class="display display-md">Работа, которую видно только в макро.</h2><p class="copy">Под отвёрткой — доли миллиметра. В кадре — то, что обычно скрыто под крышкой: мосты, винты, зубья, посадки и следы предыдущего вмешательства.</p></div></div></div></section>

<section class="section section-dark" id="services"><div class="container"><div class="services-head services-head-solo"><div><div class="eyebrow reveal">02 / Услуги</div><h2 class="display display-lg reveal one-line">Что мы делаем.</h2></div></div><div class="services-layout"><div class="service-list reveal">{service_items}</div><div class="service-preview reveal"><img src="assets/images/detail-01.webp" alt="Иллюстративный макрокадр механизма"><div class="service-preview-note"><span>Иллюстративный кадр</span><span>Механизм</span></div></div></div><div class="mt-46"><a class="btn" href="services/">Все услуги</a></div></div></section>

<section class="section section-navy"><div class="container"><div class="brands-head brands-head-solo"><div><div class="eyebrow reveal">03 / Мануфактуры</div><h2 class="display display-lg reveal one-line">Часы, с которыми приходят не за «быстрым ремонтом».</h2></div></div><div class="brand-cloud">{brand_rows}</div><p class="brands-note">Независимая мастерская. Указание товарных знаков носит информационный характер и не означает официальную аффилиацию. Возможность конкретной работы, наличие компонентов и сроки подтверждаются после осмотра.</p><div class="mt-34"><a class="btn" href="brands/">Все бренды</a></div></div></section>

<section class="section section-ivory"><div class="container"><div class="eyebrow reveal">04 / Процесс</div><h2 class="display display-lg reveal heading-margin-start one-line">От состояния к результату.</h2><div class="process-grid">{''.join([f'<div class="process-step reveal"><span class="n">{i+1:02}</span><h3>{title}</h3><p>{text}</p></div>' for i,(title,text) in enumerate([('Диагностика','Определяем состояние часов и характер вмешательства.'),('Согласование','Фиксируем перечень работ до их начала.'),('Работа','Выполняем согласованные операции без лишнего вмешательства.'),('Контроль','Проверяем параметры, относящиеся к выполненной работе.'),('Выдача','Передаём часы владельцу с понятным описанием результата.')])])}</div></div></section>

<section class="section section-dark"><div class="container"><div class="brands-head video-head"><div><div class="eyebrow reveal">05 / Мастерская</div><h2 class="display display-lg reveal one-line">Чиним премиальные часы с 1991 года.</h2></div></div><div class="video-triptych"><div class="video-tile reveal"><img src="assets/images/detail-01.webp" alt="Механизм"><video autoplay muted loop playsinline poster="assets/images/detail-01.webp"><source src="assets/videos/detail-01.mp4" type="video/mp4"></video><span class="label">Осмотр / 01</span></div><div class="video-tile reveal"><img src="assets/images/detail-02.webp" alt="Микроработа"><video autoplay muted loop playsinline poster="assets/images/detail-02.webp"><source src="assets/videos/detail-02.mp4" type="video/mp4"></video><span class="label">Регулировка / 02</span></div><div class="video-tile reveal"><img src="assets/images/detail-03.webp" alt="Браслет"><video autoplay muted loop playsinline poster="assets/images/detail-03.webp"><source src="assets/videos/detail-03.mp4" type="video/mp4"></video><span class="label">Отделка / 03</span></div></div><div class="mt-110"><a class="btn" href="atelier/">Внутри мастерской</a></div></div></section>

<section class="section section-navy"><div class="container price-layout"><div class="reveal"><div class="eyebrow">Цены и согласование</div><h2 class="display display-md">Цена после понимания задачи.</h2><a class="btn mt-28" href="prices/">Смотреть структуру прайса</a></div><div class="price-list reveal"><div class="price-row"><h3>Обслуживание механизма</h3><span>после диагностики</span></div><div class="price-row"><h3>Корпус и полировка</h3><span>по состоянию</span></div><div class="price-row"><h3>Стекло</h3><span>по модели</span></div><div class="price-row"><h3>Герметичность</h3><span>по задаче</span></div><div class="price-row"><h3>Сложные механизмы</h3><span>индивидуально</span></div></div></div></section>

<section class="section section-ivory"><div class="container narrow"><div class="eyebrow reveal">Вопросы перед обращением</div><h2 class="display display-md reveal heading-margin-start">Перед тем как оставить часы.</h2><div class="faq">{faq_html}</div></div></section>

<section class="section section-dark"><div class="container contact-block"><div class="contact-head reveal"><div class="eyebrow">Контакты</div><h2 class="display display-lg contact-title one-line">Мастерская на Петровке.</h2></div><div class="contact-columns"><div class="contact-info reveal"><dl class="contact-panel"><div class="contact-line"><dt>Адрес</dt><dd>{ADDRESS["postal_code"]}, {ADDRESS_TEXT}</dd></div><div class="contact-line"><dt>График</dt><dd>{HOURS_TEXT}</dd></div><div class="contact-line"><dt>Телефон</dt><dd><a href="{PHONE_HREF}">{PHONE}</a></dd></div></dl></div><div class="contact-map"><iframe src="https://yandex.ru/map-widget/v1/?um=constructor%3A349d14082660d41000ccf910e5fae332e234360b34a1b731d98f4ddc441a9b1b&amp;source=constructor" width="100%" height="400" frameborder="0" loading="lazy" title="Мастерская на карте: улица Петровка, 23/10, строение 5"></iframe></div></div></div></section>
</main>'''
home_schema = [
    {'@type': 'FAQPage', '@id': ORIGIN + '/#faq',
     'mainEntity': [{'@type': 'Question', 'name': q,
                     'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in faqs]},
    {'@type': 'ItemList', '@id': ORIGIN + '/#services',
     'name': 'Услуги часовой мастерской',
     'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'name': name,
                          'url': ORIGIN + f'/services/{slug}/'}
                         for i, (slug, name, desc, tag) in enumerate(services)]},
]
(ROOT/'index.html').write_text(doc('Ремонт швейцарских часов на Петровке — независимая мастерская','Диагностика, обслуживание и восстановление швейцарских часов в Москве. Независимая часовая мастерская на Петровке.',home,0,schema_extra=home_schema),encoding='utf-8')

# SERVICES INDEX
(ROOT/'services').mkdir(exist_ok=True)
service_cards=''.join([f'''<a class="content-card" href="{slug}/"><div><div class="eyebrow">{i+1:02} / {escape(tag)}</div><h2>{escape(name)}</h2><p>{escape(desc)}</p></div><span>Подробнее</span></a>''' for i,(slug,name,desc,tag) in enumerate(services)])
body=page_hero('Услуги','Услуги мастерской',1,'watchmaker.webp',breadcrumbs([('Услуги',None)],'../'))+f'''<main><section class="section section-dark"><div class="container inner-intro"><div class="eyebrow reveal">Как устроена работа</div><div><p class="lead reveal">От простого вмешательства до сложного калибра — сначала состояние часов, затем решение.</p><p class="copy reveal">Стоимость и объём работ корректно фиксировать после осмотра, а не обещать по одной фотографии.</p></div></div></section><section class="section section-dark pt-0"><div class="container content-grid">{service_cards}</div></section></main>'''
(ROOT/'services'/'index.html').write_text(doc('Услуги часовой мастерской — ремонт и обслуживание часов','Полное обслуживание, ремонт механизмов, полировка, стекло, герметичность, автоподзавод и сложные механизмы.',body,1,route="/services/",trail=[('Услуги','/services/')],schema_extra=[{'@type':'ItemList','itemListElement':[{'@type':'ListItem','position':i+1,'name':name,'url':ORIGIN+f'/services/{slug}/'} for i,(slug,name,desc,tag) in enumerate(services)]}]),encoding='utf-8')

for i,(slug,name,desc,tag) in enumerate(services):
    d=ROOT/'services'/slug; d.mkdir(parents=True,exist_ok=True)
    bc=breadcrumbs([('Услуги','../'),(name,None)],'../../')
    body=page_hero(name,tag,2,None,bc)+f'''<main><section class="section section-dark"><div class="container detail-layout"><div class="detail-sticky reveal"><img src="../../assets/images/detail-0{(i%3)+1}.webp" alt="Иллюстративный макрокадр часового механизма"></div><div class="detail-copy reveal"><div class="eyebrow">Независимая мастерская</div><h2>{escape(name)}</h2><p class="lead">{escape(desc)}</p><p>Конкретный объём вмешательства определяется после осмотра. Для часов высокого класса важно сохранить исходную геометрию деталей и не выполнять дополнительные операции без необходимости.</p><ul class="detail-list"><li>Первичный осмотр и фиксация состояния</li><li>Согласование необходимого объёма работ</li><li>Выполнение согласованной операции</li><li>Контроль параметров, связанных с выполненной услугой</li><li>Рекомендации по дальнейшей эксплуатации</li></ul><a class="btn" href="../../contacts/">Записаться на диагностику</a></div></div></section><section class="section section-ivory"><div class="container narrow"><div class="eyebrow">Важно</div><h2 class="display display-md heading-margin-block">Сначала — часы.<br>Потом — цена.</h2><p class="lead">Цена зависит от модели, состояния и доступности необходимых компонентов. Финальное согласование — до начала основных работ.</p></div></section></main>'''
    service_node = {'@type': 'Service', '@id': ORIGIN + f'/services/{slug}/#service',
                    'name': name, 'description': desc,
                    'serviceType': 'Ремонт и обслуживание часов',
                    'provider': {'@id': BIZ_ID},
                    'areaServed': {'@type': 'City', 'name': 'Москва'}}
    d.joinpath('index.html').write_text(doc(f'{name} часов в Москве — часовая мастерская',f'{name}: диагностика и обслуживание в независимой мастерской на Петровке. Стоимость после осмотра.',body,2,route=f"/services/{slug}/",trail=[('Услуги','/services/'),(name,f'/services/{slug}/')],schema_extra=[service_node]),encoding='utf-8')

# BRANDS
(ROOT/'brands').mkdir(exist_ok=True)
brand_cards=''.join([f'<a class="brand-index-card" href="{slug}/"><span class="small">{i+1:02} / МАРКА ЧАСОВ</span><span class="name">{escape(name)}</span></a>' for i,(slug,name) in enumerate(featured_brands)])
body=page_hero('Бренды','Марки часов',1,'hero-poster.webp',breadcrumbs([('Бренды',None)],'../'))+f'''<main><section class="section section-navy"><div class="container"><div class="inner-intro"><div class="eyebrow">Марки часов</div><div><p class="lead">Rolex, Omega, Patek Philippe и другие марки, перечисленные на исходном сайте мастерской.</p><p class="copy">Список используется как навигация по запросам владельцев. Возможность конкретной работы и доступность компонентов подтверждаются после диагностики.</p></div></div><div class="brand-index-grid mt-70">{brand_cards}</div><p class="brands-note">Независимая мастерская. Не является официальным сервисным центром и не аффилирована с указанными производителями. Все товарные знаки принадлежат их правообладателям.</p></div></section></main>'''
(ROOT/'brands'/'index.html').write_text(doc('Ремонт часов Rolex, Patek Philippe, Omega и других брендов','Независимое обслуживание часов ведущих швейцарских и международных мануфактур в Москве.',body,1,route="/brands/",trail=[('Бренды','/brands/')],schema_extra=[{'@type':'ItemList','itemListElement':[{'@type':'ListItem','position':i+1,'name':name,'url':ORIGIN+f'/brands/{slug}/'} for i,(slug,name) in enumerate(featured_brands)]}]),encoding='utf-8')
for i,(slug,name) in enumerate(brands):
    d=ROOT/'brands'/slug; d.mkdir(parents=True,exist_ok=True)
    bc=breadcrumbs([('Бренды','../'),(name,None)],'../../')
    body=page_hero(name,'Watch maison / service request',2,None,bc)+f'''<main><section class="section section-dark"><div class="container detail-layout"><div class="detail-sticky"><div class="brand-index-card"><span class="small">{i+1:02} / МАРКА ЧАСОВ</span><span class="name">{escape(name)}</span><span class="small">Возможность обслуживания уточняется для конкретной модели.</span></div></div><div class="detail-copy"><div class="eyebrow">{escape(name)} · Москва</div><h2>Запрос на обслуживание {escape(name)}</h2><p class="lead">Диагностика начинается с конкретной модели, состояния и истории часов — не с универсального прайса.</p><p>Для разных калибров, поколений и корпусов перечень возможных работ отличается. Перед началом вмешательства мастерская должна подтвердить техническую возможность ремонта и согласовать объём работ.</p><ul class="detail-list"><li>Диагностика механизма</li><li>Проверка состояния корпуса и внешних элементов</li><li>Согласование ремонта или обслуживания</li><li>Контроль после выполненных работ</li></ul><a class="btn" href="../../contacts/">Запросить диагностику</a><p class="small">Независимая мастерская. Упоминание {escape(name)} не означает официальную аффилиацию или авторизацию производителя.</p></div></div></section></main>'''
    brand_node = {'@type': 'Service', '@id': ORIGIN + f'/brands/{slug}/#service',
                  'name': f'Ремонт часов {name}',
                  'description': f'Диагностика и обслуживание часов {name} в независимой мастерской в Москве. Не официальный сервисный центр.',
                  'serviceType': 'Ремонт и обслуживание часов',
                  'provider': {'@id': BIZ_ID},
                  'areaServed': {'@type': 'City', 'name': 'Москва'}}
    d.joinpath('index.html').write_text(doc(f'Ремонт часов {name} в Москве — независимая мастерская',f'Диагностика и обслуживание часов {name} в Москве. Независимая мастерская на Петровке.',body,2,route=f"/brands/{slug}/",trail=[('Бренды','/brands/'),(name,f'/brands/{slug}/')],schema_extra=[brand_node]),encoding='utf-8')

# PRICES
(ROOT/'prices').mkdir(exist_ok=True)
cats=[('Механизм',['Диагностика — после осмотра','Полное обслуживание — после диагностики','Ремонт отдельных узлов — после диагностики','Автоподзавод — после диагностики']),('Корпус и браслет',['Полировка корпуса — после оценки состояния','Сатинирование — после оценки геометрии','Работы с браслетом — по модели']),('Стекло',['Замена стекла — по модели и типу стекла','Посадка и проверка — по задаче']),('Герметичность',['Проверка герметичности — по модели','Замена уплотнений — после осмотра']),('Сложные механизмы',['Хронограф — индивидуально','Турбийон и усложнения — только после предварительной диагностики'])]
price_cats=''.join([f'''<div class="price-category"><button><span>{escape(name)}</span><span>+</span></button><div class="price-category-body">{''.join([f'<div class="price-table-row"><span>{escape(row.split(" — ")[0])}</span><span>{escape(row.split(" — ")[1])}</span></div>' for row in rows])}</div></div>''' for name,rows in cats])
body=page_hero('Цены','Цены: сначала согласование',1,'detail-01.webp',breadcrumbs([('Цены',None)],'../'))+f'''<main><section class="section section-navy"><div class="container price-layout"><div><div class="eyebrow">Как считается стоимость</div><h2 class="display display-md">Без фальшивой точности.</h2></div><div class="price-accordion">{price_cats}</div></div></section></main>'''
(ROOT/'prices'/'index.html').write_text(doc('Цены на ремонт и обслуживание часов','Структура стоимости обслуживания часов: механизм, корпус, стекло, герметичность и сложные калибры.',body,1,route="/prices/",trail=[('Цены','/prices/')]),encoding='utf-8')

# ATELIER
(ROOT/'atelier').mkdir(exist_ok=True)
body=page_hero('Мастерская','Мастерская и ремесло',1,'watchmaker.webp',breadcrumbs([('Мастерская',None)],'../'))+'''<main><section class="section section-dark"><div class="container craft-grid"><div class="media-frame"><img src="../assets/images/watchmaker.webp" alt="Часовщик за работой"><video autoplay muted loop playsinline poster="../assets/images/watchmaker.webp"><source src="../assets/videos/watchmaker.mp4" type="video/mp4"></video><div class="media-caption"><span>Ручная работа · макросъёмка</span><span>01</span></div></div><div class="craft-copy"><div><div class="eyebrow">Точность важнее оформления</div><h2 class="display display-md">Мастерская должна доказывать себя процессом.</h2><p class="copy">Не сертификатами, которых владелец часов никогда не видел, и не словами «премиум», а тем, как устроена работа с изделием.</p></div></div></div></section><section class="section section-ivory"><div class="container"><div class="eyebrow">Микрооперации</div><h2 class="display display-lg heading-margin-block">Точность в трёх кадрах.</h2><div class="video-triptych"><div class="video-tile"><video autoplay muted loop playsinline poster="../assets/images/detail-01.webp"><source src="../assets/videos/detail-01.mp4" type="video/mp4"></video><span class="label">Осмотр</span></div><div class="video-tile"><video autoplay muted loop playsinline poster="../assets/images/detail-02.webp"><source src="../assets/videos/detail-02.mp4" type="video/mp4"></video><span class="label">Регулировка</span></div><div class="video-tile"><video autoplay muted loop playsinline poster="../assets/images/detail-03.webp"><source src="../assets/videos/detail-03.mp4" type="video/mp4"></video><span class="label">Отделка</span></div></div></div></section></main>'''
(ROOT/'atelier'/'index.html').write_text(doc('Часовая мастерская на Петровке','Независимая часовая мастерская: процесс обслуживания, работа мастера и макросъёмка механики.',body,1,route="/atelier/",trail=[('Мастерская','/atelier/')]),encoding='utf-8')

# CONTACTS
(ROOT/'contacts').mkdir(exist_ok=True)
body=page_hero('Контакты','Петровка · Москва',1,'hero-poster.webp',breadcrumbs([('Контакты',None)],'../'))+f'''<main><section class="section section-dark"><div class="container contact-grid"><div><div class="eyebrow">Визит и запись</div><h2 class="display display-md">Петровка,<br>Москва.</h2><p class="copy">Для часов высокого класса удобнее предварительно описать модель и задачу: так мастер подготовится к осмотру заранее.</p></div><div><dl class="contact-panel"><div class="contact-line"><dt>Адрес</dt><dd>{ADDRESS["postal_code"]}, {ADDRESS_TEXT}</dd></div><div class="contact-line"><dt>Телефон</dt><dd><a href="{PHONE_HREF}">{PHONE}</a></dd></div><div class="contact-line"><dt>График</dt><dd>{HOURS_TEXT}</dd></div></dl><div class="contact-actions"><a class="btn" href="{PHONE_HREF}">Позвонить {PHONE}</a><a class="btn ghost" href="mailto:{CONTACTS['email']}">Написать на почту</a></div><p class="small">Опишите марку, модель и что случилось с часами — мастер подскажет, нужен ли осмотр и когда удобно подъехать.</p></div></div><div class="container"><div class="contact-map"><iframe src="https://yandex.ru/map-widget/v1/?um=constructor%3A349d14082660d41000ccf910e5fae332e234360b34a1b731d98f4ddc441a9b1b&amp;source=constructor" width="100%" height="400" frameborder="0" loading="lazy" title="Мастерская на карте: улица Петровка, 23/10, строение 5"></iframe></div></div></section></main>'''
(ROOT/'contacts'/'index.html').write_text(doc('Контакты часовой мастерской на Петровке','Запись на диагностику и обслуживание часов в независимой мастерской на Петровке в Москве.',body,1,route="/contacts/",trail=[('Контакты','/contacts/')],schema_extra=[{'@type':'ContactPage','@id':ORIGIN+'/contacts/#contact','mainEntity':{'@id':BIZ_ID}}]),encoding='utf-8')

# Preview URLs remain crawlable so crawlers can read noindex.
robots_text = 'User-agent: *\nDisallow:\n'
robots_text += ('Sitemap: ' + CONFIG['production_origin'] + '/sitemap.xml\n') if CONFIG['environment'] == 'production' else '# Preview: all HTML pages use noindex.\n'
(ROOT/'robots.txt').write_text(robots_text, encoding='utf-8')
urls = ''.join(f'<url><loc>{escape(CONFIG["production_origin"] + route)}</loc></url>' for route, approved in PAGES if approved)
(ROOT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + urls + '</urlset>\n', encoding='utf-8')
print('Built', len(PAGES), 'pages in', ROOT)
