"""Genera le pagine statiche della bozza Torre Gialluise nella cartella del progetto."""
import json
from pathlib import Path
from urllib.parse import quote

SRC = Path(__file__).parent
OUT = SRC.parent
IMG = json.loads((SRC / "images.json").read_text())
CSS = (SRC / "style.css").read_text(encoding="utf-8")

SITE = "https://fraspin02.github.io/tacard-trunfio-bozza/"
TEL = "+393336629229"
TEL_TXT = "333 662 9229"
WA = "https://wa.me/393336629229"
MAPS = "https://www.google.com/maps/dir/?api=1&destination=40.9926,15.0762"
OSM = "https://www.openstreetmap.org/?mlat=40.9926&mlon=15.0762#map=15/40.9926/15.0762"


def wa(text):
    return f"{WA}?text={quote(text)}"


def todo(t="da inserire"):
    return f'<span class="todo">[{t}]</span>'


def pic(name, alt, sizes, cls="", eager=False, w=None):
    m = IMG[name]
    srcset = ", ".join(f"img/{name}-{s}.webp {s}w" for s in m["sizes"])
    src = f"img/{name}-{m['sizes'][min(1, len(m['sizes']) - 1)]}.webp"
    load = 'fetchpriority="high" decoding="async"' if eager else 'loading="lazy" decoding="async"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="{src}" srcset="{srcset}" sizes="{sizes}" width="{m["w"]}" height="{m["h"]}" '
            f'alt="{alt}" {load}>')


ICONS = {
    "phone": '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/>',
    "chat": '<path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/><path d="M8.5 10.5h.01M12 10.5h.01M15.5 10.5h.01"/>',
    "bag": '<path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4Z"/><path d="M3 6h18"/><path d="M16 10a4 4 0 0 1-8 0"/>',
    "menu": '<path d="M4 6h16M4 12h16M4 18h16"/>',
    "x": '<path d="M18 6 6 18M6 6l12 12"/>',
    "pin": '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>',
    "arrow": '<path d="M5 12h14M12 5l7 7-7 7"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "alert": '<circle cx="12" cy="12" r="10"/><path d="M12 8v4M12 16h.01"/>',
}
SPRITE = '<svg width="0" height="0" style="position:absolute" aria-hidden="true">' + "".join(
    f'<symbol id="i-{k}" viewBox="0 0 24 24">{v}</symbol>' for k, v in ICONS.items()) + "</svg>"


def ico(name, cls="i"):
    return f'<svg class="{cls}" aria-hidden="true"><use href="#i-{name}"/></svg>'


ERR = ico("alert")

NAV = [("index.html", "Il casale"), ("camere.html", "Camere"), ("cucina-eventi.html", "Cucina ed eventi"),
       ("bottega.html", "Bottega"), ("index.html#dove", "Dove siamo")]

# ---------------------------------------------------------------- prodotti (prezzi di esempio)
PRODUCTS = [
    {"slug": "olio-evo", "name": "Olio extravergine d'oliva", "size": "Bottiglia 0,75 l", "price": 14.0, "img": "olive",
     "short": "Dagli ulivi intorno al casale.",
     "long": "Olio extravergine dalle olive dei nostri ulivi, sulle colline tra Gesualdo e Villamaina. Lo usiamo ogni giorno nella cucina dell'agriturismo.",
     "facts": [("Varietà", todo()), ("Annata", todo()), ("Frantoio", todo())]},
    {"slug": "olio-evo-latta", "name": "Olio extravergine d'oliva", "size": "Latta 3 l", "price": 45.0, "img": "ulivo",
     "short": "La scorta per la dispensa di casa.",
     "long": "Lo stesso olio dei nostri ulivi, in latta da 3 litri: protegge l'olio dalla luce e dura fino al raccolto successivo.",
     "facts": [("Varietà", todo()), ("Annata", todo())]},
    {"slug": "vino-rosso", "name": "Vino rosso della casa", "size": "Bottiglia 0,75 l", "price": 10.0, "img": "uva",
     "short": "Dalla vigna accanto al casale.",
     "long": "Il vino che serviamo a tavola, fatto con l'uva della vigna dell'agriturismo. Rosso, da pasto, da bere con i salumi e la carne.",
     "facts": [("Vitigno", todo()), ("Gradazione", todo()), ("Annata", todo())]},
    {"slug": "farina", "name": "Farina di grano", "size": "Sacchetto 1 kg", "price": 3.5, "img": "colline",
     "short": "Dai campi di cereali dell'azienda.",
     "long": "Farina dal grano coltivato nei campi dell'azienda agricola, in Irpinia. Per pane, pasta fatta in casa e dolci.",
     "facts": [("Tipo di grano", todo()), ("Macinatura", todo())]},
    {"slug": "peperoni-secchi", "name": "Peperoni secchi", "size": "Busta 100 g", "price": 6.0, "img": "peperoni",
     "short": "Da friggere: diventano cruschi.",
     "long": "Peperoni seccati al sole, appesi come si fa da sempre sotto il pergolato. Fritti pochi secondi nell'olio diventano cruschi.",
     "facts": [("Provenienza", todo())]},
    {"slug": "legumi", "name": "Legumi secchi", "size": "Sacchetto 500 g", "price": 4.0, "img": None,
     "short": "Dalla stessa terra dei cereali.",
     "long": "Legumi secchi della nostra azienda agricola, per zuppe e minestre d'inverno.",
     "facts": [("Varietà", todo()), ("Foto", todo())]},
]
PBY = {p["slug"]: p for p in PRODUCTS}


