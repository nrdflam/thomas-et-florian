# thomasetflorian.com

Site statique (HTML, CSS et JavaScript sans dépendance), hébergé sur GitHub Pages.

## Fichiers

| Fichier | Rôle |
|---|---|
| `index.html` | La home : script tapé, galerie des projets, awards, frise « Nous », easter egg (Konami). Fichier source, à modifier directement. |
| `<projet>.html` | Pages projet **générées** : ne pas les modifier à la main. |
| `tools/projects.py` | Contenu des pages projet : textes, médias, crédits, awards, ordre de navigation. |
| `tools/template.html` | Gabarit commun des pages projet : mise en page, styles, scripts. |
| `tools/gen.py` | Générateur : `python3 tools/gen.py` écrit les pages ; `python3 tools/gen.py --check` vérifie qu'elles sont à jour. |
| `canape.html` | Le canapé en ASCII (ouvert par le Konami code depuis la home, ou seul). |
| `assets/` | Images, vidéos et favicon hébergés sur le site. |

## Ajouter ou modifier un projet

1. Éditer `tools/projects.py`. Les types de médias et leurs options sont décrits en tête du fichier.
2. Lancer `python3 tools/gen.py`. Le générateur refuse un contenu invalide : option inconnue, identifiant YouTube mal formé, fichier local absent.
3. Pour un nouveau projet, ajouter aussi sa case dans la galerie de `index.html` (tableau `P`).

## Bouton DEV

Il est caché aux visiteurs.

- Pour l'afficher sur un navigateur, ouvrir une page projet avec `?dev` (par exemple `immunity-potion.html?dev`). Il reste ensuite visible sur ce navigateur.
- Pour le masquer, ouvrir une page avec `?dev=0`.

## Points de vigilance

- **Médias de l'ancien WordPress.** Une partie des vidéos et images est encore chargée depuis `thomasetflorian.com/wp-content/uploads/`. Quand le domaine pointera vers ce site, ces fichiers disparaîtront : il faudra les copier dans `assets/` et mettre à jour les adresses (`UPLOADS` dans `tools/projects.py`, constante `U` dans `index.html`).
- **Vidéos `.mov`.** Elles ne sont lues par Chrome et Firefox que si elles sont encodées en H.264. Les convertir en `.mp4` H.264 au moment du rapatriement.
- **Polices.** Elles sont servies par Google Fonts. Pour ne plus dépendre de Google, les héberger dans `assets/`.
