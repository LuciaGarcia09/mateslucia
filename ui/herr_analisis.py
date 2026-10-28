"""Calculadoras nuevas de Análisis (temas 1–7 de los apuntes)."""
from __future__ import annotations

import math

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import sympy as sp

from core import analisis as A
from core import analisis2 as A2
from core.parsing import x, n as n_sym, leer, ErrorLectura
from ui.comun import (L, entrada_expr, entrada_num, verificado, figura_base, trazar, punto, num, ok_no, calcular,
                      ROSA, LILA, TURQUESA, AMARILLO, GRIS)
from ui.estilo import caja


def _rg(clave, a=-5.0, b=5.0):
    c1, c2 = st.columns(2)
    lo = c1.number_input("x mín", value=float(a), key=f"{clave}_lo")
    hi = c2.number_input("x máx", value=float(b), key=f"{clave}_hi")
    return (float(lo), float(hi)) if hi > lo else (a, b)


# ======================================================================== TEMA 1
def herr_topologia():
    st.markdown("Escribe un subconjunto de ℝ como unión de intervalos y puntos (`[0, 1) ∪ {2} ∪ (3, ∞)`) "
                "o con una desigualdad (`x^2 < 4`).")
    t = st.text_input("A =", "[0, 1) ∪ {2} ∪ (3, ∞)", key="to_A")
    S = calcular(A2.leer_conjunto_real, t)
    if S is None:
        return
    st.latex(r"A = " + L(S))
    info = calcular(A2.topologia, S)
    if info is None:
        return
    c1, c2 = st.columns(2)
    with c1:
        for k in ("interior", "adherencia (cierre)", "frontera", "puntos de acumulación", "puntos aislados"):
            st.latex(rf"\text{{{k}}}: " + L(info[k]))
    with c2:
        for k in ("supremo", "ínfimo", "máximo", "mínimo"):
            v = info[k]
            st.markdown(f"**{k.capitalize()}:** " + (f"${L(v)}$" if v is not None else "no existe"))
        st.markdown(" · ".join(f"**{k}** {ok_no(info[k])}" for k in ("abierto", "cerrado", "acotado", "compacto")),
                    unsafe_allow_html=True)
    st.caption("Compacto en ℝ ⇔ cerrado y acotado (Heine–Borel). Un conjunto puede no ser ni abierto ni cerrado, como [0, 1).")
    fig = figura_base(alto=170)
    fig.update_yaxes(visible=False, range=[-1, 1])
    partes = S.args if isinstance(S, sp.Union) else (S,)
    for p in partes:
        if isinstance(p, sp.Interval):
            a_, b_ = float(max(p.start, -20)), float(min(p.end, 20))
            fig.add_trace(go.Scatter(x=[a_, b_], y=[0, 0], mode="lines", line=dict(color=ROSA, width=8), showlegend=False))
            for v_, abierto in ((p.start, p.left_open), (p.end, p.right_open)):
                if v_.is_finite:
                    fig.add_trace(go.Scatter(x=[float(v_)], y=[0], mode="markers", showlegend=False,
                                             marker=dict(size=14, color="white" if abierto else ROSA, line=dict(color=ROSA, width=3))))
        elif isinstance(p, sp.FiniteSet):
            fig.add_trace(go.Scatter(x=[float(v) for v in p], y=[0] * len(p), mode="markers", showlegend=False,
                                     marker=dict(size=14, color=LILA)))
    st.plotly_chart(fig, width="stretch")


def herr_vectores():
    c1, c2 = st.columns(2)
    u = c1.text_input("u =", "(1, 2, 2)", key="ve_u")
    v = c2.text_input("v =", "(2, 0, 1)", key="ve_v")
    try:
        U, V = A2.leer_vector(u), A2.leer_vector(v)
        info = A2.info_vectores(U, V)
    except (ValueError, ErrorLectura) as exc:
        st.error(str(exc))
        return
    for k, val in info.items():
        if isinstance(val, bool):
            st.markdown(f"**{k}:** {ok_no(val)}", unsafe_allow_html=True)
        elif val is not None:
            st.latex(rf"\text{{{k}}} = {L(val)}" + (rf"\approx {num(sp.N(val), 6)}" if not val.is_Rational else ""))
    st.markdown("#### ¿Son base? Coordenadas de un vector")
    vs = st.text_input("Vectores (separados por ;)", "(1,1,0); (1,-1,0); (1,1,1)", key="ve_lista")
    w = st.text_input("Vector w del que quiero las coordenadas", "(1, 3, 0)", key="ve_w")
    try:
        lista = [A2.leer_vector(t) for t in vs.split(";") if t.strip()]
        W = A2.leer_vector(w)
        r = A2.estudio_sistema_vectores(lista, W)
    except (ValueError, ErrorLectura, sp.ShapeError) as exc:
        st.error(f"Revisa los vectores: {exc}")
        return
    st.markdown(f"rango = {r['rango']} · independientes {ok_no(r['independientes'])} · generan ℝ^{r['dimension']} {ok_no(r['generan'])} · "
                f"**base** {ok_no(r['base'])}", unsafe_allow_html=True)
    if r.get("coordenadas"):
        sol = r["coordenadas"][0]
        st.latex(r"w = " + " + ".join(rf"\left({L(sol.get(k, k))}\right)\cdot v_{i + 1}" for i, k in enumerate(sorted(sol, key=str))))
    elif "coordenadas" in r:
        st.info("w no es combinación lineal de esos vectores.")


def herr_complejos():
    c1, c2 = st.columns(2)
    z = c1.text_input("z =", "1 + I", key="cx_z")
    w = c2.text_input("w =", "2 - I", key="cx_w")
    try:
        Z = sp.sympify(leer(z.replace("i", "I") if "I" not in z else z))
        W = sp.sympify(leer(w.replace("i", "I") if "I" not in w else w))
    except ErrorLectura as exc:
        st.error(str(exc))
        return
    ops = A2.operar_complejos(Z, W)
    for k, v in ops.items():
        st.latex(rf"\text{{{k}}} = {L(v)}")
    st.caption("Para dividir: multiplica arriba y abajo por el conjugado del denominador (z/w = z·w̄/|w|²).")
    nexp = int(st.number_input("Potencia zⁿ con De Moivre: n =", value=8, step=1, key="cx_n"))
    mod, arg, (rm, am), directo = A2.de_moivre(Z, nexp)
    st.latex(rf"z = {L(mod)}_{{{L(arg)}}} \Rightarrow z^{{{nexp}}} = {L(mod)}^{{{nexp}}}_{{{nexp}\cdot {L(arg)}}} = {L(rm)}_{{{L(am)}}} = {L(directo)}")
    verificado(abs(complex(sp.N(rm * sp.exp(sp.I * am))) - complex(sp.N(directo))) < 1e-8 * max(1, abs(complex(sp.N(directo)))),
               "Coincide con multiplicar directamente ✔")


def herr_region_compleja():
    st.markdown("Dibuja el conjunto de z que cumplen una condición (como en el problema resuelto 1.6). "
                "Usa `|z-1|`, `re(z)`, `im(z)`, `arg(z)`; separa varias condiciones con `&`.")
    t = st.text_input("Condición", "|z - 1| <= 1 & im(z) > 0", key="rc_t")
    rango = st.slider("Ventana", 1.0, 10.0, 3.0, key="rc_r")
    res = calcular(A2.region_compleja, t, rango)
    if res is None:
        return
    xs, mask, expr = res
    st.latex(L(expr).replace("X", "x").replace("Y", "y") + r"\quad (z = x + iy)")
    fig = go.Figure(go.Heatmap(x=xs, y=xs, z=mask.astype(int), colorscale=[[0, "white"], [1, "#f7a8c6"]], showscale=False))
    fig.update_layout(height=430, margin=dict(l=10, r=10, t=10, b=10), yaxis=dict(scaleanchor="x"), plot_bgcolor="white")
    fig.add_hline(y=0, line_color=GRIS)
    fig.add_vline(x=0, line_color=GRIS)
    st.plotly_chart(fig, width="stretch")


