"""Calculadoras nuevas de Matemática Finita (temas 1, 2, 3 y ampliaciones de 4–7)."""
from __future__ import annotations

from itertools import combinations
import math

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import sympy as sp

from core import logica as LG
from core import conjuntos as CJ
from core import combinatoria as C
from core import enteros as E
from core import polinomios as P
from core.parsing import leer, x, ErrorLectura
from ui.comun import (L, verificado, analogia, figura_base, num, ok_no, calcular, ROSA, LILA, TURQUESA, GRIS, AMARILLO)
from ui.estilo import caja


def _vf(b: bool) -> str:
    return "V" if b else "F"


# ======================================================================== TEMA 1 · LÓGICA
def herr_tabla_verdad():
    st.markdown("Escribe una fórmula con variables p, q, r… y los conectivos **¬ ∧ ∨ → ↔ ⊕** "
                "(también vale `no`, `y`, `o`, `->`, `<->`, `xor`).")
    txt = st.text_input("Fórmula", "(p → q) ∧ (q → r) → (p → r)", key="tv_f")
    try:
        f = LG.leer_formula(txt)
        T = LG.tabla_verdad(f)
    except LG.ErrorFormula as exc:
        st.error(str(exc))
        return
    st.markdown(f"Leída como: **{LG.texto(f)}**  ·  {len(T.variables)} variables ⇒ {2 ** len(T.variables)} filas")
    filas = []
    for vals, cols in T.filas:
        d = {v: _vf(b) for v, b in zip(T.variables, vals)}
        for nombre, b in zip(T.columnas, cols):
            d[nombre] = _vf(b)
        filas.append(d)
    df = pd.DataFrame(filas)

    def color(v):
        return "background-color:#dff5ea;color:#1b7a4b;font-weight:700" if v == "V" else "background-color:#fde3e3;color:#b42323"
    st.dataframe(df.style.map(color), hide_index=True, width="stretch")
    st.caption("Las columnas van de dentro hacia fuera: cada una se calcula con las anteriores. La última es la fórmula completa.")
    tipo = {"tautología": ("🎉 Es una **TAUTOLOGÍA**: verdadera en todas las filas.", st.success),
            "contradicción": ("Es una **CONTRADICCIÓN**: falsa en todas las filas.", st.error),
            "contingencia": ("Es una **CONTINGENCIA**: a veces verdadera y a veces falsa.", st.info)}[T.clase]
    tipo[1](tipo[0])
    with st.expander("¿Cómo se rellena a mano?"):
        st.markdown("1. Escribe todas las combinaciones de V/F de las variables (con n variables hay $2^n$ filas).\n"
                    "2. Calcula primero las subfórmulas más pequeñas (las negaciones y lo que está dentro de paréntesis).\n"
                    "3. Recuerda: $p \\to q$ **sólo es falso** cuando p es V y q es F; $p \\leftrightarrow q$ es V cuando valen lo mismo.")


def herr_equivalencias():
    c1, c2 = st.columns(2)
    a = c1.text_input("Fórmula 1", "¬(p ∧ q)", key="eq_a")
    b = c2.text_input("Fórmula 2", "¬p ∨ ¬q", key="eq_b")
    try:
        fa, fb = LG.leer_formula(a), LG.leer_formula(b)
    except LG.ErrorFormula as exc:
        st.error(str(exc))
        return
    ok, contra = LG.equivalentes(fa, fb)
    if ok:
        st.success(f"**Son equivalentes** ({LG.texto(fa)} ≡ {LG.texto(fb)}): coinciden en todas las filas de la tabla.")
    else:
        asig = ", ".join(f"{k} = {_vf(v)}" for k, v in contra.items())
        st.error(f"**No son equivalentes.** Contraejemplo: con {asig} la fórmula 1 vale "
                 f"{_vf(LG.evaluar(fa, contra))} y la fórmula 2 vale {_vf(LG.evaluar(fb, contra))}.")
    st.markdown("#### Formas normales de la fórmula 1")
    for k, v in LG.formas_normales(fa).items():
        st.markdown(f"- **{k}:** {v}")
    st.markdown("#### Negarla paso a paso")
    for formula, regla in LG.negar_paso_a_paso(fa):
        st.markdown(f"- {formula}  ← _{regla}_")
    with st.expander("📋 Equivalencias que tienes que saber (apartados 23 y 27)"):
        st.markdown(r"""
| Nombre | Equivalencia |
|---|---|
| De Morgan | $\neg(p\wedge q)\equiv\neg p\vee\neg q$, $\ \neg(p\vee q)\equiv\neg p\wedge\neg q$ |
| Distributivas | $p\wedge(q\vee r)\equiv(p\wedge q)\vee(p\wedge r)$, $\ p\vee(q\wedge r)\equiv(p\vee q)\wedge(p\vee r)$ |
| Implicación | $p\to q\equiv\neg p\vee q$ |
| Negar implicación | $\neg(p\to q)\equiv p\wedge\neg q$ |
| Contrarrecíproco | $p\to q\equiv\neg q\to\neg p$ (¡no es $q\to p$!) |
| Bicondicional | $p\leftrightarrow q\equiv(p\to q)\wedge(q\to p)$ |
""")


def herr_cuantificadores():
    st.markdown("Elige un enunciado típico o escribe el tuyo. Separa cada cuantificador con una coma "
                "(`∀ε>0, ∃δ>0, ∀x∈A, (… → …)`).")
    ej = st.selectbox("Enunciados de los apuntes", ["(escribir el mío)"] + list(LG.EJEMPLOS_CUANT), key="cu_sel")
    defecto = LG.EJEMPLOS_CUANT.get(ej, "∀x∈ℝ, x^2 ≥ 0")
    txt = st.text_input("Enunciado", defecto, key=f"cu_txt_{ej}")
    res, pasos = LG.negar_cuantificado(txt)
    with caja("def", "Enunciado"):
        st.markdown(f"### {txt}")
    with caja("resumen", "Su negación"):
        st.markdown(f"### {res}")
    st.markdown("**Qué se ha hecho:**")
    for p in pasos:
        st.markdown(f"- {p}")
    st.caption("Regla de oro: ∀ ↔ ∃ y se niega lo de dentro. El conjunto donde vive la variable (ε>0, n∈ℕ…) NO se niega. "
               "En una implicación P → Q, la negación es P ∧ ¬Q: la hipótesis se mantiene y falla la tesis.")


