# Learner Circuit Breaker

## Problem

When the teach-mode skill is not loaded (missing dependency, profile mismatch, session context loss), the model's default "be maximally helpful" instinct takes over. The learner says "I'm stuck on this part" and the model dumps the full function body — bypassing the hint ladder entirely.

The same can happen even when skills are loaded, if the model interprets "stuck" as a rescue-level request rather than a request for the next rung.

## Learner-Side Fix

The learner can override this with a three-word circuit breaker:

> **"Hint only — I want to write the body myself."**

This is a hard signal that:

- Overrides the default-helpfulness bias regardless of what skills are loaded
- Puts the model back on the hint ladder (rungs 3-5)
- Works as an explicit contract: "I am a learner, give me rails/hints/snippets, not the solution"

## When to Use

- First sign the model is drifting toward rescue mode
- When you realize teach-mode skills may not be in context
- Any time you want to pre-empt full-answer dumping before asking for help

## Not the Learner's Job

The learner should not have to police the teaching contract. This phrase is a backup circuit breaker, not the primary guardrail. The `teach-mode` skill is the primary defense. Use this when it fails or is absent.
