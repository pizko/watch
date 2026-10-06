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
IMAGE_SIZES = {'hero-poster.webp': (1400, 900), 'watchmaker.webp': (1000, 1000),
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
    ('diagnostics','Диагностика и регулировка хода','Находим причину остановки или неточного хода и регулируем механизм. Механические и кварцевые часы.','ТОЧНОСТЬ ХОДА'),
    ('glass-replacement','Замена стекла','Подбор и замена стекла с последующей проверкой посадки и состояния корпуса.','СТЕКЛО'),
    ('water-resistance','Проверка герметичности','Контроль герметичности после вмешательства и перед повседневной эксплуатацией.','ГЕРМЕТИЧНОСТЬ'),
    ('battery','Замена батарейки','Замена элемента питания в кварцевых часах с проверкой хода и герметичности после закрытия корпуса.','КВАРЦЕВЫЕ ЧАСЫ'),
    ('bracelet','Браслеты и ремешки','Укорачивание браслета, замена ремешка или браслета, ремонт застёжки.','БРАСЛЕТ И РЕМЕШОК'),
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
    ('tag-heuer','TAG Heuer'),('tudor','Tudor'),('grand-seiko','Grand Seiko'),('seiko','Seiko'),('longines','Longines'),('rado','Rado'),
    ('tissot','Tissot'),('maurice-lacroix','Maurice Lacroix'),('frederique-constant','Frederique Constant'),('oris','Oris')
]


# ── Общие данные страниц ───────────────────────────────────────────────────
# Правятся в одном месте и попадают на все страницы, где выводится блок.
price_teaser = [
    ('Обслуживание механизма', 'после диагностики'),
    ('Корпус и полировка', 'по состоянию'),
    ('Стекло', 'по модели'),
    ('Герметичность', 'по задаче'),
    ('Сложные механизмы', 'индивидуально'),
]

process_steps = [
    ('Диагностика', 'Определяем состояние часов и характер вмешательства.'),
    ('Согласование', 'Фиксируем перечень работ до их начала.'),
    ('Работа', 'Выполняем согласованные операции без лишнего вмешательства.'),
    ('Контроль', 'Проверяем ход часов и работу узлов, которых касался ремонт.'),
    ('Выдача', 'Передаём часы владельцу с понятным описанием результата.'),
]

faqs = [
    ('Сколько занимает диагностика?','Срок зависит от модели и характера неисправности. После первичного осмотра мастер сообщает, нужна ли углублённая диагностика и когда можно согласовать работы.'),
    ('Стоимость известна заранее?','До начала основных работ согласуются перечень вмешательств и стоимость. Если по ходу работы найдётся ещё одна неисправность, мастер сначала позвонит: без вашего согласия ничего не делаем.'),
    ('Можно ли обслуживать дорогие часы без официального сервиса?','Независимая мастерская не является официальным сервисным центром брендов. Возможность конкретной работы зависит от модели, состояния часов, доступности компонентов и требований владельца.'),
    ('Что происходит после ремонта?','После сборки мастер проверяет ход и работу механизма. Если работа затрагивала корпус, отдельно проверяется герметичность.'),
    ('Нужно ли записываться заранее?','Для часов высокого класса предварительная запись удобнее: можно заранее описать модель и задачу, а мастерская подготовится к осмотру.'),
]


# ── Schema.org ─────────────────────────────────────────────────────────────
# Размечаем только то, что подтверждено: организация, адрес, телефон, график,
# услуги и вопросы-ответы. Ни цен, ни рейтингов, ни отзывов — таких данных нет.
ORIGIN = CONFIG['production_origin'].rstrip('/')
METRIKA = '''<!-- Yandex.Metrika counter --><script type="text/javascript">(function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};m[i].l=1*new Date();for (var j = 0; j < document.scripts.length; j++) {if (document.scripts[j].src === r) { return; }}k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})(window, document,'script','https://mc.yandex.ru/metrika/tag.js?id=113016242', 'ym');ym(113016242, 'init', {ssr:true, webvisor:true, clickmap:true, ecommerce:"dataLayer", referrer: document.referrer, url: location.href, accurateTrackBounce:true, trackLinks:true});</script><noscript><div><img src="https://mc.yandex.ru/watch/113016242" style="position:absolute; left:-9999px;" alt="" /></div></noscript><!-- /Yandex.Metrika counter -->'''
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
    return f'''<footer class="site-footer"><div class="container"><div class="footer-grid"><div class="footer-brand">ЧАСОВАЯ<br>МАСТЕРСКАЯ</div><nav class="footer-nav"><a href="{prefix}services/">Услуги</a><a href="{prefix}brands/">Бренды</a><a href="{prefix}prices/">Цены</a><a href="{prefix}atelier/">Мастерская</a><a href="{prefix}articles/">Статьи</a><a href="{prefix}contacts/">Контакты</a></nav><div class="footer-meta"><a href="{PHONE_HREF}">{PHONE}</a><a href="{prefix}contacts/">{ADDRESS_TEXT}</a><span>{HOURS_TEXT}</span></div></div>
<div class="footer-brands"><span class="footer-brands-title">Марки часов</span><div class="footer-brands-list">{FOOTER_BRANDS}</div></div><div class="footer-bottom"><span>© <span data-year></span> Независимая часовая мастерская · <a href="{prefix}privacy/">Политика конфиденциальности</a></span><span>Независимая мастерская. Не является официальным сервисным центром и не аффилирована с указанными производителями.</span></div></div></footer><a class="call-fab" href="{PHONE_HREF}" aria-label="Позвонить {PHONE}"><span>Позвонить</span></a><div class="toast"></div>'''