# ======================================================================== TEMA 2 · CONJUNTOS
def _venn(conj: dict, universo: list | None):
    nombres = list(conj)[:3]
    sets = [set(conj[k]) for k in nombres]
    fig = go.Figure()
    centros = {1: [(0, 0)], 2: [(-0.8, 0), (0.8, 0)], 3: [(-0.8, 0.5), (0.8, 0.5), (0, -0.8)]}[len(nombres)]
    colores = [ROSA, LILA, TURQUESA]
    for (cx, cy), nom, col in zip(centros, nombres, colores):
        t = np.linspace(0, 2 * np.pi, 200)
        fig.add_trace(go.Scatter(x=cx + 1.35 * np.cos(t), y=cy + 1.35 * np.sin(t), fill="toself", mode="lines",
                                 line=dict(color=col, width=2), fillcolor=col, opacity=0.18, name=nom, hoverinfo="skip"))
        fig.add_annotation(x=cx + (cx * 0.9 if cx else 0), y=cy + 1.55 * (1 if cy >= 0 else -1), text=f"<b>{nom}</b>",
                           showarrow=False, font=dict(size=18, color=col))
    todos = set().union(*sets) | (set(universo) if universo else set())
    import itertools
    for mask in itertools.product([True, False], repeat=len(nombres)):
        elems = [e for e in CJ.ordenar(todos) if all((e in s) == m for s, m in zip(sets, mask))]
        if not any(mask):
            px, py = 2.3, -2.0
        else:
            dentro = [c for c, m in zip(centros, mask) if m]
            px = np.mean([c[0] for c in dentro])
            py = np.mean([c[1] for c in dentro])
            if sum(mask) == 1 and len(nombres) > 1:
                i = mask.index(True)
                ox = np.mean([c[0] for c in centros])
                oy = np.mean([c[1] for c in centros])
                px += (centros[i][0] - ox) * 0.6
                py += (centros[i][1] - oy) * 0.6
        if elems:
            fig.add_annotation(x=px, y=py, text="<br>".join(", ".join(map(str, elems[i:i + 4])) for i in range(0, len(elems), 4)),
                               showarrow=False, font=dict(size=13))
    if universo:
        fig.add_shape(type="rect", x0=-3, y0=-2.6, x1=3, y1=2.4, line=dict(color=GRIS, dash="dot"))
        fig.add_annotation(x=-2.8, y=2.2, text="U", showarrow=False, font=dict(size=16, color=GRIS))
    fig.update_layout(height=430, showlegend=False, margin=dict(l=0, r=0, t=0, b=0), plot_bgcolor="white",
                      xaxis=dict(visible=False, range=[-3.2, 3.2]), yaxis=dict(visible=False, range=[-2.8, 2.6], scaleanchor="x"))
    return fig


def herr_conjuntos():
    c1, c2, c3, c4 = st.columns(4)
    A = c1.text_input("A =", "{1, 2, 3, 4}", key="cj_A")
    B = c2.text_input("B =", "{3, 4, 5, 6}", key="cj_B")
    Cc = c3.text_input("C = (opcional)", "{1, 4, 6, 7}", key="cj_C")
    U = c4.text_input("Universo U (para A')", "1..9", key="cj_U")
    try:
        conj = {"A": CJ.leer_conjunto(A), "B": CJ.leer_conjunto(B)}
        if Cc.strip():
            conj["C"] = CJ.leer_conjunto(Cc)
        uni = CJ.leer_conjunto(U) if U.strip() else None
    except CJ.ErrorConjunto as exc:
        st.error(str(exc))
        return
    if uni and not all(set(v) <= set(uni) for v in conj.values()):
        st.warning("Algún conjunto tiene elementos fuera del universo U.")
    st.plotly_chart(_venn(conj, uni), width="stretch")
    expr = st.text_input("Expresión a calcular (∪ ∩ − Δ × y ' para el complementario)", "(A ∪ B) − C", key="cj_e")
    try:
        v, pasos = CJ.evaluar_expresion(expr, conj, uni)
    except CJ.ErrorConjunto as exc:
        st.error(str(exc))
        return
    with caja("resumen", expr):
        st.markdown(f"### {CJ.fmt(v)}")
        st.caption(f"Cardinal: {len(v)}")
    with st.expander("🪜 Paso a paso", expanded=True):
        for s_, val in pasos:
            st.markdown(f"- **{s_}** = {CJ.fmt(val)}")
    with st.expander("Cardinales e inclusión–exclusión"):
        a, b = set(conj["A"]), set(conj["B"])
        st.markdown(f"|A ∪ B| = |A| + |B| − |A ∩ B| = {len(a)} + {len(b)} − {len(a & b)} = **{len(a | b)}** ✓")


def herr_partes_producto():
    c1, c2 = st.columns(2)
    A = c1.text_input("A =", "{a, b, c}", key="pp_A")
    B = c2.text_input("B =", "{0, 1}", key="pp_B")
    try:
        a, b = CJ.leer_conjunto(A), CJ.leer_conjunto(B)
        PA = CJ.partes(a)
    except CJ.ErrorConjunto as exc:
        st.error(str(exc))
        return
    st.markdown(f"#### 𝒫(A) tiene $2^{{{len(a)}}} = {len(PA)}$ elementos")
    por_tam = {}
    for X in PA:
        por_tam.setdefault(len(X), []).append(CJ.fmt(X))
    for k, v in por_tam.items():
        st.markdown(f"- **{k} elemento(s)** ({len(v)} = C({len(a)},{k})): " + ", ".join(v))
    st.markdown(f"#### A × B tiene |A|·|B| = {len(a)}·{len(b)} = {len(a) * len(b)} pares")
    prod = [(u, v) for u in a for v in b]
    st.markdown(", ".join(f"({u}, {v})" for u, v in prod))
    if all(isinstance(t, int) for t in a + b):
        fig = figura_base(alto=320)
        fig.add_trace(go.Scatter(x=[u for u, _ in prod], y=[v for _, v in prod], mode="markers",
                                 marker=dict(size=13, color=ROSA)))
        st.plotly_chart(fig, width="stretch")
    st.caption("Ojo: A × B ≠ B × A en general (pares ORDENADOS), salvo que A = B o alguno sea vacío.")


def _dibujo_aplicacion(f: "CJ.Aplicacion"):
    fig = go.Figure()
    dom, cod = f.dominio, f.codominio
    yd = np.linspace(1, 0, len(dom)) if len(dom) > 1 else [0.5]
    yc = np.linspace(1, 0, len(cod)) if len(cod) > 1 else [0.5]
    pos_d = dict(zip(dom, yd))
    pos_c = dict(zip(cod, yc))
    for a in dom:
        if a in f.regla:
            fig.add_annotation(x=0.9, y=pos_c[f.regla[a]], ax=0.1, ay=pos_d[a], xref="x", yref="y", axref="x", ayref="y",
                               showarrow=True, arrowhead=3, arrowsize=1.3, arrowwidth=2, arrowcolor=LILA)
    fig.add_trace(go.Scatter(x=[0] * len(dom), y=yd, mode="markers+text", text=[str(d) for d in dom], textposition="middle left",
                             marker=dict(size=18, color=ROSA), name="dominio"))
    fig.add_trace(go.Scatter(x=[1] * len(cod), y=yc, mode="markers+text", text=[str(c) for c in cod], textposition="middle right",
                             marker=dict(size=18, color=TURQUESA), name="llegada"))
    fig.update_layout(height=320, showlegend=False, margin=dict(l=30, r=30, t=10, b=10), plot_bgcolor="white",
                      xaxis=dict(visible=False, range=[-0.4, 1.4]), yaxis=dict(visible=False, range=[-0.15, 1.15]))
    return fig


