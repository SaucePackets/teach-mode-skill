# Contributing

Thanks for improving Teach Mode.

## Updating the teaching contract

- Keep Teach Mode domain-neutral. Domain skills should add their own specifics.
- Preserve the core rule: learner attempts first, agent coaches before rescuing.
- Do not add private learner history, private project paths, or personal ledger routes to the public core.
- If a behavior needs a concrete example, prefer `examples/scenarios/` over bloating `SKILL.md`.

## Adding scenario examples

Add Markdown files under `examples/scenarios/`.

Each scenario should include:

- what situation triggers it
- what good behavior looks like
- a `Good response shape` section
- what to avoid

## Local checks

Run:

```bash
python3 scripts/validate_skill_package.py
```

## Publishing notes

This repo currently installs from `main` via Hermes' GitHub skill-directory installer. If you change public behavior, update the relevant README, skill, reference, or example docs and run local checks before pushing.
