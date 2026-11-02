---
name: costo-real-empleado
description: Calculate the true monthly cost of an employee (gross salary + employer social charges + pro-rated 13th-month bonus + other fixed costs), and optionally the real cost per hour worked. Use when the user asks what an employee really costs them, beyond the salary figure.
---

# Costo Real de un Empleado

## Overview

Structural calculation of total employer cost per employee per month. It
does NOT assume any fixed legal percentage for social charges — the user
must supply their own current rate, because these percentages vary by
jurisdiction and change over time. This keeps the tool accurate without
hardcoding a labor-law figure that can go stale.

## When to Use

- User asks "what does an employee really cost me?" beyond the salary
- User is deciding whether to hire and wants the fully-loaded monthly cost
- User wants a real cost-per-hour figure for an employee

## Prerequisites

- No API keys required
- Python 3.9+ with standard library only
- The user must provide their own current social-charges percentage —
  never assume or invent one; if they don't know it, ask them to confirm
  it with their accountant/payroll provider before using the result for a
  real decision

## Workflow

### Step 1: Gather Inputs

- **Required**: gross monthly salary
- **Required**: employer social charges, as a percentage of gross salary
  (the user's own current rate — state in the output that it should be
  verified as current)
- **Optional**: whether to pro-rate the 13th-month bonus (on by default,
  1/12 of gross)
- **Optional**: other fixed monthly costs (equipment, software, insurance)
- **Optional**: monthly hours worked, to compute a real cost per hour

### Step 2: Run the Calculator

```bash
python3 skills/costo-real-empleado/scripts/costo_real_empleado.py \
  --sueldo-bruto 900000 \
  --cargas-sociales-pct 27 \
  --otros-costos-mensuales 40000 \
  --horas-mensuales 160
```

### Step 3: Present the Result

Report: social charges amount, pro-rated bonus (if included), other costs,
total real monthly cost, the percentage over gross salary, and the real
cost per hour (if hours were given). Always remind the user that the
social-charges percentage they used should be current for their
jurisdiction — this tool does not verify or supply that figure.

## Output Format

Plain-text summary with all the figures above, plus a one-line
interpretation ("esto es X% más que el sueldo bruto que ves en el recibo").

## Resources

- `scripts/costo_real_empleado.py` — the calculator