def herr_aplicaciones():
    c1, c2 = st.columns(2)
    dom = c1.text_input("Dominio A =", "{a, b, c}", key="ap_d")
    cod = c2.text_input("Conjunto de llegada B =", "{1, 2, 3}", key="ap_c")
    regla = st.text_input("Flechas (a→1, b→2, …)", "a→1, b→3, c→1", key="ap_r")
    try:
        A, B = CJ.leer_conjunto(dom), CJ.leer_conjunto(cod)
        f = CJ.leer_aplicacion(A, B, regla)
    except CJ.ErrorConjunto as exc:
        st.error(str(exc))
        return
    st.plotly_chart(_dibujo_aplicacion(f), width="stretch")
    if not f.es_aplicacion:
        st.error("**No es una aplicación:**\n\n" + "\n".join(f"- {p}" for p in f.problemas))
        return
    iny, rep = f.inyectiva()
    sob, faltan = f.sobreyectiva()
    c1, c2, c3 = st.columns(3)
    c1.markdown(f"**Inyectiva** {ok_no(iny)}", unsafe_allow_html=True)
    c2.markdown(f"**Sobreyectiva** {ok_no(sob)}", unsafe_allow_html=True)
    c3.markdown(f"**Biyectiva** {ok_no(iny and sob)}", unsafe_allow_html=True)
    if not iny:
        st.markdown(f"- No es inyectiva porque **f({rep[0]}) = f({rep[1]}) = {rep[2]}** con {rep[0]} ≠ {rep[1]}.")
    if not sob:
        st.markdown(f"- No es sobreyectiva porque a **{', '.join(map(str, faltan))}** no le llega ninguna flecha.")
    st.markdown(f"- Imagen f(A) = {CJ.fmt(f.imagen())}")
    inv = f.inversa()
    if inv:
        st.markdown("- **Inversa** f⁻¹: " + ", ".join(f"{b}→{a}" for b, a in inv.items()))
    sub = st.text_input("Contraimagen f⁻¹(B') de B' =", CJ.fmt([B[0]]) if B else "{}", key="ap_sub")
    try:
        st.markdown(f"f⁻¹({sub}) = **{CJ.fmt(f.contraimagen(CJ.leer_conjunto(sub)))}** "
                    "(f⁻¹ aquí es sólo notación: existe aunque f no sea biyectiva).")
    except CJ.ErrorConjunto as exc:
        st.error(str(exc))
    with st.expander("Composición g ∘ f"):
        C_ = st.text_input("Llegada de g, C =", "{x, y}", key="ap_C")
        rg = st.text_input("Flechas de g: B → C", "1→x, 2→y, 3→x", key="ap_g")
        try:
            g = CJ.leer_aplicacion(B, CJ.leer_conjunto(C_), rg)
            if not g.es_aplicacion:
                st.error("g no es aplicación: " + "; ".join(g.problemas))
            else:
                h = CJ.componer(f, g)
                st.markdown("g ∘ f (primero f, luego g): " + ", ".join(f"{a}→{h.regla[a]}" for a in A))
                st.markdown(f"Inyectiva {ok_no(h.inyectiva()[0])} · Sobreyectiva {ok_no(h.sobreyectiva()[0])}", unsafe_allow_html=True)
        except CJ.ErrorConjunto as exc:
            st.error(str(exc))


def herr_contar_aplicaciones():
    c1, c2 = st.columns(2)
    m = int(c1.number_input("|A| = m", value=3, min_value=0, max_value=30, key="ca_m"))
    nn = int(c2.number_input("|B| = n", value=4, min_value=0, max_value=30, key="ca_n"))
    filas = [
        ("Todas las aplicaciones A → B", f"n^m = {nn}^{m}", nn ** m),
        ("Inyectivas", "V(n, m) = n(n−1)…(n−m+1)", math.perm(nn, m) if m <= nn else 0),
        ("Sobreyectivas", "Σ(−1)^i C(n,i)(n−i)^m = n!·S(m,n)", C.sobreyecciones(m, nn)),
        ("Biyectivas", "n! si m = n (si no, 0)", math.factorial(nn) if m == nn else 0),
        ("Constantes", "n (si A ≠ ∅)", nn if m > 0 else 1),
        ("Subconjuntos de A", "2^m", 2 ** m),
    ]
    st.dataframe(pd.DataFrame(filas, columns=["Qué cuento", "Fórmula", "Número"]), hide_index=True, width="stretch")
    st.caption("Truco: piensa que cada elemento de A «elige» su imagen. Si no pueden repetir imagen → inyectiva; si "
               "todas las de B tienen que ser elegidas → sobreyectiva.")


def herr_induccion():
    modo = st.radio("Tipo de propiedad", ["Fórmula de una suma", "Divisibilidad"], horizontal=True, key="in_m")
    if modo.startswith("Fórmula"):
        c1, c2, c3 = st.columns([2, 2, 1])
        t = c1.text_input("Término general (en k)", "k^2", key="in_t")
        Fm = c2.text_input("Fórmula que quiero probar (en n)", "n(n+1)(2n+1)/6", key="in_F")
        n0 = int(c3.number_input("desde k =", value=1, step=1, key="in_n0"))
        try:
            I, tt, F = LG.induccion_suma(t, Fm, n0)
        except (ErrorLectura, ValueError) as exc:
            st.error(str(exc))
            return
        st.latex(rf"\sum_{{k={n0}}}^{{n}} {L(tt)} \overset{{?}}{{=}} {L(F)}")
        with caja("pasos", "1. Caso base"):
            st.markdown(f"n = {n0}: lado izquierdo = lado derecho ⇔ {I.base_detalle} → {ok_no(I.base_ok)}", unsafe_allow_html=True)
        with caja("pasos", "2. Paso inductivo (supongo cierto para n y lo pruebo para n + 1)"):
            for l_ in I.paso_detalle:
                st.latex(l_)
            st.markdown(f"¿Coinciden? {ok_no(I.paso_ok)}", unsafe_allow_html=True)
        if I.base_ok and I.paso_ok:
            st.success("✅ Las dos partes funcionan: la fórmula es cierta para todo n ≥ " + str(n0) + " (principio de inducción).")
        else:
            st.error("La fórmula NO se puede demostrar así: falla " + ("el caso base" if not I.base_ok else "el paso inductivo") +
                     ". Comprueba la fórmula (¡a veces los apuntes tienen erratas, como en el apartado 40 (ii)!).")
        verificado(I.numerico_ok, "Comprobado además con los 25 primeros valores de n ✔",
                   "Con los primeros valores de n la fórmula ya falla.")
    else:
        c1, c2, c3 = st.columns([2, 1, 1])
        e = c1.text_input("Expresión E(n)", "4^n + 15n - 1", key="in_e")
        d = int(c2.number_input("debe ser múltiplo de", value=9, min_value=2, step=1, key="in_d"))
        n0 = int(c3.number_input("desde n =", value=1, step=1, key="in_n1"))
        try:
            I, Ex = LG.induccion_divisibilidad(e, d, n0)
        except (ErrorLectura, ValueError) as exc:
            st.error(str(exc))
            return
        with caja("pasos", "1. Caso base"):
            st.markdown(f"{I.base_detalle}, ¿múltiplo de {d}? {ok_no(I.base_ok)}", unsafe_allow_html=True)
        with caja("pasos", "2. Paso inductivo"):
            for l_ in I.paso_detalle:
                st.latex(l_)
            st.markdown(f"¿Funciona? {ok_no(I.paso_ok)}", unsafe_allow_html=True)
        verificado(I.numerico_ok, "Comprobado con los 40 primeros valores ✔", "Falla para algún n pequeño.")


# ======================================================================== TEMA 3 · RELACIONES
def _leer_relacion(prefijo: str, defecto_A: str, defecto_regla: str):
    c1, c2 = st.columns([1, 2])
    modo = c1.radio("Cómo la doy", ["Con una regla en a y b", "Con la lista de pares"], key=f"{prefijo}_modo")
    presets = {"(ninguno)": None, **CJ.PRESETS_DIVISIBILIDAD}
    pre = c2.selectbox("Conjuntos del ejercicio 162 (divisibilidad)", list(presets), key=f"{prefijo}_pre")
    A_txt = st.text_input("Conjunto A =", ", ".join(map(str, presets[pre])) if presets[pre] else defecto_A, key=f"{prefijo}_A_{pre}")
    try:
        A = CJ.leer_conjunto(A_txt)
        if modo.startswith("Con una"):
            regla = st.text_input("Regla: a R b ⇔", "a | b" if presets[pre] else defecto_regla, key=f"{prefijo}_r_{pre}",
                                  help="Ejemplos: a | b · a ≡ b mod 3 · a <= b · a + b es par · abs(a-b) <= 1")
            R = CJ.relacion_por_regla(A, regla)
        else:
            pares = st.text_area("Pares (a, b)", "(1,1), (2,2), (3,3), (1,2)", key=f"{prefijo}_p")
            R = CJ.relacion_por_pares(A, pares)
    except CJ.ErrorConjunto as exc:
        st.error(str(exc))
        return None, None
    if len(A) > 60:
        st.warning("Con más de 60 elementos los dibujos son ilegibles; los cálculos sí valen.")
    return A, R