def doc(title, description, body, depth=0, route='/', trail=None, schema_extra=None):
    prefix = rel_prefix(depth)
    canonical = CONFIG['production_origin'].rstrip('/') + route
    allowed = CONFIG['indexable_routes']
    indexable = CONFIG['environment'] == 'production' and (allowed == 'all' or route in allowed)
    robots = 'index,follow' if indexable else 'noindex,follow'
    # Счётчик только в боевой сборке: просмотры preview не должны попадать в статистику сайта.
    metrika = METRIKA if CONFIG['environment'] == 'production' else ''
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
    return f'''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(title)}</title><meta name="description" content="{escape(description)}"><meta name="robots" content="{robots}"><link rel="canonical" href="{escape(canonical)}"><meta name="theme-color" content="#07090b"><meta property="og:title" content="{escape(title)}"><meta property="og:description" content="{escape(description)}"><meta property="og:url" content="{escape(canonical)}"><meta property="og:type" content="website"><meta name="twitter:card" content="summary"><meta name="twitter:title" content="{escape(title)}"><meta name="twitter:description" content="{escape(description)}"><link rel="icon" href="{prefix}assets/favicon.svg" type="image/svg+xml"><script type="application/ld+json">{schema_json}</script><link rel="stylesheet" href="{prefix}assets/css/styles.css">{metrika}</head><body>{header(prefix)}{body}{footer(prefix)}<script src="{prefix}assets/js/main.js" defer></script></body></html>'''

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


# ── Переиспользуемые секции ────────────────────────────────────────────────
# Каждая принимает префикс относительных ссылок и собирается из общих данных,
# поэтому правка прайса, этапов или контактов разом меняет все страницы.

MAP_EMBED = ('<div class="contact-map"><iframe src="https://yandex.ru/map-widget/v1/'
             '?um=constructor%3A349d14082660d41000ccf910e5fae332e234360b34a1b731d98f4ddc441a9b1b&amp;source=constructor" '
             'width="100%" height="400" frameborder="0" loading="lazy" '
             'title="Мастерская на карте: улица Петровка, 23/10, строение 5"></iframe></div>')


def block_process(prefix=''):
    steps = ''.join(
        f'<div class="process-step reveal"><span class="n">{i+1:02}</span><h3>{escape(t)}</h3><p>{escape(x)}</p></div>'
        for i, (t, x) in enumerate(process_steps))
    return (f'<section class="section section-ivory"><div class="container">'
            f'<div class="eyebrow reveal">Порядок работы</div>'
            f'<h2 class="display display-lg reveal heading-margin-start one-line">От состояния к результату.</h2>'
            f'<div class="process-grid">{steps}</div></div></section>')


def block_triptych(prefix=''):
    p = prefix
    tiles = ''.join(
        f'<div class="video-tile reveal"><img src="{p}assets/images/detail-0{i}.webp" alt="{escape(alt)}">'
        f'<video autoplay muted loop playsinline poster="{p}assets/images/detail-0{i}.webp">'
        f'<source src="{p}assets/videos/detail-0{i}.mp4" type="video/mp4"></video>'
        f'<span class="label">{escape(lab)}</span></div>'
        for i, (alt, lab) in enumerate([('Механизм', 'Осмотр / 01'), ('Микроработа', 'Регулировка / 02'),
                                        ('Браслет', 'Отделка / 03')], start=1))
    return (f'<section class="section section-dark"><div class="container">'
            f'<div class="brands-head video-head"><div><div class="eyebrow reveal">Мастерская</div>'
            f'<h2 class="display display-lg reveal one-line">Чиним премиальные часы с 1991 года.</h2></div></div>'
            f'<div class="video-triptych">{tiles}</div></div></section>')


def block_prices(prefix=''):
    rows = ''.join(f'<div class="price-row"><h3>{escape(n)}</h3><span>{escape(v)}</span></div>'
                   for n, v in price_teaser)
    return (f'<section class="section section-navy"><div class="container price-layout">'
            f'<div class="reveal"><div class="eyebrow">Цены и согласование</div>'
            f'<h2 class="display display-md">Цена после понимания задачи.</h2>'
            f'<a class="btn mt-28" href="{prefix}prices/">Смотреть структуру прайса</a></div>'
            f'<div class="price-list reveal">{rows}</div></div></section>')


def block_faq(prefix=''):
    items = ''.join(
        f'<div class="faq-item"><button class="faq-q" aria-expanded="false"><span>{escape(q)}</span>'
        f'<span class="faq-plus">+</span></button><div class="faq-a"><div class="faq-a-inner">{escape(a)}</div></div></div>'
        for q, a in faqs)
    return (f'<section class="section section-ivory"><div class="container narrow">'
            f'<div class="eyebrow reveal">Вопросы перед обращением</div>'
            f'<h2 class="display display-md reveal heading-margin-start">Перед тем как оставить часы.</h2>'
            f'<div class="faq">{items}</div></div></section>')