def herr_funciones_reales():
    c1, c2 = st.columns(2)
    f = c1.text_input("f(x) =", "2x + 3", key="fr_f")
    g = c2.text_input("g(x) =", "x^2", key="fr_g")
    try:
        F, G = leer(f), leer(g)
    except ErrorLectura as exc:
        st.error(str(exc))
        return
    st.latex(rf"(g\circ f)(x) = g(f(x)) = {L(sp.expand(G.subs(x, F)))}\qquad (f\circ g)(x) = {L(sp.expand(F.subs(x, G)))}")
    st.caption("En general g∘f ≠ f∘g: el orden importa («primero f, luego g»).")
    y = sp.Symbol("y")
    sol = calcular(sp.solve, sp.Eq(y, F), x)
    if sol:
        st.latex(r"y = f(x) \iff x = " + ", ".join(L(s) for s in sol) + r"\ \Rightarrow\ f^{-1}(y) = " + L(sol[0]))
        if len(sol) > 1:
            st.warning("Hay varias soluciones: f no es inyectiva en todo ℝ; restringe el dominio para poder invertirla.")
        else:
            verificado(A.son_iguales(F.subs(x, sol[0].subs(y, x)), x), "Comprobado: f(f⁻¹(x)) = x ✔")


# ======================================================================== TEMA 2
def herr_epsilon_delta():
    st.markdown("La definición de límite como un **juego**: tú pones el margen ε alrededor de L y yo tengo que encontrar "
                "un δ alrededor de a tal que, si x está a menos de δ de a, f(x) cae dentro de la franja.")
    c1, c2, c3 = st.columns(3)
    with c1:
        f = entrada_expr("f(x) =", "x^2", "ed_f")
    with c2:
        a = entrada_num("a =", "2", "ed_a")
    if f is None or a is None:
        return
    Lr = calcular(sp.limit, f, x, a)
    with c3:
        st.markdown(f"L = lím f(x) = **{sp.sstr(Lr)}**" if Lr is not None else "")
    if Lr is None or not Lr.is_finite:
        st.warning("El límite no es finito: este juego es para límites finitos.")
        return
    eps = st.select_slider("ε (el margen que pides)", [1.0, 0.5, 0.25, 0.1, 0.05, 0.01, 0.005, 0.001], value=0.25, key="ed_e")
    d = A2.buscar_delta(f, a, Lr, eps)
    st.success(f"Con ε = {eps} me vale δ ≈ **{d:.5g}** (o cualquier δ más pequeño).")
    af, Lf = float(sp.N(a)), float(sp.N(Lr))
    ancho = max(4 * d, 0.5)
    fig = figura_base(alto=420)
    trazar(fig, f, af - ancho, af + ancho, "f(x)")
    fig.add_hrect(y0=Lf - eps, y1=Lf + eps, fillcolor="rgba(231,84,128,0.15)", line_width=0, annotation_text="L ± ε")
    fig.add_vrect(x0=af - d, x1=af + d, fillcolor="rgba(142,91,214,0.15)", line_width=0, annotation_text="a ± δ")
    fig.update_yaxes(range=[Lf - 4 * eps - 0.5, Lf + 4 * eps + 0.5])
    st.plotly_chart(fig, width="stretch")
    st.caption("Si para TODO ε encuentras un δ, el límite es L. Si hay un ε para el que ningún δ sirve, no lo es.")


def herr_equivalencias():
    st.markdown("Comprueba si f ≡ g en un punto (lím f/g = 1) y úsalo en un límite. **Sólo en productos y cocientes**, nunca en sumas.")
    c1, c2, c3 = st.columns(3)
    with c1:
        f = entrada_expr("f(x) =", "1 - cos(2x)", "eq_f")
    with c2:
        g = entrada_expr("g(x) =", "2x^2", "eq_g")
    with c3:
        a = entrada_num("en x →", "0", "eq_a")
    if None in (f, g, a):
        return
    q = calcular(sp.limit, f / g, x, a)
    if q is not None:
        st.latex(rf"\lim_{{x\to {L(a)}}} \frac{{{L(f)}}}{{{L(g)}}} = {L(q)}")
        (st.success if q == 1 else st.warning)("Son **equivalentes** ✓" if q == 1 else "No son equivalentes (el cociente no tiende a 1).")
    with st.expander("📋 Tabla de equivalencias de los apuntes (2.3.8)", expanded=True):
        st.markdown(r"""
| En x → 0 | equivale a | En x → 0 | equivale a |
|---|---|---|---|
| $\operatorname{sen}x$, $\operatorname{tg}x$, $\arcsin x$, $\operatorname{arctg}x$ | $x$ | $1-\cos x$ | $x^2/2$ |
| $e^x-1$ | $x$ | $a^x - 1$ | $x\ln a$ |
| $\ln(1+x)$ | $x$ | $(1+x)^a - 1$ | $a x$ |
| $x-\operatorname{sen}x$ | $x^3/6$ | $x - \operatorname{tg}x$ | $-x^3/3$ |
| $x - \ln(1+x)$ | $x^2/2$ | $\ln(\cos x)$ | $-x^2/2$ |
| $\operatorname{sen}x - x\cos x$ | $x^3/3$ | $x - \operatorname{arctg}x$ | $x^3/3$ |
| $a_0 + a_1x + \dots$ ($a_0\neq0$) | $a_0$ | $(1+ax)^{1/x}$ | $\to e^a$ |
| **En x → 1:** $\ln x$ | $x-1$ | $x^a - 1$ | $a(x-1)$ |

Vale cambiando $x$ por cualquier $u(x)\to 0$: por ejemplo $\operatorname{sen}(3x^2)\equiv 3x^2$.
""")


