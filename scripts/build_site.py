#!/usr/bin/env python3
from __future__ import annotations

import re
import shutil
import subprocess
from html import escape
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SITE_SRC = REPO / "site"
PUBLIC = REPO / "_public"
PDF_DIR = PUBLIC / "pdf"
WEEKS_DIR = PUBLIC / "weeks"
REPORTS = [
    ("howtoreports", "Cómo hacer reportes"),
]

ASSET_EXTS = ("*.png", "*.jpg", "*.jpeg", "*.svg", "*.gif", "*.webp", "*.pdf")  # ojo: aquí NO copiamos notes.pdf
CODE_EXTS = ("*.py", "*.ipynb", "*.jl", "*.m", "*.r", "*.txt", "*.pdf")


def format_week_label(week_name: str) -> str:
    m = re.fullmatch(r"week(\d+)", week_name)
    if not m:
        return week_name
    return f"semana {m.group(1)}"


def week_number(week_name: str) -> int | None:
    m = re.fullmatch(r"week(\d+)", week_name)
    if not m:
        return None
    return int(m.group(1))


def run(cmd: list[str], cwd: Path) -> None:
    p = subprocess.run(cmd, cwd=str(cwd))
    if p.returncode != 0:
        raise RuntimeError(f"Command failed ({p.returncode}): {' '.join(cmd)} (cwd={cwd})")


def copy_site_skeleton() -> None:
    if PUBLIC.exists():
        shutil.rmtree(PUBLIC)
    shutil.copytree(SITE_SRC, PUBLIC)


def find_weeks() -> list[Path]:
    return sorted([p for p in REPO.glob("week*/") if p.is_dir()])


def build_directory(target: Path, label: str) -> str | None:
    mk = target / "Makefile"
    if not mk.exists():
        print(f"==> Skipping {label} (no Makefile)")
        return None

    print(f"==> Building {label} (make)")
    try:
        run(["make"], cwd=target)
    except RuntimeError as exc:
        print(f"!! Build failed for {label}: {exc}")
        return f"{label}: build failed ({exc})"

    return None


def read_links_file(week: Path) -> list[str]:
    links_file = week / "codes" / "links.txt"
    if not links_file.exists():
        return []

    links: list[str] = []
    for line in links_file.read_text(encoding="utf-8").splitlines():
        link = line.strip()
        if not link or link.startswith("#"):
            continue
        links.append(link)
    return links


def write_week_page(week: Path, out: Path, assets: list[str], codes: list[str], links: list[str]) -> None:
    week_label = format_week_label(week.name)

    def to_items(names: list[str], prefix: str) -> str:
        if not names:
            return "<li>No hay archivos disponibles todavía.</li>"
        return "\n".join([f'<li><a href="{prefix}/{name}">{name}</a></li>' for name in names])

    links_items = (
        "<li>No hay enlaces disponibles todavía.</li>"
        if not links
        else "\n".join(
            [
                f'<li><a href="{escape(link, quote=True)}" target="_blank" rel="noopener noreferrer">{escape(link)}</a></li>'
                for link in links
            ]
        )
    )

    html = f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{week_label} · Material del curso</title>
  <style>
    body {{ font-family: system-ui, sans-serif; margin: 2rem; max-width: 900px; line-height: 1.5; }}
    h1 {{ margin-bottom: .25rem; }}
    .back {{ display: inline-block; margin-bottom: 1rem; }}
    section {{ margin-top: 1.25rem; }}
  </style>
</head>
<body>
  <a class="back" href="../../index.html">← Volver al inicio</a>
  <h1>{week_label}</h1>
  <p>Recursos de la semana para el curso Modelos Computacionales para la Física y Astronomía.</p>

  <section>
    <h2>Imágenes de la presentación</h2>
    <ul>
      {to_items(assets, 'assets')}
    </ul>
  </section>

  <section>
    <h2>Códigos y documentos adicionales</h2>
    <p>Archivos de apoyo para la semana (incluye <code>.py</code>, <code>.ipynb</code>, <code>.pdf</code> y otros formatos de código/documentos).</p>
    <ul>
      {to_items(codes, 'codes')}
    </ul>
  </section>

  <section>
    <h2>Links recomendados</h2>
    <p>Si existe un archivo <code>links.txt</code>, sus enlaces se publican aquí automáticamente.</p>
    <ul>
      {links_items}
    </ul>
  </section>
