#!/usr/bin/env python3
"""Génère les pages projet Thomas & Florian à partir du gabarit (immunity-potion d'origine).
Usage : python3 /home/claude/gen/gen.py   → écrit /home/claude/thomas-et-florian/<slug>.html
"""
import html, re, json
from urllib.parse import quote

T = open(__import__("os").path.join(__import__("os").path.dirname(__file__), "template.html"), encoding="utf-8").read()
OUT = __import__("os").path.join(__import__("os").path.dirname(__file__), "..") + "/"
U = "https://thomasetflorian.com/wp-content/uploads/"

def u(path):  # encode les accents des noms de fichiers
    return U + quote(path, safe="/-_.%")

YT = lambda i: f"https://www.youtube-nocookie.com/embed/{i}?rel=0&modestbranding=1&playsinline=1"

ECD_AP = ("Executive Creative Director", "Adrien Mancel & Paul-Émile Raymond")
AD = ("Art Director", "Florian Amoneau")
CW = ("Copywriter", "Thomas Blanc")

# media : (type, url, légende, options)  type = video | img | yt
# options : loop (carré sur mobile), clean (sans ombre ni fond), nat (proportions d'origine)
P = [
  dict(slug="building-tomorrow", fn="BUILDING_TOMORROW.mp4", name="Building Tomorrow", client="Dassault Systèmes",
       h1="Le B2B aussi peut être sexy.",
       p="On est parti de ça.",
       hero=("video", u("2024/11/PL01_Seine_v3.mp4"), None, {"nat"}),   # TODO : logo par-dessus la boucle
       media=[("img", u("2024/11/buildingtomorrow-data.png"), "Boring_And_Confusing_Screenshot_01.png", {"nat", "small"}),
              ("txt", "Pour arriver à ça."),
              ("video", u("2024/11/PL02_Proche_v2-Cut.mov"), "Building_Tomorrow_Reveal.mov", {"nat", "big"}),
              ("txt", "Pour démontrer les fonctionnalités de sa plateforme de construction, nous avons proposé à Dassault Systèmes de créer le case study d’un extraordinaire projet de construction fictif : une tour Eiffel élaborée avec les techniques et les enjeux du XXIe siècle grâce à la plateforme de Dassault Systèmes."),
              ("yt", "L2TvitutMIc", "VIDEO_CASE_Building_Tomorrow.mp4", set()),
              ("img", u("2024/11/DS_BuildingTomorrow_Board_Final2-scaled.jpg"), "DS_BuildingTomorrow_Board_Final2.jpg", {"nat"})],
       gal=[], credits=[ECD_AP, CW, ("Production", "Gang Life")],
       awards=[("2023", "THE DRUM AWARDS_WINNER", "B2B Content"), ("2023", "THE DRUM AWARDS_WINNER", "B2B Response to change"),
               ("2023", "GRAND PRIX DU BRAND CONTENT_GOLD", "B2B"), ("2023", "EPICA_SHORTLIST", "Professional Products & Services"),
               ("2023", "EPICA_SHORTLIST", "Branded Content"), ("2023", "ONE SHOW_SHORTLIST X6", ""), ("2023", "ANDY AWARDS_SHORTLIST", "")]),
  dict(slug="immunity-potion", fn="IMMUNITY_POTION_Actimel.mp4", name="Immunity Potion", client="Actimel",
       h1="Protéger les joueurs aussi bien en jeu que dans la vraie vie.",
       p="Comme tout le monde, nous avons joué à Fortnite. Et comme tout le monde, nous avons perdu dès la première game. Si seulement il existait une petite boisson super forte qui booste l’immunité des joueurs et les empêche de tomber dès la première confrontation ! Et comme on bossait en même temps pour la marque Actimel, on s’est dit qu’on allait faire exactement ça. Et pour pimenter le tout, on a rajouté des zombies.",
       hero=("video", u("2024/11/IP-Logo.mov"), None, {"clean", "loop"}),
       media=[("yt", "bgGZbjq2eYg", "VIDEO_CASE_V8Def.mp4", set()),
              ("video", u("2024/11/IP-Switch.mov"), "Bottle_Switch.gif", {"loop"})],
       gal=[u(f"2024/11/Immunity-Potion-Execution-Image-{n}.jpg") for n in (1, 2, 3, 4, 6, 10)], gr="16/9",
       credits=[ECD_AP, AD, CW, ("Developer", "Apfel")],
       awards=[("2024", "EFFIE_SILVER", "")]),
  dict(slug="safety-squad", fn="NUK_SAFETY_SQUAD.mp4", name="The Safety Squad", client="Nuk",
       h1="Nuk veut prendre soin de tous les bébés.",
       p="Alors on leur a proposé d’offrir leur technologie de biberon anti-brûlures directement dans leurs publicités. Ils ont adoré l’idée. Nous avons mis la technologie dans des annonces presse, des flyers… en fait, partout où on peut croiser des bébés.",
       hero=("video", u("2024/10/Nuk_IntroMonsters.mp4"), None, {"nat"}),
       media=[("video", u("2024/10/SafetySquad-Reveal.mov"), "SafetySquad_Reveal.mov", {"nat", "loop"})],
       gal=[u(f"2024/10/{n}-scaled.jpg") for n in ("all", "bug_seul", "chaise_haute", "flyer2", "presse", "sous-bock")], gr="auto",
       credits=[ECD_AP, AD, CW, ("Character Designer", "Kristof Luyckx")],
       awards=[("2022", "CANNES LIONS_SHORTLIST", "Media"), ("2022", "EPICA_GOLD", "Direct"), ("2022", "EPICA_SHORTLIST X5", ""),
               ("2022", "CRESTA AWARDS_BRONZE X4", ""), ("2022", "INNOVATION BY DESIGN_FINALIST", ""), ("2022", "CLIO_SHORTLIST", ""),
               ("2022", "ONE SHOW_SHORTLIST X3", "")]),
  dict(slug="cuisinella", fn="CUISINEL-LÀ_Cuisinella.mp4", name="Cuisinel-là", client="Cuisinella",
       h1="Toute une campagne qui part de là. Ou plutôt d’un La.",
       p="",
       hero=("video", u("2024/11/Cuisinella-Gif-Poulet.mp4"), None, {"nat", "loop"}),
       media=[("video", u("2024/09/Cuisinella-Gif-Topinambour2.mp4"), "Cuisinella_Topinambour.gif", {"nat", "loop"})],
       gal=[u(f"2024/11/221216_CUISINELLA-20sec-WEB.mp4.01_00_{t}.jpg") for t in ("04_06.Still002", "05_23.Still003", "09_05.Still004", "11_08.Still005", "12_24.Still006", "15_11.Still007")], gr="16/9",
       credits=[ECD_AP, AD, CW, ("Réalisateur", "Big Red Button")], awards=[]),
  dict(slug="parisian-rendez-vous", fn="THE_PARISIAN_RENDEZ-VOUS.mp4", name="The Parisian Rendez-vous", client="Le Drugstore Parisien",
       h1="Vous vous souvenez des trottinettes en libre service ?",
       p="Il y en avait partout dans Paris. On s’est dit qu’il y avait forcément un truc à faire avec pour le lancement du Drugstore Parisien. Vu les résultats, il y avait effectivement un truc à faire. On en vient presque à les regretter, ces bonnes vieilles trottinettes.",
       hero=("video", u("2024/10/ANIM-LOGO.mp4"), None, {"nat", "clean", "loop"}),
       media=[], gal=[u("2024/10/1.jpg"), u("2024/10/2-1.jpg"), u("2024/10/3-1.jpg")], gr="auto",
       credits=[("Executive Creative Director", "Thomas Derouault"), ("Creative Directors", "Paul-Émile Raymond & Adrien Mancel"), AD, CW,
                ("Motion Designer", "Thomas Mouilley"), ("Editing", "Agathe Soula – The Good Tape"), ("Head of Production", "Raphaël Fruchard")],
       awards=[("2020", "CLUB DES DA_SILVER", "Activation"), ("2020", "CLUB DES DA_SILVER", "Use of digital"), ("2020", "CLUB DES DA_BRONZE", "Ambient"),
               ("2020", "D&AD_SHORTLIST", "Direct"), ("2020", "D&AD_SHORTLIST", "Digital"), ("2019", "CANNES LIONS_BRONZE", "Media"),
               ("2019", "EPICA_GRAND PRIX", "Alternative"), ("2019", "EPICA_GOLD", "Experiential marketing"), ("2019", "EPICA_GOLD", "Mobile")]),
  dict(slug="euphytose-etudiants", fn="EUPHYTOSE_ÉTUDIANTS.mp4", name="Euphytose Étudiants", client="Euphytose",
       h1="Les étudiants aussi sont stressés.",
       p="Euphytose Stress a voulu s’adresser à eux pendant la période de révisions. La marque, plutôt habituée à communiquer auprès de leurs mamans, a accepté d’adopter un ton beaucoup plus amusant.",
       hero=None, media=[],
       gal=[u("2024/10/" + n) for n in ("Napoelon_Revision_v2_29s.00_00_05_04.Still003.jpg", "Napoelon_Revision_v2_29s.00_00_07_15.Still002.jpg",
            "Napoelon_Revision_v2_29s.00_00_12_06.Still001.jpg", "Leonard_Revision_v2_29s.00_00_05_08.Still001.jpg",
            "Leonard_Revision_v2_29s.00_00_03_08.Still003.jpg", "Leonard_Revision_v2_29s.00_00_13_09.Still004.jpg")], gr="16/9",
       credits=[("Executive Creative Director", "Thomas Derouault"), AD, CW, ("Director", "Nico Galoux")], awards=[]),
  dict(slug="euphytose-stress", fn="EUPHYTOSE_STRESS.mp4", name="Euphytose Stress", client="Euphytose",
       h1="La publicité est partout. Et ça peut être un peu stressant.",
       p="Alors comment faire la pub d’un produit supposé lutter contre le stress ? Comme ça.",
       hero=None, media=[], gal=[],
       credits=[("Executive Creative Director", "Thomas Derouault"), AD, CW, ("Production", "Blue Paris")], awards=[]),
  dict(slug="synaesthesia", fn="SYNAESTHESIA_Moët&Chandon.mp4", name="Synaesthesia", client="Moët & Chandon",
       h1="Moët & Chandon Synaesthesia.",
       p="Une nouvelle gamme de cocktails destinée à éveiller vos sens en fusionnant champagne et recettes de cocktails emblématiques. À travers cette campagne, nous nous sommes fixé comme objectif de faire ressentir au spectateur les sensations procurées par les cocktails, tout en déguisant une campagne d’image de marque en tutoriels de mixologie.",
       hero=None,
       media=[("video", u("2021/07/Slide1-MoëtSynesthesia-InstaStory-V5.mp4"), "InstaStory_V5.mp4", {"nat", "tall"}),
              ("video", u("2021/07/Slide2-MoëtSynesthesia-Recipes-V2.mp4"), "Recipes_V2.mp4", {"nat", "tall"})],
       gal=[], credits=[("Creative Directors", "Paul-Émile Raymond & Adrien Mancel"), AD, CW, ("Directors", "Julien & Quentin")], awards=[]),
]

