#!/usr/bin/env python3
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SITE_SRC = REPO / "site"
PUBLIC = REPO / "_public"
PDF_DIR = PUBLIC / "pdf"
WEEKS_DIR = PUBLIC / "weeks"

ASSET_EXTS = ("*.png", "*.jpg", "*.jpeg", "*.svg", "*.gif", "*.webp", "*.pdf")  # ojo: aquí NO copiamos notes.pdf
CODE_EXTS = ("*.py", "*.ipynb")  # opcional

def run(cmd: list[str], cwd: Path) -> None:
    p = subprocess.run(cmd, cwd=str(cwd))
    if p.returncode != 0:
        raise RuntimeError(f"Command failed ({p.returncode}): {' '.join(cmd)} (cwd={cwd})")

def copy_site_skeleton():
    if PUBLIC.exists():
        shutil.rmtree(PUBLIC)
    shutil.copytree(SITE_SRC, PUBLIC)

def find_weeks():
    return sorted([p for p in REPO.glob("week*/") if p.is_dir()])

def build_week(week: Path) -> None:
    mk = week / "Makefile"
    if mk.exists():
        # Esto fuerza a que exista notes.pdf si el Makefile lo produce
        print(f"==> Building {week.name} (make)")
        run(["make"], cwd=week)
    else:
        print(f"==> Skipping {week.name} (no Makefile)")

def publish_week_assets(week: Path):
    out = WEEKS_DIR / week.name
    out.mkdir(parents=True, exist_ok=True)

    # Copia imágenes/logo/etc
    for ext in ASSET_EXTS:
        for f in week.glob(ext):
            # Evita duplicar notes.pdf en assets (lo servimos desde /pdf/)
            if f.name == "notes.pdf":
                continue
            shutil.copy2(f, out / f.name)

    # (Opcional) publicar scripts
    # for ext in CODE_EXTS:
    #     for f in week.glob(ext):
    #         shutil.copy2(f, out / f.name)

def collect_pdfs():
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    items = []

    for week in find_weeks():
        # 1) Compila semana (make)
        build_week(week)

        # 2) Copia PDF si existe
        pdf = week / "notes.pdf"
        if pdf.exists():
            target = PDF_DIR / f"{week.name}.pdf"
            shutil.copy2(pdf, target)
            items.append((week.name, target.name))
        else:
            print(f"!! No PDF found for {week.name}: expected {pdf}")

        # 3) Copia assets
        publish_week_assets(week)

    return items

def write_index(pdfs):
    idx = PUBLIC / "index.html"
    html = idx.read_text(encoding="utf-8")

    marker = '<ul id="weeks">'
    start = html.find(marker)
    if start == -1:
        raise RuntimeError('No encuentro <ul id="weeks"> en site/index.html')

    before = html[: start + len(marker)]
    after = html[html.find("</ul>", start):]

    items = []
    for week, fname in pdfs:
        # cache-buster por mtime: evita que el browser muestre PDF viejo
        mtime = int((PDF_DIR / fname).stat().st_mtime)
        items.append(
            f'\n      <li>'
            f'<a href="pdf/{fname}?v={mtime}" target="_blank">{week}</a>'
            f' — <a href="weeks/{week}/">assets</a>'
            f'</li>'
        )

    new_list = "".join(items) + "\n    "
    idx.write_text(before + new_list + after, encoding="utf-8")

def main():
    copy_site_skeleton()
    pdfs = collect_pdfs()
    write_index(pdfs)
    print(f"Public listo en: {PUBLIC}")
    print(f"PDFs publicados: {len(pdfs)}")

if __name__ == "__main__":
    main()
