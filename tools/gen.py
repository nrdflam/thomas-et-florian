#!/usr/bin/env python3
"""Génère les pages projet à partir de tools/template.html et du contenu de tools/projects.py.

    python3 tools/gen.py           écrit <slug>.html à la racine du site
    python3 tools/gen.py --check   vérifie seulement que les pages sont à jour (code de sortie 1 sinon)

Le gabarit contient des marqueurs {{…}} ; chacun doit apparaître exactement une fois.
Ne pas modifier les pages générées à la main : modifier le gabarit ou le contenu, puis relancer.
"""
import html
import json
import re
import sys
from pathlib import Path

from projects import PROJECTS

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parent
TEMPLATE = (TOOLS / "template.html").read_text(encoding="utf-8")
MARKERS = ["HEAD_META", "FNAME", "MAIN", "GALLERY", "CREDITS", "PREV", "NEXT", "DATA"]

KINDS = {"yt", "video", "img", "txt"}
OPTIONS = {"nat", "loop", "clean", "right", "small", "big", "full", "tall", "v1", "v2", "v3", "v4"}
VARIANTS = ["v1", "v2", "v3", "v4"]
YT_ID = re.compile(r"[\w-]{11}")
RATIO = re.compile(r"auto|\d+(\.\d+)?/\d+(\.\d+)?")
YEAR = re.compile(r"\d{4}")

ARROW_L = "<svg class='ar' viewBox='0 0 9 7' width='9' height='7' aria-hidden='true' shape-rendering='crispEdges' fill='currentColor'><path d='M0 3h9v1H0zM1 2h1v1H1zM1 4h1v1H1zM2 1h1v1H2zM2 5h1v1H2zM3 0h1v1H3zM3 6h1v1H3z'/></svg>"
ARROW_R = "<svg class='ar' viewBox='0 0 9 7' width='9' height='7' aria-hidden='true' shape-rendering='crispEdges' fill='currentColor'><path d='M0 3h9v1H0zM7 2h1v1H7zM7 4h1v1H7zM6 1h1v1H6zM6 5h1v1H6zM5 0h1v1H5zM5 6h1v1H5z'/></svg>"


def esc(t):
    """Texte ou URL placé dans du HTML (contenu ou attribut)."""
    return html.escape(str(t), quote=True)


def fr(t):
    """Typographie française : apostrophes courbes, espace fine insécable avant ? ! : ;"""
    return re.sub(r" ([?!:;])", " \\1", t.replace("'", "’"))


def json_script(data):
    """JSON lisible par le JS de la page, sans risque de fermer la balise <script>."""
    return json.dumps(data, ensure_ascii=False).replace("</", "<\\/").replace("<!--", "<\\!--")


# ---------------------------------------------------------------- vérifications

def validate(projects):
    errors, slugs = [], set()
    for d in projects:
        where = d.get("slug", "?")
        for key in ("slug", "fn", "name", "client", "h1", "p", "media", "gal", "credits", "awards"):
            if key not in d:
                errors.append(f"{where} : champ « {key} » manquant")
        if d.get("slug") in slugs:
            errors.append(f"{where} : slug en double")
        slugs.add(d.get("slug"))
        if not re.fullmatch(r"[a-z0-9-]+", d.get("slug", "")):
            errors.append(f"{where} : slug invalide (minuscules, chiffres, tirets)")
        items = ([d["hero"]] if d.get("hero") else []) + d.get("media", [])
        for m in items:
            kind, src, cap, opts = m
            if kind not in KINDS:
                errors.append(f"{where} : type de média inconnu « {kind} »")
            if opts - OPTIONS:
                errors.append(f"{where} : option(s) inconnue(s) {sorted(opts - OPTIONS)}")
            if kind == "yt" and not YT_ID.fullmatch(src):
                errors.append(f"{where} : identifiant YouTube invalide « {src} »")
            if kind in ("video", "img") and not src.startswith("https://") and not (ROOT / src).is_file():
                errors.append(f"{where} : fichier local introuvable « {src} »")
        if d.get("gal") and not RATIO.fullmatch(d.get("gr", "16/9")):
            errors.append(f"{where} : format de galerie invalide « {d.get('gr')} »")
        for year, _, _ in d.get("awards", []):
            if not YEAR.fullmatch(year):
                errors.append(f"{where} : année d'award invalide « {year} »")
    if errors:
        raise SystemExit("Contenu invalide :\n  " + "\n  ".join(errors))