def herr_trozos():
    st.markdown("Función definida **a trozos**, con o sin parámetros (a, b, c, k, m…). Te digo si es continua y derivable en "
                "cada punto de corte y, si hay parámetros, **qué valores hacen falta** (como en los problemas 3.10 y 3.12).")
    n_tr = int(st.number_input("Número de trozos", value=2, min_value=1, max_value=5, key="tz_n"))
    defs = [("a*x + b", "x <= 0"), ("x^2 + 1", "x > 0"), ("x", "x > 3"), ("1", "x > 4"), ("0", "x > 5")]
    lineas = []
    for i in range(n_tr):
        c1, c2 = st.columns([2, 1])
        e = c1.text_input(f"Trozo {i + 1}: f(x) =", defs[i][0], key=f"tz_e{i}")
        c = c2.text_input("si", defs[i][1] if not (n_tr == 3 and i == 1) else "0 < x <= 3", key=f"tz_c{i}_{n_tr}")
        lineas.append((e, c))
    try:
        tr = A2.leer_trozos(lineas)
    except (ValueError, ErrorLectura) as exc:
        st.error(str(exc))
        return
    E_ = calcular(A2.estudiar_trozos, tr)
    if E_ is None:
        return
    for info in E_["estudio"]:
        c = info["punto"]
        with caja("pasos", f"Punto de corte x = {sp.sstr(c)}"):
            nodef = r"\text{no definida}"
            st.latex(rf"\lim_{{x\to {L(c)}^-}} f = {L(info['lim_izq']) if info['lim_izq'] is not None else '—'},\quad "
                     rf"\lim_{{x\to {L(c)}^+}} f = {L(info['lim_der']) if info['lim_der'] is not None else '—'},\quad "
                     rf"f({L(c)}) = {L(info['valor']) if info['valor'] is not None else nodef}")
            if "ec_continuidad" in info:
                ecs = info["ec_continuidad"]
                if E_["parametros"]:
                    st.markdown("Continuidad exige: " + ", ".join(f"${L(e)}$" for e in ecs))
                else:
                    cont = all(e is sp.true for e in ecs) if ecs else True
                    st.markdown(f"**Continua** {ok_no(cont)}", unsafe_allow_html=True)
                st.latex(rf"f'({L(c)}^-) = {L(info['der_izq'])},\qquad f'({L(c)}^+) = {L(info['der_der'])}")
                if not E_["parametros"]:
                    cont = all(e is sp.true for e in info["ec_continuidad"]) if info["ec_continuidad"] else True
                    der = cont and info["ec_derivabilidad"] is sp.true
                    st.markdown(f"**Derivable** {ok_no(der)}" + ("" if cont else " (si no es continua, no puede ser derivable)"),
                                unsafe_allow_html=True)
            st.caption("Las derivadas laterales se calculan como límite de f′ a cada lado: es válido cuando f es continua en el punto "
                       "(Observación 3.1.16 de los apuntes).")
    if E_["parametros"]:
        ps = ", ".join(map(str, E_["parametros"]))
        sc, sd = E_["sol_continua"], E_["sol_derivable"]
        with caja("resumen", "Parámetros"):
            st.markdown(f"**Continua en todo ℝ** ⇔ " + (", ".join("$" + ", ".join(f"{L(k)} = {L(v)}" for k, v in s.items()) + "$" for s in sc)
                                                        if sc else "ningún valor de " + ps))
            st.markdown(f"**Derivable en todo ℝ** ⇔ " + (", ".join("$" + ", ".join(f"{L(k)} = {L(v)}" for k, v in s.items()) + "$" for s in sd)
                                                         if sd else "ningún valor de " + ps + " (las derivadas laterales no pueden coincidir)"))
        if sd and len(sd) == 1 and len(sd[0]) == len(E_["parametros"]):
            fij = sd[0]
        elif sc and len(sc) == 1 and len(sc[0]) == len(E_["parametros"]):
            fij = sc[0]
        else:
            fij = None
    else:
        fij = {}
    if fij is not None:
        pw = A2.a_piecewise(tr).subs(fij)
        fig = figura_base(alto=360)
        trazar(fig, pw, *_rg("tz_rg", -4, 4), "f(x)")
        st.plotly_chart(fig, width="stretch")


def herr_weierstrass():
    st.markdown("**Extremos absolutos** de f continua en [a, b] (Weierstrass dice que existen). Se comparan los valores en "
                "los extremos del intervalo, en los puntos críticos y donde f no es derivable.")
    c1, c2, c3 = st.columns(3)
    with c1:
        f = entrada_expr("f(x) =", "x^3 - 3x", "we_f")
    with c2:
        a = entrada_num("a =", "-3", "we_a")
    with c3:
        b = entrada_num("b =", "2", "we_b")
    if None in (f, a, b):
        return
    r = calcular(A2.extremos_absolutos, f, a, b)
    if r is None:
        return
    tabla, mx, mn = r
    st.dataframe(pd.DataFrame([(sp.sstr(c), sp.sstr(v), num(vf, 8)) for c, v, vf in tabla],
                              columns=["candidato x", "f(x) exacto", "≈"]), hide_index=True, width="stretch")
    st.success(f"Máximo absoluto {sp.sstr(mx[1])} en x = {sp.sstr(mx[0])} · Mínimo absoluto {sp.sstr(mn[1])} en x = {sp.sstr(mn[0])}")
    fig = figura_base(alto=360)
    trazar(fig, f, float(sp.N(a)), float(sp.N(b)), "f(x)")
    punto(fig, float(sp.N(mx[0])), mx[2], "máx")
    punto(fig, float(sp.N(mn[0])), mn[2], "mín", color=TURQUESA)
    st.plotly_chart(fig, width="stretch")


def herr_uniforme():
    st.markdown("**Continuidad uniforme**: el mismo δ tiene que servir en TODOS los puntos. Si |f′| está acotada por L en el "
                "intervalo, f es Lipschitz y por tanto uniformemente continua (δ = ε/L).")
    c1, c2, c3 = st.columns(3)
    with c1:
        f = entrada_expr("f(x) =", "1/x", "uc_f")
    with c2:
        a = entrada_num("intervalo desde", "0", "uc_a")
    with c3:
        b = entrada_num("hasta", "1", "uc_b")
    if None in (f, a, b):
        return
    af, bf = float(sp.N(a)), float(sp.N(b))
    xs = np.linspace(af + (bf - af) * 1e-4, bf - (bf - af) * 1e-4, 4000)
    df = sp.diff(f, x)
    d = np.abs(A.lambdificar(df)(xs))
    Lip = float(np.nanmax(d))
    st.latex(rf"\sup |f'(x)| \approx {num(Lip, 6)}")
    if Lip > 1e5:
        st.warning("|f′| se dispara cerca del borde: probablemente **no** es uniformemente continua en el intervalo abierto. "
                 "Prueba el criterio secuencial: busca xₙ, yₙ con |xₙ − yₙ| → 0 pero |f(xₙ) − f(yₙ)| ≥ ε₀ (Ej. 2.5.3: xₙ = 1/n, yₙ = 1/(n+1) para 1/x).")
    else:
        st.success(f"|f′| ≤ {num(Lip, 4)} ⇒ f es Lipschitz ⇒ **uniformemente continua** en el intervalo.")
    st.caption("Heine–Cantor: si f es continua en un intervalo CERRADO y acotado [a, b], siempre es uniformemente continua.")


# ======================================================================== TEMA 3
def herr_valor_medio():
    tipo = st.radio("Teorema", ["Rolle", "Lagrange (valor medio)", "Cauchy (generalizado)"], horizontal=True, key="vm_t")
    c1, c2, c3 = st.columns(3)
    with c1:
        f = entrada_expr("f(x) =", "x^3 - x" if tipo == "Rolle" else "x^3", "vm_f")
    with c2:
        a = entrada_num("a =", "-1" if tipo == "Rolle" else "0", "vm_a")
    with c3:
        b = entrada_num("b =", "1" if tipo == "Rolle" else "2", "vm_b")
    g = None
    if tipo.startswith("Cauchy"):
        g = entrada_expr("g(x) =", "x^2", "vm_g")
    if None in (f, a, b) or (tipo.startswith("Cauchy") and g is None):
        return
    clave = {"Rolle": "rolle", "Lagrange (valor medio)": "lagrange", "Cauchy (generalizado)": "cauchy"}[tipo]
    r = calcular(A2.valor_medio, f, a, b, clave, g)
    if r is None:
        return
    with caja("pasos", "Hipótesis"):
        for h, ok in r["hipotesis"]:
            st.markdown(f"- {h}: {ok_no(ok)}", unsafe_allow_html=True)
    st.latex(L(r["ecuacion"]))
    if r["c"]:
        st.success("Puntos c ∈ (a, b) que cumplen la tesis: " + ", ".join(f"c = {sp.sstr(c)} ≈ {num(sp.N(c), 6)}" for c in r["c"]))
    else:
        st.warning("No hay ningún c: alguna hipótesis falla (mira arriba).")
    fig = figura_base(alto=380)
    af, bf = float(sp.N(a)), float(sp.N(b))
    trazar(fig, f, af - 0.3 * (bf - af), bf + 0.3 * (bf - af), "f(x)")
    fa, fb = float(sp.N(r["fa"])), float(sp.N(r["fb"]))
    fig.add_trace(go.Scatter(x=[af, bf], y=[fa, fb], mode="lines+markers", line=dict(color=GRIS, dash="dash"), name="cuerda"))
    m = (fb - fa) / (bf - af)
    for c in r["c"][:3]:
        cf = float(sp.N(c))
        yc = float(sp.N(f.subs(x, c)))
        if tipo == "Rolle":
            m_ = 0.0
        else:
            m_ = float(sp.N(sp.diff(f, x).subs(x, c)))
        xs = np.array([cf - (bf - af) / 2, cf + (bf - af) / 2])
        fig.add_trace(go.Scatter(x=xs, y=yc + m_ * (xs - cf), mode="lines", line=dict(color=LILA, width=2), name=f"tangente en c={num(cf, 4)}"))
    st.plotly_chart(fig, width="stretch")
    st.caption("Geométricamente: hay un punto donde la tangente es PARALELA a la cuerda (en Rolle la cuerda es horizontal).")


