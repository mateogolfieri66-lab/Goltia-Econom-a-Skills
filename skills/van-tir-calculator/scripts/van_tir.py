#!/usr/bin/env python3
"""NPV (VAN) / IRR (TIR) calculator for a simple cash flow stream.

Standard financial-math model. Period 0 is the initial investment (outflow).
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="VAN/TIR calculator")
    p.add_argument("--investment", type=float, required=True, help="Initial investment (positive number, outflow at t=0)")
    p.add_argument("--cashflows", type=float, nargs="+", required=True, help="Future cash flows, one per period")
    p.add_argument("--discount-rate", type=float, required=True, help="Discount rate in %% for VAN")
    p.add_argument("--output-dir", default=None)
    return p.parse_args()


def npv(rate_pct: float, investment: float, cashflows: list[float]) -> tuple[float, list[dict]]:
    r = rate_pct / 100.0
    rows = []
    total = -investment
    rows.append({"period": 0, "cashflow": -investment, "discount_factor": 1.0, "present_value": -investment})
    for t, cf in enumerate(cashflows, start=1):
        df = 1.0 / ((1 + r) ** t)
        pv = cf * df
        total += pv
        rows.append({"period": t, "cashflow": cf, "discount_factor": round(df, 4), "present_value": round(pv, 2)})
    return total, rows


def irr(investment: float, cashflows: list[float], guess: float = 0.1) -> float | None:
    """Simple IRR via Newton-Raphson; returns None if it doesn't converge."""
    flows = [-investment] + list(cashflows)
    if all(c >= 0 for c in flows) or all(c <= 0 for c in flows):
        return None  # no sign change -> no IRR

    rate = guess
    for _ in range(200):
        npv_val = sum(cf / ((1 + rate) ** t) for t, cf in enumerate(flows))
        d_npv = sum(-t * cf / ((1 + rate) ** (t + 1)) for t, cf in enumerate(flows))
        if abs(d_npv) < 1e-12:
            break
        new_rate = rate - npv_val / d_npv
        if abs(new_rate - rate) < 1e-9:
            rate = new_rate
            break
        rate = new_rate
        if rate <= -0.99:
            return None
    if abs(sum(cf / ((1 + rate) ** t) for t, cf in enumerate(flows))) > 1.0:
        return None
    return rate * 100


def payback_period(investment: float, cashflows: list[float]) -> str:
    remaining = investment
    for t, cf in enumerate(cashflows, start=1):
        remaining -= cf
        if remaining <= 0:
            prev_remaining = remaining + cf
            fraction = prev_remaining / cf if cf else 0
            return f"{t - 1 + fraction:.2f} periodos"
    return "no se recupera en el horizonte dado"


def explain(investment: float, discount_rate: float, van_value: float, tir_value: float | None, cashflows: list[float]) -> str:
    """Build a plain-language explanation tailored to this specific result,
    not a canned paragraph. A first-time user should understand WHY the
    number came out the way it did, not just read the number."""
    lines = []
    total_nominal = sum(cashflows)
    lines.append(
        f"¿QUÉ ESTÁ HACIENDO ESTE CÁLCULO? Sumaste los flujos sin más, te da "
        f"${total_nominal:,.2f} de ganancia nominal sobre una inversión de "
        f"${investment:,.2f}. Pero un peso que cobrás en 3 años no vale lo "
        f"mismo que un peso hoy — con esa plata, mientras esperás, podrías "
        f"haber hecho otra cosa que te rinda. Por eso se usa una tasa de "
        f"descuento ({discount_rate}%): representa lo mínimo que exigís "
        f"ganar por esperar y por el riesgo de no cobrar."
    )
    lines.append(
        f"Al traer cada flujo futuro a 'pesos de hoy' con esa tasa, la "
        f"ganancia nominal de ${total_nominal:,.2f} se convierte en un VAN "
        f"de ${van_value:,.2f}. Esa es la diferencia real entre sumar fechas "
        f"distintas sin pensar, y comparar peras con peras."
    )
    if van_value > 0:
        lines.append(
            f"VAN POSITIVO significa: después de exigirte ese {discount_rate}% "
            f"mínimo de rendimiento, el proyecto todavía te deja "
            f"${van_value:,.2f} de valor extra. Conviene, bajo ese supuesto "
            f"de tasa."
        )
    else:
        lines.append(
            f"VAN NEGATIVO significa: ni siquiera llegando al {discount_rate}% "
            f"mínimo que pediste, el proyecto cubre esa exigencia — te faltan "
            f"${abs(van_value):,.2f}. No conviene a esa tasa (podría convenir "
            f"a una tasa más baja: revisá qué tasa estás exigiendo y por qué)."
        )
    if tir_value is not None:
        gap = tir_value - discount_rate
        lines.append(
            f"La TIR ({tir_value:.2f}%) es la tasa a la que el VAN sería "
            f"exactamente cero — el 'punto de empate'. Como tu tasa exigida "
            f"es {discount_rate}%, tenés {abs(gap):.2f} puntos de "
            f"{'colchón' if gap > 0 else 'déficit'} por encima de lo mínimo "
            f"que pediste."
        )
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    van_value, rows = npv(args.discount_rate, args.investment, args.cashflows)
    tir_value = irr(args.investment, args.cashflows)
    payback = payback_period(args.investment, args.cashflows)

    print(f"{'Periodo':<8} {'Flujo':>14} {'Factor desc.':>14} {'Valor presente':>16}")
    for r in rows:
        print(f"{r['period']:<8} {r['cashflow']:>14,.2f} {r['discount_factor']:>14} {r['present_value']:>16,.2f}")

    print(f"\nVAN @ {args.discount_rate}%: ${van_value:,.2f}")
    print(f"TIR: {tir_value:.2f}%" if tir_value is not None else "TIR: no converge (sin cambio de signo en los flujos)")
    print(f"Payback simple: {payback}")

    print("\n--- Para entenderlo, no solo verlo ---")
    print(explain(args.investment, args.discount_rate, van_value, tir_value, args.cashflows))

    if args.output_dir:
        out_dir = Path(args.output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        ts = dt.datetime.now().strftime("%Y-%m-%d_%H%M%S")
        data = {
            "investment": args.investment,
            "cashflows": args.cashflows,
            "discount_rate_pct": args.discount_rate,
            "van": van_value,
            "tir_pct": tir_value,
            "payback": payback,
        }
        (out_dir / f"van_tir_{ts}.json").write_text(json.dumps(data, indent=2))

    return 0


if __name__ == "__main__":
    sys.exit(main())
