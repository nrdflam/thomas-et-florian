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
| `tools/dist.py` | Prépare `dist/`, le dossier à envoyer chez OVH (vérifie pages, liens et poids). |
| `.htaccess` | Réglages Apache pour OVH : redirections des anciennes adresses WordPress, page 404, sécurité, cache. |
| `404.html` | Page « introuvable ». |
| `canape.html` | Le canapé en ASCII (ouvert par le Konami code depuis la home, ou seul). |
| `assets/` | Images, vidéos et favicon hébergés sur le site. `assets/wp/` : médias rapatriés de l'ancien WordPress, compressés. |

## Ajouter ou modifier un projet

1. Éditer `tools/projects.py`. Les types de médias et leurs options sont décrits en tête du fichier.
2. Lancer `python3 tools/gen.py`. Le générateur refuse un contenu invalide : option inconnue, identifiant YouTube mal formé, fichier local absent.
3. Pour un nouveau projet, ajouter aussi sa case dans la galerie de `index.html` (tableau `P`).

## Bouton DEV

Il est caché aux visiteurs.

- Pour l'afficher sur un navigateur, ouvrir une page projet avec `?dev` (par exemple `immunity-potion.html?dev`). Il reste ensuite visible sur ce navigateur.
- Pour le masquer, ouvrir une page avec `?dev=0`.

## Mise en ligne (OVH)

1. `python3 tools/gen.py` puis `python3 tools/dist.py`.
2. Envoyer **le contenu** de `dist/` à la racine du dossier du site sur l'hébergement (Cyberduck, FTP), fichiers cachés compris (`.htaccess`).
3. Une fois le certificat SSL actif chez OVH, décommenter le bloc « HTTPS obligatoire » de `.htaccess`.

Quota de l'hébergement gratuit : 100 Mo. `dist.py` refuse de préparer le dossier au-delà de 90 Mo.

## Points de vigilance

- **Vidéos.** Encoder en `.mp4` H.264 (`yuv420p`, `-movflags +faststart`, sans piste son pour les boucles) : les `.mov` ne sont pas lus partout. Les films longs restent sur YouTube.
- **Polices.** Elles sont servies par Google Fonts. Pour ne plus dépendre de Google, les héberger dans `assets/`.
