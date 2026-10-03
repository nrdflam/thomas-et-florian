"""Contenu des pages projet, dans l'ordre de la navigation précédent / suivant.

Chaque projet :
  slug     nom du fichier généré (<slug>.html), aussi utilisé par la home
  fn       faux nom de fichier affiché dans la barre du haut et la navigation
  name     nom du projet ; client : la marque (affichée au-dessus du titre)
  h1       titre tapé lettre à lettre (« \\n » force un retour à la ligne)
  p        paragraphe sous le titre (peut être vide)
  desc     description pour les moteurs et le partage (sinon : le paragraphe)
  hero     média d'en-tête (ou None)
  media    médias et textes de la page, dans l'ordre
  gal      images de la galerie bleue ; gr : leur format (« 16/9 », « auto »…)
  credits  (rôle, noms) ; awards : (année, prix, catégorie)

Médias : yt(id, légende), video(url, légende), img(url, légende), txt(texte), avec des options :
  nat    garde les proportions d'origine du fichier
  loop   passe en carré sur mobile
  clean  sans ombre ni fond
  right  recadrage carré mobile calé à droite
  small / big / full   taille réduite, grande, pleine largeur
  tall   format vertical (deux « tall » qui se suivent passent côte à côte)
  v1…v4  impose une taille de colonne (sinon elles alternent)
"""
from urllib.parse import quote
import unicodedata

UPLOADS = "https://thomasetflorian.com/wp-content/uploads/"


def u(path, nfd=False):
    """URL d'un fichier de l'ancien WordPress. nfd=True pour les noms dont les accents
    ont été enregistrés décomposés (ex. « Moët » = e + tréma combinant)."""
    if nfd:
        path = unicodedata.normalize("NFD", path)
    return UPLOADS + quote(path, safe="/-_.")


def yt(vid, cap=None, *opts): return ("yt", vid, cap, set(opts))
def video(src, cap=None, *opts): return ("video", src, cap, set(opts))
def img(src, cap=None, *opts): return ("img", src, cap, set(opts))
def txt(text): return ("txt", text, None, set())


ECD_AP = ("Executive Creative Director", "Adrien Mancel & Paul-Émile Raymond")
ECD_TD = ("Executive Creative Director", "Thomas Derouault")
AD = ("Art Director", "Florian Amoneau")
CW = ("Copywriter", "Thomas Blanc")

