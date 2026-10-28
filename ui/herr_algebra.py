"""Calculadoras del tema 8: permutaciones, ℤₙ como anillo y cocientes 𝔽ₚ[x]/(f)."""
from __future__ import annotations

import pandas as pd
import streamlit as st
import sympy as sp

from core import algebra as G
from core.parsing import leer
from ui.comun import verificado
from ui.estilo import caja


def _fmt(p):
    return "".join(map(str, p)) if len(p) < 10 else " ".join(map(str, p))


def herr_permutaciones():
    st.markdown("Escribe permutaciones en **una línea** (`2314` = 1→2, 2→3, 3→1, 4→4) o con **ciclos** (`(1 2 3)(4 5)`).")
    c1, c2 = st.columns(2)
    tf = c1.text_input("f =", "2314", key="perm_f")
    tg = c2.text_input("g =", "3214", key="perm_g")
    try:
        f, g = G.leer_permutacion(tf), G.leer_permutacion(tg)
    except G.ErrorPermutacion as exc:
        st.error(str(exc))
        return
    n = max(len(f), len(g))
    f, g = G.leer_permutacion(tf, n), G.leer_permutacion(tg, n)
    fg, gf = G.componer(f, g), G.componer(g, f)
    filas = []
    for nombre, p in (("f", f), ("g", g), ("f∘g (primero g)", fg), ("g∘f (primero f)", gf), ("f⁻¹", G.inversa(f))):
        filas.append({"permutación": nombre, "una línea": _fmt(p), "ciclos": G.texto_ciclos(p),
                      "orden": G.orden_permutacion(p), "signo": "par (+1)" if G.signo(p) == 1 else "impar (−1)"})
    st.dataframe(pd.DataFrame(filas), hide_index=True, width="stretch")
    if fg != gf:
        st.info(f"f∘g ≠ g∘f ⇒ **$S_{{{n}}}$ no es abeliano** (y por tanto tampoco cíclico).")
    else:
        st.info("Estas dos conmutan (f∘g = g∘f), pero eso no hace abeliano al grupo: busca un par que no conmute.")
    pot = G.potencias(f)
    with caja("pasos", f"Potencias de f: su orden es {len(pot)}"):
        st.markdown(" → ".join(f"f^{k} = {_fmt(p)}" for k, p in enumerate(pot, 1)))
        lon = [len(c) for c in G.ciclos(f)]
        st.markdown(f"Ciclos disjuntos de longitudes {lon} ⇒ orden = mcm{tuple(lon)} = **{G.orden_permutacion(f)}**.")
        verificado(len(pot) == G.orden_permutacion(f), "Comprobado: la primera potencia que da la identidad coincide con el mcm ✔")
    if n <= 7:
        cuenta = G.ordenes_en_Sn(n)
        st.markdown(f"**Órdenes en $S_{{{n}}}$** ($|S_{{{n}}}|$ = {sum(cuenta.values())}): " +
                    " · ".join(f"orden {o}: {c} elementos" for o, c in cuenta.items()))
        faltan = [o for o in range(1, 7) if o not in cuenta]
        if faltan:
            st.caption(f"No hay elementos de orden {', '.join(map(str, faltan))} en $S_{{{n}}}$.")


