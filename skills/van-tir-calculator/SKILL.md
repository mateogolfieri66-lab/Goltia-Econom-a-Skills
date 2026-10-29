---
name: van-tir-calculator
description: Calculate NPV (VAN) and IRR (TIR) for a cash flow stream, with a clear accept/reject read against a discount rate. Use when the user asks whether a project or investment is worth doing, wants to compare projects, or asks about VAN, TIR, payback, or discounted cash flow.
---

# VAN / TIR Calculator

## Overview

Classic project-evaluation calculator (Formulación y Evaluación de
Proyectos): given an initial investment and a stream of future cash flows,
computes Net Present Value (VAN) at a given discount rate, Internal Rate of
Return (TIR), and simple payback period.

This is a standard financial-math calculation, not investment advice about
any specific real asset. Clearly state assumptions (discount rate, cash flow
timing) in the output.

## When to Use

- User asks "is this project worth it?" or "should I invest in this?"
- User gives an initial investment and a series of expected cash flows
- User asks about VAN, TIR, payback period, or discounted cash flow
- User wants to compare two or more projects by VAN or TIR

## Prerequisites

- No API keys required
- Python 3.9+ with standard library only

## Workflow

### Step 1: Gather Inputs

- **Required**: initial investment (as a positive number, treated as outflow
  at t=0)
- **Required**: list of future cash flows, one per period (year/month,
  whatever the user states — be explicit about the period length)
- **Required for VAN**: discount rate (%)

### Step 2: Run the Calculator

```bash
python3 skills/van-tir-calculator/scripts/van_tir.py \
  --investment 100000 \
  --cashflows 30000 35000 40000 45000 \
  --discount-rate 15
```

### Step 3: Present the Result AND Explain It

Report VAN, TIR, and simple payback. Interpretation:
- VAN > 0 at the given discount rate → the project adds value at that
  required return
- VAN < 0 → the project destroys value at that required return
- TIR vs discount rate → same read, expressed as a rate instead of a dollar
  amount

The script prints a "--- Para entenderlo, no solo verlo ---" section that
explains, using the user's own numbers, why a peso today isn't worth a peso
in the future, how the nominal total differs from the VAN, and what the gap
between TIR and the discount rate actually represents. **Always relay this
explanation in your own words before or alongside the numbers** — someone
with no finance background should come away understanding WHY discounting
matters, not just whether the number was positive or negative.

Always state the discount rate and cash flow timing assumption used, and
note this is a standard financial model, not advice on a specific real
investment.

## Output Format

Markdown with VAN, TIR (if it converges — note when cash flows have no sign
change and TIR cannot be computed), payback period, and the discounted cash
flow table (period, cash flow, discount factor, present value).

## Resources

- `scripts/van_tir.py` — the calculator
