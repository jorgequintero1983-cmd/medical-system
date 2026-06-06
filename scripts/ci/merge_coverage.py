#!/usr/bin/env python3
"""Fusiona cobertura backend (coverage.py) y frontend (Vitest) en un solo Cobertura.xml."""

from __future__ import annotations

import argparse
import time
import xml.etree.ElementTree as ET
from copy import deepcopy
from pathlib import Path


def _count_lines(root: ET.Element) -> tuple[int, int]:
    valid = 0
    covered = 0
    for line in root.iter("line"):
        valid += 1
        if int(line.get("hits", "0")) > 0:
            covered += 1
    return valid, covered


def _load_packages(path: Path) -> list[ET.Element]:
    root = ET.parse(path).getroot()
    packages = root.find("packages")
    if packages is None:
        return []
    return list(packages.findall("package"))


def _normalize_frontend_class(class_elem: ET.Element) -> None:
    filename = class_elem.get("filename", "").replace("\\", "/")
    if filename.startswith("src/"):
        filename = filename[4:]
    class_elem.set("filename", filename)


def merge_coverage(
    backend_xml: Path,
    frontend_xml: Path,
    output_xml: Path,
) -> tuple[int, int, float]:
    packages: list[ET.Element] = []

    for package in _load_packages(backend_xml):
        merged_pkg = deepcopy(package)
        merged_pkg.set("name", f"backend.{package.get('name') or 'root'}")
        packages.append(merged_pkg)

    for package in _load_packages(frontend_xml):
        merged_pkg = deepcopy(package)
        merged_pkg.set("name", f"frontend.{package.get('name', 'main')}")
        classes = merged_pkg.find("classes")
        if classes is not None:
            for class_elem in classes.findall("class"):
                _normalize_frontend_class(class_elem)
        packages.append(merged_pkg)

    lines_valid, lines_covered = 0, 0
    for package in packages:
        valid, covered = _count_lines(package)
        lines_valid += valid
        lines_covered += covered

    line_rate = lines_covered / lines_valid if lines_valid else 0.0

    root = ET.Element("coverage")
    root.set("version", "1.0")
    root.set("timestamp", str(int(time.time() * 1000)))
    root.set("lines-valid", str(lines_valid))
    root.set("lines-covered", str(lines_covered))
    root.set("line-rate", f"{line_rate:.4f}")
    root.set("branches-valid", "0")
    root.set("branches-covered", "0")
    root.set("branch-rate", "0")

    sources = ET.SubElement(root, "sources")
    ET.SubElement(sources, "source").text = "backend/app"
    ET.SubElement(sources, "source").text = "frontend/medical-frontend/src"

    packages_el = ET.SubElement(root, "packages")
    for package in packages:
        packages_el.append(package)

    output_xml.parent.mkdir(parents=True, exist_ok=True)
    tree = ET.ElementTree(root)
    if hasattr(ET, "indent"):
        ET.indent(tree, space="  ")
    tree.write(
        output_xml,
        encoding="unicode",
        xml_declaration=True,
    )

    return lines_valid, lines_covered, line_rate


def main() -> None:
    parser = argparse.ArgumentParser(description="Fusionar reportes Cobertura backend + frontend")
    parser.add_argument(
        "--backend",
        default="coverage.xml",
        help="Ruta al coverage.xml del backend",
    )
    parser.add_argument(
        "--frontend",
        default="frontend/medical-frontend/coverage/cobertura-coverage.xml",
        help="Ruta al cobertura-coverage.xml del frontend",
    )
    parser.add_argument(
        "--output",
        default="reportes-html/cobertura-proyecto/Cobertura.xml",
        help="Ruta de salida del reporte unificado",
    )
    args = parser.parse_args()

    backend = Path(args.backend)
    frontend = Path(args.frontend)
    output = Path(args.output)

    if not backend.is_file():
        raise SystemExit(f"No se encontró cobertura backend: {backend}")
    if not frontend.is_file():
        raise SystemExit(f"No se encontró cobertura frontend: {frontend}")

    valid, covered, rate = merge_coverage(backend, frontend, output)
    print(
        f"Reporte unificado generado: {output} "
        f"({covered}/{valid} líneas, {rate * 100:.1f}%)"
    )


if __name__ == "__main__":
    main()
