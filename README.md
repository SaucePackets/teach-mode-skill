# teach-mode-skill

Teach Mode is a learner-first teaching skill for AI-assisted practice.

Core rule:

**The learner attempts first. The agent scaffolds, hints, reviews, verifies, and explains before rescuing.**

## Install

```bash
hermes skills install SaucePackets/teach-mode-skill/skills/teach-mode --category education --yes --force
```

Then ask your agent to use `teach-mode` whenever you are learning, practicing, debugging, or reinforcing a course.

## Repo structure

```text
teach-mode-skill/
├── skills/
│   └── teach-mode/
│       └── SKILL.md
├── examples/
│   └── scenarios/
├── references/
│   └── ledger-routes.example.md
└── scripts/
    └── validate_skill_package.py
```

## What it is for

- Dojo/course skills that need one shared teaching contract.
- Learners using AI for practice without becoming passive.
- Skill authors who do not want to vendor copied teaching rules.

## Companion skills

- `bdk-dojo`
- `prompt-dojo`
- `coding-dojo-teach-mode`
- course reinforcement skills

## Public-clean note

This repo contains generic teaching behavior only. It does not include private learner history, critique logs, private ledger routes, or project-specific course notes.