def lead_form(prefix=''):
    """Короткая заявка: телефон обязателен, остальное — по желанию. Отправка — /send.php → Telegram."""
    return (f'<form class="lead-form" action="/send.php" method="post" novalidate>'
            f'<div class="lead-form-title">Оставить заявку</div>'
            f'<p class="lead-form-note">Опишите часы и что случилось — мастер перезвонит и подскажет, что делать.</p>'
            f'<label><span>Телефон</span><input type="tel" name="phone" autocomplete="tel" inputmode="tel" required placeholder="+7 ___ ___-__-__"></label>'
            f'<label><span>Имя</span><input type="text" name="name" autocomplete="name" maxlength="80"></label>'
            f'<label><span>Марка и что случилось</span><textarea name="message" rows="3" maxlength="1000" placeholder="Например: Omega, остановились после удара"></textarea></label>'
            f'<input class="lead-hp" type="text" name="website" tabindex="-1" autocomplete="off" aria-hidden="true">'
            f'<input type="hidden" name="ts" value="">'
            f'<button class="btn" type="submit">Отправить заявку</button>'
            f'<p class="lead-form-consent">Нажимая кнопку, вы соглашаетесь с <a href="{prefix}privacy/">политикой обработки персональных данных</a>.</p>'
            f'</form>')


def block_contacts(prefix=''):
    return (f'<section class="section section-dark"><div class="container contact-block">'
            f'<div class="contact-head reveal"><div class="eyebrow">Контакты</div>'
            f'<h2 class="display display-lg contact-title one-line">Мастерская на Петровке.</h2></div>'
            f'<div class="contact-columns"><div class="contact-info reveal"><dl class="contact-panel">'
            f'<div class="contact-line"><dt>Адрес</dt><dd>{ADDRESS["postal_code"]}, {ADDRESS_TEXT}</dd></div>'
            f'<div class="contact-line"><dt>График</dt><dd>{HOURS_TEXT}</dd></div>'
            f'<div class="contact-line"><dt>Телефон</dt><dd><a href="{PHONE_HREF}">{PHONE}</a></dd></div>'
            f'</dl>{lead_form(prefix)}</div>{MAP_EMBED}</div></div></section>')


def video_hero(title, label, breadcrumbs_html, prefix='', lead=''):
    """Первый экран с видео на фоне — как на главной."""
    p = prefix
    lead_html = f'<p class="page-hero-lead">{escape(lead)}</p>' if lead else ''
    return (f'<section class="page-hero page-hero-video">'
            f'<div class="page-hero-media"><img src="{p}assets/images/hero-poster.webp" alt="">'
            f'<video autoplay muted loop playsinline poster="{p}assets/images/hero-poster.webp">'
            f'<source src="{p}assets/videos/hero-watch.mp4" type="video/mp4"></video></div>'
            f'<div class="container page-hero-content">{breadcrumbs_html}'
            f'<div class="eyebrow">{escape(label)}</div>'
            f'<h1 class="display display-lg">{escape(title)}</h1>{lead_html}</div></section>')


# HOME
BRAND_DATA = {b['slug']: b for b in json.loads((ROOT/'data/brands.json').read_text())}
featured_brands = [(slug,name) for slug,name in brands if BRAND_DATA[slug]['status'] in ('listed_on_source', 'confirmed_by_owner')]
service_items=''.join([f'''<a class="service-item" href="services/{slug}/" ><span class="index">{i+1:02}</span><h3>{escape(name)}</h3><div class="meta"><span>{escape(tag)}</span></div></a>''' for i,(slug,name,desc,tag) in enumerate(services)])
brand_rows=''.join([f'''<a class="brand-row" href="brands/{slug}/"><span class="brand-no">{i+1:02}</span><span class="brand-name">{escape(name)}</span><span class="brand-tag">Подробнее</span></a>''' for i,(slug,name) in enumerate(featured_brands)])
faq_html=''.join([f'''<div class="faq-item"><button class="faq-q" aria-expanded="false"><span>{escape(q)}</span><span class="faq-plus">+</span></button><div class="faq-a"><div class="faq-a-inner">{escape(a)}</div></div></div>''' for q,a in faqs])

