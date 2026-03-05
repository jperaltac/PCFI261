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
CODE_EXTS = ("*.py", "*.ipynb", "*.jl", "*.m", "*.r", "*.txt")

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

def write_week_page(week: Path, out: Path, assets: list[str], codes: list[str]):
    def to_items(names: list[str], prefix: str) -> str:
        if not names:
            return "<li>No hay archivos disponibles todavía.</li>"
        return "\n".join([f'<li><a href="{prefix}/{name}">{name}</a></li>' for name in names])

    html = f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{week.name} · Material del curso</title>
  <style>
    body {{ font-family: system-ui, sans-serif; margin: 2rem; max-width: 900px; line-height: 1.5; }}
    h1 {{ margin-bottom: .25rem; }}
    .back {{ display: inline-block; margin-bottom: 1rem; }}
    section {{ margin-top: 1.25rem; }}
  </style>
</head>
<body>
  <a class="back" href="../../index.html">← Volver al inicio</a>
  <h1>{week.name}</h1>
  <p>Recursos de la semana para el curso Modelos Computacionales para la Física y Astronomía.</p>

  <section>
    <h2>Contenido</h2>
    <ul>
      {to_items(assets, 'assets')}
    </ul>
  </section>

  <section>
    <h2>codes/</h2>
    <ul>
      {to_items(codes, 'codes')}
    </ul>
  </section>
</body>
</html>
"""
    (out / "index.html").write_text(html, encoding="utf-8")


def publish_week_assets(week: Path):
    out = WEEKS_DIR / week.name
    out.mkdir(parents=True, exist_ok=True)
    asset_dir = out / "assets"
    codes_dir = out / "codes"
    asset_dir.mkdir(exist_ok=True)
    codes_dir.mkdir(exist_ok=True)

    published_assets: list[str] = []
    published_codes: list[str] = []

    # Copia imágenes/logo/etc
    for ext in ASSET_EXTS:
        for f in week.glob(ext):
            # Evita duplicar notes.pdf en assets (lo servimos desde /pdf/)
            if f.name == "notes.pdf":
                continue
            shutil.copy2(f, asset_dir / f.name)
            published_assets.append(f.name)

    for ext in CODE_EXTS:
        for f in (week / "codes").glob(ext):
            shutil.copy2(f, codes_dir / f.name)
            published_codes.append(f.name)

    write_week_page(week, out, sorted(published_assets), sorted(published_codes))

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
            pdf_name = target.name
        else:
            print(f"!! No PDF found for {week.name}: expected {pdf}")
            pdf_name = None

        # 3) Copia assets
        publish_week_assets(week)

        items.append((week.name, pdf_name))

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
        links = [f'<a href="weeks/{week}/">contenido</a>', f'<a href="weeks/{week}/codes/">codes/</a>']
        if fname:
            mtime = int((PDF_DIR / fname).stat().st_mtime)
            links.insert(0, f'<a href="pdf/{fname}?v={mtime}" target="_blank">apuntes</a>')

        items.append(f'\n      <li><strong>{week}</strong><span>{" · ".join(links)}</span></li>')

    new_list = "".join(items) + "\n    "
    idx.write_text(before + new_list + after, encoding="utf-8")

def main():
    copy_site_skeleton()
    pdfs = collect_pdfs()
    write_index(pdfs)
    print(f"Public listo en: {PUBLIC}")
    published = sum(1 for _week, fname in pdfs if fname)
    print(f"PDFs publicados: {published}")

if __name__ == "__main__":
    main()
