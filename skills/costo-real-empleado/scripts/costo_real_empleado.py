#!/usr/bin/env python3
"""Costo real de un empleado por mes (sueldo bruto + cargas sobre el salario).

Herramienta educativa, determinista: no asume ningun porcentaje legal fijo.
El usuario (operador) pasa sus propios porcentajes vigentes como parametro,
porque las cargas sociales cambian por jurisdiccion y en el tiempo.
"""
from __future__ import annotations

import argparse


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Costo real de un empleado")
    p.add_argument("--sueldo-bruto", type=float, required=True, help="Sueldo bruto mensual")
    p.add_argument("--cargas-sociales-pct", type=float, required=True,
                   help="Porcentaje de aportes patronales sobre el bruto (vos lo confirmas vigente)")
    p.add_argument("--incluir-aguinaldo", action="store_true", default=True,
                   help="Prorratea el SAC (1/12 del bruto) como costo mensual")
    p.add_argument("--no-aguinaldo", dest="incluir_aguinaldo", action="store_false")
    p.add_argument("--otros-costos-mensuales", type=float, default=0.0,
                   help="Equipamiento, software, seguro, lo que corresponda")
    p.add_argument("--horas-mensuales", type=float, default=None,
                   help="Si se pasa, calcula el costo real por hora trabajada")
    return p.parse_args()


def main() -> int:
    args = parse_args()

    cargas = args.sueldo_bruto * (args.cargas_sociales_pct / 100)
    sac_mensual = args.sueldo_bruto / 12 if args.incluir_aguinaldo else 0.0
    total = args.sueldo_bruto + cargas + sac_mensual + args.otros_costos_mensuales
    extra_pct = (total / args.sueldo_bruto - 1) * 100

    print(f"Sueldo bruto: ${args.sueldo_bruto:,.2f}")
    print(f"Cargas sociales ({args.cargas_sociales_pct:.1f}%): ${cargas:,.2f}")
    if args.incluir_aguinaldo:
        print(f"SAC prorrateado (1/12): ${sac_mensual:,.2f}")
    if args.otros_costos_mensuales:
        print(f"Otros costos mensuales: ${args.otros_costos_mensuales:,.2f}")
    print(f"\nCOSTO REAL MENSUAL: ${total:,.2f}")
    print(f"Eso es un {extra_pct:.1f}% MAS que el sueldo bruto que ves en el recibo.")

    if args.horas_mensuales:
        costo_hora = total / args.horas_mensuales
        print(f"\nCosto real por hora trabajada: ${costo_hora:,.2f} (sobre {args.horas_mensuales:.0f} hs/mes)")

    print(
        "\nEsto es un calculo estructural con los porcentajes que vos cargaste "
        "-- confirma que tus % de cargas sociales esten vigentes antes de usar "
        "el numero para decidir algo real."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