def fr(t):  # espaces fines avant ? ! : ; et apostrophes typographiques
    t = t.replace("'", "’")
    return re.sub(r" ([?!:;])", " \\1", t)

def esc(t): return html.escape(t, quote=True)

VARIANTS = ["v1", "v2", "v3", "v4"]

def media_html(m, cls, label):
    kind, src, cap, opt = m
    c = "m " + cls + "".join(" " + o for o in sorted(opt))
    if kind == "yt":
        box = f'<div class="box"><iframe src="{YT(src)}" title="{esc(label)}" allow="autoplay; encrypted-media; picture-in-picture; fullscreen" allowfullscreen loading="lazy"></iframe></div>'
    elif kind == "video":
        auto = " autoplay preload=\"auto\"" if cls == "logo" else " preload=\"metadata\""
        box = f'<div class="box"><video muted loop playsinline{auto} src="{src}" aria-label="{esc(label)}"></video></div>'
    else:
        box = f'<div class="box"><img loading="lazy" decoding="async" src="{src}" alt="{esc(label)}"></div>'
    capt = ""
    if cap:
        side = "right" if cls in ("v1", "v3") else "left"
        capt = f'\n    <figcaption class="cap {side}" data-t="{esc(cap)}"></figcaption>'
    return f'  <figure class="{c}">\n    {box}{capt}\n  </figure>\n'