def herr_hopital():
    c1, c2, c3 = st.columns(3)
    with c1:
        f = entrada_expr("Numerador f(x)", "x - sen(x)", "ho_f")
    with c2:
        g = entrada_expr("Denominador g(x)", "x^3", "ho_g")
    with c3:
        a = entrada_num("x →", "0", "ho_a")
    if None in (f, g, a):
        return
    r = calcular(A2.hopital, f, g, a)
    if r is None:
        return
    pasos, res = r
    for i, p in enumerate(pasos):
        with caja("pasos", f"Paso {i}" + (" (cociente original)" if i == 0 else f" (derivo {i} vez/veces arriba y abajo)")):
            st.latex(rf"\frac{{{L(p.num)}}}{{{L(p.den)}}}\quad\longrightarrow\quad \frac{{{L(p.lim_num)}}}{{{L(p.lim_den)}}}")
            st.markdown("**Indeterminación " + p.tipo + "** ⇒ aplico L'Hôpital" if p.tipo != "determinado" else "Ya no hay indeterminación.")
    st.latex(rf"\lim_{{x\to {L(a)}}} \frac{{{L(f)}}}{{{L(g)}}} = {L(res)}")
    st.caption("Ojo: se derivan numerador y denominador POR SEPARADO (no es la regla del cociente). Y la regla sólo dice "
               "algo si existe el límite del cociente de derivadas (Nota 3.3.11). Para 0·∞, ∞−∞ o 1^∞, primero pásalo a cociente.")


def herr_implicita():
    t1, t2 = st.tabs(["Derivación implícita", "Fórmula de Leibniz (fg)⁽ⁿ⁾"])
    with t1:
        e = st.text_input("Ecuación en x e y", "y^3 + y^2 - 5y - x^2 + 4 = 0", key="im_e")
        r = calcular(A2.derivada_implicita, e)
        if r is None:
            return
        h, hx, hy, dydx, d2 = r
        st.latex(rf"h(x,y) = {L(h)} = 0")
        st.latex(rf"\text{{Derivo respecto de }} x \text{{ (y depende de x)}}:\ {L(hx)} + \left({L(hy)}\right) y' = 0")
        st.latex(rf"y' = \frac{{dy}}{{dx}} = {L(dydx)}")
        st.latex(rf"y'' = {L(d2)}")
        with st.expander("Recta tangente en un punto de la curva"):
            c1, c2 = st.columns(2)
            x0 = entrada_num("x₀", "2", "im_x0")
            y0 = entrada_num("y₀", "1", "im_y0")
            if x0 is not None and y0 is not None:
                y = sp.Symbol("y", real=True)
                if sp.simplify(h.subs({x: x0, y: y0})) != 0:
                    st.warning("Ese punto no está en la curva.")
                else:
                    m = sp.simplify(dydx.subs({x: x0, y: y0}))
                    st.latex(rf"y - {L(y0)} = {L(m)}\,(x - {L(x0)})")
    with t2:
        c1, c2, c3 = st.columns(3)
        with c1:
            f = entrada_expr("f(x) =", "x^2", "lb_f")
        with c2:
            g = entrada_expr("g(x) =", "e^x", "lb_g")
        with c3:
            nn = int(st.number_input("orden n", value=3, min_value=1, max_value=12, key="lb_n"))
        if f is None or g is None:
            return
        terms, total, ok = A2.leibniz(f, g, nn)
        st.latex(rf"(fg)^{{({nn})}} = \sum_{{k=0}}^{{{nn}}}\binom{{{nn}}}{{k}} f^{{(k)}} g^{{({nn}-k)}} = " +
                 " + ".join(rf"{L(c)}\cdot\left({L(a)}\right)\left({L(b)}\right)" for k, c, a, b in terms if a != 0 and b != 0))
        st.latex(rf"= {L(total)}")
        verificado(ok, "Coincide con derivar el producto directamente ✔")


def herr_taylor_resto():
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        f = entrada_expr("f(x) =", "sen(x)", "tr_f")
    with c2:
        a = entrada_num("centro a", "0", "tr_a")
    with c3:
        x0 = entrada_num("evaluar en", "0.1", "tr_x0")
    with c4:
        orden = int(st.number_input("orden n", value=7, min_value=0, max_value=30, key="tr_n"))
    if None in (f, a, x0):
        return
    r = calcular(A2.cota_lagrange, f, a, x0, orden)
    if r is None:
        return
    d, M, cota = r
    T = sp.series(f, x, a, orden + 1).removeO()
    real = abs(float(sp.N(f.subs(x, x0) - T.subs(x, x0))))
    st.latex(rf"|R_{{{orden}}}| = \left|\frac{{f^{{({orden + 1})}}(\xi)}}{{({orden + 1})!}}(x-a)^{{{orden + 1}}}\right| \le "
             rf"\frac{{M\,|{L(x0)} - {L(a)}|^{{{orden + 1}}}}}{{{orden + 1}!}},\quad M = \max|f^{{({orden + 1})}}| \approx {num(M, 5)}")
    c1, c2 = st.columns(2)
    c1.metric("Cota del error (Lagrange)", f"{cota:.3e}")
    c2.metric("Error real", f"{real:.3e}")
    verificado(real <= cota * (1 + 1e-9) + 1e-300, "El error real está por debajo de la cota ✔", "¡El error real supera la cota! Revisa.")
    tol = st.select_slider("¿Qué orden necesito para un error menor que…?", [1e-2, 1e-3, 1e-4, 1e-6, 1e-8, 1e-10], value=1e-6, key="tr_tol")
    k, c = A2.orden_necesario(f, a, x0, tol)
    st.info(f"Con orden **n = {k}** la cota ya es {c:.2e} < {tol:g}." if k is not None else "No lo consigo con órdenes razonables.")


def herr_extremos_derivadas():
    c1, c2 = st.columns(2)
    with c1:
        f = entrada_expr("f(x) =", "x^4 - 4x^3 + 6x^2 - 4x", "ex_f")
    with c2:
        c = entrada_num("punto c", "1", "ex_c")
    if f is None or c is None:
        return
    r = calcular(A2.criterio_derivadas_sucesivas, f, c)
    if r is None:
        return
    ders, concl = r
    st.dataframe(pd.DataFrame([(f"f^({k})(c)", sp.sstr(v)) for k, v in ders], columns=["derivada", "valor"]), hide_index=True)
    st.success(concl)
    st.caption("Teorema 3.2.6 / 3.5.9: si la primera derivada no nula (a partir de f′) es de orden PAR, hay extremo (mín si es > 0, "
               "máx si es < 0); si es IMPAR, no hay extremo. Para inflexión se mira la primera no nula a partir de f″ (orden impar ≥ 3).")


# ======================================================================== TEMA 4
def herr_pasos_integral():
    f = entrada_expr("Integrar f(x) =", "x^2*e^x", "pi_f")
    if f is None:
        return
    with caja("truco", "¿Qué método uso?"):
        for p_ in A2.sugerir_metodo(f):
            st.markdown(f"- {p_}")
    pasos = calcular(A2.pasos_integral, f, segundos=20)
    if pasos:
        with caja("pasos", "Resolución paso a paso"):
            for nivel, linea in pasos:
                st.latex(r"\quad " * nivel + linea)
    F = calcular(sp.integrate, f, x)
    if F is not None and not F.has(sp.Integral):
        st.latex(rf"\int {L(f)}\,dx = {L(sp.simplify(F))} + C")
        verificado(A.son_iguales(sp.diff(F, x), f), "Comprobado: al derivar el resultado sale f ✔")
    num_, den = sp.fraction(sp.together(f))
    if f.is_rational_function(x) and sp.degree(den, x) >= 1:
        with st.expander("Fracciones simples (apart)"):
            st.latex(rf"{L(f)} = {L(sp.apart(f, x))}")