home=f'''
<main>
<section class="hero"><div class="hero-media"><img src="assets/images/hero-poster.webp" alt=""><video autoplay muted loop playsinline poster="assets/images/hero-poster.webp"><source src="assets/videos/hero-watch.mp4" type="video/mp4"></video></div><div class="container hero-inner"><div class="hero-copy reveal"><div class="eyebrow">Независимая мастерская · Москва</div><h1 class="display display-xl">Часовая мастерская:<br>ремонт швейцарских часов.</h1><p class="hero-sub">Швейцарские и брендовые часы: диагностика, обслуживание, восстановление корпуса и механизма. Мастерская на Петровке.</p><div class="hero-actions"><a class="btn" href="contacts/">Записаться на диагностику</a></div></div><div class="hero-bottom"><div class="hero-brands"><span>Rolex</span><span>Patek Philippe</span><span>Audemars Piguet</span><span>Omega</span><span>Cartier</span></div><div class="hero-scroll">Листайте вниз</div></div></div></section>

<section class="section section-ivory"><div class="container intro-wide"><div class="eyebrow reveal">01 / Мастерская</div><h2 class="display display-lg intro-statement reveal">Механика не терпит приблизительности.</h2><div class="intro-columns reveal"><p class="lead">Часы высокого класса требуют не громких обещаний, а точной диагностики, аккуратной работы и понятного согласования каждого вмешательства.</p><p class="copy">Сначала диагностика и понятный ответ, что с часами. Затем согласование объёма и цены. Только после этого — работа и проверка результата.</p></div></div></section>

<section class="section section-dark"><div class="container craft-grid"><div class="media-frame reveal"><img src="assets/images/watchmaker.webp" alt="Работа часовщика"><video autoplay muted loop playsinline poster="assets/images/watchmaker.webp"><source src="assets/videos/watchmaker.mp4" type="video/mp4"></video><div class="media-caption"><span>РАБОТА МАСТЕРА</span><span>01</span></div></div><div class="craft-copy reveal"><div><div class="eyebrow">Ремесло и точность</div><h2 class="display display-md">Работа, которую видно только в макро.</h2><p class="copy">Под отвёрткой — доли миллиметра. В кадре — то, что обычно скрыто под крышкой: мосты, винты, зубья, посадки и следы предыдущего вмешательства.</p></div></div></div></section>

<section class="section section-dark" id="services"><div class="container"><div class="services-head services-head-solo"><div><div class="eyebrow reveal">02 / Услуги</div><h2 class="display display-lg reveal one-line">Что мы делаем.</h2></div></div><div class="services-layout"><div class="service-list reveal">{service_items}</div><div class="service-preview reveal"><img src="assets/images/detail-01.webp" alt="Иллюстративный макрокадр механизма"><div class="service-preview-note"><span>Иллюстративный кадр</span><span>Механизм</span></div></div></div><div class="mt-46"><a class="btn" href="services/">Все услуги</a></div></div></section>

<section class="section section-navy"><div class="container"><div class="brands-head brands-head-solo"><div><div class="eyebrow reveal">03 / Мануфактуры</div><h2 class="display display-lg reveal one-line">Марки, которые мы обслуживаем.</h2></div></div><div class="brand-cloud">{brand_rows}</div><p class="brands-note">Независимая мастерская. Указание товарных знаков носит информационный характер и не означает официальную аффилиацию. Возможность конкретной работы, наличие компонентов и сроки подтверждаются после осмотра.</p><div class="mt-34"><a class="btn" href="brands/">Все бренды</a></div></div></section>

{block_process()}

{block_triptych()}

<section class="section section-navy"><div class="container price-layout"><div class="reveal"><div class="eyebrow">Цены и согласование</div><h2 class="display display-md">Цена после понимания задачи.</h2><a class="btn mt-28" href="prices/">Смотреть структуру прайса</a></div><div class="price-list reveal"><div class="price-row"><h3>Обслуживание механизма</h3><span>после диагностики</span></div><div class="price-row"><h3>Корпус и полировка</h3><span>по состоянию</span></div><div class="price-row"><h3>Стекло</h3><span>по модели</span></div><div class="price-row"><h3>Герметичность</h3><span>по задаче</span></div><div class="price-row"><h3>Сложные механизмы</h3><span>индивидуально</span></div></div></div></section>

{block_faq()}

{block_contacts()}
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
(ROOT/'index.html').write_text(doc('Ремонт часов в Москве — часовая мастерская на Петровке','Ремонт швейцарских часов в Москве: диагностика, обслуживание механизма, замена батарейки и стекла, полировка. Независимая часовая мастерская на Петровке.',home,0,schema_extra=home_schema),encoding='utf-8')

# SERVICES INDEX
(ROOT/'services').mkdir(exist_ok=True)
service_cards=''.join([f'''<a class="content-card" href="{slug}/"><div><div class="eyebrow">{i+1:02} / {escape(tag)}</div><h2>{escape(name)}</h2><p>{escape(desc)}</p></div><span>Подробнее</span></a>''' for i,(slug,name,desc,tag) in enumerate(services)])
body=(video_hero('Услуги','Услуги мастерской',breadcrumbs([('Услуги',None)],'../'),'../',
                'Обслуживание и ремонт механизмов, точность хода, батарейка, стекло, браслеты, полировка, герметичность и сложные калибры.')
      + f'''<main><section class="section section-dark pt-0"><div class="container content-grid">{service_cards}</div></section>'''
      + block_process('../') + block_prices('../') + block_faq('../') + block_contacts('../') + '</main>')
(ROOT/'services'/'index.html').write_text(doc('Услуги часовой мастерской — ремонт и обслуживание часов','Ремонт часов в Москве: обслуживание механизма, регулировка хода, замена батарейки, стекла и ремешка, полировка, герметичность, сложные механизмы.',body,1,route="/services/",trail=[('Услуги','/services/')],schema_extra=[{'@type':'ItemList','itemListElement':[{'@type':'ListItem','position':i+1,'name':name,'url':ORIGIN+f'/services/{slug}/'} for i,(slug,name,desc,tag) in enumerate(services)]}]),encoding='utf-8')

# H1 услуг со словом «часов»: по нему ищут, а название в карточках остаётся коротким
SERVICE_H1 = {
    'full-service': 'Чистка и полное обслуживание механизма часов',
    'diagnostics': 'Часы остановились, отстают или спешат',
    'battery': 'Замена батарейки в часах',
    'bracelet': 'Замена ремешка и ремонт браслета часов',
    'movement-repair': 'Ремонт механизма часов',
    'polishing': 'Полировка и восстановление корпуса часов',
    'glass-replacement': 'Замена стекла часов',
    'water-resistance': 'Проверка герметичности часов',
    'automatic-winding': 'Ремонт автоподзавода часов',
    'chronograph': 'Ремонт хронографов и сложных механизмов',
    'restoration': 'Реставрация часов',
}
# Title и description под частотные запросы; остальные услуги — по общему шаблону
SERVICE_META = {
    'full-service': ('Чистка и обслуживание механизма часов в Москве — часовая мастерская',
                     'Чистка, смазка и полное обслуживание механизма часов в независимой мастерской на Петровке. Объём работ и стоимость — после осмотра.'),
    'diagnostics': ('Часы остановились, отстают или спешат — ремонт в Москве',
                    'Часы остановились, стали отставать или спешить: диагностика причины и регулировка точности хода в часовой мастерской на Петровке.'),
    'battery': ('Замена батарейки в часах в Москве — часовая мастерская',
                'Замена батарейки в кварцевых часах с проверкой хода и герметичности после закрытия корпуса. Часовая мастерская на Петровке.'),
    'bracelet': ('Замена ремешка, укоротить браслет часов в Москве',
                 'Укоротить браслет, заменить ремешок или браслет, отремонтировать застёжку часов. Часовая мастерская на Петровке.'),
}

# Свой текст для страниц, где у запроса понятный интент. Только общие сведения
# о работе — без цен, сроков и гарантий, пока они не подтверждены.
SERVICE_EXTRA = {
    'diagnostics': [
        ('Часы остановились', 'У кварцевых часов чаще всего села батарейка, но остановка бывает и из-за окисления контактов или попавшей влаги. Механические могут встать из-за загустевшей смазки, повреждённой оси баланса или проблем с пружиной. Причину показывает осмотр механизма.'),
        ('Часы отстают или спешат', 'Отклонение хода появляется из-за износа смазки, намагничивания после контакта с телефоном, сумкой или колонкой, удара или долгого перерыва в обслуживании. Мастер проверяет ход в нескольких положениях и решает, достаточно ли регулировки или нужно обслуживание механизма.'),
        ('Что сделать до визита', 'Не открывайте корпус и не пытайтесь подкрутить головку с усилием. Если под стеклом появился конденсат, не нагревайте часы — принесите их как можно скорее: влага вредит механизму и циферблату.'),
    ],
    'battery': [
        ('Почему не только батарейка', 'При вскрытии корпуса снимается крышка и затрагиваются уплотнения. Поэтому после замены элемента питания мастер проверяет ход часов и посадку крышки, а при необходимости — герметичность.'),
        ('Когда менять', 'Явный признак — остановка часов или секундная стрелка, которая прыгает через несколько делений. Не держите севшую батарейку в часах долго: она может протечь и повредить механизм.'),
        ('Какие часы', 'Кварцевые наручные часы швейцарских и других марок, в том числе с хронографом. Возможность работы с конкретной моделью уточняется при обращении.'),
    ],
    'bracelet': [
        ('Укоротить браслет', 'Подгоняем металлический браслет по руке, убирая лишние звенья. Снятые звенья стоит сохранить: с ними браслет можно вернуть к исходной длине.'),
        ('Замена ремешка или браслета', 'Подбираем ремешок или браслет под ширину и крепление корпуса, переставляем застёжку и проверяем надёжность посадки.'),
        ('Ремонт застёжки', 'Если застёжка раскрывается сама или не фиксируется, мастер оценивает, можно ли её восстановить. Подробнее — по телефону или при осмотре.'),
    ],
}

_ARTS = {a['slug']: a for a in json.loads((ROOT/'data/articles.json').read_text())}
SERVICE_ARTICLES = {}
for _a in _ARTS.values():
    for _n, _href in _a['related']:
        SERVICE_ARTICLES.setdefault(_href.split('/')[1], []).append(_a)

for i,(slug,name,desc,tag) in enumerate(services):
    d=ROOT/'services'/slug; d.mkdir(parents=True,exist_ok=True)
    bc=breadcrumbs([('Услуги','../'),(name,None)],'../../')
    detail=(f'<section class="section section-dark"><div class="container detail-layout">'
            f'<div class="detail-sticky reveal"><img src="../../assets/images/detail-0{(i%3)+1}.webp" alt="Иллюстративный макрокадр часового механизма"></div>'
            f'<div class="detail-copy reveal"><div class="eyebrow">Независимая мастерская</div><h2>{escape(name)}</h2>'
            f'<p class="lead">{escape(desc)}</p>'
            + ''.join(f'<h3>{escape(h)}</h3><p>{escape(t)}</p>' for h, t in SERVICE_EXTRA.get(slug, []))
            + f'<p>Конкретный объём вмешательства определяется после осмотра. Для часов высокого класса важно сохранить '
            f'исходную геометрию деталей и не выполнять дополнительные операции без необходимости.</p>'
            f'<ul class="detail-list"><li>Первичный осмотр и фиксация состояния</li>'
            f'<li>Согласование необходимого объёма работ</li><li>Выполнение согласованной операции</li>'
            f'<li>Проверка работы часов после ремонта</li>'
            f'<li>Рекомендации по дальнейшей эксплуатации</li></ul>'
            + ''.join(f'<p class="detail-article">Статья по теме: <a href="../../articles/{a["slug"]}/">{escape(a["title"])}</a></p>'
                      for a in SERVICE_ARTICLES.get(slug, []))
            + f'<a class="btn" href="{PHONE_HREF}">Позвонить {PHONE}</a></div></div></section>')
    body=(video_hero(SERVICE_H1.get(slug, name), tag, bc, '../../', desc)
          + '<main>' + detail + block_process('../../') + block_triptych('../../')
          + block_prices('../../') + block_faq('../../') + block_contacts('../../') + '</main>')
    service_node = {'@type': 'Service', '@id': ORIGIN + f'/services/{slug}/#service',
                    'name': name, 'description': desc,
                    'serviceType': 'Ремонт и обслуживание часов',
                    'provider': {'@id': BIZ_ID},
                    'areaServed': {'@type': 'City', 'name': 'Москва'}}
    title, meta = SERVICE_META.get(slug, (f'{name} часов в Москве — часовая мастерская',
                                          f'{name}: диагностика и обслуживание в независимой мастерской на Петровке. Стоимость после осмотра.'))
    d.joinpath('index.html').write_text(doc(title, meta,body,2,route=f"/services/{slug}/",trail=[('Услуги','/services/'),(name,f'/services/{slug}/')],schema_extra=[service_node]),encoding='utf-8')

# BRANDS
(ROOT/'brands').mkdir(exist_ok=True)
brand_cards=''.join([f'<a class="brand-index-card" href="{slug}/"><span class="small">{i+1:02} / МАРКА ЧАСОВ</span><span class="name">{escape(name)}</span></a>' for i,(slug,name) in enumerate(featured_brands)])
body=(video_hero('Бренды','Марки часов',breadcrumbs([('Бренды',None)],'../'),'../',
                'Марки, с которыми работает мастерская. Возможность конкретной работы подтверждается после диагностики.')
      + f'''<main><section class="section section-navy"><div class="container"><div class="brand-index-grid">{brand_cards}</div><p class="brands-note">Независимая мастерская. Не является официальным сервисным центром и не аффилирована с указанными производителями. Все товарные знаки принадлежат их правообладателям.</p></div></section>'''
      + block_process('../') + block_prices('../') + block_faq('../') + block_contacts('../') + '</main>')
(ROOT/'brands'/'index.html').write_text(doc('Ремонт часов Rolex, Patek Philippe, Omega и других брендов','Независимое обслуживание часов ведущих швейцарских и международных мануфактур в Москве.',body,1,route="/brands/",trail=[('Бренды','/brands/')],schema_extra=[{'@type':'ItemList','itemListElement':[{'@type':'ListItem','position':i+1,'name':name,'url':ORIGIN+f'/brands/{slug}/'} for i,(slug,name) in enumerate(featured_brands)]}]),encoding='utf-8')
# Русское написание марок: так ищут заметную часть запросов (Wordstat, Москва, 10.2026:
# «ремонт часов омега» 70 против «omega» 9, «радо» 46 против 28, «картье» 22 против 9)
BRAND_RU = {
    'rolex': 'Ролекс', 'patek-philippe': 'Патек Филипп', 'audemars-piguet': 'Одемар Пиге',
    'vacheron-constantin': 'Вашерон Константин', 'breguet': 'Бреге', 'jaeger-lecoultre': 'Жагер-Лекультр',
    'a-lange-soehne': 'Ланге и Зёне', 'omega': 'Омега', 'cartier': 'Картье', 'blancpain': 'Бланпен',
    'iwc': 'ИВЦ Шаффхаузен', 'zenith': 'Зенит', 'ulysse-nardin': 'Улисс Нардин', 'girard-perregaux': 'Жирар-Перрего',
    'hublot': 'Хублот', 'panerai': 'Панерай', 'chopard': 'Шопард', 'piaget': 'Пьяже', 'franck-muller': 'Франк Мюллер',
    'parmigiani': 'Пармиджани', 'h-moser': 'Мозер', 'breitling': 'Брайтлинг', 'tag-heuer': 'Таг Хоер',
    'tudor': 'Тюдор', 'grand-seiko': 'Гранд Сейко', 'seiko': 'Сейко', 'longines': 'Лонжин', 'rado': 'Радо', 'tissot': 'Тиссот',
    'maurice-lacroix': 'Морис Лакруа', 'frederique-constant': 'Фредерик Констант', 'oris': 'Орис',
}
# Свой текст для марок со спросом (Wordstat, Москва, 10.2026) — общие сведения о механизмах
# и типичных работах, без обещаний конкретного ремонта
BRAND_TEXT = json.loads((ROOT/'data/brand_texts.json').read_text())
for i,(slug,name) in enumerate(brands):
    ru = BRAND_RU[slug]
    brand_extra = ''.join(f'<h3>{escape(h)}</h3><p class="copy">{escape(t)}</p>' for h, t in BRAND_TEXT.get(slug, []))
    d=ROOT/'brands'/slug; d.mkdir(parents=True,exist_ok=True)
    bc=breadcrumbs([('Бренды','../'),(name,None)],'../../')
    intro=(f'<section class="section section-dark"><div class="container brand-intro">'
           f'<div class="brand-intro-copy reveal"><div class="eyebrow">Независимая мастерская</div>'
           f'<h2 class="display display-md">Обслуживание часов {escape(ru)}</h2>'
           f'<p class="lead">Диагностика начинается с конкретной модели, состояния и истории часов — не с универсального прайса.</p>'
           f'<p class="copy">Для разных калибров, поколений и корпусов перечень возможных работ отличается. '
           f'Перед началом вмешательства мастерская подтверждает техническую возможность ремонта и согласовывает объём работ.</p>'
           f'{brand_extra}'
           f'<a class="btn" href="{PHONE_HREF}">Позвонить {PHONE}</a></div>'
           f'<div class="brand-intro-side reveal"><div class="brand-mark"><span>{escape(name)}</span></div>'
           f'<ul class="detail-list"><li>Диагностика механизма</li><li>Проверка состояния корпуса и внешних элементов</li>'
           f'<li>Согласование ремонта или обслуживания</li><li>Контроль после выполненных работ</li></ul>'
           f'<p class="small">Независимая мастерская. Упоминание {escape(name)} не означает официальную аффилиацию '
           f'или авторизацию производителя.</p></div></div></section>')
    body=(video_hero(f'Ремонт часов {name}', 'Марка часов', bc, '../../',
                     f'Диагностика, обслуживание и восстановление часов {name} ({ru}) в Москве.')
          + '<main>' + intro + block_process('../../') + block_triptych('../../')
          + block_prices('../../') + block_faq('../../') + block_contacts('../../') + '</main>')
    brand_node = {'@type': 'Service', '@id': ORIGIN + f'/brands/{slug}/#service',
                  'name': f'Ремонт часов {name}',
                  'alternateName': f'Ремонт часов {ru}',
                  'description': f'Диагностика и обслуживание часов {name} в независимой мастерской в Москве. Не официальный сервисный центр.',
                  'serviceType': 'Ремонт и обслуживание часов',
                  'provider': {'@id': BIZ_ID},
                  'areaServed': {'@type': 'City', 'name': 'Москва'}}
    d.joinpath('index.html').write_text(doc(f'Ремонт часов {name} ({ru}) в Москве — независимая мастерская',f'Ремонт часов {ru} ({name}) в Москве: диагностика и обслуживание в независимой мастерской на Петровке.',body,2,route=f"/brands/{slug}/",trail=[('Бренды','/brands/'),(name,f'/brands/{slug}/')],schema_extra=[brand_node]),encoding='utf-8')

# PRICES
(ROOT/'prices').mkdir(exist_ok=True)
cats=[('Механизм',['Диагностика — после осмотра','Полное обслуживание — после диагностики','Ремонт отдельных узлов — после диагностики','Автоподзавод — после диагностики']),('Корпус и браслет',['Полировка корпуса — после оценки состояния','Сатинирование — после оценки геометрии','Работы с браслетом — по модели']),('Стекло',['Замена стекла — по модели и типу стекла','Посадка и проверка — по задаче']),('Герметичность',['Проверка герметичности — по модели','Замена уплотнений — после осмотра']),('Сложные механизмы',['Хронограф — индивидуально','Турбийон и усложнения — только после предварительной диагностики'])]
price_cats=''.join([f'''<div class="price-category"><button><span>{escape(name)}</span><span>+</span></button><div class="price-category-body">{''.join([f'<div class="price-table-row"><span>{escape(row.split(" — ")[0])}</span><span>{escape(row.split(" — ")[1])}</span></div>' for row in rows])}</div></div>''' for name,rows in cats])
body=(video_hero('Цены','Цены: сначала согласование',breadcrumbs([('Цены',None)],'../'),'../',
                'Структура стоимости обслуживания часов. Итог подтверждается после диагностики.')
      + f'''<main><section class="section section-navy"><div class="container price-layout"><div><div class="eyebrow">Как считается стоимость</div><h2 class="display display-md">Точная цена — после диагностики.</h2><a class="btn mt-28" href="{PHONE_HREF}">Позвонить {PHONE}</a></div><div class="price-accordion">{price_cats}</div></div></section>'''
      + block_process('../') + block_faq('../') + block_contacts('../') + '</main>')
(ROOT/'prices'/'index.html').write_text(doc('Цены на ремонт и обслуживание часов','Структура стоимости обслуживания часов: механизм, корпус, стекло, герметичность и сложные калибры.',body,1,route="/prices/",trail=[('Цены','/prices/')]),encoding='utf-8')

# ATELIER
(ROOT/'atelier').mkdir(exist_ok=True)
body=(video_hero('Часовая мастерская на Петровке','Мастерская и ремесло',breadcrumbs([('Мастерская',None)],'../'),'../',
                'Как устроена работа с изделием: осмотр, согласование, вмешательство и контроль.')
      + '''<main><section class="section section-dark"><div class="container craft-grid"><div class="media-frame"><img src="../assets/images/watchmaker.webp" alt="Часовщик за работой"><video autoplay muted loop playsinline poster="../assets/images/watchmaker.webp"><source src="../assets/videos/watchmaker.mp4" type="video/mp4"></video><div class="media-caption"><span>Ручная работа · макросъёмка</span><span>01</span></div></div><div class="craft-copy"><div><div class="eyebrow">Точность важнее оформления</div><h2 class="display display-md">Как мы работаем с часами.</h2><p class="copy">Каждые часы проходят один и тот же путь: осмотр, согласование, работа и проверка. Без сюрпризов в счёте и без лишнего вмешательства в механизм.</p></div></div></div></section>'''
      + block_process('../') + block_triptych('../') + block_prices('../') + block_contacts('../') + '</main>')
(ROOT/'atelier'/'index.html').write_text(doc('Часовая мастерская на Петровке','Независимая часовая мастерская: процесс обслуживания, работа мастера и макросъёмка механики.',body,1,route="/atelier/",trail=[('Мастерская','/atelier/')]),encoding='utf-8')

# CONTACTS
(ROOT/'contacts').mkdir(exist_ok=True)
body=(video_hero('Контакты часовой мастерской','Петровка · Москва',breadcrumbs([('Контакты',None)],'../'),'../',
                'Запись на диагностику и обслуживание часов в мастерской на Петровке.')
      + '<main>' + block_contacts('../') + block_prices('../') + block_faq('../') + '</main>')
(ROOT/'contacts'/'index.html').write_text(doc('Контакты часовой мастерской на Петровке','Запись на диагностику и обслуживание часов в независимой мастерской на Петровке в Москве.',body,1,route="/contacts/",trail=[('Контакты','/contacts/')],schema_extra=[{'@type':'ContactPage','@id':ORIGIN+'/contacts/#contact','mainEntity':{'@id':BIZ_ID}}]),encoding='utf-8')

# ARTICLES
ARTICLES = json.loads((ROOT/'data/articles.json').read_text())
(ROOT/'articles').mkdir(exist_ok=True)
article_cards = ''.join(
    f'<a class="content-card" href="{a["slug"]}/"><div><div class="eyebrow">{i+1:02} / Статья</div>'
    f'<h2>{escape(a["title"])}</h2><p>{escape(a["description"])}</p></div><span>Читать</span></a>'
    for i, a in enumerate(ARTICLES))
body = (video_hero('Статьи о часах', 'Полезно знать', breadcrumbs([('Статьи', None)], '../'), '../',
                   'Как ухаживать за часами и когда пора к мастеру.')
        + f'<main><section class="section section-dark pt-0"><div class="container content-grid">{article_cards}</div></section>'
        + block_contacts('../') + '</main>')
(ROOT/'articles'/'index.html').write_text(doc('Статьи о ремонте и обслуживании часов — часовая мастерская',
    'Полезные статьи о механических и кварцевых часах: обслуживание, точность хода, влага, намагничивание.',
    body, 1, route='/articles/', trail=[('Статьи', '/articles/')]), encoding='utf-8')
for a in ARTICLES:
    d = ROOT/'articles'/a['slug']; d.mkdir(parents=True, exist_ok=True)
    route = f'/articles/{a["slug"]}/'
    sections = ''.join(f'<h2>{escape(h)}</h2><p>{escape(t)}</p>' for h, t in a['sections'])
    related = ''.join(f'<li><a href="../../{href}">{escape(n)}</a></li>' for n, href in a['related'])
    article = (f'<section class="section section-ivory"><div class="container narrow article-body reveal">'
               f'<p class="lead">{escape(a["lead"])}</p>{sections}'
               f'<div class="article-related"><div class="eyebrow">Услуги по теме</div><ul>{related}</ul></div>'
               f'</div></section>')
    body = (video_hero(a['title'], 'Статья', breadcrumbs([('Статьи', '../'), (a['title'], None)], '../../'), '../../')
            + '<main>' + article + block_contacts('../../') + '</main>')
    node = {'@type': 'Article', 'headline': a['title'], 'description': a['description'],
            'inLanguage': 'ru', 'mainEntityOfPage': ORIGIN + route,
            'author': {'@id': BIZ_ID}, 'publisher': {'@id': BIZ_ID}, 'datePublished': '2026-10-06'}
    d.joinpath('index.html').write_text(doc(a['meta_title'], a['description'], body, 2, route=route,
        trail=[('Статьи', '/articles/'), (a['title'], route)], schema_extra=[node]), encoding='utf-8')

# PRIVACY
# Оператор указан по данным сайта; ФИО/ИНН владельца — добавить, когда пришлют (TODO-CONTENT.md)
(ROOT/'privacy').mkdir(exist_ok=True)
PRIVACY = [
    ('Общие положения', f'Настоящая политика описывает, как часовая мастерская на Петровке (сайт {CONFIG["production_origin_human"]}) обрабатывает персональные данные посетителей сайта в соответствии с Федеральным законом № 152-ФЗ «О персональных данных».'),
    ('Какие данные мы получаем', 'Номер телефона, имя и текст сообщения, которые вы указываете в форме заявки, а также технические данные посещения сайта, которые собирает сервис Яндекс Метрика: IP-адрес, сведения о браузере и устройстве, файлы cookie, страницы просмотра.'),
    ('Зачем', 'Чтобы связаться с вами по заявке, ответить на вопрос и записать на диагностику, а также чтобы анализировать посещаемость и улучшать сайт. Данные не используются для рассылок без вашего отдельного согласия.'),
    ('Передача третьим лицам', 'Данные заявки передаются мастерской через защищённый канал связи и не продаются и не передаются третьим лицам, кроме случаев, предусмотренных законом. Статистика посещений обрабатывается сервисом Яндекс Метрика по правилам ООО «Яндекс».'),
    ('Сроки хранения', 'Данные заявок хранятся не дольше, чем это нужно для ответа на обращение и выполнения работ, после чего удаляются.'),
    ('Ваши права', f'Вы можете запросить сведения о своих данных, их исправление или удаление, а также отозвать согласие на обработку, написав на {CONTACTS["email"]} или позвонив по телефону {PHONE}.'),
]
privacy_html = ''.join(f'<h2>{escape(h)}</h2><p>{escape(t)}</p>' for h, t in PRIVACY)
body = (page_hero('Политика обработки персональных данных', 'Документы', 1, media=None,
                  breadcrumbs_html=breadcrumbs([('Политика конфиденциальности', None)], '../'))
        + f'<main><section class="section section-ivory"><div class="container narrow article-body">{privacy_html}</div></section></main>')
(ROOT/'privacy'/'index.html').write_text(doc('Политика обработки персональных данных — часовая мастерская',
    'Как часовая мастерская на Петровке обрабатывает персональные данные посетителей сайта и заявок.',
    body, 1, route='/privacy/', trail=[('Политика конфиденциальности', '/privacy/')]), encoding='utf-8')

# Preview URLs remain crawlable so crawlers can read noindex.
robots_text = 'User-agent: *\nDisallow:\n'
robots_text += ('Sitemap: ' + CONFIG['production_origin'] + '/sitemap.xml\n') if CONFIG['environment'] == 'production' else '# Preview: all HTML pages use noindex.\n'
(ROOT/'robots.txt').write_text(robots_text, encoding='utf-8')
urls = ''.join(f'<url><loc>{escape(CONFIG["production_origin"] + route)}</loc></url>' for route, approved in PAGES if approved)
(ROOT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + urls + '</urlset>\n', encoding='utf-8')
print('Built', len(PAGES), 'pages in', ROOT)