# ---------------------------------------------------------------- fragments HTML

def youtube_src(vid):
    return f"https://www.youtube-nocookie.com/embed/{vid}?rel=0&playsinline=1"


def media_html(m, size, label, is_hero=False):
    kind, src, cap, opts = m
    classes = " ".join(["m", size] + sorted(opts - set(VARIANTS)))
    if kind == "yt":
        box = (f'<iframe src="{esc(youtube_src(src))}" title="{esc(label)}" allow="encrypted-media; picture-in-picture; fullscreen" '
               f'allowfullscreen loading="lazy" referrerpolicy="strict-origin-when-cross-origin"></iframe>')
    elif kind == "video":
        # boucle silencieuse : lancée par le JS quand elle est à l'écran (pas d'autoplay en mouvement réduit)
        preload = "auto" if is_hero else "metadata"
        box = f'<video muted loop playsinline preload="{preload}" src="{esc(src)}" aria-label="{esc(label)}"></video>'
    else:
        loading = 'fetchpriority="high"' if is_hero else 'loading="lazy"'
        box = f'<img {loading} decoding="async" src="{esc(src)}" alt="{esc(label)}">'
    caption = ""
    if cap:
        side = "right" if size in ("v1", "v3") else "left"
        caption = f'\n    <figcaption class="cap {side}" data-t="{esc(cap)}"></figcaption>'
    return f'  <figure class="{classes}">\n    <div class="box">{box}</div>{caption}\n  </figure>\n'


def main_html(d):
    out = ""
    if d.get("hero"):
        out += media_html(d["hero"], "hero", f'{d["name"]}, {d["client"]}', is_hero=True) + "\n"
    para = f'\n    <p><span>{esc(fr(d["p"]))}</span></p>' if d["p"] else ""
    title = esc(fr(d["h1"]).replace("\n", " "))
    out += (f'  <section class="intro" id="intro">\n'
            f'    <div class="kick">{esc(d["client"])}</div>\n'
            f'    <h1 id="ideaT" aria-label="{title}"></h1>{para}\n'
            f'  </section>\n')
    items, k, n = d["media"], 0, 0
    while k < len(items):
        m = items[k]
        label = f'{d["name"]}, média {k + 1}'
        if m[0] == "txt":                                   # paragraphe entre deux médias
            out += f'\n  <p class="say"><span>{esc(fr(m[1]))}</span></p>\n'
            k += 1
            continue
        if "tall" in m[3] and k + 1 < len(items) and "tall" in items[k + 1][3]:   # deux verticaux côte à côte
            out += ('\n  <div class="pair">\n' + media_html(m, "v2", label)
                    + media_html(items[k + 1], "v1", f'{d["name"]}, média {k + 2}') + "  </div>\n")
            k += 2
            continue
        size = next((o for o in sorted(m[3]) if o in VARIANTS), VARIANTS[n % len(VARIANTS)])
        out += "\n" + media_html(m, size, label)
        k += 1
        n += 1
    return out


def gallery_html(d):
    if not d["gal"]:
        return ""
    return (f'<section class="gal" aria-label="Images du projet" style="--gr:{d.get("gr", "16/9")}">\n'
            f'  <div class="row" id="row" tabindex="0" aria-label="Images, faire défiler"></div>\n'
            f'</section>')