def _mostrar_propiedades(A, R):
    props = CJ.propiedades(A, R)
    cols = st.columns(5)
    for col, (k, pr) in zip(cols, props.items()):
        col.markdown(f"**{pr.nombre}**<br>{ok_no(pr.cumple)}", unsafe_allow_html=True)
    for pr in props.values():
        if not pr.cumple:
            st.markdown(f"- No es **{pr.nombre.lower()}**: {pr.contraejemplo}.")
    eq = props["reflexiva"].cumple and props["simetrica"].cumple and props["transitiva"].cumple
    orden = props["reflexiva"].cumple and props["antisimetrica"].cumple and props["transitiva"].cumple
    if eq:
        st.success("Es una **relación de equivalencia** (reflexiva + simétrica + transitiva).")
    if orden:
        st.success("Es una **relación de orden** (reflexiva + antisimétrica + transitiva)" +
                   (" **total**." if props["total"].cumple else " **parcial** (hay pares no comparables)."))
    if not eq and not orden:
        if props["reflexiva"].cumple and props["transitiva"].cumple:
            st.info("Es un **preorden** (reflexiva y transitiva, pero ni simétrica ni antisimétrica).")
        else:
            st.info("No es de equivalencia ni de orden.")
    return props, eq, orden


def herr_relacion():
    A, R = _leer_relacion("rel", "1..6", "a ≡ b mod 2")
    if A is None:
        return
    st.markdown(f"|R| = {len(R)} pares de {len(A)}² = {len(A) ** 2} posibles")
    _mostrar_propiedades(A, R)
    if len(A) <= 16:
        M = CJ.matriz(A, R)
        df = pd.DataFrame(M, index=[str(a) for a in A], columns=[str(a) for a in A])
        st.markdown("**Matriz de la relación** (fila a, columna b: 1 si a R b)")
        st.dataframe(df.style.map(lambda v: "background-color:#ffd6e5;font-weight:700" if v else "color:#ccc"), width="stretch")
        st.caption("Reflexiva ⇔ diagonal llena de 1. Simétrica ⇔ matriz simétrica. Antisimétrica ⇔ fuera de la diagonal nunca hay 1 en (a,b) y (b,a).")


def herr_equivalencia():
    A, R = _leer_relacion("equ", "0..11", "a ≡ b mod 3")
    if A is None:
        return
    props, eq, _ = _mostrar_propiedades(A, R)
    if not eq:
        st.warning("No es de equivalencia, así que no tiene sentido hablar de clases.")
        return
    clases = CJ.clases_equivalencia(A, R)
    st.markdown(f"#### Conjunto cociente A/R: {len(clases)} clases")
    cols = st.columns(min(4, len(clases)))
    for i, cl in enumerate(clases):
        with cols[i % len(cols)]:
            with caja("ej", f"[{cl[0]}]"):
                st.markdown(CJ.fmt(cl))
    st.caption("Las clases son disjuntas y cubren A: forman una partición. (Número de equivalencias posibles en un conjunto "
               "de n elementos = número de Bell B(n).)")


def herr_orden():
    A, R = _leer_relacion("ord", "1..12", "a | b")
    if A is None:
        return
    props, _, orden = _mostrar_propiedades(A, R)
    if not orden:
        st.warning("No es una relación de orden: el diagrama de Hasse sólo tiene sentido para órdenes.")
        return
    niv = CJ.niveles_hasse(A, R)
    cub = CJ.hasse(A, R)
    por_nivel = {}
    for a in A:
        por_nivel.setdefault(niv[a], []).append(a)
    pos = {}
    for k, elems in por_nivel.items():
        for i, a in enumerate(elems):
            pos[a] = ((i - (len(elems) - 1) / 2) * 1.0, k)
    fig = go.Figure()
    for a, b in cub:
        fig.add_trace(go.Scatter(x=[pos[a][0], pos[b][0]], y=[pos[a][1], pos[b][1]], mode="lines",
                                 line=dict(color=LILA, width=2), hoverinfo="skip", showlegend=False))
    fig.add_trace(go.Scatter(x=[pos[a][0] for a in A], y=[pos[a][1] for a in A], mode="markers+text",
                             text=[str(a) for a in A], textposition="middle center", textfont=dict(color="white", size=13),
                             marker=dict(size=30, color=ROSA, line=dict(color="white", width=2)), showlegend=False))
    fig.update_layout(height=120 + 90 * (max(niv.values()) + 1), margin=dict(l=10, r=10, t=10, b=10), plot_bgcolor="white",
                      xaxis=dict(visible=False), yaxis=dict(visible=False))
    st.markdown("#### Diagrama de Hasse")
    st.plotly_chart(fig, width="stretch")
    st.caption("Se une a con b (b arriba) si a ≺ b y no hay nada entre medias. Se omiten los lazos y lo que se deduce por transitividad.")
    st.markdown("#### Cotas y extremos de un subconjunto B ⊆ A")
    B_txt = st.text_input("B =", ", ".join(map(str, A)), key="ord_B")
    try:
        B = CJ.leer_conjunto(B_txt)
        if not set(B) <= set(A):
            st.error("B tiene que estar dentro de A.")
            return
    except CJ.ErrorConjunto as exc:
        st.error(str(exc))
        return
    ex = CJ.extremos(A, R, B)
    filas = [("Cotas superiores", CJ.fmt(ex.cotas_sup)), ("Cotas inferiores", CJ.fmt(ex.cotas_inf)),
             ("Supremo (menor cota superior)", str(ex.supremo) if ex.supremo is not None else "no existe"),
             ("Ínfimo (mayor cota inferior)", str(ex.infimo) if ex.infimo is not None else "no existe"),
             ("Máximo", str(ex.maximo) if ex.maximo is not None else "no existe"),
             ("Mínimo", str(ex.minimo) if ex.minimo is not None else "no existe"),
             ("Maximales", CJ.fmt(ex.maximales)), ("Minimales", CJ.fmt(ex.minimales))]
    st.dataframe(pd.DataFrame(filas, columns=["Concepto", "Valor"]), hide_index=True, width="stretch")
    bo, motivo = CJ.bien_ordenado(B, {(a, b) for (a, b) in R if a in B and b in B})
    st.markdown(f"**¿B está bien ordenado?** {ok_no(bo)} — {motivo}", unsafe_allow_html=True)
    st.caption("Las cotas se buscan en A (no hace falta que estén en B); máximo/mínimo tienen que estar en B. "
               "Maximal = nadie por encima dentro de B (puede haber varios); máximo = por encima de todos (es único).")