def product_js():
    return json.dumps({p["slug"]: {"name": p["name"], "size": p["size"], "price": p["price"],
                                   "img": f"img/{p['img']}-480.webp" if p["img"] else None} for p in PRODUCTS},
                      ensure_ascii=False)


def eur(n):
    return f"{n:,.2f} €".replace(",", "X").replace(".", ",").replace("X", ".")


# ---------------------------------------------------------------- layout
def head(title, desc, path, extra=""):
    url = SITE + ("" if path == "index.html" else path)
    return f"""<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#F4EFE6">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:locale" content="it_IT">
<meta property="og:site_name" content="Agriturismo Torre Gialluise">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="preload" href="fonts/newsreader-latin-500-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="fonts/work-sans-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
{extra}<style>{CSS}</style>
</head>
"""


def header(active):
    cur = ' aria-current="page"'
    links = "".join(f'<a href="{h}"{cur if h == active else ""}>{t}</a>' for h, t in NAV)
    return f"""<body>
{SPRITE}
<a class="skip" href="#main">Vai al contenuto</a>
<header class="hdr">
 <div class="wrap hdr__in">
  <a class="brand" href="index.html" translate="no"><b>Torre Gialluise</b><small>Agriturismo · Irpinia</small></a>
  <nav class="nav" aria-label="Principale">{links}</nav>
  <button class="ico-btn cart-btn" type="button" aria-label="Carrello, vuoto" aria-controls="cart">{ico("bag")}<span class="badge" hidden>0</span></button>
  <a class="ico-btn ico-btn--tel" href="tel:{TEL}" aria-label="Chiama il {TEL_TXT}">{ico("phone")}<span class="lbl">{TEL_TXT}</span></a>
  <a class="ico-btn ico-btn--wa" href="{wa("Buongiorno, vorrei avere informazioni sull'agriturismo.")}" aria-label="WhatsApp, scriveteci">{ico("chat")}<span class="lbl">WhatsApp</span></a>
  <button class="ico-btn menu-btn" type="button" aria-expanded="false" aria-controls="mnav" aria-label="Apri menu"><svg class="i" aria-hidden="true"><use href="#i-menu"/></svg></button>
 </div>
 <nav id="mnav" class="mnav" aria-label="Menu" hidden>{links}
  <div class="btn-row"><a class="btn btn--line" href="tel:{TEL}">{ico("phone")} Chiama</a><a class="btn btn--olive" href="{WA}">{ico("chat")} WhatsApp</a></div>
 </nav>
</header>
"""


def footer():
    return f"""<footer class="ftr">
 <div class="wrap">
  <div class="ftr__grid">
   <div>
    <h2>Torre Gialluise</h2>
    <p>Agriturismo con camere, cucina ed eventi tra Gesualdo e Villamaina, in Irpinia.</p>
    <p><a href="tel:{TEL}">{TEL_TXT}</a> · <a href="{WA}">WhatsApp</a><br>Email {todo()}</p>
   </div>
   <div>
    <h3>Pagine</h3>
    <ul>{"".join(f'<li><a href="{h}">{t}</a></li>' for h, t in NAV)}<li><a href="checkout.html">Checkout</a></li></ul>
   </div>
   <div>
    <h3>Dove siamo</h3>
    <p>Via Cupa del Paradiso, SS 428<br>83040 Gesualdo (AV)</p>
    <p><a href="{MAPS}" rel="noopener">Indicazioni stradali</a></p>
   </div>
  </div>
  <div class="ftr__legal">
   <p>Società Agricola T.A.C.A.R.D. S.a.s. di Raffaele Trunfio &amp; C. · Piazza Risorgimento 1, 83050 Villamaina (AV) · P.IVA 02667150649</p>
   <p>CIN {todo()} · Privacy e cookie {todo()} · Foto: Agriturismo Torre Gialluise</p>
   <p>Bozza dimostrativa: testi, prezzi e moduli sono di esempio, nessun dato viene inviato.</p>
  </div>
 </div>
</footer>
<div id="cart" class="drawer" role="dialog" aria-modal="true" aria-labelledby="cart-t" hidden>
 <button class="drawer__bg" type="button" data-close-cart tabindex="-1" aria-label="Chiudi il carrello"></button>
 <div class="drawer__panel">
  <div class="drawer__hd"><h2 id="cart-t">Il vostro carrello</h2><button class="ico-btn drawer__close" type="button" data-close-cart aria-label="Chiudi il carrello">{ico("x")}</button></div>
  <ul id="cart-list" class="drawer__list"></ul>
  <div id="cart-empty" class="empty"><p>Il carrello è vuoto.<br>Date un'occhiata alla bottega.</p><a class="btn btn--line" href="bottega.html">Vai alla bottega</a></div>
  <div id="cart-ft" class="drawer__ft" hidden>
   <div class="row"><span>Subtotale</span><b id="cart-sub">0,00 €</b></div>
   <div class="row"><span>Spedizione</span><span>calcolata al checkout</span></div>
   <a class="btn btn--main" href="checkout.html">Vai al checkout {ico("arrow")}</a>
   <button class="btn btn--line" type="button" data-close-cart style="width:100%;margin-top:8px">Continua a guardare</button>
  </div>
 </div>
</div>
<p id="cart-live" class="visually-hidden" aria-live="polite"></p>
<script src="app.js" defer></script>
</body>
</html>
"""


