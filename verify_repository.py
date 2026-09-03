#!/usr/bin/env python3
"""Verify the integrity and inspectability of the published repository artifacts.

This checker intentionally uses only the Python standard library. It verifies the
files that are actually published here; it does not pretend to reproduce the
financial engine or reperform accounting tests that require the private instance.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote
from zipfile import BadZipFile, ZipFile
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "artifact-manifest.json"
MAIN_NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
REL_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def inspect_workbook(path: Path) -> dict[str, object]:
    with ZipFile(path) as archive:
        names = archive.namelist()
        workbook = ET.fromstring(archive.read("xl/workbook.xml"))
        sheets = [
            node.attrib["name"]
            for node in workbook.findall(f".//{{{MAIN_NS}}}sheet")
        ]
        formulas = 0
        for name in names:
            if name.startswith("xl/worksheets/sheet") and name.endswith(".xml"):
                sheet = ET.fromstring(archive.read(name))
                formulas += len(sheet.findall(f".//{{{MAIN_NS}}}f"))

        calc = workbook.find(f".//{{{MAIN_NS}}}calcPr")
        full_calc = calc is not None and calc.attrib.get("fullCalcOnLoad") == "1"
        external_links = [name for name in names if name.startswith("xl/externalLinks/")]
        macros = [name for name in names if name.endswith("vbaProject.bin")]

    return {
        "sheets": sheets,
        "formula_cells": formulas,
        "full_calculation_on_load": full_calc,
        "external_links": external_links,
        "macros": macros,
    }


def check_artifacts(manifest: dict[str, object]) -> tuple[list[str], list[str]]:
    passed: list[str] = []
    failed: list[str] = []

    for artifact in manifest["artifacts"]:
        relative = artifact["path"]
        path = ROOT / relative
        if not path.is_file():
            failed.append(f"missing artifact: {relative}")
            continue

        actual_hash = sha256(path)
        if actual_hash != artifact["sha256"]:
            failed.append(f"checksum mismatch: {relative}")
            continue

        if artifact["type"] != "xlsx":
            passed.append(f"{relative}: checksum")
            continue

        try:
            observed = inspect_workbook(path)
        except (BadZipFile, ET.ParseError, KeyError) as error:
            failed.append(f"invalid workbook {relative}: {error}")
            continue

        expected_fields = ("sheets", "formula_cells", "full_calculation_on_load")
        mismatches = [
            field
            for field in expected_fields
            if observed[field] != artifact[field]
        ]
        if observed["external_links"] and not artifact["allow_external_links"]:
            mismatches.append("external_links")
        if observed["macros"] and not artifact["allow_macros"]:
            mismatches.append("macros")

        if mismatches:
            failed.append(f"{relative}: unexpected {', '.join(mismatches)}")
        else:
            passed.append(
                f"{relative}: {len(observed['sheets'])} sheets, "
                f"{observed['formula_cells']} formulas, no external links or macros"
            )

    return passed, failed


LINK_PATTERN = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")


def check_markdown_links() -> tuple[list[str], list[str]]:
    failed: list[str] = []
    markdown_files = sorted(ROOT.rglob("*.md"))

    for document in markdown_files:
        text = document.read_text(encoding="utf-8")
        for raw_target in LINK_PATTERN.findall(text):
            target = raw_target.strip().split(maxsplit=1)[0].strip("<>")
            if not target or target.startswith(("#", "http://", "https://", "mailto:")):
                continue
            file_part = unquote(target.split("#", 1)[0])
            if file_part and not (document.parent / file_part).exists():
                failed.append(f"broken link in {document.relative_to(ROOT)}: {target}")

    passed = [f"{len(markdown_files)} Markdown files: relative links resolve"] if not failed else []
    return passed, failed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="emit machine-readable output")
    args = parser.parse_args()

    try:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        print(f"FAIL: cannot read artifact-manifest.json: {error}", file=sys.stderr)
        return 1

    passed, failed = check_artifacts(manifest)
    link_passed, link_failed = check_markdown_links()
    passed.extend(link_passed)
    failed.extend(link_failed)

    result = {"ok": not failed, "passed": passed, "failed": failed}
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        for message in passed:
            print(f"PASS  {message}")
        for message in failed:
            print(f"FAIL  {message}")
        print(f"\n{'VERIFIED' if not failed else 'FAILED'}: {len(passed)} passed, {len(failed)} failed")

    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
