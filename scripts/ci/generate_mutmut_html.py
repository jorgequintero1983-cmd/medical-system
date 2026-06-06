"""Genera reporte HTML a partir de la salida de mutmut."""

from __future__ import annotations

import html
import sys
from pathlib import Path


def _read(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def generate(
    results_path: str = "resultados-mutacion.txt",
    log_path: str = "resultados-mutacion.log",
    output_path: str = "reportes-html/mutacion/index.html",
) -> None:
    results = _read(Path(results_path))
    log = _read(Path(log_path))

    sections = [
        ("Resumen de mutación", results or "Sin resultados disponibles."),
    ]
    if log.strip():
        sections.append(("Log de ejecución", log))

    body = ""
    for title, content in sections:
        body += f"""
    <section>
      <h2>{html.escape(title)}</h2>
      <pre>{html.escape(content)}</pre>
    </section>"""

    page = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Reporte de Mutación - Backend</title>
  <style>
    body {{
      font-family: Segoe UI, Arial, sans-serif;
      margin: 2rem auto;
      max-width: 1100px;
      background: #f5f7fa;
      color: #1f2937;
    }}
    h1 {{ color: #0078d4; margin-bottom: 0.25rem; }}
    p {{ color: #4b5563; }}
    section {{
      background: #fff;
      border: 1px solid #d1d5db;
      border-radius: 8px;
      padding: 1rem 1.25rem;
      margin-top: 1.25rem;
    }}
    h2 {{ margin-top: 0; font-size: 1.1rem; }}
    pre {{
      white-space: pre-wrap;
      word-break: break-word;
      background: #f9fafb;
      padding: 1rem;
      border-radius: 6px;
      overflow-x: auto;
    }}
  </style>
</head>
<body>
  <h1>Pruebas de Mutación - Backend</h1>
  <p>Medical System — reporte generado en pipeline CI/CD</p>
  {body}
</body>
</html>"""

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8")
    print(f"Reporte HTML generado: {output_path}")


if __name__ == "__main__":
    results = sys.argv[1] if len(sys.argv) > 1 else "resultados-mutacion.txt"
    log = sys.argv[2] if len(sys.argv) > 2 else "resultados-mutacion.log"
    output = sys.argv[3] if len(sys.argv) > 3 else "reportes-html/mutacion/index.html"
    generate(results, log, output)
