# Answer-Leak Diagnostics

## Problem

The learner asks for a hint and receives the full function body instead. This is the most common teach-mode failure mode — and the least ambiguous signal that the teaching contract was broken.

## Three Causes (in order of likelihood)

### 1. Teaching skills not loaded for that turn

`teach-mode` (and any related domain dojo skill) contain the hint ladder, the "no full-function-body as hint" rule, and the rescue-gating logic. Without them in context, the model reverts to its default "be maximally helpful" behavior, which means reproducing the complete reference implementation.

**Check:** Was `skill_view(name="teach-mode")` called this turn? For domain dojos, was the related dojo skill loaded?

**Fix:** Load the skills before the next teaching turn.

### 2. Hint ladder's rescue rung fires too easily

Even with skills loaded, the gap between "give me a hint" and "give me the answer" can collapse if the model interprets "I'm stuck on this part" as a rescue-level request rather than a request for the next hint rung.

**Check:** Did the learner say "help," "I'm stuck," or "can you show me what to do here"? Any of these could have been handled with rungs 3-5 (hint, targeted snippet, review) but escalated to rung 6 (rescue).

**Fix:** The circuit breaker phrase "Hint only — I want to write the body myself" overrides this. But the root cause is the model's default-helpfulness bias interpreting "stuck" as "rescue me." The default response to any "I'm stuck" message should be: "Want another hint, or do you want rescue?"

### 3. Reference implementation leaks through project context

The reference solution lives in the same project as the stub files. For example, in a coding dojo:

```
examples/dojo-wallet/src/wallet.rs:92-105  # next_unused_address
```

A single `read_file` or `search_files` call surfaces the complete function body. If discoverability is wide enough (file search, grep, codebase inspection), the model finds it and reproduces it.

**Check:** Did the model read or search the reference implementation file during the session?

**Fix:** When teaching from a project with a reference implementation, either (a) keep the reference implementation out of the file tree visible to the model during lesson time, or (b) add an explicit pre-teaching instruction: "Do not read the reference implementation. The learner has not attempted yet."

## Recovery

When the user calls out the leak:

1. **Acknowledge directly.** Do not deflect. Say "You're right, I gave you the full function when you asked for a hint."

2. **Name the cause.** "The teaching skills weren't loaded for that turn." or "I jumped past the hint ladder."

3. **Give the circuit breaker.** "Next time, say 'Hint only — I want to write the body myself.' That's a signal that overrides the default-helpfulness bias regardless of what skills are loaded."

4. **Reset the teaching contract.** "Not your job to police this. But that phrase is your circuit breaker until I can make the skill loading more reliable."

5. **If the learner still wants to do the work** — ask if they want to delete the leaked code and start fresh, or if they want to move on with the concept understood.

## Prevention

- Load teaching skills at the start of every education session.
- Default to "Want another hint, or do you want rescue?" when the learner says "help" or "I'm stuck."
- Before reading any file in a teaching project, check whether it's a reference implementation. If so, read only the tests/file structure, not the function bodies.
