# Programming Bitcoin coaching notes

Use when coaching Jerry through Jimmy Song's *Programming Bitcoin*, especially early math chapters.

## Verify before teaching

Before explaining a new chapter or answering an exercise question, read the actual exercises and answers from the book's companion code first. Do not assume parameters carry over from previous chapters — the book changes curves between chapters without announcing it.

This matters because I taught the wrong curve for an entire session by assuming Chapter 3 used the same curve as Chapter 2. The fix is simple: check the source material before teaching, not after correcting.

## Equation formatting preferences

Jerry finds dense inline equations hard to follow. Use the vertical step format instead.

Avoid this:

```
s = (y2-y1)/(x2-x1) = (139-142)/(60-170) = -3/-110, field div gives... s = 221, x3 = 221² - 170 - 60 = 48611 % 223 = 220, y3 = 221*(170-220)-142 = -11192 % 223 = 181
```

Use this:

```
s_num = (139 - 142) % 223 = 220
s_den = (60 - 170)  % 223 = 113
inv   = pow(113, 221, 223) = 75
s     = 220 * 75 % 223 = 221

x3 = (221² - 170 - 60) % 223
x3 = (48841 - 230) % 223
x3 = 48611 % 223
x3 = 220

y3 = (221 * (170 - 220) - 142) % 223
y3 = (221 * (-50) - 142) % 223
y3 = (-11050 - 142) % 223
y3 = (-11192) % 223
y3 = 181
```

Rules:
- One operation per line, each fully written out before simplifying.
- Label intermediate values so each line reads as a complete step.
- Use `% 223` explicitly — do not say "mod p" and assume the wrapping is obvious.
- When the learner's answer diverges from expected, step through their numbers line by line, not by re-explaining the theory.

## Field division explanation order

When Jerry asks "how does division work in a finite field?" do NOT start with Fermat's formula. Start with the brute-force intuition:

1. "Division means: find k such that den * k % p = num."
2. Try a few k values concretely (2-3 examples, showing the trial).
3. Show the pattern: you can find k by first finding the inverse (den * inv % p = 1).
4. Then show Fermat as the shortcut to find the inverse without brute force: `inv = pow(den, p-2, p)`.
5. Finally show: `result = num * inv % p`.

If he says "that doesn't click," stay on step 1-2 longer with tiny fields (F_7, F_13) before introducing Fermat.

## Structured equation walkthroughs

When the learner needs to see *how* numbers go into an equation, use this structured format — it worked well for Jerry with Chapter 3's curve check:

```
Equation: y² = x³ + 7   (over F_223)

Point: (192, 105)

Step 1 — plug x into the right side:
  x³ + 7 = 192³ + 7
         = 7077888 + 7
         = 7077895
  7077895 % 223 = 98   ← reduce mod p

Step 2 — plug y into the left side:
  y² = 105² = 11025
  11025 % 223 = 98      ← reduce mod p

Step 3 — compare:
  98 == 98 → on the curve ✓
```

Key principles:
- Show every intermediate value explicitly. Do not skip reduction steps.
- Label each number's source ("plug x", "plug y").
- Show the full expression before simplifying.
- Only reach for the %-once-at-the-end shortcut after the step-by-step lands.

Same pattern for point addition:

```
Formula: s = (y2 - y1) / (x2 - x1)

P1 = (192, 105), P2 = (17, 56)

Step 1 — numerator and denominator:
  y2 - y1 = 56 - 105 = -49
  -49 % 223 = 174
  x2 - x1 = 17 - 192 = -175
  -175 % 223 = 48

Step 2 — field divide: s = 174 * pow(48, 223-2, 223) = 143

Step 3 — x3 = (s² - x1 - x2) % 223:
  x3 = (143² - 192 - 17) % 223
  x3 = (20449 - 209) % 223
  x3 = 20240 % 223
  x3 = 170

Step 4 — y3 = (s(x1 - x3) - y1) % 223:
  y3 = (143 * (192 - 170) - 105) % 223
  y3 = (143 * 22 - 105) % 223
  y3 = (3146 - 105) % 223
  y3 = 3041 % 223
  y3 = 142

Result: (170, 142)
```

When the equation has a mod p on every term, write it like:

  `x3 = (s² - x1 - x2) % p`

  not abstractly "x3 in F_p". Show both the raw value and the wrapped value.

