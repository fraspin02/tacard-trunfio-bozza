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

NAV = [("index.html", "Il casale"), ("camere.html", "Camere"), ("menu.html", "Menù"),
       ("index.html#eventi", "Eventi"), ("index.html#dove", "Dove siamo")]

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
    <ul>{"".join(f'<li><a href="{h}">{t}</a></li>' for h, t in NAV)}</ul>
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
<script src="app.js" defer></script>
</body>
</html>
"""


def page(path, title, desc, body, extra="", active=None):
    html = head(title, desc, path, extra) + header(active or path) + f'<main id="main">{body}</main>\n' + footer()
    (OUT / path).write_text(html, encoding="utf-8")
    print("scritto", path, len(html) // 1024, "KB")


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
    quotes = "".join(f'<blockquote class="quote"><p>“{q}”</p><footer>{s}</footer></blockquote>' for q, s in QUOTES)
    body = f"""
<section class="hero">
 <div class="wrap hero__grid">
  <div>
   <span class="eyebrow">Agriturismo tra Gesualdo e Villamaina</span>
   <h1>Torre Gialluise <span class="it">casale in pietra sulle colline dell'Irpinia</span></h1>
   <p class="lead">Tre camere con vista, la cucina di casa e il vino della nostra vigna. A 1,6 km dal Castello di Gesualdo.</p>
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
    <div><dt>Vino di casa</dt><dd>dalla vigna accanto al casale</dd></div>
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
   <div class="btn-row"><a class="btn btn--main" href="{wa("Buongiorno, vorrei prenotare un tavolo per ")}">Prenota un tavolo</a><a class="link-arrow" href="menu.html">Vedi il menù {ico("arrow")}</a></div>
  </div>
 </div>
</section>

<section class="sec" id="eventi" aria-labelledby="eventi-t">
 <div class="wrap">
  <div class="grid grid--2" style="align-items:stretch">
   <div class="tile">{pic("evento-torta", "Torta a piani decorata con fiori davanti al casale", "(min-width:640px) 45vw, 100vw")}<div class="tile__t"><h3>Battesimi e comunioni</h3><span>Pranzi in terrazza o in sala</span></div></div>
   <div class="tile">{pic("arco-sera", "Tavolata sotto un arco in pietra al tramonto", "(min-width:640px) 45vw, 100vw")}<div class="tile__t"><h3>Feste e pranzi di famiglia</h3><span>Compleanni, anniversari, incontri</span></div></div>
  </div>
  <div class="sec-head" style="margin:28px 0 0">
   <span class="eyebrow">Eventi</span>
   <h2 id="eventi-t">La vostra festa, in campagna</h2>
   <p class="lead">Organizziamo pranzi per battesimi, comunioni, compleanni e anniversari, con il menù concordato insieme e gli spazi solo per voi.</p>
   <a class="btn btn--olive" href="{wa("Buongiorno, vorrei un preventivo per un evento: tipo, data e numero di invitati: ")}">{ico("chat")} Chiedi un preventivo</a>
  </div>
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
         "Casale in pietra in Irpinia, a 1,6 km dal Castello di Gesualdo: tre camere con vista, cucina di casa, eventi e il vino della vigna di casa.",
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


def menu():
    menu = "".join(f"""<div><h3>{cat}</h3><ul class="dishes">{"".join(
        f'<li><span><b>{n}</b><small>{d}</small></span><span class="pr">{todo("€")}</span></li>' for n, d in items)}</ul></div>"""
        for cat, items in MENU)
    body = f"""
<section class="phead"><div class="wrap">
 <p class="crumbs"><a href="index.html">Home</a> / Menù</p>
 <h1>Il menù</h1>
 <p class="lead">A tavola mettiamo i piatti dell'Irpinia, i salumi e il vino della nostra vigna.</p>
</div></section>
<section class="sec" style="padding-top:8px" aria-labelledby="menu-t"><div class="wrap split" style="align-items:start">
 <div>
  <h2 id="menu-t">Piatti di esempio</h2>
  <p>Menù di esempio: i piatti cambiano con le stagioni. Prezzo medio 22–36 € a persona {todo("da confermare")}</p>
  <div class="grid">{menu}</div>
  <p style="margin-top:20px"><b>Orari del ristorante:</b> {todo()} · solo su prenotazione</p>
  <p>Allergie o intolleranze? Ditecelo quando prenotate: prepariamo anche piatti vegetariani e vegani.</p>
  <a class="btn btn--main" href="{wa("Buongiorno, vorrei prenotare un tavolo per ")}">{ico("chat")} Prenota un tavolo</a>
 </div>
 <div class="mosaic">
  <div class="rimg">{pic("tavola", "Tavola lunga apparecchiata all'aperto la sera", "(min-width:880px) 300px, 55vw")}</div>
  <div class="rimg">{pic("olive", "Olive sui rami degli ulivi intorno al casale", "(min-width:880px) 240px, 45vw")}</div>
  <div class="rimg">{pic("uva", "Grappoli d'uva nera nella vigna dell'agriturismo", "(min-width:880px) 240px, 45vw")}</div>
 </div>
</div></section>
"""
    page("menu.html", "Menù · Agriturismo Torre Gialluise",
         "Cucina irpina con salumi, ricotta di Carmasciano e pasta fatta in casa. Il ristorante del casale tra Gesualdo e Villamaina, su prenotazione.",
         body)


if __name__ == "__main__":
    home()
    camere()
    menu()
    (OUT / "app.js").write_text((SRC / "app.js").read_text(encoding="utf-8"), encoding="utf-8")
    print("scritto app.js")