def herr_clausuras():
    A, R = _leer_relacion("cla", "1..4", "a < b - 1")
    if A is None:
        return
    st.markdown(f"R = {{{', '.join(f'({a},{b})' for a, b in sorted(R))}}}")
    Rr = CJ.clausura_reflexiva(A, R)
    Rs = CJ.clausura_simetrica(R)
    Rt = CJ.clausura_transitiva(A, R)
    Req = CJ.clausura_transitiva(A, CJ.clausura_simetrica(CJ.clausura_reflexiva(A, R)))
    for nombre, S_, idea in (("reflexiva", Rr, "añado todos los (a, a)"), ("simétrica", Rs, "añado (b, a) por cada (a, b)"),
                             ("transitiva (Warshall)", Rt, "si (a,b) y (b,c) están, añado (a,c), hasta que no cambie"),
                             ("de equivalencia (la menor que contiene a R)", Req, "reflexiva → simétrica → transitiva")):
        nuevos = sorted(S_ - R)
        st.markdown(f"**Clausura {nombre}** — _{idea}_: añade {len(nuevos)} pares" +
                    (": " + ", ".join(f"({a},{b})" for a, b in nuevos[:40]) + (" …" if len(nuevos) > 40 else "") if nuevos else "."))


def herr_lexicografico():
    st.markdown("Compara dos palabras o dos tuplas con el orden **lexicográfico** (el del diccionario) y con el **lexicográfico inverso** (apartados 96–97).")
    c1, c2 = st.columns(2)
    u = c1.text_input("u", "casa", key="lx_u")
    v = c2.text_input("v", "casco", key="lx_v")
    a, b = list(u), list(v)
    i = next((k for k in range(min(len(a), len(b))) if a[k] != b[k]), None)
    if a == b:
        st.info("Son iguales.")
    elif i is None:
        corta = u if len(a) < len(b) else v
        st.success(f"«{corta}» es prefijo de la otra ⇒ va antes: **{corta} ≺ {v if corta == u else u}**.")
    else:
        menor = u if a[i] < b[i] else v
        st.success(f"Primera posición distinta: la {i + 1}ª («{a[i]}» frente a «{b[i]}») ⇒ **{menor}** va antes en el lexicográfico.")
    if len(a) != len(b):
        st.markdown(f"En el **lexicográfico inverso para palabras** se compara primero la longitud: va antes la más corta, «{u if len(a) < len(b) else v}».")
    else:
        j = next((k for k in range(len(a) - 1, -1, -1) if a[k] != b[k]), None)
        if j is not None:
            st.markdown(f"En el **inverso** se decide por la última posición distinta (la {j + 1}ª): va antes «{u if a[j] < b[j] else v}».")


# ======================================================================== TEMA 4 · COMBINATORIA (extras)
def herr_palomar():
    c1, c2 = st.columns(2)
    N = int(c1.number_input("Palomas (objetos) N", value=15, min_value=1, key="pa_N"))
    k = int(c2.number_input("Nidos (cajas) k", value=12, min_value=1, key="pa_k"))
    r = C.palomar(N, k)
    st.latex(rf"\left\lceil \frac{{N}}{{k}} \right\rceil = \left\lceil \frac{{{N}}}{{{k}}} \right\rceil = {r}")
    st.success(f"Alguna caja tiene **al menos {r}** objetos. (Si todas tuvieran ≤ {r - 1}, en total habría ≤ {k * (r - 1)} < {N}.)")
    st.caption("Lo difícil de los ejercicios de palomar es decidir QUIÉNES son las palomas y QUIÉNES los nidos "
               "(meses, restos al dividir, parejas que suman 100…).")
    with st.expander("¿Múltiplos de algún número? (inclusión–exclusión)"):
        c1, c2 = st.columns(2)
        Nn = int(c1.number_input("Del 1 al", value=100, min_value=1, key="pa_m"))
        ds = c2.text_input("múltiplos de alguno de", "2, 3, 5", key="pa_ds")
        try:
            divs = [int(t) for t in ds.replace(";", ",").split(",") if t.strip()]
            total, terms, directo = C.multiplos_inclusion_exclusion(Nn, divs)
        except ValueError:
            st.error("Escribe números separados por comas.")
            return
        st.markdown(" ".join(f"{'+' if s > 0 else '−'} ⌊{Nn}/{m}⌋ ({c})" for S, m, c, s in terms) + f" = **{total}**")
        verificado(total == directo, f"Comprobado contando uno a uno: {directo} ✔")


def herr_particiones():
    modo = st.radio("Qué quiero partir", ["Un número (sumandos)", "Un conjunto (bloques)", "ν(n; J)"], horizontal=True, key="pt_m")
    if modo.startswith("Un número"):
        c1, c2 = st.columns(2)
        nn = int(c1.number_input("n", value=7, min_value=1, max_value=40, key="pt_n"))
        k = int(c2.number_input("en exactamente k sumandos (0 = todas)", value=0, min_value=0, max_value=40, key="pt_k"))
        ps = C.particiones_numero(nn, k or None)
        st.markdown(f"**{len(ps)}** particiones" + (f" de {nn} en {k} sumandos = P({nn},{k})" if k else f" de {nn} = p({nn})"))
        st.markdown(" · ".join("+".join(map(str, p)) for p in ps[:120]) + (" …" if len(ps) > 120 else ""))
        if ps:
            elegido = st.selectbox("Diagrama de Ferrers de", ps, format_func=lambda p: "+".join(map(str, p)), key="pt_f")
            conj = C.conjugada(elegido)
            c1, c2 = st.columns(2)
            c1.markdown("**Ferrers**\n\n" + "\n\n".join("● " * p for p in elegido))
            c2.markdown(f"**Conjugada (trasponer)**: {'+'.join(map(str, conj))}\n\n" + "\n\n".join("● " * p for p in conj))
            st.caption("Trasponer cambia «número de sumandos» por «sumando mayor»: por eso P(n, k) = P′ₖ(n) (apartado 141).")
    elif modo.startswith("Un conjunto"):
        c1, c2 = st.columns(2)
        el = c1.text_input("Conjunto", "1, 2, 3, 4", key="pt_s")
        k = int(c2.number_input("en exactamente k bloques (0 = todos)", value=2, min_value=0, max_value=10, key="pt_sk"))
        elems = CJ.leer_conjunto(el)
        if len(elems) > 8:
            st.warning("Con más de 8 elementos salen demasiadas; muestro sólo el número.")
            st.metric("Número", C.stirling2(len(elems), k) if k else C.bell(len(elems)))
            return
        ps = C.particiones_conjunto(elems, k or None)
        st.markdown(f"**{len(ps)}** particiones = " + (f"S({len(elems)},{k}) (Stirling 2ª especie)" if k else f"B({len(elems)}) (Bell)"))
        st.markdown(" · ".join(" | ".join("{" + ",".join(map(str, b)) + "}" for b in p) for p in ps[:80]))
        verificado(len(ps) == (C.stirling2(len(elems), k) if k else C.bell(len(elems))), "Coincide con la fórmula ✔")
    else:
        c1, c2 = st.columns(2)
        nn = int(c1.number_input("n", value=40, min_value=1, max_value=500, key="nu_n"))
        J = c2.text_input("J (sumandos que tienen que aparecer todos)", "2, 5", key="nu_J")
        try:
            js = [int(t) for t in J.replace(";", ",").split(",") if t.strip()]
        except ValueError:
            st.error("J tiene que ser una lista de enteros positivos.")
            return
        v = C.nu(nn, js)
        st.metric(f"ν({nn}; {set(js)})", v)
        if nn <= 60:
            verificado(v == C.nu_fuerza_bruta(nn, js), "Comprobado listando todas las particiones ✔")
        st.caption("Recurrencia (apartado 145): se clasifica por cuántas veces aparece el último sumando, se quitan y queda una "
                   "partición con los demás. ¡Ojo con el caso en que no queda nada (ν(0, ·) = 0)!")