</body>
</html>
"""
    (out / "index.html").write_text(html, encoding="utf-8")


def publish_week_assets(week: Path) -> None:
    out = WEEKS_DIR / week.name
    out.mkdir(parents=True, exist_ok=True)
    asset_dir = out / "assets"
    codes_dir = out / "codes"
    asset_dir.mkdir(exist_ok=True)
    codes_dir.mkdir(exist_ok=True)

    published_assets: list[str] = []
    published_codes: list[str] = []

    for ext in ASSET_EXTS:
        for f in week.glob(ext):
            if f.name == "notes.pdf":
                continue
            shutil.copy2(f, asset_dir / f.name)
            published_assets.append(f.name)

    week_codes_dir = week / "codes"
    if week_codes_dir.exists():
        for ext in CODE_EXTS:
            for f in week_codes_dir.glob(ext):
                shutil.copy2(f, codes_dir / f.name)
                published_codes.append(f.name)

    links = read_links_file(week)
    write_week_page(week, out, sorted(published_assets), sorted(published_codes), links)


def collect_pdfs() -> tuple[list[tuple[str, str | None]], list[str]]:
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    items: list[tuple[str, str | None]] = []
    failures: list[str] = []

    for week in find_weeks():
        build_error = build_directory(week, week.name)
        if build_error:
            failures.append(build_error)

        pdf = week / "notes.pdf"
        if pdf.exists():
            target = PDF_DIR / f"{week.name}.pdf"
            shutil.copy2(pdf, target)
            pdf_name = target.name
        else:
            print(f"!! No PDF found for {week.name}: expected {pdf}")
            pdf_name = None
            if (week / "Makefile").exists():
                failures.append(f"{week.name}: Makefile present but notes.pdf was not produced")

        publish_week_assets(week)
        items.append((week.name, pdf_name))

    return items, failures


def collect_reports() -> tuple[list[tuple[str, str, str | None]], list[str]]:
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    items: list[tuple[str, str, str | None]] = []
    failures: list[str] = []

    for folder, label in REPORTS:
        report_dir = REPO / folder
        if not report_dir.exists():
            print(f"!! Report folder not found: {report_dir}")
            items.append((folder, label, None))
            failures.append(f"{folder}: report folder not found")
            continue

        build_error = build_directory(report_dir, folder)
        if build_error:
            failures.append(build_error)

        pdf = report_dir / "notes.pdf"
        if pdf.exists():
            target = PDF_DIR / f"{folder}.pdf"
            shutil.copy2(pdf, target)
            pdf_name = target.name
        else:
            print(f"!! No PDF found for report {folder}: expected {pdf}")
            pdf_name = None
            if (report_dir / "Makefile").exists():
                failures.append(f"{folder}: Makefile present but notes.pdf was not produced")

        items.append((folder, label, pdf_name))

    return items, failures


def write_index(
    pdfs: list[tuple[str, str | None]],
    reports: list[tuple[str, str, str | None]],
) -> None:
    idx = PUBLIC / "index.html"
    html = idx.read_text(encoding="utf-8")

    marker = '<div id="weeks-units">'
    start = html.find(marker)
    if start == -1:
        raise RuntimeError('No encuentro <div id="weeks-units"> en site/index.html')

    before = html[: start + len(marker)]
    after = html[html.find("</div>", start):]

    units = [
        ("UNIDAD I", 1, 4),
        ("UNIDAD II", 5, 8),
        ("UNIDAD III", 9, 12),
        ("UNIDAD EXTRA", 13, 16),
    ]

    sections: list[str] = []
    for title, week_min, week_max in units:
        unit_items: list[str] = []
        for week, fname in pdfs:
            wnum = week_number(week)
            if wnum is None or not (week_min <= wnum <= week_max):
                continue

            week_label = format_week_label(week)
            links = [f'<a href="weeks/{week}/">contenido</a>']
            if fname:
                mtime = int((PDF_DIR / fname).stat().st_mtime)
                links.insert(0, f'<a href="pdf/{fname}?v={mtime}" target="_blank">apuntes</a>')

            unit_items.append(f'\n          <li><strong>{week_label}</strong><span>{" · ".join(links)}</span></li>')

        if not unit_items:
            unit_items.append('\n          <li><strong>Sin semanas publicadas</strong><span>Próximamente</span></li>')

        section_html = (
            f'\n        <section class="weeks-unit">'
            '\n          <details class="weeks-unit-details" open>'
            '\n            <summary class="weeks-unit-summary">'
            f'\n              <h2>Contenido por semana {title}</h2>'
            '\n              <span class="toggle-label" aria-hidden="true"></span>'
            '\n            </summary>'
            '\n            <p>Accede al contenido organizado por semana. Cada entrada incluye el material de lectura y la carpeta <code>codes/</code> para scripts y notebooks.</p>'
            '\n            <ul class="weeks-list">'
            + "".join(unit_items)
            + '\n            </ul>'
            '\n          </details>'
            '\n        </section>'
        )
        sections.append(section_html)

    html = before + "".join(sections) + "\n      " + after

    reports_marker = '<ul id="reports">'
    reports_start = html.find(reports_marker)
    if reports_start == -1:
        raise RuntimeError('No encuentro <ul id="reports"> en site/index.html')

    reports_before = html[: reports_start + len(reports_marker)]
    reports_after = html[html.find("</ul>", reports_start):]

    reports_list = []
    for _report_folder, report_label, report_fname in reports:
        if report_fname:
            mtime = int((PDF_DIR / report_fname).stat().st_mtime)
            report_link = f'pdf/{report_fname}?v={mtime}'
            reports_list.append(
                f'\n      <li><strong>{escape(report_label)}</strong><span><a href="{report_link}" target="_blank">ver PDF</a></span></li>'
            )
        else:
            reports_list.append(
                f'\n      <li><strong>{escape(report_label)}</strong><span>PDF no disponible</span></li>'
            )

    reports_html = "".join(reports_list) + "\n    "
    idx.write_text(reports_before + reports_html + reports_after, encoding="utf-8")


def main() -> None:
    copy_site_skeleton()
    pdfs, week_failures = collect_pdfs()
    reports, report_failures = collect_reports()
    write_index(pdfs, reports)

    print(f"Public listo en: {PUBLIC}")
    published = sum(1 for _week, fname in pdfs if fname)
    print(f"PDFs publicados: {published}")

    failures = week_failures + report_failures
    if failures:
        details = "\n".join(f"- {failure}" for failure in failures)
        raise SystemExit(f"Build completed with missing required PDFs:\n{details}")


if __name__ == "__main__":
    main()
