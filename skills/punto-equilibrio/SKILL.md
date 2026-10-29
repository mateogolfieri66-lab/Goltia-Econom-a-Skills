---
name: punto-equilibrio
description: Calculate the break-even point (units and revenue) given fixed costs, variable cost per unit, and sale price, plus the margin of safety at a given sales volume. Use when the user asks how many units they need to sell to break even, or wants to check how far they are from break-even.
---

# Punto de Equilibrio (Break-Even)

## Overview

Standard break-even analysis: fixed costs / (price - variable cost per unit)
= break-even units. Also reports break-even revenue and, if the user gives
their actual or planned sales volume, the margin of safety.

## When to Use

- User asks "how many units do I need to sell to break even?"
- User wants to know how much room they have before they start losing money
- User is pricing a product and wants to see the break-even impact of a
  price or cost change

## Prerequisites

- No API keys required
- Python 3.9+ with standard library only

## Workflow

### Step 1: Gather Inputs

- **Required**: fixed costs (period total)
- **Required**: sale price per unit
- **Required**: variable cost per unit
- **Optional**: current/planned sales volume (units), to compute margin of
  safety

### Step 2: Run the Calculator

```bash
python3 skills/punto-equilibrio/scripts/breakeven.py \
  --fixed-costs 500000 \
  --price 2500 \
  --variable-cost 1500 \
  --sales-volume 700
```

### Step 3: Present the Result AND Explain It

Report break-even units, break-even revenue, contribution margin per unit
and as a percentage, and (if sales volume given) margin of safety in units,
revenue, and percentage.

The script prints a "--- Para entenderlo, no solo verlo ---" section
explaining, with the user's own numbers, why the sale price isn't pure
profit, what the contribution margin actually pays for, and why dividing
fixed costs by that margin gives the break-even point. **Relay this
explanation, not just the final numbers** — someone with no business
background should understand the mechanism (margin pays fixed costs first),
not just memorize "500 units."

## Output Format

Markdown summary with all the figures above, plain language interpretation
("vendiendo X unidades cubrís tus costos; a partir de ahí es ganancia").

## Resources

- `scripts/breakeven.py` — the calculator
