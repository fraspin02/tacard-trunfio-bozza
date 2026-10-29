"""Converte le foto della scheda Booking (raw/ph) in webp ridimensionate + manifest."""
import json
from pathlib import Path
from PIL import Image, ImageOps

SRC = Path(__file__).parent / "raw" / "ph"
OUT = Path(__file__).parent.parent / "img"
OUT.mkdir(exist_ok=True)

PHOTOS = {
    "hero": "676232829",
    "scala": "384794149",
    "pergolato": "384794370",
    "sala": "380286260",
    "arco-sera": "384794325",
    "terrazza": "676062247",
    "panorama": "676233107",
    "colline": "384794163",
    "camera-letto-aggiunto": "481503237",
    "camera-balcone": "480745426",
    "camera-doppia": "481503289",
    "tavola": "384643323",
    "tavolata": "473941336",
    "colazione": "384643628",
    "peperoni": "380286267",
    "olive": "384794284",
    "uva": "384794302",
    "evento-torta": "708763210",
    "evento-fiori": "708806406",
    "sera": "384794360",
    "ulivo": "694168660",
}
WIDTHS = (480, 800, 1200)

manifest = {}
for name, pid in PHOTOS.items():
    im = ImageOps.exif_transpose(Image.open(SRC / f"{pid}.jpg")).convert("RGB")
    w, h = im.size
    sizes = []
    for tw in WIDTHS:
        if tw > w and sizes:
            break
        tw = min(tw, w)
        th = round(h * tw / w)
        im.resize((tw, th), Image.LANCZOS).save(OUT / f"{name}-{tw}.webp", "WEBP", quality=72, method=6)
        sizes.append(tw)
    if sizes[-1] < min(w, WIDTHS[-1]):
        im.save(OUT / f"{name}-{w}.webp", "WEBP", quality=72, method=6)
        sizes.append(w)
    manifest[name] = {"w": w, "h": h, "sizes": sizes}
    print(name, w, h, sizes)

(Path(__file__).parent / "images.json").write_text(json.dumps(manifest, indent=1))