def herr_darboux():
    c1, c2, c3 = st.columns(3)
    with c1:
        f = entrada_expr("f(x) =", "x^2", "da_f")
    with c2:
        a = entrada_num("a", "0", "da_a")
    with c3:
        b = entrada_num("b", "1", "da_b")
    if None in (f, a, b):
        return
    N = st.slider("Número de subintervalos de la partición", 1, 200, 8, key="da_N")
    xs, Ms, ms, U, Lw = A2.sumas_darboux(f, a, b, N)
    exacto = sp.integrate(f, (x, a, b))
    c1, c2, c3 = st.columns(3)
    c1.metric("Suma inferior L(P, f)", num(Lw, 8))
    c2.metric("Integral", num(sp.N(exacto), 8) if not exacto.has(sp.Integral) else "?")
    c3.metric("Suma superior U(P, f)", num(U, 8))
    fig = figura_base(alto=380)
    w = np.diff(xs)
    mids = xs[:-1] + w / 2
    fig.add_trace(go.Bar(x=mids, y=Ms, width=w, marker_color="rgba(231,84,128,0.25)", name="superior (sup)"))
    fig.add_trace(go.Bar(x=mids, y=ms, width=w, marker_color="rgba(142,91,214,0.45)", name="inferior (inf)"))
    trazar(fig, f, float(sp.N(a)), float(sp.N(b)), "f(x)")
    fig.update_layout(barmode="overlay")
    st.plotly_chart(fig, width="stretch")
    st.caption(f"U − L = {U - Lw:.4g}. f es integrable ⇔ U − L se puede hacer tan pequeño como quieras afinando la partición.")


def herr_tfc():
    st.markdown("**F(x) = ∫ de h(x) a g(x) de f(t) dt** ⇒ F′(x) = f(g(x))·g′(x) − f(h(x))·h′(x) (sin calcular la integral).")
    c1, c2, c3 = st.columns(3)
    with c1:
        f = entrada_expr("f(t) (escríbela con x)", "sen(x)^3", "tf_f")
    with c2:
        g = entrada_expr("límite superior g(x)", "x^3", "tf_g")
    with c3:
        h = entrada_expr("límite inferior h(x)", "x^2", "tf_h")
    if None in (f, g, h):
        return
    res = A2.derivada_integral_variable(f, g, h)
    st.latex(rf"F(x) = \int_{{{L(h)}}}^{{{L(g)}}} {L(f.subs(x, sp.Symbol('t')))}\,dt \ \Rightarrow\ F'(x) = {L(res)}")
    x0 = 0.7
    t = sp.Symbol("t", real=True)
    fl = sp.lambdify(t, f.subs(x, t), "mpmath")
    import mpmath as mp
    Fn = lambda v: mp.quad(fl, [float(sp.N(h.subs(x, v))), float(sp.N(g.subs(x, v)))])  # noqa: E731
    e = 1e-5
    num_d = float((Fn(x0 + e) - Fn(x0 - e)) / (2 * e))
    verificado(abs(num_d - float(sp.N(res.subs(x, x0)))) < 1e-6 * max(1, abs(num_d)),
               f"Comprobado derivando numéricamente F en x = {x0} ✔")


def herr_areas():
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        f = entrada_expr("f(x) =", "x^2", "ar_f")
    with c2:
        g = entrada_expr("g(x) =", "x", "ar_g")
    with c3:
        a = entrada_num("desde", "0", "ar_a")
    with c4:
        b = entrada_num("hasta", "2", "ar_b")
    if None in (f, g, a, b):
        return
    r = calcular(A2.area_entre, f, g, a, b)
    if r is None:
        return
    cortes, trozos, total, numerico = r
    st.markdown("Cortes entre las curvas en el intervalo: " + (", ".join(sp.sstr(c) for c in cortes) or "ninguno"))
    for p_, q_, v in trozos:
        st.latex(rf"\int_{{{L(p_)}}}^{{{L(q_)}}} (f-g)\,dx = {L(v)}")
    st.latex(rf"\text{{Área}} = \sum \left|\int (f-g)\right| = {L(total)} \approx {num(sp.N(total), 8)}")
    verificado(abs(float(sp.N(total)) - numerico) < 1e-6 * max(1, numerico), "Comprobado integrando |f − g| numéricamente ✔")
    fig = figura_base(alto=380)
    af, bf = float(sp.N(a)), float(sp.N(b))
    xs = np.linspace(af, bf, 400)
    yf, yg = A.lambdificar(f)(xs), A.lambdificar(g)(xs)
    fig.add_trace(go.Scatter(x=np.concatenate([xs, xs[::-1]]), y=np.concatenate([yf, yg[::-1]]), fill="toself",
                             fillcolor="rgba(231,84,128,0.25)", line=dict(width=0), name="área"))
    trazar(fig, f, af, bf, "f")
    trazar(fig, g, af, bf, "g", color=LILA)
    st.plotly_chart(fig, width="stretch")
    st.caption("Error típico: integrar f − g de golpe. Si las curvas se cruzan, las zonas se restan; hay que partir en los cortes.")


def herr_volumenes():
    c1, c2, c3 = st.columns(3)
    with c1:
        f = entrada_expr("f(x) =", "raiz(x)", "vo_f")
    with c2:
        a = entrada_num("a", "0", "vo_a")
    with c3:
        b = entrada_num("b", "1", "vo_b")
    if None in (f, a, b):
        return
    r = calcular(A2.aplicaciones_integral, f, a, b, segundos=25)
    if r is None:
        return
    for nombre, (integ, ex, nm) in r.items():
        with caja("ej", nombre.capitalize()):
            st.latex(rf"\int_{{{L(a)}}}^{{{L(b)}}} {L(integ)}\,dx = " + (L(ex) + r"\approx " if ex is not None else "") + num(nm, 8))
            if ex is not None and nm is not None:
                verificado(abs(float(sp.N(ex)) - nm) < 1e-6 * max(1, abs(nm)), "exacto = numérico ✔")


def herr_parametricas():
    modo = st.radio("Tipo de curva", ["Paramétrica (x(t), y(t))", "Polar ρ(θ)"], horizontal=True, key="pa_modo")
    if modo.startswith("Param"):
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            xt = entrada_expr("x(t) (usa x como t)", "cos(x)^3", "pm_x")
        with c2:
            yt = entrada_expr("y(t)", "sen(x)^3", "pm_y")
        with c3:
            t0 = entrada_num("t desde", "0", "pm_t0")
        with c4:
            t1 = entrada_num("t hasta", "2*pi", "pm_t1")
        if None in (xt, yt, t0, t1):
            return
        r = calcular(A2.parametrica, xt, yt, t0, t1, segundos=25)
        if r is None:
            return
        res, X, Y, t = r
        for nombre, (integ, ex, nm) in res.items():
            st.latex(rf"\text{{{nombre}}}: \int {L(integ)}\,dt = " + (L(ex) + r"\approx " if ex is not None else "") + num(nm, 8))
        ts = np.linspace(float(sp.N(t0)), float(sp.N(t1)), 600)
        fx, fy = sp.lambdify(t, X, "numpy"), sp.lambdify(t, Y, "numpy")
        fig = figura_base(alto=400)
        fig.add_trace(go.Scatter(x=fx(ts) * np.ones_like(ts), y=fy(ts) * np.ones_like(ts), mode="lines", line=dict(color=ROSA, width=3)))
        fig.update_yaxes(scaleanchor="x")
        st.plotly_chart(fig, width="stretch")
        st.caption("El área ½∫(xy′ − yx′) sale positiva si la curva se recorre en sentido antihorario; si no, toma el valor absoluto.")
    else:
        c1, c2, c3 = st.columns(3)
        with c1:
            rho = entrada_expr("ρ(θ) (usa x como θ)", "2*(1 - cos(x))", "po_r")
        with c2:
            t0 = entrada_num("θ desde", "0", "po_t0")
        with c3:
            t1 = entrada_num("θ hasta", "2*pi", "po_t1")
        if None in (rho, t0, t1):
            return
        r_, ex, nm, t = A2.area_polar(rho, t0, t1)
        st.latex(rf"A = \frac12\int \rho(\theta)^2\,d\theta = " + (L(ex) + r"\approx " if ex is not None else "") + num(nm, 8))
        ts = np.linspace(float(sp.N(t0)), float(sp.N(t1)), 600)
        rr = sp.lambdify(t, r_, "numpy")(ts) * np.ones_like(ts)
        fig = figura_base(alto=400)
        fig.add_trace(go.Scatter(x=rr * np.cos(ts), y=rr * np.sin(ts), mode="lines", fill="toself",
                                 fillcolor="rgba(231,84,128,0.2)", line=dict(color=ROSA, width=3)))
        fig.update_yaxes(scaleanchor="x")
        st.plotly_chart(fig, width="stretch")


