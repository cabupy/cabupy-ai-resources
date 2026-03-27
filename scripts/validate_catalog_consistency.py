#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]


def read_text(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def extract_agent_ids_from_readme(text: str) -> set[str]:
    return set(re.findall(r"- `([a-z0-9-]+)`:", text))


def extract_agent_ids_from_matrix(text: str) -> set[str]:
    return set(re.findall(r"\| `([a-z0-9-]+)` \|", text))


def extract_skill_ids_from_readme(text: str) -> set[str]:
    return set(re.findall(r"- `([a-z0-9-]+)`", text))


def extract_used_skills(agent_text: str) -> set[str]:
    m = re.search(r"## Skills Used\n\n([\s\S]*?)(\n## |\Z)", agent_text)
    if not m:
        return set()
    result: set[str] = set()
    for line in m.group(1).splitlines():
        line = line.strip()
        if line.startswith("- "):
            result.add(line[2:].strip())
    return result


def main() -> int:
    errors: list[str] = []

    agent_files = sorted(ROOT.glob("agents/*/agent.md"))
    skill_files = sorted(ROOT.glob("skills/*/skill.md"))

    agent_ids = {p.parent.name for p in agent_files}
    skill_ids = {p.parent.name for p in skill_files}

    agents_readme_ids = extract_agent_ids_from_readme(read_text("agents/README.md"))
    matrix_ids = extract_agent_ids_from_matrix(read_text("docs/tooling-matrix.md"))
    skills_readme_ids = extract_skill_ids_from_readme(read_text("skills/README.md"))

    missing_agents_readme = sorted(agent_ids - agents_readme_ids)
    missing_agents_matrix = sorted(agent_ids - matrix_ids)
    extra_agents_readme = sorted(agents_readme_ids - agent_ids)
    extra_agents_matrix = sorted(matrix_ids - agent_ids)

    if missing_agents_readme:
        errors.append(
            "agents/README.md no lista estos agentes: "
            + ", ".join(missing_agents_readme)
        )
    if missing_agents_matrix:
        errors.append(
            "docs/tooling-matrix.md no lista estos agentes: "
            + ", ".join(missing_agents_matrix)
        )
    if extra_agents_readme:
        errors.append(
            "agents/README.md lista agentes inexistentes: "
            + ", ".join(extra_agents_readme)
        )
    if extra_agents_matrix:
        errors.append(
            "docs/tooling-matrix.md lista agentes inexistentes: "
            + ", ".join(extra_agents_matrix)
        )

    missing_skills_readme = sorted(skill_ids - skills_readme_ids)
    extra_skills_readme = sorted(skills_readme_ids - skill_ids)
    if missing_skills_readme:
        errors.append(
            "skills/README.md no lista estas skills: "
            + ", ".join(missing_skills_readme)
        )
    if extra_skills_readme:
        errors.append(
            "skills/README.md lista skills inexistentes: "
            + ", ".join(extra_skills_readme)
        )

    used_skills: set[str] = set()
    for agent in agent_files:
        text = agent.read_text(encoding="utf-8")
        used = extract_used_skills(text)
        if not used:
            errors.append(f"{agent.relative_to(ROOT)} no declara '## Skills Used'.")
        used_skills |= used
        unknown = sorted(used - skill_ids)
        if unknown:
            errors.append(
                f"{agent.relative_to(ROOT)} referencia skills inexistentes: "
                + ", ".join(unknown)
            )

    orphan_skills = sorted(skill_ids - used_skills)
    if orphan_skills:
        errors.append("Skills sin uso en agentes: " + ", ".join(orphan_skills))

    for agent in agent_ids:
        ex = ROOT / "agents" / agent / "examples"
        if not ex.exists() or not any(ex.glob("*.md")):
            errors.append(f"agents/{agent}/examples no tiene ejemplos Markdown.")

    for skill in skill_ids:
        ex = ROOT / "skills" / skill / "examples"
        if not ex.exists() or not any(ex.glob("*.md")):
            errors.append(f"skills/{skill}/examples no tiene ejemplos Markdown.")

    if errors:
        print("Consistencia de catalogo: FALLA")
        for e in errors:
            print(f"- {e}")
        return 1

    print("Consistencia de catalogo: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
