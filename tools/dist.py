#!/usr/bin/env python3
"""Prépare le dossier à envoyer sur l'hébergement OVH.

    python3 tools/dist.py        écrit dist/ (pages, assets, .htaccess), sans les outils de dev

Vérifie avant : pages générées à jour, aucun fichier local référencé manquant,
taille totale sous le quota de l'hébergement gratuit (100 Mo).
"""
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
QUOTA_MB = 100
MARGIN_MB = 10          # place laissée aux fichiers techniques d'OVH


def site_files():
    files = [p for p in ROOT.glob("*.html")] + [ROOT / ".htaccess"]
    files += [p for p in (ROOT / "assets").rglob("*") if p.is_file() and not p.name.startswith(".")]
    return sorted(files)


def check_refs(files):
    """Chaque src/href/url() local des pages doit exister."""
    missing = []
    for page in (p for p in files if p.suffix == ".html"):
        text = page.read_text(encoding="utf-8")
        for ref in re.findall(r'(?:src|href)=["\']([^"\'#?]+)|"(assets/[^"]+)"', text):
            ref = ref[0] or ref[1]
            if re.match(r"(https?:|mailto:|tel:|data:|//)", ref) or "${" in ref or ref in ("/", ""):
                continue
            if not (ROOT / ref.lstrip("/")).is_file():
                missing.append(f"{page.name} → {ref}")
    return missing


def main():
    if subprocess.run([sys.executable, str(ROOT / "tools/gen.py"), "--check"]).returncode:
        raise SystemExit("Pages projet pas à jour : lancer python3 tools/gen.py")
    files = site_files()
    missing = check_refs(files)
    if missing:
        raise SystemExit("Fichiers référencés introuvables :\n  " + "\n  ".join(missing))
    total = sum(p.stat().st_size for p in files) / 1e6
    if total > QUOTA_MB - MARGIN_MB:
        raise SystemExit(f"Trop lourd : {total:.1f} Mo (limite conseillée {QUOTA_MB - MARGIN_MB} Mo)")
    shutil.rmtree(DIST, ignore_errors=True)
    for p in files:
        dst = DIST / p.relative_to(ROOT)
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, dst)
    print(f"dist/ prêt : {len(files)} fichiers, {total:.1f} Mo sur {QUOTA_MB} Mo")


if __name__ == "__main__":
    main()