def herr_impropias():
    st.markdown("¿Converge sin calcularla? Comparo con $1/x^s$ (en ∞: converge ⇔ s > 1) o con $1/|x-b|^s$ "
                "(en un punto: converge ⇔ s < 1).")
    c1, c2 = st.columns(2)
    with c1:
        f = entrada_expr("f(x) =", "x^2/(1+x^2)^2", "im_f")
    with c2:
        donde = st.selectbox("¿Dónde está el problema?", ["en +∞", "en un punto (asíntota vertical)"], key="im_d")
    if f is None:
        return
    if donde == "en +∞":
        r = calcular(A2.comparacion_impropia, f, sp.oo)
    else:
        c1, c2 = st.columns(2)
        with c1:
            b = entrada_num("punto", "0", "im_b")
        with c2:
            lado = st.radio("lado", ["por la derecha (b⁺)", "por la izquierda (b⁻)"], key="im_l")
        if b is None:
            return
        r = calcular(A2.comparacion_impropia, f, b, "inf" if "derecha" in lado else "sup")
    if not r:
        st.info("No he podido decidir el orden de la función; calcula la integral con límite en la pestaña de integrales.")
        return
    st.latex(r["explicacion"] if r["explicacion"].startswith("\\") else rf"\text{{{r['explicacion']}}}")
    if r["converge"] is True:
        st.success(f"s = {sp.sstr(r['s'])} ⇒ **converge**.")
    elif r["converge"] is False:
        st.error(f"s = {sp.sstr(r['s'])} ⇒ **diverge**.")
    else:
        st.info("El criterio no decide con este s (límite 0 o ∞): usa las versiones i) / ii) del criterio de comparación.")


def herr_beta_gamma():
    c1, c2 = st.columns(2)
    p = entrada_num("p", "1/2", "bg_p")
    q = entrada_num("q (vacío = sólo Γ(p))", "1/2", "bg_q")
    if p is None:
        return
    g, gn = A2.beta_gamma(p)
    st.latex(rf"\Gamma({L(p)}) = \int_0^\infty x^{{{L(p)}-1}}e^{{-x}}dx = {L(g)} \approx {num(gn, 10)}")
    if q is not None:
        b, bn = A2.beta_gamma(p, q)
        st.latex(rf"\beta({L(p)},{L(q)}) = \frac{{\Gamma(p)\Gamma(q)}}{{\Gamma(p+q)}} = {L(b)} \approx {num(bn, 10)}")
    st.caption("Γ(n) = (n − 1)! para n natural · Γ(p) = (p − 1)Γ(p − 1) · Γ(1/2) = √π · β(p, q) = β(q, p).")


# ======================================================================== TEMA 5
def herr_recurrentes():
    st.markdown("Sucesión **recurrente** x₁ dado, xₙ₊₁ = g(xₙ). Si converge a L y g es continua, L = g(L) (punto fijo).")
    c1, c2, c3 = st.columns(3)
    with c1:
        g = entrada_expr("g(x) =", "raiz(2 + x)", "rec_g")
    with c2:
        x1 = st.number_input("x₁", value=1.0, key="rec_x1")
    with c3:
        N = st.slider("términos", 5, 200, 30, key="rec_N")
    if g is None:
        return
    vals = A2.recurrencia_iterar(g, float(x1), N)
    pf = A2.puntos_fijos(g)
    st.markdown("**Puntos fijos** g(L) = L: " + (", ".join(f"L = {sp.sstr(p)} ≈ {num(sp.N(p), 6)} — {t}" for p, d, t in pf) or "no encuentro"))
    dif = np.diff(vals)
    mono = "creciente" if np.all(dif >= -1e-12) else ("decreciente" if np.all(dif <= 1e-12) else "no monótona")
    st.markdown(f"Los términos calculados son **{mono}** y están entre {num(min(vals), 6)} y {num(max(vals), 6)}. "
                f"Último término: x_{len(vals)} ≈ **{num(vals[-1], 12)}**")
    st.caption("Para demostrarlo en el examen: (1) acotada (por inducción), (2) monótona (por inducción), ⇒ converge "
               "(Prop. 5.2.13), y (3) el límite cumple L = g(L).")
    c1, c2 = st.columns(2)
    fig = figura_base("Términos", alto=330)
    fig.add_trace(go.Scatter(x=list(range(1, len(vals) + 1)), y=vals, mode="lines+markers", line=dict(color=ROSA)))
    c1.plotly_chart(fig, width="stretch")
    lo, hi = min(vals + [0]) - 0.5, max(vals) + 0.5
    fig2 = figura_base("Diagrama de telaraña", alto=330)
    trazar(fig2, g, lo, hi, "y = g(x)")
    fig2.add_trace(go.Scatter(x=[lo, hi], y=[lo, hi], mode="lines", line=dict(color=GRIS, dash="dot"), name="y = x"))
    cx, cy = [vals[0]], [0]
    for i in range(min(len(vals) - 1, 40)):
        cx += [vals[i], vals[i + 1]]
        cy += [vals[i + 1], vals[i + 1]]
    fig2.add_trace(go.Scatter(x=cx, y=cy, mode="lines", line=dict(color=LILA, width=1.5), name="iteraciones"))
    c2.plotly_chart(fig2, width="stretch")


def herr_limsup():
    an = entrada_expr("aₙ =", "(-1)^n * n/(n+1)", "ls_a", "Usa n como variable")
    if an is None:
        return
    an = an.subs(x, n_sym)
    r = calcular(A2.lim_sup_inf, an)
    if r is None:
        return
    simb, ls, li, vals = r
    if simb:
        st.latex(rf"a_{{2m}} \to {L(simb['pares'])},\qquad a_{{2m+1}} \to {L(simb['impares'])}")
    st.markdown(f"Numéricamente (cola de la sucesión): **lím sup ≈ {num(ls, 6)}**, **lím inf ≈ {num(li, 6)}**")
    if abs(ls - li) < 1e-3:
        st.success("Coinciden ⇒ la sucesión converge a ese valor.")
    else:
        st.warning("Son distintos ⇒ la sucesión NO converge (tiene subsucesiones con límites distintos).")
    fig = figura_base(alto=330)
    nmax = min(200, len(vals))
    fig.add_trace(go.Scatter(x=list(range(1, nmax + 1)), y=vals[:nmax], mode="markers", marker=dict(color=ROSA, size=6)))
    fig.add_hline(y=ls, line_dash="dash", line_color=LILA, annotation_text="lím sup")
    fig.add_hline(y=li, line_dash="dash", line_color=TURQUESA, annotation_text="lím inf")
    st.plotly_chart(fig, width="stretch")