- Keep explanations synced to the user's current page. If he says he has not reached modulo/Fermat/finite-field shortcuts yet, stop using that as the main explanation and give only a hook.
- When a formula introduces a derived value, show where every number came from before using the shortcut.
  - Example: for `17^-3` in `F_31`, do not jump straight to `-3 % 30 = 27`.
  - First show `17^-1` means "the number that makes `17 * ? % 31 = 1`."
  - Then show `17^29 % 31 = 11`, and verify `17 * 11 % 31 = 1`.
  - Then build `17^-3 = 11^3 % 31 = 29`.
  - Only after that introduce the shortcut `17^-3 = 17^27`.
- For notation questions, translate symbols literally before explaining concepts:
  - `F_19` = the whole field/set `{0..18}`, not a value.
  - `∈` = "is an element of" / "is inside".
  - `+_f` = field addition, usually normal addition then `% p`.
- For exercises, first explain what the exercise is asking and the shape of the work, not the final answer. Give one worked example only if needed, then let Jerry do the rest.
- For Chapter 2 point-addition geometry, use diagrams early. Jerry benefits from generated/drawn visuals showing: line through A and B → third intersection → reflect; vertical-line inverse → point at infinity; associativity as two paths to the same final point. Pair the image with a short explanation of what is chosen first and what is forced by the graph.
- Chapter notes should be reference-first, not answer dumps: why it matters, core formulas, common stuck points, exercise map, check-yourself questions.
- For visual-heavy explanations in chat, prefer broken-down diagram/example images with the explanation immediately after each image. Jerry learns better when each example is paired with the exact explanation that references it.
- Use PDFs only when they are highly readable: one idea per page, large text, no overflow, no dense single-page poster unless the user asks for a poster. If a generated PDF has cramped or overflowing text, replace it with a multi-page readable guide and clean up the failed draft assets.
- In Obsidian notes, place each image immediately above the section it explains, copy assets into a local `assets/` folder, and run `ob sync` from `/home/clawdbot/vault` after updates so Jerry's devices receive the changes.
- When walking through the point-addition derivation, use a single consistent worked example with real numbers (P1=(2,5), P2=(-1,-1) on y²=x³+5x+7) from start to finish. Use the book's official formula labeling (`s = (y2 - y1) / (x2 - x1)`) without mixing point order.
- For the cubic derivation, lean on Vieta's formula as the key bridge: show that the cubic's two forms (expanded from substitution vs factored as (x-x1)(x-x2)(x-x3)) must have matching x² coefficients. This skips the messy polynomial expansion and gives the correct `x3 = s² - x1 - x2` directly.
- After finding x3, show the two-step mental model before the condensed formula:
  1. Find C on the line: `y = s(x3 - x1) + y1`
  2. Reflect: `y3 = -(s(x3 - x1) + y1) = s(x1 - x3) - y1`
- Always verify the final answer: plug (x3, y3) into the curve equation and confirm both sides match.

## Pitfalls

- Recurring failure: **dumping full solution code when the exercise only asks for the shape.** This happens despite the teach-mode skill being loaded. The fix is not more skill text — it is checking before every answer: "Am I giving a working code solution or explaining the shape?" If it is a working solution, stop and give the shape instead. If uncertain, err on the side of too little code.
- The book **switches curves between chapters.** Chapter 2 uses `y² = x³ + 5x + 7` (a=5, b=7) as a teaching curve. Chapter 3 switches to `y² = x³ + 7` (a=0, b=7 — the real secp256k1 curve). Do not carry Chapter 2's `a=5` into Chapter 3 examples or notes. Jerry will get wrong answers and be confused because none of the points pass the check.
- Always verify the curve parameters (`a`, `b`) from the actual chapter before writing notes or examples. The book does not always announce the switch explicitly.
- When explaining "over F_p", emphasize that it means **both sides of the equation reduce by % p before comparing.** Not one side. Not optionally. The "over F_p" wraps the entire equality: `y² % p == (x³ + ax + b) % p`. This is where Jerry gets stuck most.
- Do not answer finite-field exponent questions with only the compact formula. Jerry may need value provenance.
- Do not over-abstract early. Use tiny fields (`F_5`, `F_19`, `F_31`) and explicit arithmetic.
- Do not present modulo as "modulus of the values in the set"; phrase it as "mod by the field's order/size."
- Do not use full exercise solutions unless he asks for rescue or has already attempted and is blocked.
- When labeling P1 and P2 in worked examples, always use the book's formula order (`s = (y2 - y1) / (x2 - x1)`) and label x1/y1/x2/y2 clearly. Mixing the order confuses Jerry — he will catch swapped labels.