def herr_binomio():
    c1, c2 = st.columns(2)
    e = c1.text_input("Expresión a desarrollar", "(x + y)^5", key="bi_e")
    try:
        ex = sp.sympify(e.replace("^", "**"))
        st.latex(L(ex) + " = " + L(sp.expand(ex)))
    except Exception:  # noqa: BLE001
        st.error("No entiendo la expresión (usa ^ para potencias).")
    nmax = int(c2.number_input("Filas del triángulo de Pascal", value=8, min_value=1, max_value=20, key="bi_n"))
    filas = [" ".join(str(math.comb(i, j)) for j in range(i + 1)) for i in range(nmax + 1)]
    st.code("\n".join(f.center(len(filas[-1])) for f in filas))
    st.caption("Cada número es la suma de los dos de arriba: C(m+1, n) = C(m, n) + C(m, n−1) (identidad de Pascal).")


# ======================================================================== TEMA 5 · ENTEROS (extras)
def herr_division_entera():
    c1, c2 = st.columns(2)
    a = int(c1.number_input("Dividendo a", value=-17, step=1, key="de_a"))
    b = int(c2.number_input("Divisor b (≠ 0)", value=5, step=1, key="de_b"))
    if b == 0:
        st.error("No se divide entre 0.")
        return
    q, r = E.division_entera(a, b)
    st.latex(rf"{a} = ({q})\cdot({b}) + {r},\qquad 0 \le {r} < |{b}|")
    verificado(q * b + r == a and 0 <= r < abs(b), "Comprobado ✔")
    st.caption("El resto NUNCA es negativo: −17 = (−4)·5 + 3, no (−3)·5 − 2. (Python hace lo mismo con // y % si b > 0.)")
    if a >= 0 and b > 0 and a // b <= 30:
        c, rr, pasos = E.division_por_restas(a, b)
        with st.expander("Algoritmo por restas sucesivas (apartado 150, corregido: while resto ≥ m)"):
            st.markdown(" → ".join(f"{a - b * i}" for i in range(c + 1)) + f"  ⇒ C = {c}, R = {rr}")


def herr_criba():
    N = int(st.slider("Primos hasta N", 10, 400, 100, key="cr_N"))
    primos, pasos = E.criba(N)
    tachado_por = {}
    for k, nuevos in pasos:
        for t in nuevos:
            tachado_por[t] = k
    cols = 10
    filas = []
    for i in range(1, N + 1, cols):
        filas.append([i + j if i + j <= N else None for j in range(cols)])
    df = pd.DataFrame(filas)

    def color(v):
        if v is None or pd.isna(v):
            return ""
        v = int(v)
        if v in primos:
            return "background-color:#ffd6e5;color:#b8336a;font-weight:800"
        if v in tachado_por:
            pal = {2: "#f4f4f4", 3: "#eef7ff", 5: "#f3fff0", 7: "#fff8e6"}
            return f"background-color:{pal.get(tachado_por[v], '#f6f0ff')};color:#aaa;text-decoration:line-through"
        return "color:#bbb"
    st.dataframe(df.style.map(color).format(lambda v: "" if v is None or pd.isna(v) else int(v)), hide_index=True, width="stretch")
    st.markdown(f"**{len(primos)} primos** ≤ {N}. Se ha tachado con k = " + ", ".join(str(k) for k, _ in pasos) +
                f": basta llegar a k ≤ √{N} ≈ {math.isqrt(N)} porque un compuesto n = a·b tiene un factor ≤ √n.")
    verificado(primos == list(sp.primerange(0, N + 1)), "Coincide con la lista de primos de SymPy ✔")


def herr_bases():
    t1, t2, t3, t4 = st.tabs(["10 → base b", "base b → 10", "base b₁ → b₂ (sin pasar por 10)", "Operar en base b"])
    with t1:
        c1, c2 = st.columns(2)
        m = int(c1.number_input("Número (base 10)", value=73, step=1, key="ba_m"))
        b = int(c2.number_input("Base b", value=2, min_value=2, max_value=36, key="ba_b"))
        s, pasos = E.a_base(m, b)
        st.dataframe(pd.DataFrame([(f"{q0} ÷ {b}", q, r) for q0, q, r in pasos], columns=["división", "cociente", "resto"]),
                     hide_index=True)
        st.success(f"{m} = **{s}** en base {b} (los restos leídos de abajo arriba)")
        verificado(int(s, b) == m if b <= 36 else None, "Comprobado convirtiendo de vuelta ✔")
    with t2:
        c1, c2 = st.columns(2)
        s = c1.text_input("Número en base b", "1001001", key="bb_s")
        b = int(c2.number_input("Base b", value=2, min_value=2, max_value=36, key="bb_b"))
        try:
            v, pasos = E.desde_base(s, b)
            st.markdown("Horner: " + " → ".join(f"{a}·{b}+{d} = {n}" for a, d, n in pasos))
            st.success(f"**{v}** en base 10")
        except ValueError as exc:
            st.error(str(exc))
    with t3:
        c1, c2, c3 = st.columns(3)
        s = c1.text_input("Número", "4664", key="bd_s")
        b1 = int(c2.number_input("en base", value=7, min_value=3, max_value=36, key="bd_1"))
        b2 = int(c3.number_input("pasar a base (menor)", value=3, min_value=2, max_value=35, key="bd_2"))
        try:
            res, pasos = E.cambiar_base_directo(s, b1, b2)
        except ValueError as exc:
            st.error(str(exc))
            return
        for actual, q, r, sub in pasos:
            st.markdown(f"**{actual}₍{b1}₎ ÷ {b2}** = {q}₍{b1}₎, resto **{r}** · cifra a cifra: " +
                        ", ".join(f"{ch}: {act}÷{b2}={qq} r{rr}" for ch, act, qq, rr in sub))
        st.success(f"{s}₍{b1}₎ = **{res}₍{b2}₎**")
        try:
            verificado(E.a_base(E.desde_base(s, b1)[0], b2)[0] == res, "Coincide con el camino por base 10 ✔")
        except ValueError:
            pass
        st.caption("Es el apartado 166: dividir entre 3 haciendo las cuentas en base 7 (cada «llevada» vale 7, no 10).")
    with t4:
        c1, c2, c3 = st.columns(3)
        u = c1.text_input("u", "1011", key="bo_u")
        v = c2.text_input("v", "111", key="bo_v")
        b = int(c3.number_input("base", value=2, min_value=2, max_value=16, key="bo_b"))
        try:
            s, llev = E.sumar_en_base(u, v, b)
            st.success(f"{u} + {v} = **{s}** (base {b}); llevadas por columna (de derecha a izquierda): {llev}")
            verificado(E.desde_base(s, b)[0] == E.desde_base(u, b)[0] + E.desde_base(v, b)[0], "Comprobado en base 10 ✔")
        except (ValueError, IndexError):
            st.error("Alguna cifra no existe en esa base.")
        if b <= 12:
            st.markdown(f"**Tablas de la suma y del producto en base {b}** (son las únicas «tablas» que necesitas, apartado 164)")
            c1, c2 = st.columns(2)
            c1.dataframe(pd.DataFrame(E.tabla_base(b, "+")), width="stretch")
            c2.dataframe(pd.DataFrame(E.tabla_base(b, "*")), width="stretch")