def herr_stolz():
    c1, c2 = st.columns(2)
    with c1:
        a = entrada_expr("aₙ =", "1 + 1/2 + 1/3", "st_a", "Para sumas acumuladas usa harmonic(n) o Sum")
    with c2:
        b = entrada_expr("bₙ =", "ln(n)", "st_b")
    st.caption("Ejemplos: aₙ = harmonic(n) (=1+1/2+…+1/n), bₙ = ln(n) ⇒ límite 1.")
    if a is None or b is None:
        return
    a, b = a.subs(x, n_sym), b.subs(x, n_sym)
    if a.free_symbols == set():
        a = sp.harmonic(n_sym)
    r = calcular(A2.stolz, a, b)
    if r is None:
        return
    q, Ls, directo = r
    st.latex(rf"\frac{{a_n - a_{{n-1}}}}{{b_n - b_{{n-1}}}} = {L(q)} \ \longrightarrow\ {L(Ls)}")
    st.success(f"Por Stolz, lím aₙ/bₙ = {sp.sstr(Ls)}" + (f" (y directamente sale {sp.sstr(directo)} ✓)" if directo is not None else ""))
    st.caption("Condiciones: bₙ estrictamente monótona y divergente (o aₙ, bₙ → 0 con bₙ estrictamente monótona). "
               "Es el «L'Hôpital de las sucesiones».")


# ======================================================================== TEMA 6
def herr_criterios_series():
    an = entrada_expr("aₙ (términos positivos) =", "factorial(n)/(n^n)", "cs_a", "Usa n como variable")
    if an is None:
        return
    an = an.subs(x, n_sym)
    r = calcular(A2.criterios_extra, an, segundos=25)
    if r is None:
        return
    for nombre, (val, veredicto) in r.items():
        with caja("pasos", nombre):
            st.latex(L(val))
            st.markdown(f"→ **{veredicto}**")
    S = calcular(A.estudiar_serie, an, 1, segundos=25)
    if S:
        for l_ in S.explicacion:
            st.latex(l_)


def herr_sumar_series():
    modo = st.radio("Tipo", ["Sumar directamente", "Telescópica (bₙ − bₙ₊₁)"], horizontal=True, key="ss_m")
    if modo.startswith("Sumar"):
        c1, c2 = st.columns([3, 1])
        with c1:
            an = entrada_expr("aₙ =", "1/(n*(n+1))", "ss_a")
        ini = int(c2.number_input("desde n =", value=1, step=1, key="ss_i"))
        if an is None:
            return
        an = an.subs(x, n_sym)
        r = calcular(A2.suma_serie, an, ini, segundos=20)
        if r is None:
            return
        v, nm = r
        st.latex(rf"\sum_{{n={ini}}}^\infty {L(an)} = " + (L(v) if v is not None else "?") + (rf"\approx {num(nm, 12)}" if nm is not None else ""))
        if v is not None and nm is not None and v.is_finite:
            verificado(abs(float(sp.N(v)) - nm) < 1e-6 * max(1, abs(nm)), "La suma exacta coincide con la numérica ✔")
        st.caption("Geométricas: Σ a₀rⁿ = a₀/(1 − r) si |r| < 1 · Aritmético-geométricas Σ P(n)rⁿ: calcula S − rS · "
                   "Hipergeométricas aₙ₊₁/aₙ = (αn+β)/(αn+γ): convergen ⇔ γ > α + β y suman a₁γ/(γ − α − β).")
    else:
        bn = entrada_expr("bₙ =", "1/n", "ss_b")
        if bn is None:
            return
        bn = bn.subs(x, n_sym)
        an, b1, Lb = A2.telescopica(bn)
        st.latex(rf"a_n = b_n - b_{{n+1}} = {L(an)},\qquad \sum_{{n=1}}^\infty a_n = b_1 - \lim b_n = {L(b1)} - {L(Lb)} = {L(sp.simplify(b1 - Lb))}")


def herr_producto_cauchy():
    c1, c2 = st.columns(2)
    with c1:
        a = entrada_expr("aₙ (desde n = 0)", "1/factorial(n)", "pc_a")
    with c2:
        b = entrada_expr("bₙ (desde n = 0)", "1/factorial(n)", "pc_b")
    if a is None or b is None:
        return
    a, b = a.subs(x, n_sym), b.subs(x, n_sym)
    cn, cerrado, terms = A2.producto_cauchy(a, b, 8)
    st.latex(rf"c_n = \sum_{{k=0}}^n a_k b_{{n-k}}" + (rf" = {L(cerrado)}" if cerrado is not None else ""))
    st.markdown("Primeros términos: " + ", ".join(sp.sstr(t) for t in terms))
    st.caption("Mertens: si una serie converge y la otra converge ABSOLUTAMENTE, Σcₙ converge a (Σaₙ)(Σbₙ). "
               "Ejemplo estrella: eˣ·eʸ = e^{x+y} (con aₙ = 1/n! sale cₙ = 2ⁿ/n!).")


def herr_riemann():
    st.markdown("La serie armónica alternada 1 − 1/2 + 1/3 − 1/4 + … converge a ln 2 ≈ 0,693 **condicionalmente**. "
                "Riemann: reordenando sus términos puedo hacer que sume **lo que yo quiera**.")
    obj = st.slider("Quiero que sume…", -3.0, 3.0, 1.5, 0.1, key="ri_o")
    sumas, usados = A2.reordenar_riemann(obj, 3000)
    st.success(f"Tras 3000 términos reordenados la suma vale {sumas[-1]:.6f} (objetivo {obj}).")
    st.markdown("Primeros términos usados: " + " ".join(f"{'+' if u > 0 else '−'}1/{abs(u)}" for u in usados[:30]) + " …")
    fig = figura_base(alto=330)
    fig.add_trace(go.Scatter(x=list(range(1, 401)), y=sumas[:400], mode="lines", line=dict(color=ROSA)))
    fig.add_hline(y=obj, line_dash="dash", line_color=LILA)
    st.plotly_chart(fig, width="stretch")
    st.caption("Receta: sumo positivos hasta pasarme del objetivo, resto negativos hasta quedarme por debajo, y repito. Como "
               "los términos → 0, cada vez me paso menos. Con series ABSOLUTAMENTE convergentes esto es imposible (Teorema 6.4.6).")


