#!/usr/bin/env python3
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "teach-mode" / "SKILL.md"
README = ROOT / "README.md"
SCENARIOS = ROOT / "examples" / "scenarios"
EXPECTED_VERSION = "0.0.3"

errors: list[str] = []


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        errors.append("skills/teach-mode/SKILL.md must start with YAML frontmatter")
        return {}
    end = text.find("\n---\n", 4)
    if end == -1:
        errors.append("skills/teach-mode/SKILL.md frontmatter is not closed")
        return {}
    frontmatter = text[4:end]
    fields: dict[str, str] = {}
    for line in frontmatter.splitlines():
        if not line or line.startswith(" ") or line.startswith("metadata:"):
            continue
        if ":" in line:
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip().strip('"')
    return fields


text = SKILL.read_text(encoding="utf-8")
frontmatter = parse_frontmatter(text)
for key in ["name", "description", "version", "author", "license"]:
    if not frontmatter.get(key):
        errors.append(f"frontmatter missing {key}")

if frontmatter.get("name") != "teach-mode":
    errors.append("frontmatter name must be exactly teach-mode")
if frontmatter.get("version") != EXPECTED_VERSION:
    errors.append(f"frontmatter version must be {EXPECTED_VERSION}")

required_phrases = [
    "The learner attempts first. The agent coaches.",
    "Assistance Ladder",
    "Understanding Gate",
    "Do not mark a lesson complete until the learner can explain",
    "Domain skills may define their own routes",
]
for phrase in required_phrases:
    if phrase not in text:
        errors.append(f"missing required teaching contract phrase: {phrase}")

readme = README.read_text(encoding="utf-8")
readme_requirements = [
    "learner-first teaching skill",
    "hermes skills install SaucePackets/teach-mode-skill/skills/teach-mode",
    "Dojo/course skills that need one shared teaching contract",
    "Skill authors who do not want to vendor copied teaching rules",
]
for phrase in readme_requirements:
    if phrase not in readme:
        errors.append(f"README missing teaching/package wording: {phrase}")

scenario_files = sorted(SCENARIOS.glob("*.md"))
if len(scenario_files) < 5:
    errors.append("expected at least 5 example scenario transcripts")

for path in scenario_files:
    body = path.read_text(encoding="utf-8")
    if "Good response shape" not in body:
        errors.append(f"{path.relative_to(ROOT)} missing Good response shape")

if errors:
    print("Skill package validation failed:")
    for err in errors:
        print(f"- {err}")
    sys.exit(1)

print(f"OK: {SKILL.relative_to(ROOT)} version {EXPECTED_VERSION} and {len(scenario_files)} scenarios validated")