def herr_divisores():
    nn = int(st.number_input("n", value=360, min_value=1, step=1, key="dv_n"))
    info = E.info_divisores(nn)
    fac = info["factorizacion"]
    st.latex(rf"{nn} = " + (r"\cdot ".join(f"{p}^{{{e}}}" for p, e in fac.items()) if fac else "1"))
    c1, c2, c3 = st.columns(3)
    c1.metric("Nº de divisores", info["numero"])
    c2.metric("Suma de divisores", info["suma"])
    c3.metric("Producto de divisores", f"{nn}^{info['numero']}/2" if info["numero"] % 2 == 0 else str(info["producto"]))
    st.latex(r"d(n) = " + "".join(f"({e}+1)" for e in fac.values()) + f" = {info['numero']}")
    st.latex(r"\sigma(n) = " + r"\cdot".join(rf"\frac{{{p}^{{{e + 1}}}-1}}{{{p}-1}}" for p, e in fac.items()) + f" = {info['suma']}")
    st.latex(r"\prod_{d\mid n} d = \sqrt{n^{d(n)}} = " + rf"\sqrt{{{nn}^{{{info['numero']}}}}}")
    verificado(info["comprobacion"], "Comprobado listando los divisores uno a uno ✔")
    st.caption("Divisores: " + ", ".join(map(str, info["divisores"][:150])))
    st.markdown("#### mcd y mcm con las factorizaciones (apartado 160)")
    c1, c2 = st.columns(2)
    a = int(c1.number_input("m", value=360, min_value=1, key="dv_a"))
    b = int(c2.number_input("n", value=84, min_value=1, key="dv_b"))
    filas, d, M = E.mcd_mcm_factorizacion(a, b)
    st.dataframe(pd.DataFrame(filas, columns=["primo p", "exp. en m", "exp. en n", "mín → mcd", "máx → mcm"]), hide_index=True)
    st.success(f"mcd = **{d}**, mcm = **{M}**, y mcd·mcm = {d * M} = m·n = {a * b} ✓")


# ======================================================================== TEMA 6 · POLINOMIOS (extras)
def herr_poli_operaciones():
    c1, c2 = st.columns(2)
    a = c1.text_input("p(x) =", "2 + 3x - 5x^2 + 8x^7", key="po_a")
    b = c2.text_input("q(x) =", "1 + x + x^3 - x^5", key="po_b")
    try:
        pa, pb = sp.Poly(leer(a), x), sp.Poly(leer(b), x)
    except Exception as exc:  # noqa: BLE001
        st.error(f"No son polinomios en x: {exc}")
        return
    K = P.Cuerpo()
    ca, cb = P.desde_expr(pa.as_expr(), K), P.desde_expr(pb.as_expr(), K)
    st.latex(rf"p + q = {L(sp.expand(pa.as_expr() + pb.as_expr()))}")
    st.latex(rf"p \cdot q = {L(sp.expand(pa.as_expr() * pb.as_expr()))}")
    g = lambda c: P.grado(c) if not P.es_cero(c) else r"-\infty"  # noqa: E731
    th = lambda c: P.orden(c) if P.orden(c) is not None else r"+\infty"  # noqa: E731
    prod = P.producto(ca, cb, K)
    st.markdown(f"Grados: ∂p = {g(ca)}, ∂q = {g(cb)}, ∂(p·q) = {g(prod)} = ∂p + ∂q ✓ · "
                f"Órdenes: θ(p) = {th(ca)}, θ(q) = {th(cb)}, θ(p·q) = {th(prod)} = θ(p) + θ(q) ✓")
    st.caption("Orden θ = el menor exponente con coeficiente no nulo. Convenio: θ(0) = +∞ y ∂(0) = −∞ (así las fórmulas del "
               "producto siguen valiendo).")


def herr_raices_racionales():
    e = st.text_input("Polinomio con coeficientes enteros (o racionales)", "2x^3 + x^2 - 7x - 6", key="rr_e")
    try:
        ex = leer(e)
        cand, cero = P.candidatos_racionales(ex)
    except Exception as exc:  # noqa: BLE001
        st.error(str(exc))
        return
    st.markdown("**Candidatos p/q** (p divide al término independiente, q al coeficiente líder): " +
                ", ".join(sp.sstr(c) for c in cand))
    K = P.Cuerpo()
    raices, resto, pasos = P.factorizar_por_ruffini(ex, K)
    for rf in pasos:
        st.markdown(f"- Ruffini con **{sp.sstr(rf.a)}**: resto 0 ✓ ⇒ cociente {sp.sstr(P.a_expr(rf.cociente))}")
    if raices:
        fact = " · ".join(f"(x − ({sp.sstr(r)}))" for r in raices) + (f" · ({sp.sstr(P.a_expr(resto))})" if P.grado(resto) >= 1 or P.a_expr(resto) != 1 else "")
        st.success("Raíces racionales: " + ", ".join(sp.sstr(r) for r in raices) + f"  ⇒  p(x) = {fact}")
    else:
        st.info("No tiene raíces racionales.")
    st.latex(r"\text{Factorización completa en } \mathbb{Q}: " + L(sp.factor(ex)))


def herr_irreducibles():
    e = st.text_input("Polinomio", "x^4 + 1", key="ir_e")
    p = int(st.number_input("p (para ℤₚ)", value=5, min_value=2, key="ir_p"))
    try:
        ex = leer(e)
    except ErrorLectura as exc:
        st.error(str(exc))
        return
    filas = []
    for cu, nombre in (("Q", "ℚ"), ("R", "ℝ"), ("C", "ℂ"), ("Zp", f"ℤ_{p}")):
        if cu == "Zp" and not sp.isprime(p):
            continue
        try:
            irr, expl, fact = P.irreducible(ex, cu, p if cu == "Zp" else None)
        except Exception as exc:  # noqa: BLE001
            irr, expl, fact = None, str(exc), "—"
        filas.append((nombre, irr, expl, fact))
    for nombre, irr, expl, fact in filas:
        with caja("teo" if irr else "ej", f"En {nombre}"):
            st.markdown(f"**¿Irreducible?** {ok_no(irr)}", unsafe_allow_html=True)
            st.markdown(expl)
            if nombre != "ℂ":
                st.latex(L(fact))
            else:
                rts = sp.Poly(ex, x).all_roots() if sp.degree(ex, x) <= 6 else []
                if rts:
                    st.latex(r"\text{Raíces: } " + ", ".join(L(sp.nsimplify(r)) if sp.nsimplify(r).count_ops() < 12 else
                                                              L(sp.N(r, 5)) for r in rts))


# ======================================================================== TEMA 7 · MODULAR (extras)
def herr_zn():
    nn = int(st.number_input("n (para ℤₙ)", value=8, min_value=2, max_value=40, key="zn_n"))
    U = E.unidades(nn)
    c1, c2, c3 = st.columns(3)
    c1.metric("Unidades |ℤₙˣ| = φ(n)", len(U))
    c2.metric("¿Es cuerpo?", "sí (n primo)" if sp.isprime(nn) else "no")
    c3.metric("Divisores de cero", len(E.divisores_de_cero(nn)))
    st.markdown("**Unidades (tienen inverso):** " + ", ".join(f"{a} (inverso {pow(a, -1, nn)})" for a in U))
    if E.divisores_de_cero(nn):
        st.markdown("**Divisores de cero:** " + ", ".join(map(str, E.divisores_de_cero(nn))) +
                    " — por ejemplo " + next(f"{a}·{b} ≡ 0" for a in range(1, nn) for b in range(1, nn) if (a * b) % nn == 0))
    c1, c2 = st.columns(2)
    for col, op, nombre in ((c1, "+", "Suma"), (c2, "*", "Producto")):
        T = pd.DataFrame(E.tabla_zn(nn, op), index=range(nn), columns=range(nn))
        with col:
            st.markdown(f"**{nombre} en ℤ_{nn}**")
            st.dataframe(T.style.map(lambda v: "background-color:#ffd6e5;font-weight:800" if v == (0 if op == "+" else 1) else ""),
                         width="stretch")
    st.caption("En la tabla del producto, la fila de a tiene un 1 ⇔ a tiene inverso ⇔ mcd(a, n) = 1 (Teorema 210).")