ARL = "<svg class='ar' viewBox='0 0 9 7' width='9' height='7' aria-hidden='true' shape-rendering='crispEdges' fill='currentColor'><path d='M0 3h9v1H0zM1 2h1v1H1zM1 4h1v1H1zM2 1h1v1H2zM2 5h1v1H2zM3 0h1v1H3zM3 6h1v1H3z'/></svg>"
ARR = "<svg class='ar' viewBox='0 0 9 7' width='9' height='7' aria-hidden='true' shape-rendering='crispEdges' fill='currentColor'><path d='M0 3h9v1H0zM7 2h1v1H7zM7 4h1v1H7zM6 1h1v1H6zM6 5h1v1H6zM5 0h1v1H5zM5 6h1v1H5z'/></svg>"

def build(i, d):
    s = T
    def rep(a, b, cnt=1):
        nonlocal s
        assert s.count(a) >= 1, (d["slug"], a[:80])
        s = s.replace(a, b, cnt)
    title = f'{d["name"]} · Thomas & Florian'
    desc = f'{d["name"]} pour {d["client"]} : {d["h1"]}'
    rep("<title>Immunity Potion · Thomas & Florian</title>", f"<title>{esc(title)}</title>")
    rep('<meta name="description" content="Immunity Potion pour Actimel : protéger les joueurs aussi bien en jeu que dans la vraie vie.">',
        f'<meta name="description" content="{esc(desc)}">')
    rep('<span class="fn" id="fname">IMMUNITY_POTION_Actimel.mp4</span>', f'<span class="fn" id="fname">{esc(d["fn"])}</span>')

    # ---- CSS générique (variantes de colonne, proportions d'origine, carré mobile)
    rep(""".logo .box{box-shadow:none;background:transparent}
.case{--w:1040px;--dx:-1.6vw;margin-top:12vh}
.bottle{--w:760px;--dx:2vw;margin-top:14vh}""",
""".clean .box{box-shadow:none;background:transparent}
.v1{--w:1040px;margin-top:12vh}
.v2{--w:760px;margin-top:14vh}
.v3{--w:900px;margin-top:14vh}
.v4{--w:820px;margin-top:14vh}
.intro + .m{margin-top:12vh}
/* tous les médias centrés */
/* proportions d'origine : le média garde son format, l'ombre passe sur le média */
.nat .box{aspect-ratio:auto;background:none;box-shadow:none;display:flex;justify-content:center}
.nat .box video,.nat .box img{position:static;display:block;width:auto;max-width:100%;height:auto;max-height:82vh;object-fit:contain;box-shadow:0 18px 50px rgba(1,8,36,.12)}
.nat.clean .box video,.nat.clean .box img{box-shadow:none}
.nat.tall{--w:440px}
.m.small{--w:560px}
.m.big{--w:1240px}
.say{width:min(960px, calc(100% - 32px));max-width:60ch;margin:12vh auto 0;text-align:center;font-family:var(--script);font-size:16px;line-height:1.6;text-wrap:pretty}
.say span{background:rgba(236,237,243,.6);box-shadow:0 0 0 4px rgba(236,237,243,.6);-webkit-box-decoration-break:clone;box-decoration-break:clone}
.say + .m{margin-top:8vh}

.pair{display:flex;justify-content:center;align-items:flex-start;gap:clamp(14px,5vw,80px);margin:12vh auto 0;padding:0 16px;max-width:1040px}
.pair .m{width:min(400px,48%);margin:0;transform:none}
.pair .m:last-child{margin-top:8vh}
.intro + .pair{margin-top:12vh}
.m img{display:block;width:100%}""")
    rep("  .logo .box,.bottle .box{aspect-ratio:1/1}",
        "  .loop .box{aspect-ratio:1/1}\n  .nat.loop .box video{position:absolute;inset:0;width:100%;height:100%;max-height:none;object-fit:cover}")
    rep("  .case{margin-top:5vh}\n  .bottle{margin-top:6vh}", "  .v1,.v2,.v3,.v4,.intro + .m,.pair,.say{margin-top:6vh}\n  .say + .m{margin-top:5vh}\n  .m.small{--w:76vw}\n  .pair .m:last-child{margin-top:4vh}")
    rep(".row img{display:block;width:100%;aspect-ratio:16/9;", ".row img{display:block;width:100%;aspect-ratio:var(--gr,16/9);")

    # ---- contenu principal
    a = s.index("<main>\n") + len("<main>\n"); b = s.index("</main>")
    main = ""
    if d["hero"]:
        main += media_html(d["hero"], "logo", f'{d["name"]}, {d["client"]}') + "\n"
    kick = esc(d["client"])
    para = f'\n    <p><span>{esc(fr(d["p"]))}</span></p>' if d["p"] else ""
    main += f'''  <section class="intro" id="intro">
    <div class="kick">{kick}</div>
    <h1 id="ideaT" aria-label="{esc(fr(d["h1"]))}"></h1>{para}
  </section>
'''
    k = 0; ms = d["media"]; vi = 0
    while k < len(ms):
        m = ms[k]
        if m[0] == "txt":                                  # paragraphe entre deux médias
            main += f'\n  <p class="say"><span>{esc(fr(m[1]))}</span></p>\n'; k += 1; continue
        if "tall" in m[3] and k + 1 < len(ms) and "tall" in ms[k + 1][3]:   # deux formats verticaux côte à côte
            main += '\n  <div class="pair">\n' + media_html(m, "v2", f'{d["name"]}, média {k + 1}') + media_html(ms[k + 1], "v1", f'{d["name"]}, média {k + 2}') + "  </div>\n"
            k += 2; continue
        main += "\n" + media_html(m, VARIANTS[vi % 4], f'{d["name"]}, média {k + 1}'); k += 1; vi += 1
    s = s[:a] + main + s[b:]
    rep('const TITLE = "Protéger les joueurs aussi bien en jeu que dans la vraie vie.";', f"const TITLE = {json.dumps(fr(d['h1']), ensure_ascii=False)};")

    # ---- galerie
    g = d["gal"]
    gr = d.get("gr", "16/9")
    rep('<section class="gal" aria-label="Images du projet">',
        f'<section class="gal" aria-label="Images du projet" style="--gr:{gr}"' + ("" if g else " hidden") + ">")
    rep('''const SRC = "https://thomasetflorian.com/wp-content/uploads/2024/11/Immunity-Potion-Execution-Image-";
const G = [1, 2, 3, 4, 6, 10];''', f"const G = {json.dumps(g)};")
    rep('src="${SRC + n}.jpg" alt="Immunity Potion, image ${i + 1}"', 'src="${n}" alt="' + esc(d["name"]) + ', image ${i + 1}"')
    rep("""    f.style.setProperty("--z", (1 + (Z[i] - 1) * k).toFixed(3));
    f.style.setProperty("--ox", (OX[i] * k).toFixed(1) + "px"); f.style.setProperty("--oy", (OY[i] * k).toFixed(1) + "px");""",
        """    const j = i % Z.length;
    f.style.setProperty("--z", (1 + (Z[j] - 1) * k).toFixed(3));
    f.style.setProperty("--ox", (OX[j] * k).toFixed(1) + "px"); f.style.setProperty("--oy", (OY[j] * k).toFixed(1) + "px");""")
    rep("/* galerie : six images sur deux lignes, sur la bande bleue */", "/* galerie : les images par lignes de trois, sur la bande bleue */")

    rep('  if (sg.dataset.k !== "rule") playAscii();', '  if (sg.dataset.k === "scope" || sg.dataset.k === "color") playAscii();')
    rep('document.querySelectorAll(".intro p span").forEach(el => {', 'document.querySelectorAll(".intro p span, .say span").forEach(el => {')

    # ---- reveal « photo » : le premier média de la page
    rep('logoCover = asciiCover(document.querySelector(".logo .box"), ...PAL[dev.color]); logoCover.play(150);',
        'const lb = document.querySelector("main .m .box"); if (!lb) return;\n  logoCover = asciiCover(lb, ...PAL[dev.color]); logoCover.play(150);')

    # ---- crédits et awards
    a = s.index('<section class="credits"'); b = s.index("</section>", a) + len("</section>")
    dl = "\n".join(f'        <div><dt>{esc(r)}</dt><dd>{esc(n)}</dd></div>' for r, n in d["credits"])
    aw = ""
    if d["awards"]:
        lines = "\n".join(f'      <p class="aw"><span class="y">{y}</span>{esc(t)}' + (f' <span class="c">{esc(c)}</span>' if c else "") + "</p>" for y, t, c in d["awards"])
        aw = f'''
    <div>
      <h2>{"Awards" if len(d["awards"]) > 1 else "Award"}</h2>
{lines}
    </div>'''
    s = s[:a] + f'''<section class="credits" aria-label="Crédits{" et awards" if d["awards"] else ""}">
  <div class="cols">
    <div>
      <h2>Crédits</h2>
      <dl>
{dl}
      </dl>
    </div>{aw}
  </div>
</section>''' + s[b:]
    rep(".cols .aw .y{", ".cols .aw + .aw{margin-top:12px}\n.cols .aw .c{display:block;margin-top:3px;font-size:9.5px;letter-spacing:.1em;text-transform:uppercase;opacity:.5}\n.cols .aw .y{")

    # ---- navigation précédent / suivant (en boucle)
    pv, nx = P[i - 1], P[(i + 1) % len(P)]
    a = s.index('    <a class="prev"'); b = s.index("\n", a)
    s = s[:a] + f'    <a class="prev" href="{pv["slug"]}.html">{ARL}<span class="t">{esc(pv["fn"])}</span></a>' + s[b:]
    a = s.index('    <a class="next"'); b = s.index("\n", a)
    s = s[:a] + f'    <a class="next" href="{nx["slug"]}.html"><span class="t">{esc(nx["fn"])}</span>{ARR}</a>' + s[b:]
    return s

if __name__ == "__main__":
    for i, d in enumerate(P):
        open(OUT + d["slug"] + ".html", "w", encoding="utf-8").write(build(i, d))
        print("ok", d["slug"])