def herr_zn_anillo():
    n = int(st.number_input("n (para el anillo ℤₙ)", value=24, min_value=2, max_value=200, key="zna_n"))
    z = G.info_zn(n)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Unidades φ(n)", len(z.unidades))
    c2.metric("Divisores de cero", len(z.divisores_cero))
    c3.metric("¿Dominio?", "sí" if z.es_dominio else "no")
    c4.metric("¿Cuerpo?", "sí" if z.es_cuerpo else "no")
    st.markdown("**Unidades:** " + ", ".join(map(str, z.unidades)))
    if z.divisores_cero:
        st.markdown("**Divisores de cero:** " + ", ".join(map(str, z.divisores_cero)))
    st.markdown("**Nilpotentes** (aᵏ = 0): " + ", ".join(map(str, z.nilpotentes)) +
                " · **Idempotentes** (a² = a): " + ", ".join(map(str, z.idempotentes)))
    verificado(len(z.unidades) + len(z.divisores_cero) == n - 1,
               "Cada elemento no nulo es unidad o divisor de cero (nunca las dos cosas) ✔")
    st.markdown("#### Ideales de ℤₙ: uno por cada divisor d de n")
    filas = [{"ideal": f"⟨{d}⟩", "elementos": len(el), "cociente ℤₙ/⟨d⟩": f"≅ ℤ{str(d).translate(str.maketrans('0123456789', '₀₁₂₃₄₅₆₇₈₉'))}" if d < n else "≅ ℤₙ (ideal 0)",
              "¿maximal?": "sí (d primo)" if d in z.maximales else "no",
              "lista": ", ".join(map(str, el[:16])) + (" …" if len(el) > 16 else "")}
             for d, el in z.ideales if d != 1] + [{"ideal": "⟨1⟩ = ℤₙ", "elementos": n, "cociente ℤₙ/⟨d⟩": "0 (no es ideal propio)",
                                                     "¿maximal?": "no", "lista": "todo"}]
    st.dataframe(pd.DataFrame(filas), hide_index=True, width="stretch")
    c1, c2 = st.columns(2)
    a = int(c1.number_input("Orden aditivo de a =", value=7, step=1, key="zna_a"))
    c1.markdown(f"o({a}) en ($\\mathbb Z_{{{n}}}$, +) = {n}/mcd({a % n}, {n}) = **{G.orden_aditivo(a, n)}**")
    r = c2.text_input("Orden en ℚ/ℤ de r =", "-2/7", key="zna_r")
    try:
        v = sp.Rational(leer(r))
        c2.markdown(f"[{sp.sstr(v)}] tiene orden **{G.orden_en_Q_Z(v)}** (el denominador de la fracción irreducible).")
    except Exception:  # noqa: BLE001
        c2.warning("Escribe un número racional, por ejemplo 333/1000.")


def herr_cocientes():
    st.markdown("Estudia el anillo **𝔽ₚ[x]/(f)**: sus elementos son los restos de grado < gr(f).")
    c1, c2 = st.columns([3, 1])
    tf = c1.text_input("f(x) =", "x^2 + x + 1", key="coc_f")
    p = int(c2.number_input("p (primo)", value=2, min_value=2, max_value=13, key="coc_p"))
    try:
        c = G.cociente_fp(leer(tf), p)
    except Exception as exc:  # noqa: BLE001
        st.error(str(exc))
        return
    d = c.f.degree()
    a1, a2, a3, a4 = st.columns(4)
    a1.metric("Elementos", f"{p}^{d} = {len(c.elementos)}")
    a2.metric("¿f irreducible?", "sí" if c.irreducible else "no")
    a3.metric("¿Es cuerpo?", "sí" if c.irreducible else "no")
    a4.metric("Nilpotentes ≠ 0", len(c.nilpotentes) - 1)
    fac = " · ".join(f"({sp.sstr(b)})" + (f"^{e}" if e > 1 else "") for b, e in c.factores)
    st.markdown(f"Factorización en $\\mathbb F_{{{p}}}[x]$: {fac.replace('**', '^')}")
    verificado(c.irreducible == (len(c.unidades) == len(c.elementos) - 1),
               "Comprobado: es cuerpo exactamente cuando todo elemento no nulo tiene inverso ✔")
    st.markdown("**Unidades:** " + ", ".join(G.fmt_poly(u) for u in c.unidades))
    if c.divisores_cero:
        st.markdown("**Divisores de cero:** " + ", ".join(G.fmt_poly(u) for u in c.divisores_cero))
    st.markdown(f"**Característica:** {p} (1 + 1 + ⋯ + 1, {p} veces, = 0) ⇒ " +
                (f"no es isomorfo a $\\mathbb Z_{{{len(c.elementos)}}}$." if len(c.elementos) != p else f"es $\\mathbb Z_{{{p}}}$."))
    if len(c.elementos) <= 16:
        nombres = [G.fmt_poly(e) for e in c.elementos]
        T = [[G.fmt_poly((a * b).rem(c.f)) for b in c.elementos] for a in c.elementos]
        st.markdown("**Tabla del producto**")
        st.dataframe(pd.DataFrame(T, index=nombres, columns=nombres), width="stretch")