def herr_fermat_euler():
    t1, t2, t3 = st.tabs(["Fermat y Euler", "Wilson", "Últimas cifras"])
    with t1:
        c1, c2 = st.columns(2)
        a = int(c1.number_input("a", value=3, step=1, key="fe_a"))
        m = int(c2.number_input("m", value=10, min_value=2, step=1, key="fe_m"))
        g = math.gcd(a, m)
        ph = E.phi(m)
        if g != 1:
            st.warning(f"mcd({a}, {m}) = {g} ≠ 1: Euler no se aplica (y {a} no tiene inverso módulo {m}).")
        else:
            st.latex(rf"\varphi({m}) = {ph},\qquad {a}^{{{ph}}} \equiv {pow(a, ph, m)} \pmod{{{m}}}")
            st.success(f"Euler ✓: {a}^φ({m}) ≡ 1." + (" Como m es primo, es el pequeño teorema de Fermat (φ(p) = p − 1)." if sp.isprime(m) else ""))
            o = E.orden_multiplicativo(a, m)
            st.markdown(f"Además, la primera potencia que da 1 es {a}^{o} (el orden de {a}); siempre divide a φ(m) = {ph}.")
    with t2:
        n_ = int(st.number_input("n", value=7, min_value=2, max_value=10 ** 5, key="wi_n"))
        f, ok = E.wilson(n_)
        st.latex(rf"({n_}-1)! \equiv {f} \pmod{{{n_}}}")
        st.markdown(("✅ Da −1 ≡ " + str(n_ - 1) + " ⇒ **" + str(n_) + " es primo** (Wilson)") if ok else
                    f"No da −1 ⇒ **{n_} no es primo**.")
        verificado(ok == sp.isprime(n_), "Coincide con el test de primalidad ✔")
    with t3:
        c1, c2, c3 = st.columns(3)
        b = int(c1.number_input("base", value=7, step=1, key="uc_b"))
        e = int(c2.number_input("exponente", value=103, min_value=0, step=1, key="uc_e"))
        k = int(c3.number_input("cuántas cifras", value=3, min_value=1, max_value=12, key="uc_k"))
        v = E.ultimas_cifras(b, e, k)
        st.success(f"Las {k} últimas cifras de {b}^{e} son **{str(v).zfill(k)}**  ({b}^{e} mód 10^{k})")
        m = 10 ** k
        if math.gcd(b, m) == 1:
            ph = E.phi(m)
            st.markdown(f"Atajo de Euler: φ(10^{k}) = {ph} y {e} ≡ {e % ph} (mód {ph}) ⇒ {b}^{e} ≡ {b}^{e % ph} ≡ {pow(b, e % ph, m)} (mód {m}).")


def herr_sistemas_p():
    st.markdown("Sistema lineal **A·X ≡ b (mód p)**, con p primo (en ℤₚ se puede dividir, así que vale Gauss).")
    c1, c2 = st.columns([3, 1])
    txt = c1.text_area("Filas: coeficientes | término independiente", "1 1 | 1\n1 -1 | 0", key="sp_t", height=110)
    p = int(c2.number_input("p (primo)", value=5, min_value=2, key="sp_p"))
    try:
        A, b = [], []
        for ln in txt.strip().splitlines():
            izq, der = ln.split("|")
            A.append([int(v) for v in izq.split()])
            b.append(int(der))
        if len({len(f) for f in A}) != 1:
            raise ValueError("Todas las filas tienen que tener el mismo número de coeficientes.")
        r = E.gauss_mod_p(A, b, p)
    except ValueError as exc:
        st.error(f"Revisa el sistema: {exc}")
        return
    for titulo, M in r["pasos"]:
        with st.expander(titulo, expanded=len(r["pasos"]) <= 5):
            st.latex(r"\left(\begin{array}{" + "c" * r["nvar"] + "|c}" +
                     r"\\".join(" & ".join(map(str, f)) for f in M) + r"\end{array}\right)")
    st.markdown(f"rango(A) = {r['rango']}, rango(A|b) = {r['rango_ampliada']}")
    if not r["compatible"]:
        st.error("**Incompatible** (Rouché–Frobenius): aparece una fila 0 = algo ≠ 0.")
        return
    nv = r["nvar"]
    st.success(f"**Compatible** con {r['num_soluciones']} soluciones = p^(n − rango) = {p}^{nv - r['rango']}.")
    st.markdown("Solución particular: X = (" + ", ".join(map(str, r["particular"])) + ")")
    if r["nucleo"]:
        st.markdown("Solución general: X = particular + " + " + ".join(f"t{i + 1}·(" + ", ".join(map(str, v)) + ")"
                                                                       for i, v in enumerate(r["nucleo"])) + f",  tᵢ ∈ ℤ_{p}")
    verificado(r["comprobado"], "La solución particular cumple todas las ecuaciones ✔")


def herr_congruencia_varias():
    st.markdown("**a₁X₁ + … + aₙXₙ ≡ b (mód m)** (apartados 224, 230–233)")
    c1, c2, c3 = st.columns([3, 1, 1])
    co = c1.text_input("Coeficientes a₁, …, aₙ", "2, 3", key="cv_a")
    b = int(c2.number_input("b", value=10, step=1, key="cv_b"))
    m = int(c3.number_input("m", value=30, min_value=2, step=1, key="cv_m"))
    try:
        coefs = [int(t) for t in co.replace(";", ",").split(",") if t.strip()]
    except ValueError:
        st.error("Coeficientes enteros separados por comas.")
        return
    r = E.congruencia_varias(coefs, b, m)
    st.latex(rf"g = \operatorname{{mcd}}({', '.join(map(str, coefs))}, {m}) = {r['g']}")
    if not r["compatible"]:
        st.error(f"{r['g']} no divide a {b} ⇒ **no tiene solución**.")
    else:
        st.success(f"{r['g']} | {b} ⇒ tiene **g·m^(n−1) = {r['g']}·{m}^{len(coefs) - 1} = {r['num_soluciones']}** soluciones en ℤ_{m}^{len(coefs)}.")
        if r["particular"]:
            st.markdown("Una solución: (" + ", ".join(map(str, r["particular"])) + ")")
    if r["fuerza_bruta"] is not None:
        verificado(r["fuerza_bruta"] == r["num_soluciones"], f"Comprobado probando las {m}^{len(coefs)} combinaciones: {r['fuerza_bruta']} ✔")
    libre, malos = E.libre_de_cuadrados(m)
    st.markdown(f"¿{m} es libre de cuadrados? {ok_no(libre)}" + ("" if libre else f" (lo dividen {', '.join(f'{p}²' for p in malos)})"),
                unsafe_allow_html=True)
    if libre:
        partes = E.congruencia_por_primos(coefs, b, m)
        with st.expander("Descomposición en una congruencia por cada primo (teorema chino)"):
            for p, cs, bp in partes:
                terminos = " + ".join(f"{c}·X{i + 1}" for i, c in enumerate(cs) if c) or "0"
                st.markdown(f"- mód **{p}**: {terminos} ≡ {bp}")
    with st.expander("Ecuación diofántica en ℤ con n incógnitas"):
        d = E.diofantica_n(coefs, b)
        st.markdown(f"a₁x₁ + … + aₙxₙ = {b} tiene solución entera ⇔ mcd(aᵢ) = {d['g']} divide a {b}: {ok_no(d['compatible'])}",
                    unsafe_allow_html=True)
        if d["particular"]:
            st.markdown("Una solución entera: (" + ", ".join(map(str, d["particular"])) + ")")