def page(path, title, desc, body, extra="", active=None):
    html = head(title, desc, path, extra) + header(active or path) + f'<main id="main">{body}</main>\n' + footer()
    (OUT / path).write_text(html, encoding="utf-8")
    print("scritto", path, len(html) // 1024, "KB")


def product_card(p):
    img = (pic(p["img"], "", "(min-width:960px) 270px, (min-width:640px) 45vw, 100vw", "card__img")
           if p["img"] else f'<div class="noimg">Foto prodotto {todo()}</div>')
    return f"""<article class="card">
 <a href="prodotto-{p['slug']}.html" tabindex="-1" aria-hidden="true">{img}</a>
 <div class="card__body">
  <h3><a href="prodotto-{p['slug']}.html" style="color:inherit;text-decoration:none">{p['name']}</a></h3>
  <span class="card__meta">{p['size']}</span>
  <p>{p['short']}</p>
  <div class="card__foot"><span><span class="price">{eur(p['price'])}</span> <span class="price-tag">esempio</span></span>
  <button class="btn btn--main add" type="button" data-add="{p['slug']}">Aggiungi <span class="visually-hidden">{p['name']} {p['size']}</span></button></div>
 </div>
</article>"""


# ---------------------------------------------------------------- HOME
ROOMS = [
    {"id": "balcone", "name": "Camera con balcone", "img": "camera-balcone", "mq": 23, "ospiti": "fino a 4 ospiti",
     "letti": "letto matrimoniale grande e divano letto", "extra": ["bagno privato con vasca", "balcone con vista sulle colline"],
     "alt": "Camera con letto matrimoniale in ferro battuto e pavimento in cotto"},
    {"id": "terrazza", "name": "Camera con terrazza", "img": "camera-letto-aggiunto", "mq": 20, "ospiti": "2 ospiti, più un letto aggiunto",
     "letti": "letto matrimoniale grande", "extra": ["bagno privato con doccia", "terrazza privata vista montagna"],
     "alt": "Camera matrimoniale luminosa con copriletto chiaro"},
    {"id": "doppia", "name": "Camera doppia", "img": "camera-doppia", "mq": 20, "ospiti": "2 ospiti",
     "letti": "letto matrimoniale grande", "extra": ["bagno privato con doccia", "scrivania e TV, vista sul giardino"],
     "alt": "Camera doppia con letto in ferro battuto e specchio"},
]
COMMON = ["ingresso indipendente", "aria condizionata e riscaldamento", "Wi-Fi gratuito"]

QUOTES = [
    ("Il posto è bellissimo, in un casale ristrutturato con cura e mantenuto con passione.", "Ospite su Trip.com, agosto 2024"),
    ("Menu ottimo. Antipasto con una ricotta di Carmasciano altissimo livello.", "Recensione su Restaurant Guru"),
    ("Grande ospitalità, ottimo cibo e tanta gentilezza.", "Fortunato C., Restaurant Guru"),
]


def home():
    hero_pre = (f'<link rel="preload" as="image" type="image/webp" fetchpriority="high" '
                f'imagesrcset="{", ".join(f"img/hero-{s}.webp {s}w" for s in IMG["hero"]["sizes"])}" '
                f'imagesizes="(min-width:880px) 520px, calc(100vw - 32px)">\n')
    rooms = "".join(f"""<a class="card" href="camere.html#{r['id']}">
 {pic(r['img'], r['alt'], "(min-width:960px) 360px, (min-width:640px) 45vw, 100vw", "card__img")}
 <div class="card__body"><h3>{r['name']}</h3><span class="card__meta">{r['mq']} m² · {r['ospiti']}</span>
 <p>{r['extra'][1].capitalize()}.</p><span class="link-arrow">Vedi la camera {ico("arrow")}</span></div></a>""" for r in ROOMS)
    shop = "".join(product_card(p) for p in PRODUCTS[:4])
    quotes = "".join(f'<blockquote class="quote"><p>“{q}”</p><footer>{s}</footer></blockquote>' for q, s in QUOTES)
    body = f"""
<section class="hero">
 <div class="wrap hero__grid">
  <div>
   <span class="eyebrow">Agriturismo tra Gesualdo e Villamaina</span>
   <h1>Torre Gialluise <span class="it">casale in pietra sulle colline dell'Irpinia</span></h1>
   <p class="lead">Tre camere con vista, la cucina di casa, il vino e l'olio della nostra terra. A 1,6 km dal Castello di Gesualdo.</p>
   <div class="btn-row">
    <a class="btn btn--main" href="{wa("Buongiorno, vorrei sapere se avete camere libere per queste date: ")}">{ico("chat")} Scrivici su WhatsApp</a>
    <a class="btn btn--line" href="camere.html">Vedi le camere</a>
   </div>
   <p class="hero__note">{ico("phone")} <span>Oppure chiamate il <a href="tel:{TEL}">{TEL_TXT}</a></span></p>
  </div>
  <div class="arch">{pic("hero", "Il casale-torre in pietra di Torre Gialluise tra gli ulivi, sotto un cielo con nuvole", "(min-width:880px) 520px, calc(100vw - 32px)", "hero__img", eager=True)}</div>
 </div>
</section>

<section class="sec sec--alt" id="casale" aria-labelledby="casale-t">
 <div class="wrap split">
  <div class="mosaic">
   <div class="rimg">{pic("scala", "Scala esterna in pietra del casale con lavanda in fiore", "(min-width:880px) 300px, 55vw")}</div>
   <div class="rimg">{pic("sala", "Sala da pranzo con archi in pietra e tavolo in legno", "(min-width:880px) 240px, 45vw")}</div>
   <div class="rimg">{pic("pergolato", "Pergolato in legno con peperoni appesi e vista sulla campagna", "(min-width:880px) 240px, 45vw")}</div>
  </div>
  <div>
   <span class="eyebrow">Il casale</span>
   <h2 id="casale-t">Una torre di pietra in mezzo alla campagna</h2>
   <p>Torre Gialluise è un casale storico in pietra, sulla strada tra Gesualdo e Villamaina. Lo abbiamo ristrutturato tenendo gli archi, le travi in legno e i muri di una volta.</p>
   <p>Intorno ci sono gli ulivi, la vigna e i campi della nostra azienda agricola. Dalla terrazza si vedono le colline dell'Irpinia e il borgo di Gesualdo.</p>
   <dl class="facts">
    <div><dt>3 camere</dt><dd>con bagno privato e ingresso indipendente</dd></div>
    <div><dt>1,6 km</dt><dd>dal Castello di Gesualdo</dd></div>
    <div><dt>Vino e olio</dt><dd>dalla vigna e dagli ulivi di casa</dd></div>
    <div><dt>Eventi</dt><dd>battesimi, comunioni, feste e pranzi</dd></div>
   </dl>
  </div>
 </div>
</section>

<section class="sec" aria-labelledby="camere-t">
 <div class="wrap">
  <div class="sec-head"><span class="eyebrow">Dormire</span><h2 id="camere-t">Tre camere, tutte con vista</h2>
  <p class="lead">Camere ampie con il pavimento in cotto, bagno privato e ingresso indipendente. La mattina, colazione con i dolci fatti in casa.</p></div>
  <div class="grid grid--3">{rooms}</div>
  <p style="margin-top:24px"><a class="btn btn--olive" href="camere.html#prenota">Chiedi disponibilità</a></p>
 </div>
</section>

<section class="sec sec--alt" aria-labelledby="cucina-t">
 <div class="wrap split split--rev">
  <div class="mosaic">
   <div class="rimg">{pic("tavolata", "Tavola apparecchiata con tovaglia a maioliche, antipasti e vino", "(min-width:880px) 300px, 55vw")}</div>
   <div class="rimg">{pic("peperoni", "Collana di peperoni rossi appesa a un muro in pietra", "(min-width:880px) 240px, 45vw")}</div>
   <div class="rimg">{pic("colazione", "Crostata, cornetti e dolci fatti in casa per la colazione", "(min-width:880px) 240px, 45vw")}</div>
  </div>
  <div>
   <span class="eyebrow">La cucina</span>
   <h2 id="cucina-t">I piatti di casa, con quello che abbiamo intorno</h2>
   <p>Salumi, ricotta di Carmasciano, pasta fatta a mano e carne cotta con calma. Il vino è quello della nostra vigna.</p>
   <ul class="ticks">
    <li>{ico("check")}<span>Antipasto della casa con salumi e ricotta di Carmasciano</span></li>
    <li>{ico("check")}<span>Ravioli e fusilli fatti in casa</span></li>
    <li>{ico("check")}<span>Maialino con patate e peperoni cruschi</span></li>
   </ul>
   <p>Il ristorante lavora su prenotazione. Orari {todo()}</p>
   <div class="btn-row"><a class="btn btn--main" href="{wa("Buongiorno, vorrei prenotare un tavolo per ")}">Prenota un tavolo</a><a class="link-arrow" href="cucina-eventi.html">Vedi il menù {ico("arrow")}</a></div>
  </div>
 </div>
</section>

<section class="sec" aria-labelledby="eventi-t">
 <div class="wrap">
  <div class="grid grid--2" style="align-items:stretch">
   <a class="tile" href="cucina-eventi.html#eventi">{pic("evento-torta", "Torta a piani decorata con fiori davanti al casale", "(min-width:640px) 45vw, 100vw")}<div class="tile__t"><h3>Battesimi e comunioni</h3><span>Pranzi in terrazza o in sala</span></div></a>
   <a class="tile" href="cucina-eventi.html#eventi">{pic("arco-sera", "Tavolata sotto un arco in pietra al tramonto", "(min-width:640px) 45vw, 100vw")}<div class="tile__t"><h3>Feste e pranzi di famiglia</h3><span>Compleanni, anniversari, incontri</span></div></a>
  </div>
  <div class="sec-head" style="margin:28px 0 0">
   <span class="eyebrow">Eventi</span>
   <h2 id="eventi-t">La vostra festa, in campagna</h2>
   <p class="lead">Organizziamo pranzi per battesimi, comunioni, compleanni e anniversari, con il menù concordato insieme e gli spazi solo per voi.</p>
   <a class="btn btn--olive" href="cucina-eventi.html#preventivo">Chiedi un preventivo</a>
  </div>
 </div>
</section>

<section class="sec sec--alt" aria-labelledby="bottega-t">
 <div class="wrap">
  <div class="sec-head"><span class="eyebrow">La bottega</span><h2 id="bottega-t">Portate a casa i nostri prodotti</h2>
  <p class="lead">Olio, vino, farina e legumi della nostra azienda agricola. Spedizione in Italia o ritiro all'agriturismo.</p></div>
  <div class="grid grid--4">{shop}</div>
  <p style="margin-top:24px"><a class="link-arrow" href="bottega.html">Vedi tutti i prodotti {ico("arrow")}</a></p>
 </div>
</section>

<section class="sec sec--dark" aria-labelledby="rec-t">
 <div class="wrap">
  <span class="eyebrow">Recensioni</span>
  <h2 id="rec-t">Cosa dicono gli ospiti</h2>
  <ul class="scores">
   <li><b>9,3</b> su 10 su Booking</li>
   <li><b>4,8</b> su 5 su Google</li>
   <li><b>4,9</b> su 5 su Tripadvisor</li>
  </ul>
  <div class="quotes">{quotes}</div>
 </div>
</section>

<section class="sec" id="dove" aria-labelledby="dove-t">
 <div class="wrap where">
  <div>
   <span class="eyebrow">Dove siamo</span>
   <h2 id="dove-t">Sulla SS 428, tra Gesualdo e Villamaina</h2>
   <address class="addr">Agriturismo Torre Gialluise<br>Via Cupa del Paradiso, SS 428<br>83040 Gesualdo (AV)</address>
   <ul class="dist">
    <li><span>Castello di Gesualdo</span><span>1,6 km</span></li>
    <li><span>Santuario di San Gerardo, Materdomini</span><span>30 km</span></li>
    <li><span>Aeroporto di Napoli</span><span>87 km</span></li>
   </ul>
   <div class="btn-row"><a class="btn btn--olive" href="{MAPS}" rel="noopener">{ico("pin")} Indicazioni stradali</a><a class="link-arrow" href="{OSM}" rel="noopener">Apri la mappa {ico("arrow")}</a></div>
  </div>
  <div class="rimg">{pic("panorama", "Panorama sulle colline verdi dell'Irpinia visto dal casale", "(min-width:880px) 580px, 100vw")}</div>
 </div>
</section>

<section class="sec sec--dark cta" aria-labelledby="cta-t">
 <div class="wrap">
  <h2 id="cta-t">Volete venire a trovarci?</h2>
  <p class="lead">Per camere, tavoli ed eventi chiamate o scrivete: risponde la famiglia.</p>
  <a class="tel-big" href="tel:{TEL}">{TEL_TXT}</a>
  <div class="btn-row"><a class="btn btn--main" href="{WA}">{ico("chat")} Scrivici su WhatsApp</a><a class="btn btn--line" href="tel:{TEL}">{ico("phone")} Chiama</a></div>
 </div>
</section>
"""
    page("index.html", "Agriturismo Torre Gialluise · Camere e cucina tra Gesualdo e Villamaina",
         "Casale in pietra in Irpinia, a 1,6 km dal Castello di Gesualdo: tre camere con vista, cucina di casa, eventi, vino e olio dell'azienda.",
         body, hero_pre)


# ---------------------------------------------------------------- CAMERE
def field(id, label, kind="input", typ="text", req=True, err="", opt=False, full=False, extra="", options=None, help=""):
    lab = f'{label}{" <span class=opt>(facoltativo)</span>" if opt else ""}'
    desc = []
    if help:
        desc.append(f"{id}-h")
    if err:
        desc.append(f"{id}-e")
    d = f' aria-describedby="{" ".join(desc)}"' if desc else ""
    r = " required" if req else ""
    if kind == "select":
        ctl = f'<select id="{id}" name="{id}"{r}{d}{extra}>' + "".join(f"<option>{o}</option>" for o in options) + "</select>"
    elif kind == "textarea":
        ctl = f'<textarea id="{id}" name="{id}"{r}{d}{extra}></textarea>'
    else:
        ctl = f'<input id="{id}" name="{id}" type="{typ}"{r}{d}{extra}>'
    h = f'<p class="help" id="{id}-h">{help}</p>' if help else ""
    e = f'<p class="err" id="{id}-e" hidden>{ERR}{err}</p>' if err else ""
    return f'<div class="field{" full" if full else ""}"><label for="{id}">{lab}</label>{ctl}{h}{e}</div>'


def camere():
    rooms = "".join(f"""<article class="room" id="{r['id']}">
 <div class="rimg">{pic(r['img'], r['alt'], "(min-width:880px) 560px, 100vw", "room__img")}</div>
 <div>
  <h2>{r['name']}</h2>
  <ul class="room__spec"><li>{r['mq']} m²</li><li>{r['ospiti']}</li><li>{r['letti']}</li></ul>
  <ul class="ticks">{"".join(f"<li>{ico('check')}<span>{x.capitalize()}</span></li>" for x in r['extra'] + COMMON)}</ul>
  <p class="room__price">da {todo("prezzo")} a notte</p>
  <a class="btn btn--main" href="#prenota" data-room="{r['name']}">Chiedi disponibilità</a>
 </div>
</article>""" for r in ROOMS)
    form = f"""<form class="form" id="pren-form" data-demo="pren-ok" aria-labelledby="prenota-t">
 <div class="fgrid">
  {field("arrivo", "Arrivo", typ="date", err="Scegliete la data di arrivo")}
  {field("partenza", "Partenza", typ="date", err="La partenza deve essere dopo l'arrivo", extra=' data-after="arrivo"')}
  {field("ospiti", "Ospiti", "select", options=["2 adulti", "1 adulto", "2 adulti + 1 bambino", "2 adulti + 2 bambini", "3 adulti", "4 adulti"])}
  {field("camera", "Camera", "select", req=False, options=["Indifferente"] + [r["name"] for r in ROOMS])}
  {field("nome", "Nome", err="Inserite il vostro nome", extra=' autocomplete="name"')}
  {field("tel", "Telefono", typ="tel", err="Inserite un numero di telefono, ci serve per rispondervi", extra=' autocomplete="tel" inputmode="tel" data-rule="tel"')}
  {field("note", "Note", "textarea", req=False, opt=True, full=True, help="Per esempio: orario di arrivo, cena in agriturismo, allergie.")}
 </div>
 <p class="help" style="margin:16px 0">Vi rispondiamo su WhatsApp o al telefono, di solito in giornata.</p>
 <button class="btn btn--main" type="submit">Invia la richiesta</button>
</form>
<div class="done" id="pren-ok" hidden role="status"><h3>{ico("check")} Richiesta pronta</h3><p>Vi ricontattiamo al numero indicato per confermare la disponibilità.</p><p class="demo-note">Questa è una bozza: il modulo non invia ancora nulla.</p></div>"""
    body = f"""
<section class="phead"><div class="wrap">
 <p class="crumbs"><a href="index.html">Home</a> / Camere</p>
 <h1>Le camere</h1>
 <p class="lead">Tre camere nel casale in pietra, ognuna con bagno privato, ingresso indipendente e vista sulla campagna irpina.</p>
</div></section>
<section class="sec" style="padding-top:8px"><div class="wrap">{rooms}</div></section>
<section class="sec sec--alt" aria-labelledby="serv-t"><div class="wrap">
 <div class="sec-head"><h2 id="serv-t">Da sapere prima di arrivare</h2></div>
 <dl class="info">
  <div><dt>Check-in e check-out</dt><dd>Arrivo dalle 14 alle 20, partenza entro le 10.</dd></div>
  <div><dt>Colazione</dt><dd>Con dolci fatti in casa, frutta e succhi. Costo {todo()}</dd></div>
  <div><dt>Parcheggio e Wi-Fi</dt><dd>Gratuiti, nella proprietà.</dd></div>
  <div><dt>Bambini</dt><dd>Benvenuti, con area giochi in giardino. Culla su richiesta {todo("da verificare")}</dd></div>
  <div><dt>Animali</dt><dd>Non ammessi.</dd></div>
  <div><dt>Spazi comuni</dt><dd>Giardino, terrazza panoramica, area picnic.</dd></div>
 </dl>
</div></section>
<section class="sec" id="prenota" aria-labelledby="prenota-t"><div class="wrap split" style="align-items:start">
 <div><span class="eyebrow">Prenotazione diretta</span><h2 id="prenota-t">Chiedete la disponibilità</h2>
 <p class="lead">Scriveteci le date: vi rispondiamo noi, senza intermediari.</p>
 <p>Preferite parlare? Chiamate il <a href="tel:{TEL}">{TEL_TXT}</a> o <a href="{wa("Buongiorno, vorrei sapere se avete camere libere per queste date: ")}">scrivete su WhatsApp</a>.</p>
 <div class="rimg" style="margin-top:20px">{pic("terrazza", "Tavolino apparecchiato per la colazione sulla terrazza con vista", "(min-width:880px) 560px, 100vw")}</div></div>
 <div>{form}</div>
</div></section>
"""
    page("camere.html", "Camere · Agriturismo Torre Gialluise, Gesualdo",
         "Tre camere con bagno privato e vista sulle colline dell'Irpinia, nel casale in pietra tra Gesualdo e Villamaina. Chiedete la disponibilità.",
         body)


# ---------------------------------------------------------------- CUCINA ED EVENTI
MENU = [
    ("Antipasti", [("Antipasto della casa", "salumi, formaggi e ricotta di Carmasciano"), ("Verdure dell'orto", "secondo stagione")]),
    ("Primi", [("Ravioli fatti in casa", "ripieni di ricotta"), ("Fusilli al ferretto", "con crema di zucchine")]),
    ("Secondi", [("Maialino al forno", "con patate e peperoni cruschi"), ("Grigliata di carne", "carni del territorio")]),
    ("Dolci", [("Dolci della casa", "crostate e dolci del giorno")]),
]


def cucina():
    menu = "".join(f"""<div><h3>{cat}</h3><ul class="dishes">{"".join(
        f'<li><span><b>{n}</b><small>{d}</small></span><span class="pr">{todo("€")}</span></li>' for n, d in items)}</ul></div>"""
        for cat, items in MENU)
    form = f"""<form class="form" id="ev-form" data-demo="ev-ok" aria-labelledby="preventivo-t">
 <div class="fgrid">
  {field("tipo", "Tipo di evento", "select", options=["Battesimo", "Comunione", "Cresima", "Compleanno", "Anniversario", "Matrimonio", "Pranzo aziendale", "Altro"])}
  {field("data", "Data indicativa", typ="date", err="Scegliete una data, anche indicativa")}
  {field("invitati", "Numero di invitati", typ="number", err="Indicate quante persone, anche circa", extra=' min="1" inputmode="numeric"')}
  {field("ev-nome", "Nome", err="Inserite il vostro nome", extra=' autocomplete="name"')}
  {field("ev-tel", "Telefono", typ="tel", err="Inserite un numero di telefono, ci serve per rispondervi", extra=' autocomplete="tel" inputmode="tel" data-rule="tel"')}
  {field("ev-note", "Raccontateci l'evento", "textarea", req=False, opt=True, full=True, help="Pranzo o cena, esigenze alimentari, allestimenti.")}
 </div>
 <button class="btn btn--main" type="submit" style="margin-top:18px">Chiedi un preventivo</button>
</form>
<div class="done" id="ev-ok" hidden role="status"><h3>{ico("check")} Richiesta pronta</h3><p>Vi chiamiamo per parlare del menù e degli spazi.</p><p class="demo-note">Questa è una bozza: il modulo non invia ancora nulla.</p></div>"""
    body = f"""
<section class="phead"><div class="wrap">
 <p class="crumbs"><a href="index.html">Home</a> / Cucina ed eventi</p>
 <h1>Cucina ed eventi</h1>
 <p class="lead">A tavola mettiamo i piatti dell'Irpinia, i salumi, il vino della nostra vigna e l'olio dei nostri ulivi.</p>
</div></section>
<section class="sec" style="padding-top:8px" aria-labelledby="menu-t"><div class="wrap split" style="align-items:start">
 <div>
  <h2 id="menu-t">Il menù</h2>
  <p>Menù di esempio: i piatti cambiano con le stagioni. Prezzo medio 22–36 € a persona {todo("da confermare")}</p>
  <div class="grid">{menu}</div>
  <p style="margin-top:20px"><b>Orari del ristorante:</b> {todo()} · solo su prenotazione</p>
  <p>Allergie o intolleranze? Ditecelo quando prenotate: prepariamo anche piatti vegetariani e vegani.</p>
  <a class="btn btn--main" href="{wa("Buongiorno, vorrei prenotare un tavolo per ")}">{ico("chat")} Prenota un tavolo</a>
 </div>
 <div class="mosaic">
  <div class="rimg">{pic("tavola", "Tavola lunga apparecchiata all'aperto la sera", "(min-width:880px) 300px, 55vw")}</div>
  <div class="rimg">{pic("olive", "Olive nere sui rami degli ulivi dell'azienda", "(min-width:880px) 240px, 45vw")}</div>
  <div class="rimg">{pic("uva", "Grappoli d'uva nera nella vigna dell'agriturismo", "(min-width:880px) 240px, 45vw")}</div>
 </div>
</div></section>
<section class="sec sec--alt" id="eventi" aria-labelledby="ev-t"><div class="wrap split">
 <div class="mosaic">
  <div class="rimg">{pic("evento-fiori", "Allestimento con fiori bianchi per una cerimonia", "(min-width:880px) 300px, 55vw")}</div>
  <div class="rimg">{pic("sera", "Il casale illuminato di sera con i tavoli in giardino", "(min-width:880px) 240px, 45vw")}</div>
  <div class="rimg">{pic("arco-sera", "Tavolata sotto un arco in pietra al tramonto", "(min-width:880px) 240px, 45vw")}</div>
 </div>
 <div>
  <span class="eyebrow">Eventi</span>
  <h2 id="ev-t">Feste e cerimonie al casale</h2>
  <p>Battesimi, comunioni, compleanni, anniversari e pranzi di lavoro. Scegliete con noi il menù, poi pensiamo noi alla tavola e al servizio.</p>
  <ul class="ticks">
   <li>{ico("check")}<span>Sala con archi in pietra e terrazza sulle colline</span></li>
   <li>{ico("check")}<span>Menù concordato, con i prodotti dell'azienda</span></li>
   <li>{ico("check")}<span>Giardino e area giochi per i bambini</span></li>
   <li>{ico("check")}<span>Parcheggio nella proprietà</span></li>
  </ul>
  <p>Capienza: {todo()} invitati in sala, {todo()} all'aperto.</p>
 </div>
</div></section>
<section class="sec" id="preventivo" aria-labelledby="preventivo-t"><div class="wrap split" style="align-items:start">
 <div><h2 id="preventivo-t">Chiedete un preventivo</h2><p class="lead">Diteci data e numero di invitati: vi richiamiamo noi per i dettagli.</p>
 <p>Oppure chiamate il <a href="tel:{TEL}">{TEL_TXT}</a>.</p></div>
 <div>{form}</div>
</div></section>
"""
    page("cucina-eventi.html", "Cucina ed eventi · Agriturismo Torre Gialluise",
         "Cucina irpina con salumi, ricotta di Carmasciano e pasta fatta in casa. Battesimi, comunioni e feste nel casale tra Gesualdo e Villamaina.",
         body)


# ---------------------------------------------------------------- BOTTEGA
def bottega():
    body = f"""
<section class="phead"><div class="wrap">
 <p class="crumbs"><a href="index.html">Home</a> / Bottega</p>
 <h1>La bottega</h1>
 <p class="lead">I prodotti della nostra azienda agricola: olio, vino, farina e legumi. Spedizione in Italia o ritiro all'agriturismo.</p>
 <p><span class="price-tag">Prezzi di esempio</span> I prezzi e i prodotti definitivi li sistemiamo insieme.</p>
</div></section>
<section class="sec" style="padding-top:8px" aria-labelledby="prod-t"><div class="wrap"><h2 id="prod-t" class="visually-hidden">Prodotti</h2><div class="grid grid--3">{"".join(product_card(p) for p in PRODUCTS)}</div></div></section>
<section class="sec sec--alt"><div class="wrap">
 <dl class="info">
  <div><dt>Spedizione</dt><dd>In tutta Italia, 7 € a ordine. Tempi {todo()}</dd></div>
  <div><dt>Ritiro in azienda</dt><dd>Gratis, all'agriturismo sulla SS 428.</dd></div>
  <div><dt>Pagamento</dt><dd>Carta, bonifico o alla consegna.</dd></div>
  <div><dt>Ordini grandi o regali</dt><dd>Scriveteci su <a href="{WA}">WhatsApp</a>.</dd></div>
 </dl>
</div></section>
"""
    page("bottega.html", "Bottega · Olio, vino e farina di Torre Gialluise",
         "Olio extravergine, vino della casa, farina e legumi dell'azienda agricola Torre Gialluise. Spedizione in Italia o ritiro in azienda.",
         body)
    for p in PRODUCTS:
        img = (pic(p["img"], f"{p['name']}: foto dall'azienda", "(min-width:880px) 540px, 100vw", "pd__img", eager=True)
               if p["img"] else f'<div class="noimg">Foto prodotto {todo()}</div>')
        facts = "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in p["facts"])
        rel = "".join(product_card(o) for o in [x for x in PRODUCTS if x["slug"] != p["slug"]][:3])
        body = f"""
<section class="phead" style="padding-bottom:12px"><div class="wrap"><p class="crumbs"><a href="index.html">Home</a> / <a href="bottega.html">Bottega</a> / {p['name']}</p></div></section>
<section class="sec" style="padding-top:8px"><div class="wrap pd">
 <div class="rimg">{img}</div>
 <div>
  <h1 style="font-size:clamp(2rem,6vw,3rem)">{p['name']}</h1>
  <p class="card__meta" style="font-size:1rem">{p['size']}</p>
  <p><span class="price" style="font-size:1.5rem">{eur(p['price'])}</span> <span class="price-tag">prezzo di esempio</span></p>
  <p>{p['long']}</p>
  <div class="buy">
   <span class="qty"><button type="button" data-step="-1" aria-label="Diminuisci quantità">−</button><input id="pd-qty" type="number" min="1" max="99" value="1" aria-label="Quantità" inputmode="numeric"><button type="button" data-step="1" aria-label="Aumenta quantità">+</button></span>
   <button class="btn btn--main" type="button" data-add="{p['slug']}">{ico("bag")} Aggiungi al carrello</button>
  </div>
  <dl class="info" style="grid-template-columns:1fr 1fr">{facts}</dl>
  <ul class="ticks" style="margin-top:20px">
   <li>{ico("check")}<span>Spedizione in Italia, 7 € a ordine</span></li>
   <li>{ico("check")}<span>Ritiro gratis all'agriturismo</span></li>
  </ul>
 </div>
</div></section>
<section class="sec sec--alt" aria-labelledby="rel-t"><div class="wrap"><h2 id="rel-t">Altri prodotti</h2><div class="grid grid--3">{rel}</div></div></section>
"""
        page(f"prodotto-{p['slug']}.html", f"{p['name']} ({p['size']}) · Bottega Torre Gialluise",
             f"{p['short']} {p['name']}, {p['size']}, dalla bottega dell'agriturismo Torre Gialluise in Irpinia.",
             body, active="bottega.html")


# ---------------------------------------------------------------- CHECKOUT
def checkout():
    def radio(name, val, label, checked=False):
        return f'<label class="radio"><input type="radio" name="{name}" value="{val}"{" checked" if checked else ""}> {label}</label>'
    body = f"""
<section class="phead"><div class="wrap">
 <p class="crumbs"><a href="index.html">Home</a> / <a href="bottega.html">Bottega</a> / Checkout</p>
 <h1>Checkout</h1>
 <p class="lead">Tre passaggi e avete finito. In questa bozza non si paga nulla.</p>
</div></section>
<section class="sec" style="padding-top:8px"><div class="wrap co">
 <div>
  <form id="co-form" data-demo="co-ok" aria-label="Dati dell'ordine">
   <fieldset><legend><span>1</span> I vostri dati</legend><div class="fgrid">
    {field("co-nome", "Nome e cognome", err="Inserite nome e cognome", full=True, extra=' autocomplete="name"')}
    {field("co-email", "Email", typ="email", err="L'email deve contenere @ e un dominio, per esempio nome@gmail.com", extra=' autocomplete="email" spellcheck="false" data-rule="email"')}
    {field("co-tel", "Telefono", typ="tel", err="Inserite un numero di telefono valido", extra=' autocomplete="tel" inputmode="tel" data-rule="tel"')}
   </div></fieldset>
   <fieldset><legend><span>2</span> Consegna</legend>
    {radio("consegna", "spedizione", "Spedizione in Italia (7 €)", True)}
    {radio("consegna", "ritiro", "Ritiro all'agriturismo (gratis)")}
    <div id="addr" class="fgrid" style="margin-top:12px">
     {field("co-ind", "Indirizzo", err="Inserite via e numero civico", full=True, extra=' autocomplete="street-address"')}
     {field("co-cap", "CAP", err="Il CAP ha 5 cifre", extra=' autocomplete="postal-code" inputmode="numeric" data-rule="cap"')}
     {field("co-citta", "Città", err="Inserite la città", extra=' autocomplete="address-level2"')}
    </div>
   </fieldset>
   <fieldset><legend><span>3</span> Pagamento</legend>
    {radio("pag", "carta", "Carta di credito o debito", True)}
    {radio("pag", "bonifico", "Bonifico bancario")}
    {radio("pag", "consegna", "Alla consegna o al ritiro")}
    <p class="help">Nella versione definitiva il pagamento con carta avviene su una pagina sicura del circuito.</p>
   </fieldset>
   <button id="co-submit" class="btn btn--main" type="submit">Conferma l'ordine</button>
  </form>
  <div class="done" id="co-ok" hidden role="status"><h3>{ico("check")} Ordine di prova registrato</h3><p>In questa bozza non si paga e non parte nessun ordine. Nella versione definitiva qui arriva il riepilogo e una email di conferma.</p><a class="btn btn--line" href="bottega.html">Torna alla bottega</a></div>
 </div>
 <aside aria-labelledby="sum-t"><div class="sum" id="co-sum">
  <h2 id="sum-t" style="font-size:1.5rem">Riepilogo</h2>
  <ul id="co-items"></ul>
  <div class="row"><span>Subtotale</span><span id="co-sub">0,00 €</span></div>
  <div class="row"><span>Spedizione</span><span id="co-ship">—</span></div>
  <div class="row row--tot"><span>Totale</span><span id="co-tot">0,00 €</span></div>
  <p class="help">Prezzi di esempio, IVA inclusa.</p>
 </div></aside>
</div></section>
"""
    page("checkout.html", "Checkout · Bottega Torre Gialluise",
         "Riepilogo dell'ordine dalla bottega dell'agriturismo Torre Gialluise.", body, active="bottega.html")


if __name__ == "__main__":
    home()
    camere()
    cucina()
    bottega()
    checkout()
    (OUT / "app.js").write_text((SRC / "app.js").read_text(encoding="utf-8").replace("/*PRODUCTS*/", product_js()), encoding="utf-8")
    print("scritto app.js")
