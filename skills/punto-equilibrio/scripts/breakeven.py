#!/usr/bin/env python3
"""Break-even point calculator."""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Punto de equilibrio")
    p.add_argument("--fixed-costs", type=float, required=True)
    p.add_argument("--price", type=float, required=True, help="Precio de venta por unidad")
    p.add_argument("--variable-cost", type=float, required=True, help="Costo variable por unidad")
    p.add_argument("--sales-volume", type=float, default=None, help="Ventas actuales/planeadas, en unidades")
    p.add_argument("--output-dir", default=None)
    return p.parse_args()


def main() -> int:
    args = parse_args()

    contribution = args.price - args.variable_cost
    if contribution <= 0:
        print(
            "ERROR: el precio de venta no supera el costo variable por unidad. "
            "No existe punto de equilibrio posible con estos números: cada unidad "
            "vendida profundiza la pérdida."
        )
        return 1

    contribution_pct = contribution / args.price * 100
    breakeven_units = args.fixed_costs / contribution
    breakeven_revenue = breakeven_units * args.price

    print(f"Margen de contribución por unidad: ${contribution:,.2f} ({contribution_pct:.1f}% del precio)")
    print(f"Punto de equilibrio: {breakeven_units:,.1f} unidades")
    print(f"Punto de equilibrio en facturación: ${breakeven_revenue:,.2f}")

    if args.sales_volume is not None:
        safety_units = args.sales_volume - breakeven_units
        safety_pct = (safety_units / args.sales_volume * 100) if args.sales_volume else 0.0
        safety_revenue = safety_units * args.price
        print(f"\nVentas dadas: {args.sales_volume:,.1f} unidades")
        if safety_units >= 0:
            print(f"Margen de seguridad: {safety_units:,.1f} unidades (${safety_revenue:,.2f}) = {safety_pct:.1f}% por encima del equilibrio")
        else:
            print(f"Estás {abs(safety_units):,.1f} unidades POR DEBAJO del punto de equilibrio (faltan ${abs(safety_revenue):,.2f} en facturación)")

    print(
        f"\nVendiendo {breakeven_units:,.0f} unidades cubrís tus costos fijos y "
        "variables. A partir de esa cantidad, cada unidad extra es ganancia neta "
        f"de ${contribution:,.2f}."
    )

    print("\n--- Para entenderlo, no solo verlo ---")
    print(
        f"¿QUÉ ESTÁ HACIENDO ESTE CÁLCULO? Cada unidad que vendés a ${args.price:,.2f} "
        f"no te deja ${args.price:,.2f} de ganancia — primero hay que restarle lo que "
        f"cuesta producir/comprar esa unidad puntual (${args.variable_cost:,.2f}, el "
        f"costo variable). Lo que queda, ${contribution:,.2f}, se llama margen de "
        f"contribución: es lo que cada unidad aporta para pagar los costos fijos "
        f"(alquiler, sueldos, lo que pagás vendas una unidad o mil)."
    )
    print(
        f"Como tenés ${args.fixed_costs:,.2f} de costos fijos para cubrir, y cada "
        f"unidad aporta ${contribution:,.2f}, dividís uno por el otro: "
        f"${args.fixed_costs:,.0f} / ${contribution:,.0f} = {breakeven_units:,.0f} "
        f"unidades. Ese es el punto exacto donde no ganás ni perdés — por eso se "
        "llama punto de equilibrio."
    )
    if args.sales_volume is not None:
        if safety_units >= 0:
            print(
                f"Vendiendo {args.sales_volume:,.0f} unidades, ya pasaste ese punto "
                f"por {safety_units:,.0f} unidades. Eso es tu colchón: podrías vender "
                f"{safety_units:,.0f} unidades menos de lo planeado y todavía no "
                "perderías plata."
            )
        else:
            print(
                f"Con {args.sales_volume:,.0f} unidades todavía no llegaste al punto "
                f"de equilibrio — te faltan {abs(safety_units):,.0f} unidades más "
                "para empezar a ganar, no para empezar a perder menos: hasta ese "
                "número, cada venta reduce la pérdida pero no genera ganancia."
            )

    if args.output_dir:
        out_dir = Path(args.output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        ts = dt.datetime.now().strftime("%Y-%m-%d_%H%M%S")
        data = {
            "fixed_costs": args.fixed_costs,
            "price": args.price,
            "variable_cost": args.variable_cost,
            "contribution": contribution,
            "breakeven_units": breakeven_units,
            "breakeven_revenue": breakeven_revenue,
            "sales_volume": args.sales_volume,
        }
        (out_dir / f"breakeven_{ts}.json").write_text(json.dumps(data, indent=2))

    return 0


if __name__ == "__main__":
    sys.exit(main())