PROJECTS = [
    dict(slug="the-infrastructors", fn="THE_INFRASTRUCTORS.mp4", name="The Infrastructors", client="Dassault Systèmes",
         h1="Les enfants reprennent les commandes.",
         p="Ce ne sont pas des ingénieurs. Pas des urbanistes. Juste des enfants. Et c’est précisément pour ça qu’il faut les écouter.",
         hero=video("assets/infrastructors-arya-limonade.mp4", None, "loop"),
         media=[yt("qDF0eK64afA", "VIDEO_The_Infrastructors.mp4")],
         gal=[u("2025/07/DASSAULT_" + n) for n in ("EP01.mp4.00_01_13_07.Still005.jpg", "EP03.mp4.00_00_18_24.Still003.jpg",
              "EP02.mp4.00_01_18_14.Still005.jpg", "EP04.mp4.00_00_11_17.Still002.jpg", "EP05.mp4.00_00_00_00.Still001.jpg",
              "EP03.mp4.00_00_08_17.Still002.jpg")], gr="16/9",
         credits=[ECD_AP, AD, CW, ("Directors", "Thomas & Florian")], awards=[]),

    dict(slug="building-tomorrow", fn="BUILDING_TOMORROW.mp4", name="Building Tomorrow", client="Dassault Systèmes",
         h1="Le B2B aussi peut être sexy.",
         p="On est parti de ça.",
         desc="Une tour Eiffel du XXIe siècle, imaginée avec la plateforme de construction de Dassault Systèmes.",
         hero=video(u("2024/11/PL01_Seine_v3.mp4"), None, "nat", "loop"),   # à faire : logo par-dessus la boucle
         media=[img(u("2024/11/buildingtomorrow-data.png"), "Boring_And_Confusing_Screenshot_01.png", "nat", "small"),
                txt("Pour arriver à ça."),
                video(u("2024/11/PL02_Proche_v2-Cut.mov"), "Building_Tomorrow_Reveal.mov", "nat", "big", "loop"),
                txt("Pour démontrer les fonctionnalités de sa plateforme de construction, nous avons proposé à Dassault Systèmes de créer le case study d’un extraordinaire projet de construction fictif : une tour Eiffel élaborée avec les techniques et les enjeux du XXIe siècle grâce à la plateforme de Dassault Systèmes."),
                yt("L2TvitutMIc", "VIDEO_CASE_Building_Tomorrow.mp4"),
                img(u("2024/11/DS_BuildingTomorrow_Board_Final2-scaled.jpg"), "DS_BuildingTomorrow_Board_Final2.jpg", "nat")],
         gal=[], credits=[ECD_AP, CW, ("Production", "Gang Life")],
         awards=[("2023", "THE DRUM AWARDS_WINNER", "B2B Content"), ("2023", "THE DRUM AWARDS_WINNER", "B2B Response to change"),
                 ("2023", "GRAND PRIX DU BRAND CONTENT_GOLD", "B2B"), ("2023", "EPICA_SHORTLIST", "Professional Products & Services"),
                 ("2023", "EPICA_SHORTLIST", "Branded Content"), ("2023", "ONE SHOW_SHORTLIST X6", ""), ("2023", "ANDY AWARDS_SHORTLIST", "")]),

    dict(slug="immunity-potion", fn="IMMUNITY_POTION_Actimel.mp4", name="Immunity Potion", client="Actimel",
         h1="Protéger les joueurs aussi bien en jeu que dans la vraie vie.",
         p="Comme tout le monde, nous avons joué à Fortnite. Et comme tout le monde, nous avons perdu dès la première game. Si seulement il existait une petite boisson super forte qui booste l’immunité des joueurs et les empêche de tomber dès la première confrontation ! Et comme on bossait en même temps pour la marque Actimel, on s’est dit qu’on allait faire exactement ça. Et pour pimenter le tout, on a rajouté des zombies.",
         hero=video(u("2024/11/IP-Logo.mov"), None, "clean", "loop"),
         media=[yt("bgGZbjq2eYg", "VIDEO_CASE_V8Def.mp4"),
                video(u("2024/11/IP-Switch.mov"), "Bottle_Switch.gif", "loop")],
         gal=[u(f"2024/11/Immunity-Potion-Execution-Image-{n}.jpg") for n in (1, 2, 3, 4, 6, 10)], gr="16/9",
         credits=[ECD_AP, AD, CW, ("Developer", "Apfel")],
         awards=[("2024", "EFFIE_SILVER", "")]),

    dict(slug="safety-squad", fn="NUK_SAFETY_SQUAD.mp4", name="The Safety Squad", client="Nuk",
         h1="Nuk veut prendre soin de tous les bébés.",
         p="Alors on leur a proposé d’offrir leur technologie de biberon anti-brûlures directement dans leurs publicités. Ils ont adoré l’idée. Nous avons mis la technologie dans des annonces presse, des flyers… en fait, partout où on peut croiser des bébés.",
         hero=video(u("2024/10/Nuk_IntroMonsters.mp4"), None, "nat", "clean", "loop"),
         media=[video(u("2024/10/SafetySquad-Reveal.mov"), "SafetySquad_Reveal.mov", "nat", "loop", "clean"),
                yt("H4puCuvlLUU", "VIDEO_CASE_Safety_Squad.mp4", "clean")],
         gal=[u(f"2024/10/{n}-scaled.jpg") for n in ("all", "bug_seul", "chaise_haute", "flyer2", "presse", "sous-bock")], gr="auto",
         credits=[ECD_AP, AD, CW, ("Character Designer", "Kristof Luyckx")],
         awards=[("2022", "CANNES LIONS_SHORTLIST", "Media"), ("2022", "EPICA_GOLD", "Direct"), ("2022", "EPICA_SHORTLIST X5", ""),
                 ("2022", "CRESTA AWARDS_BRONZE X4", ""), ("2022", "INNOVATION BY DESIGN_FINALIST", ""), ("2022", "CLIO_SHORTLIST", ""),
                 ("2022", "ONE SHOW_SHORTLIST X3", "")]),

    dict(slug="cuisinella", fn="CUISINEL-LÀ_Cuisinella.mp4", name="Cuisinel-là", client="Cuisinella",
         h1="Toute une campagne qui part de là.\nOu plutôt d’un La.",
         p="",
         desc="Toute une campagne Cuisinella qui part de là. Ou plutôt d’un La.",
         hero=video(u("2024/11/Cuisinella-Gif-Poulet.mp4")),
         media=[video(u("2024/09/Cuisinella-Gif-Topinambour2.mp4"), "Cuisinella_Topinambour.gif"),
                yt("lhlVSG6ijYY", "VIDEO_Cuisinella.mp4")],
         gal=[u(f"2024/11/221216_CUISINELLA-20sec-WEB.mp4.01_00_{t}.jpg") for t in
              ("04_06.Still002", "05_23.Still003", "09_05.Still004", "11_08.Still005", "12_24.Still006", "15_11.Still007")], gr="16/9",
         credits=[ECD_AP, AD, CW, ("Réalisateur", "Big Red Button")], awards=[]),

    dict(slug="parisian-rendez-vous", fn="THE_PARISIAN_RENDEZ-VOUS.mp4", name="The Parisian Rendez-vous", client="Le Drugstore Parisien",
         h1="Vous vous souvenez des trottinettes en libre service ?",
         p="Il y en avait partout dans Paris. On s’est dit qu’il y avait forcément un truc à faire avec pour le lancement du Drugstore Parisien. Vu les résultats, il y avait effectivement un truc à faire. On en vient presque à les regretter, ces bonnes vieilles trottinettes.",
         hero=video(u("2024/10/ANIM-LOGO.mp4"), None, "nat", "clean", "loop"),
         media=[yt("gvrgHtK3zx0", "VIDEO_CASE_Parisian_Rendez-vous.mp4")],
         gal=[u("2024/10/1.jpg"), u("2024/10/2-1.jpg"), u("2024/10/3-1.jpg")], gr="auto",
         credits=[ECD_TD, ("Creative Directors", "Paul-Émile Raymond & Adrien Mancel"), AD, CW,
                  ("Motion Designer", "Thomas Mouilley"), ("Editing", "Agathe Soula – The Good Tape"), ("Head of Production", "Raphaël Fruchard")],
         awards=[("2020", "CLUB DES DA_SILVER", "Activation"), ("2020", "CLUB DES DA_SILVER", "Use of digital"), ("2020", "CLUB DES DA_BRONZE", "Ambient"),
                 ("2020", "D&AD_SHORTLIST", "Direct"), ("2020", "D&AD_SHORTLIST", "Digital"), ("2019", "CANNES LIONS_BRONZE", "Media"),
                 ("2019", "EPICA_GRAND PRIX", "Alternative"), ("2019", "EPICA_GOLD", "Experiential marketing"), ("2019", "EPICA_GOLD", "Mobile")]),

    dict(slug="euphytose-etudiants", fn="EUPHYTOSE_ÉTUDIANTS.mp4", name="Euphytose Étudiants", client="Euphytose",
         h1="Les étudiants aussi sont stressés.",
         p="Euphytose Stress a voulu s’adresser à eux pendant la période de révisions. La marque, plutôt habituée à communiquer auprès de leurs mamans, a accepté d’adopter un ton beaucoup plus amusant.",
         hero=img("assets/euphytose-etudiants-header.jpg", None, "loop"),
         media=[yt("5VE7IdXRTNg", "VIDEO_Revision_01.mp4", "v1"),
                yt("n-SYL-BNttk", "VIDEO_Revision_02.mp4", "v1")],
         gal=[u("2024/10/" + n) for n in ("Napoelon_Revision_v2_29s.00_00_05_04.Still003.jpg", "Napoelon_Revision_v2_29s.00_00_07_15.Still002.jpg",
              "Napoelon_Revision_v2_29s.00_00_12_06.Still001.jpg", "Leonard_Revision_v2_29s.00_00_05_08.Still001.jpg",
              "Leonard_Revision_v2_29s.00_00_03_08.Still003.jpg", "Leonard_Revision_v2_29s.00_00_13_09.Still004.jpg")], gr="16/9",
         credits=[ECD_TD, AD, CW, ("Director", "Nico Galoux")], awards=[]),

    dict(slug="euphytose-stress", fn="EUPHYTOSE_STRESS.mp4", name="Euphytose Stress", client="Euphytose",
         h1="La publicité est partout. Et ça peut être un peu stressant.",
         p="Alors comment faire la pub d’un produit supposé lutter contre le stress ? Comme ça.",
         hero=img("assets/euphytose-stress-header.jpg", None, "loop", "right"),
         media=[yt("2Xf4RDGxRGM", "VIDEO_Euphytose_Stress.mp4")], gal=[],
         credits=[ECD_TD, AD, CW, ("Production", "Blue Paris")], awards=[]),

    dict(slug="synaesthesia", fn="SYNAESTHESIA_Moët&Chandon.mp4", name="Synaesthesia", client="Moët & Chandon",
         h1="Moët & Chandon Synaesthesia.",
         p="Une nouvelle gamme de cocktails destinée à éveiller vos sens en fusionnant champagne et recettes de cocktails emblématiques. À travers cette campagne, nous nous sommes fixé comme objectif de faire ressentir au spectateur les sensations procurées par les cocktails, tout en déguisant une campagne d’image de marque en tutoriels de mixologie.",
         hero=img("assets/synaesthesia-header.jpg", None, "loop"),
         media=[yt("cQ46NoSYuZk", "FILM_Synaesthesia.mp4"),
                video(u("2021/07/Slide1-MoëtSynesthesia-InstaStory-V5.mp4", nfd=True), None, "nat", "full", "loop"),
                video(u("2021/07/Slide2-MoëtSynesthesia-Recipes-V2.mp4", nfd=True), None, "nat", "full", "loop")],
         gal=[], credits=[("Creative Directors", "Paul-Émile Raymond & Adrien Mancel"), AD, CW, ("Directors", "Julien & Quentin")], awards=[]),
]
