#!/usr/bin/env python3

"""Valida politica de idioma definida en AGENTS.md."""

from __future__ import annotations

import argparse
import fnmatch
import pathlib
import re
import subprocess
import sys


ENGLISH_ONLY_PATTERNS = [
    "agents/*/agent.md",
    "skills/*/skill.md",
]

SPANISH_REQUIRED_PATTERNS = [
    "README.md",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    "SECURITY.md",
    "GOVERNANCE.md",
    "AGENTS.md",
    "docs/**/*.md",
    "templates/**/*.md",
    "agents/**/README.md",
    "agents/**/examples/**/*.md",
    "skills/**/README.md",
    "skills/**/examples/**/*.md",
    ".github/ISSUE_TEMPLATE/*.md",
    ".github/pull_request_template.md",
]

ENGLISH_MARKERS_FOR_SPANISH_FILES = [
    "## Purpose",
    "## Inputs",
    "## Workflow",
    "## Process",
    "## Output Format",
    "## Guardrails",
    "## Quality Checks",
    "## Failure Mode",
    "## Current Docs",
    "## Available",
    "## Usage",
    "## Summary",
    "## Why",
    "## Scope",
    "## Validation",
    "# Example",
    "Input:",
    "Output:",
    "Used by:",
]

SPANISH_MARKERS_FOR_ENGLISH_FILES = [
    "## Proposito",
    "## Entradas",
    "## Flujo",
    "## Proceso",
    "## Formato de salida",
    "## Barandillas",
    "## Controles de calidad",
    "## Modo de falla",
    "Salida:",
    "Entrada:",
    "# Ejemplo",
]

CONVENTIONAL_RE = re.compile(
    r"^(feat|fix|docs|ci|chore|refactor|test|build|perf|style|revert)(\([^)]+\))?!?:\s+(.+)$",
    re.IGNORECASE,
)

SPANISH_HINT_WORDS = {
    "agrega",
    "actualiza",
    "corrige",
    "mejora",
    "define",
    "valida",
    "normaliza",
    "documenta",
    "habilita",
    "elimina",
    "ajusta",
    "crea",
    "cambia",
    "soporte",
    "politica",
    "idioma",
    "calidad",
    "guia",
    "plantilla",
    "estructura",
    "agente",
    "skill",
    "skills",
    "matriz",
}


def run(cmd: list[str]) -> str:
    return subprocess.check_output(cmd, text=True).strip()


def matches_any(path: str, patterns: list[str]) -> bool:
    return any(fnmatch.fnmatch(path, pattern) for pattern in patterns)


def marker_hits(content: str, markers: list[str]) -> list[tuple[int, str]]:
    hits: list[tuple[int, str]] = []
    for line_no, line in enumerate(content.splitlines(), start=1):
        for marker in markers:
            if marker in line:
                hits.append((line_no, marker))
    return hits


def has_spanish_hint(text: str) -> bool:
    if re.search(r"[áéíóúñ]", text.lower()):
        return True
    tokens = re.findall(r"[a-záéíóúñ]+", text.lower())
    return any(token in SPANISH_HINT_WORDS for token in tokens)


def validate_commit_messages(base: str, head: str) -> list[str]:
    subjects_raw = run(["git", "log", "--format=%s", f"{base}..{head}"])
    if not subjects_raw:
        return []
    errors: list[str] = []
    for subject in subjects_raw.splitlines():
        if subject.startswith("Merge "):
            continue
        m = CONVENTIONAL_RE.match(subject)
        if not m:
            errors.append(
                f"Mensaje de commit invalido (no Conventional Commits): '{subject}'"
            )
            continue
        desc = m.group(3)
        if not has_spanish_hint(desc):
            errors.append(
                "Descripcion de commit parece no estar en espanol: "
                f"'{subject}'"
            )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", required=True)
    parser.add_argument("--head", required=True)
    args = parser.parse_args()

    repo_root = pathlib.Path(run(["git", "rev-parse", "--show-toplevel"]))
    changed_raw = run(["git", "diff", "--name-only", f"{args.base}..{args.head}"])
    changed_files = [p for p in changed_raw.splitlines() if p]

    errors: list[str] = []

    for rel_path in changed_files:
        if not rel_path.endswith(".md"):
            continue

        full_path = repo_root / rel_path
        if not full_path.exists():
            continue

        content = full_path.read_text(encoding="utf-8")

        if matches_any(rel_path, ENGLISH_ONLY_PATTERNS):
            hits = marker_hits(content, SPANISH_MARKERS_FOR_ENGLISH_FILES)
            for line_no, marker in hits:
                errors.append(
                    f"{rel_path}:{line_no} contiene marcador en espanol en archivo"
                    f" que debe estar en ingles ('{marker}')."
                )
            continue

        if matches_any(rel_path, SPANISH_REQUIRED_PATTERNS):
            hits = marker_hits(content, ENGLISH_MARKERS_FOR_SPANISH_FILES)
            for line_no, marker in hits:
                errors.append(
                    f"{rel_path}:{line_no} contiene marcador en ingles en archivo"
                    f" que debe estar en espanol ('{marker}')."
                )

    errors.extend(validate_commit_messages(args.base, args.head))

    if errors:
        print("Politica de idioma: FALLA")
        for err in errors:
            print(f"- {err}")
        return 1

    print("Politica de idioma: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