# ======================================================================== TEMA 7
def herr_puntual_uniforme():
    ej = st.selectbox("Ejemplos de los apuntes", ["(escribir la mía)"] + list(A2.EJEMPLOS_FUNCIONES), key="pu_e")
    d = A2.EJEMPLOS_FUNCIONES.get(ej, ("x/(1+n*x^2)", "-2", "2"))
    c1, c2, c3 = st.columns([2, 1, 1])
    fn_t = c1.text_input("fₙ(x) =", d[0], key=f"pu_f_{ej}")
    a_t = c2.text_input("x desde", d[1], key=f"pu_a_{ej}")
    b_t = c3.text_input("x hasta", d[2], key=f"pu_b_{ej}")
    try:
        fn, a, b = leer(fn_t), leer(a_t), leer(b_t)
    except ErrorLectura as exc:
        st.error(str(exc))
        return
    f = A2.limite_puntual(fn)
    af, bf = float(sp.N(a)), float(sp.N(b))
    if f is not None:
        st.latex(rf"f(x) = \lim_{{n\to\infty}} {L(fn)} = {L(f)}")
    else:
        st.info("El límite depende de x de forma no uniforme (p. ej. xⁿ → 0 si |x| < 1 y → 1 si x = 1): lo calculo punto a punto.")
    xs = np.linspace(af, bf, 300)
    if f is not None:
        fvals = A.lambdificar(f)(xs) if f.has(x) else np.full_like(xs, float(sp.N(f)))
    else:
        fvals = A2.evaluar_limite_en_puntos(fn, xs)
    nsel = st.slider("n", 1, 100, 5, key="pu_n")
    fig = figura_base(alto=400)
    for k, col in ((1, "#f3c1d3"), (2, "#eea7c1"), (5, "#e88bb0"), (nsel, ROSA)):
        trazar(fig, fn.subs(n_sym, k), af, bf, f"f_{k}", color=col, ancho=3 if k == nsel else 1.5)
    fig.add_trace(go.Scatter(x=xs, y=fvals, mode="lines", line=dict(color=LILA, width=3, dash="dash"), name="límite f"))
    st.plotly_chart(fig, width="stretch")
    if f is not None or True:
        filas = []
        for k in (1, 2, 5, 10, 20, 50, 100, 200, 500, 1000):
            g = fn.subs(n_sym, k)
            vals = A.lambdificar(g)(np.linspace(af, bf, 3001))
            fv = (A.lambdificar(f)(np.linspace(af, bf, 3001)) if (f is not None and f.has(x)) else
                  (np.full(3001, float(sp.N(f))) if f is not None else A2.evaluar_limite_en_puntos(fn, np.linspace(af, bf, 3001))))
            dd = np.abs(vals - fv)
            filas.append((k, float(np.nanmax(dd))))
        st.dataframe(pd.DataFrame(filas, columns=["n", "Mₙ = sup |fₙ − f| (aprox.)"]).T, width="stretch")
        ult = filas[-1][1]
        if ult < 1e-2 and filas[-1][1] <= filas[-3][1]:
            st.success("Mₙ → 0 ⇒ la convergencia es **uniforme** en el intervalo (Teorema 7.2.4).")
        else:
            st.warning("Mₙ no tiende a 0 ⇒ la convergencia **no es uniforme** (sólo puntual). Siempre hay un x donde fₙ sigue lejos de f.")
    st.caption("Uniforme = toda la gráfica de fₙ cabe en una «manguera» de radio ε alrededor de f a partir de cierto n. "
               "Si f es discontinua y las fₙ son continuas, NO puede ser uniforme (Teorema 7.3.2).")


def herr_criterio_m():
    st.markdown("Criterio M de Weierstrass: si |fₙ(x)| ≤ Mₙ para todo x y ΣMₙ converge, Σfₙ converge **uniformemente**.")
    c1, c2, c3 = st.columns([2, 1, 1])
    fn_t = c1.text_input("fₙ(x) =", "sen(n*x)/n^2", key="cm_f")
    a_t = c2.text_input("x desde", "-pi", key="cm_a")
    b_t = c3.text_input("x hasta", "pi", key="cm_b")
    try:
        fn, a, b = leer(fn_t), leer(a_t), leer(b_t)
    except ErrorLectura as exc:
        st.error(str(exc))
        return
    xs = np.linspace(float(sp.N(a)), float(sp.N(b)), 2001)
    Ms = []
    for k in range(1, 31):
        Ms.append(float(np.nanmax(np.abs(A.lambdificar(fn.subs(n_sym, k))(xs)))))
    st.markdown("Mₙ = sup|fₙ| (numérico) para n = 1…8: " + ", ".join(num(m, 4) for m in Ms[:8]))
    # conjetura de Mn simbólica: probamos 1/n^p
    ratios = [Ms[k] * (k + 1) ** 2 for k in range(len(Ms))]
    Mn_sim = st.text_input("Propón Mₙ (en n)", "1/n^2", key="cm_M")
    try:
        Mn = leer(Mn_sim).subs(x, n_sym)
        ok_cota = all(Ms[k - 1] <= float(sp.N(Mn.subs(n_sym, k))) * (1 + 1e-9) for k in range(1, 31))
        S = A.estudiar_serie(Mn, 1)
        st.markdown(f"¿|fₙ| ≤ Mₙ? {ok_no(ok_cota)} · ¿ΣMₙ converge? {ok_no(S.convergente)}", unsafe_allow_html=True)
        if ok_cota and S.convergente:
            st.success("⇒ Σ fₙ converge **uniformemente** (y si las fₙ son continuas, la suma también lo es).")
    except ErrorLectura as exc:
        st.error(str(exc))


def herr_potencias():
    st.markdown("Serie de potencias **Σ cₙ (x − a)ⁿ**: radio R = 1/lím sup |cₙ|^(1/n) (Cauchy–Hadamard).")
    c1, c2 = st.columns([3, 1])
    with c1:
        cn = entrada_expr("cₙ =", "1/n", "sp_c", "Usa n como variable")
    with c2:
        a = entrada_num("centro a", "0", "sp_a")
    if cn is None or a is None:
        return
    cn = cn.subs(x, n_sym)
    r = calcular(A2.radio_convergencia, cn, a)
    if r is None:
        return
    Rr, raiz, coc = r
    st.latex(rf"\lim |c_n|^{{1/n}} = {L(raiz) if raiz is not None else '?'},\quad \lim\left|\frac{{c_{{n+1}}}}{{c_n}}\right| = "
             rf"{L(coc) if coc is not None else '?'}\ \Rightarrow\ R = {L(Rr) if Rr is not None else '?'}")
    if Rr is None:
        return
    if Rr == sp.oo:
        st.success("R = ∞: converge para TODO x real.")
    elif Rr == 0:
        st.warning("R = 0: sólo converge en x = a.")
    else:
        ext = calcular(A2.extremos_serie_potencias, cn, a, Rr, segundos=25) or []
        st.markdown(f"Converge absolutamente en |x − {sp.sstr(a)}| < {sp.sstr(Rr)}, diverge si |x − {sp.sstr(a)}| > {sp.sstr(Rr)}.")
        for p_, term, conv in ext:
            st.markdown(f"- En x = {sp.sstr(p_)}: serie Σ {sp.sstr(term)} → " + ({True: "**converge**", False: "**diverge**"}.get(conv, "no lo sé")))
        if len(ext) == 2 and None not in (ext[0][2], ext[1][2]):
            izq = "[" if ext[0][2] else "("
            der = "]" if ext[1][2] else ")"
            st.success(f"Intervalo de convergencia: {izq}{sp.sstr(ext[0][0])}, {sp.sstr(ext[1][0])}{der}")


def herr_analiticas():
    c1, c2, c3 = st.columns(3)
    with c1:
        f = entrada_expr("f(x) =", "ln(1+x)", "an_f")
    with c2:
        a = entrada_num("centro", "0", "an_a")
    with c3:
        N = int(st.number_input("términos", value=8, min_value=2, max_value=25, key="an_N"))
    if f is None or a is None:
        return
    k = sp.Symbol("k", integer=True, nonnegative=True)
    T = sp.series(f, x, a, N).removeO()
    st.latex(rf"{L(f)} = {L(T)} + \cdots")
    try:
        gen = sp.fps(f, x, a)
        st.latex(rf"= \sum_{{k}} {L(gen.ak.formula)}\,(x - {L(a)})^k" if a != 0 else rf"= \sum_{{k}} {L(gen.ak.formula)}\,x^k")
    except Exception:  # noqa: BLE001
        pass
    fig = figura_base(alto=380)
    af = float(sp.N(a))
    trazar(fig, f, af - 2, af + 2, "f", ancho=4)
    for m, col in ((2, "#f3c1d3"), (4, "#e88bb0"), (N, LILA)):
        trazar(fig, sp.series(f, x, a, m).removeO(), af - 2, af + 2, f"suma hasta grado {m - 1}", color=col, ancho=2, guion="dash")
    fig.update_yaxes(range=[-4, 4])
    st.plotly_chart(fig, width="stretch")
    st.caption("Dentro del radio de convergencia las sumas parciales se pegan a f; fuera se separan. Cuidado: hay funciones C∞ que "
               "NO son analíticas, como e^(−1/x²) (su serie en 0 es la serie nula).")