def credits_html(d):
    rows = "\n".join(f"        <div><dt>{esc(role)}</dt><dd>{esc(names)}</dd></div>" for role, names in d["credits"])
    awards = ""
    if d["awards"]:
        lines = "\n".join(
            f'      <p class="aw"><span class="y">{year}</span>{esc(prize)}' + (f' <span class="c">{esc(cat)}</span>' if cat else "") + "</p>"
            for year, prize, cat in d["awards"])
        awards = f'\n    <div>\n      <h2>{"Awards" if len(d["awards"]) > 1 else "Award"}</h2>\n{lines}\n    </div>'
    label = "Crédits et awards" if d["awards"] else "Crédits"
    return (f'<section class="credits" aria-label="{label}">\n  <div class="cols">\n    <div>\n      <h2>Crédits</h2>\n'
            f'      <dl>\n{rows}\n      </dl>\n    </div>{awards}\n  </div>\n</section>')


def head_meta(d):
    title = f'{d["name"]} · Thomas & Florian'
    desc = fr(d.get("desc") or d["p"] or d["h1"]).replace("\n", " ")
    if len(desc) > 160:
        desc = desc[:157].rsplit(" ", 1)[0] + "…"
    image = next((src for kind, src, _, _ in [d.get("hero") or ("", "", None, set())] + d["media"] if kind == "img"), None)
    image = image or (d["gal"][0] if d["gal"] else "assets/nous.webp")
    return "\n".join([
        f"<title>{esc(title)}</title>",
        f'<meta name="description" content="{esc(desc)}">',
        '<meta property="og:type" content="article">',
        '<meta property="og:locale" content="fr_FR">',
        f'<meta property="og:title" content="{esc(title)}">',
        f'<meta property="og:description" content="{esc(desc)}">',
        f'<meta property="og:image" content="{esc(image)}">',
    ])


def nav_link(d, side):
    arrow_l, arrow_r = (ARROW_L, "") if side == "prev" else ("", ARROW_R)
    label = ("Projet précédent : " if side == "prev" else "Projet suivant : ") + d["name"]
    return (f'    <a class="{side}" href="{d["slug"]}.html" aria-label="{esc(label)}">'
            f'{arrow_l}<span class="t">{esc(d["fn"])}</span>{arrow_r}</a>')


def build(i, d):
    prev, nxt = PROJECTS[i - 1], PROJECTS[(i + 1) % len(PROJECTS)]
    data = {"title": fr(d["h1"]), "name": d["name"], "gallery": d["gal"]}
    parts = {
        "HEAD_META": head_meta(d),
        "FNAME": esc(d["fn"]),
        "MAIN": main_html(d),
        "GALLERY": gallery_html(d),
        "CREDITS": credits_html(d),
        "PREV": nav_link(prev, "prev"),
        "NEXT": nav_link(nxt, "next"),
        "DATA": f'<script type="application/json" id="tf-data">{json_script(data)}</script>',
    }
    page = TEMPLATE
    for key in MARKERS:
        marker = "{{" + key + "}}"
        if page.count(marker) != 1:
            raise SystemExit(f"gabarit : le marqueur {marker} doit apparaître une fois")
        page = page.replace(marker, parts[key])
    if "{{" in page:
        raise SystemExit("gabarit : marqueur inconnu restant : " + page[page.index("{{"):][:40])
    return page


def main():
    validate(PROJECTS)
    check = "--check" in sys.argv
    stale = []
    for i, d in enumerate(PROJECTS):
        path = ROOT / f'{d["slug"]}.html'
        page = build(i, d)
        if check:
            if not path.exists() or path.read_text(encoding="utf-8") != page:
                stale.append(path.name)
        else:
            path.write_text(page, encoding="utf-8")
            print("ok", path.name)
    if check:
        if stale:
            raise SystemExit("pages à régénérer : " + ", ".join(stale))
        print("pages à jour")


if __name__ == "__main__":
    main()
