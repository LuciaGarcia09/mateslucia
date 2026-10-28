"""Páginas de Análisis matemático."""
from __future__ import annotations

import math
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import sympy as sp

from core import analisis as A
from core.parsing import x, n as n_sym, leer, ErrorLectura
from ui.comun import (L, entrada_expr, entrada_num, verificado, analogia, ia, figura_base, trazar, punto, num,
                      ROSA, LILA, TURQUESA, AMARILLO, GRIS)


def _rango(clave, a=-6.0, b=6.0):
    c1, c2 = st.columns(2)
    lo = c1.number_input("x mínimo de la gráfica", value=a, key=f"{clave}_lo")
    hi = c2.number_input("x máximo de la gráfica", value=b, key=f"{clave}_hi")
    if hi <= lo:
        st.error("El máximo tiene que ser mayor que el mínimo.")
        return None
    return float(lo), float(hi)


def _lado_tex(lado: str) -> str:
    return lado.replace("∞", r"\infty").replace("−", "-")


def _iv_txt(iv: str) -> str:
    """Intervalo en LaTeX -> texto plano para las tablas."""
    for a, b in ((r"\left", ""), (r"\right", ""), (r"\infty", "∞"), (r"\ ", " ")):
        iv = iv.replace(a, b)
    return iv.replace("\\", "")


def _tabla_signos(cab_signo, cab_res, filas):
    cuerpo = r" \\ ".join(rf"{iv} & {'+' if pos else '-'} & {res}" for iv, pos, res in filas)
    return (r"\begin{array}{c|c|l} \text{intervalo} & " + cab_signo + " & " + cab_res + r" \\ \hline "
            + cuerpo + r" \end{array}")


def _intervalo_tex(S):
    try:
        return L(S)
    except Exception:  # noqa: BLE001
        return sp.sstr(S)


# =================================================================== ESTUDIO COMPLETO
def pagina_estudio():
    analogia("estudiar una función es hacer la <b>ficha técnica de una montaña rusa</b>: dónde existe la vía (dominio), "
             "dónde cruza el suelo (cortes), dónde sube y baja (monotonía), las cimas y valles (extremos), si se curva "
             "como una sonrisa o como un ceño (curvatura) y hacia dónde se va a lo lejos (asíntotas).")
    f = entrada_expr("f(x) =", "(x^2-1)/(x-2)", "est_f")
    if f is None:
        return
    if not f.has(x):
        st.info("Es una función constante: dominio ℝ, sin extremos estrictos, derivada 0.")
        return
    with st.spinner("Estudiando la función…"):
        try:
            E = A.estudio_funcion(f)
        except Exception as exc:  # noqa: BLE001
            st.error(f"No he podido completar el estudio: {exc}")
            return
    for av in E.avisos:
        st.warning(av)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**1. Dominio**")
        st.latex(r"D(f) = " + (_intervalo_tex(E.dominio) if E.dominio is not None else r"\text{?}"))
        st.markdown("**2. Cortes con los ejes**")
        st.latex(r"\text{OY: } " + (rf"(0,\ {L(E.corte_y)})" if E.corte_y is not None else r"\text{no corta (0} \notin D)"))
        st.latex(r"\text{OX: } f(x)=0 \iff x \in " + (_intervalo_tex(E.cortes_x) if E.cortes_x is not None else r"\text{?}"))
        st.markdown(f"**3. Simetría:** {E.paridad}")
    with c2:
        st.markdown("**4. Asíntotas**")
        if E.asintotas_v:
            for c, li, ld in E.asintotas_v:
                st.latex(rf"\text{{Vertical }} x = {L(c)}:\ \lim_{{x\to {L(c)}^-}} f = {L(li) if li is not None else '?'},\ "
                         rf"\lim_{{x\to {L(c)}^+}} f = {L(ld) if ld is not None else '?'}")
        else:
            st.write("Verticales: ninguna.")
        for lado, val in E.asintota_h.items():
            st.latex(rf"\text{{Horizontal en }} {_lado_tex(lado)}:\ y = {L(val)}")
        for lado, rect in E.asintota_o.items():
            st.latex(rf"\text{{Oblicua en }} {_lado_tex(lado)}:\ y = {L(rect)}")
        if not E.asintota_h and not E.asintota_o:
            st.write("Horizontales/oblicuas: ninguna.")
    st.markdown("**5. Monotonía y extremos**")
    st.latex(r"f'(x) = " + L(E.df))
    if E.criticos:
        st.latex(r"f'(x) = 0 \iff x \in \left\{" + r",\ ".join(L(c) for c in E.criticos) + r"\right\}")
    if E.monotonia:
        st.latex(_tabla_signos("f'(x)", "f(x)", [(iv, m.startswith("crec"),
                                                    r"\nearrow\ \text{crece}" if m.startswith("crec") else r"\searrow\ \text{decrece}")
                                                   for iv, m in E.monotonia]))
    for c, yv, tipo in E.extremos:
        st.latex(rf"\text{{{tipo}}}\ \text{{en}}\ \left({L(c)},\ {L(yv)}\right)" +
                 (rf"\approx ({num(sp.N(c), 5)},\ {num(sp.N(yv), 5)})" if not (c.is_Rational and yv.is_Rational) else ""))
    if not E.extremos:
        st.write("No hay extremos relativos.")
    st.markdown("**6. Curvatura e inflexión**")
    st.latex(r"f''(x) = " + L(E.d2f))
    if E.curvatura:
        st.latex(_tabla_signos("f''(x)", r"\text{forma}", [(iv, c.startswith("convexa"),
                                                              r"\cup\ \text{convexa}" if c.startswith("convexa") else r"\cap\ \text{cóncava}")
                                                             for iv, c in E.curvatura]))
    for c, yv in E.inflexion:
        st.latex(rf"\text{{Punto de inflexión en}}\ \left({L(c)},\ {L(yv)}\right)")
    st.caption("Convenio: convexa ∪ (f'' > 0, «sonrisa»), cóncava ∩ (f'' < 0). Algunos libros lo dicen al revés: "
               "mira cuál usa tu profesor.")
    verificado(A.comprobar_derivada(f, E.df), "La derivada se ha comprobado numéricamente en varios puntos ✔")
    st.markdown("**7. Gráfica**")
    rg = _rango("est")
    if rg:
        fig = figura_base()
        trazar(fig, f, *rg, "f(x)")
        for c, *_ in E.asintotas_v:
            cf = A.a_float(c)
            if cf is not None and rg[0] < cf < rg[1]:
                fig.add_vline(x=cf, line_dash="dash", line_color=GRIS)
        for lado, val in E.asintota_h.items():
            fig.add_hline(y=float(sp.N(val)), line_dash="dot", line_color=GRIS)
        for lado, rect in list(E.asintota_o.items())[:1]:
            trazar(fig, rect, *rg, f"y = {sp.sstr(rect)}", color=GRIS, ancho=1.5, guion="dash")
        for c, yv, tipo in E.extremos:
            cf, yf = A.a_float(c), A.a_float(yv)
            if cf is not None and yf is not None and rg[0] <= cf <= rg[1]:
                punto(fig, cf, yf, "máx" if "máx" in tipo else "mín", color=LILA)
        for c, yv in E.inflexion:
            cf, yf = A.a_float(c), A.a_float(yv)
            if cf is not None and yf is not None and rg[0] <= cf <= rg[1]:
                punto(fig, cf, yf, "inflexión", color=TURQUESA, simbolo="diamond")
        if st.checkbox("Dibujar también f' y f''", key="est_der"):
            trazar(fig, E.df, *rg, "f'(x)", color=LILA, ancho=1.5, guion="dot")
            trazar(fig, E.d2f, *rg, "f''(x)", color=TURQUESA, ancho=1.5, guion="dot")
        st.plotly_chart(fig, width="stretch")
    ia("buscar dónde f' = 0 es exactamente lo que hace el <b>entrenamiento de una red neuronal</b>: minimizar una "
       "función de error. Pruébalo en «Rincón Datos e IA → descenso de gradiente».")


# =================================================================== LÍMITES
def pagina_limites():
    analogia("un límite es <b>hacia dónde apunta la flecha</b> aunque nunca llegue a clavarse: no importa lo que "
             "valga f justo en el punto (incluso puede no existir), sólo a qué valor se acerca cuando x se acerca.")
    f = entrada_expr("f(x) =", "sen(x)/x", "lim_f")
    c1, c2 = st.columns(2)
    with c1:
        a = entrada_num("x tiende a", "0", "lim_a")
    with c2:
        lado = st.radio("Por", ["ambos lados", "la derecha (x→a⁺)", "la izquierda (x→a⁻)"], horizontal=True, key="lim_l")
    if f is None or a is None:
        return
    lado_k = {"ambos lados": "+-", "la derecha (x→a⁺)": "+", "la izquierda (x→a⁻)": "-"}[lado]
    try:
        with st.spinner("Calculando…"):
            Li = A.limite(f, a, lado_k)
    except Exception as exc:  # noqa: BLE001
        st.error(f"No he podido calcularlo: {exc}")
        return
    sup = {"+": "^+", "-": "^-", "+-": ""}[lado_k] if a not in (sp.oo, -sp.oo) else ""
    a_tex = L(a).replace(r"\infty", r"+\infty") if a == sp.oo else L(a)
    if Li.valor is sp.nan and Li.laterales:
        st.latex(rf"\lim_{{x\to {a_tex}^-}} {L(f)} = {L(Li.laterales[0])} \neq {L(Li.laterales[1])} = "
                 rf"\lim_{{x\to {a_tex}^+}} {L(f)}")
        st.error("Los límites laterales son distintos ⇒ **el límite no existe**.")
    else:
        st.latex(rf"\lim_{{x\to {a_tex}{sup}}} {L(f)} = {L(Li.valor)}")
        if isinstance(Li.valor, sp.AccumBounds):
            st.warning("El resultado es un intervalo: la función oscila sin acercarse a un único valor ⇒ el límite no existe.")
        verificado(Li.coincide_numerico, "Comprobado con una tabla de valores cada vez más cerca ✔",
                   "La tabla numérica no se acerca claramente al valor simbólico: revisa (puede ser un caso con "
                   "oscilaciones o errores de redondeo).")
    with st.expander("📋 Tabla de valores (la idea intuitiva del límite)", expanded=True):
        st.dataframe(pd.DataFrame([{"x": num(xv, 10), "f(x)": num(yv, 12) if yv is not None else "no definida"}
                                   for xv, yv in Li.tabla]), hide_index=True, width="stretch")
    if a not in (sp.oo, -sp.oo):
        try:
            fa = f.subs(x, a)
            if fa.is_finite and fa.is_real:
                cont = Li.valor is not sp.nan and sp.simplify(Li.valor - fa) == 0
                st.markdown(f"f({sp.sstr(a)}) = {sp.sstr(sp.simplify(fa))} ⇒ "
                            + ("**f es continua en ese punto** (límite = valor)." if cont and lado_k == "+-" else
                               "**f no es continua** en ese punto." if lado_k == "+-" else ""))
            else:
                st.markdown(f"f no está definida en x = {sp.sstr(a)}" +
                            (" pero el límite existe y es finito ⇒ **discontinuidad evitable**."
                             if Li.valor is not sp.nan and Li.valor.is_finite else "."))
        except Exception:  # noqa: BLE001
            pass
    with st.expander("🧠 Chuleta de indeterminaciones y equivalencias"):
        st.markdown(r"""
| Indeterminación | Qué hacer |
|---|---|
| $\frac{0}{0}$ | Factorizar y simplificar, conjugado, equivalencias, L'Hôpital |
| $\frac{\infty}{\infty}$ | Dividir por la mayor potencia, jerarquía: $\ln x \ll x^a \ll e^x \ll x!$ |
| $\infty - \infty$ | Común denominador o conjugado |
| $0\cdot\infty$ | Pasar a cociente |
| $1^\infty$ | $\lim f^g = e^{\lim g\,(f-1)}$ |
| $0^0,\ \infty^0$ | Tomar logaritmos |

Equivalencias cuando $t\to 0$: $\operatorname{sen} t \sim t$, $\operatorname{tg} t \sim t$, $1-\cos t\sim \tfrac{t^2}{2}$,
$e^t-1\sim t$, $\ln(1+t)\sim t$, $(1+t)^a - 1 \sim a t$, $\arcsin t \sim t$, $\operatorname{arctg} t\sim t$.
""")


# =================================================================== DERIVADAS
def pagina_derivadas():
    analogia("la derivada es el <b>velocímetro</b> de la función: no te dice dónde estás, sino lo rápido que cambias "
             "en ese instante. La recta tangente es «seguir recto» con esa velocidad.")
    f = entrada_expr("f(x) =", "ln(x^2+1)*e^(3x)", "der_f")
    if f is None:
        return
    orden = st.slider("Orden de la derivada", 1, 6, 1, key="der_o")
    d = f
    for _ in range(orden):
        d = sp.diff(d, x)
    d_s = A.mas_simple(d)
    marcas = "'" * orden if orden <= 3 else f"^{{({orden})}}"
    st.latex(rf"f{marcas}(x) = {L(d_s)}")
    if sp.factor(d_s) != d_s and len(str(sp.factor(d_s))) < len(str(d_s)) * 1.3:
        st.latex(r"\phantom{f'(x)} = " + L(sp.factor(d_s)))
    if orden == 1:
        verificado(A.comprobar_derivada(f, d_s), "Comprobado contra la derivada numérica en 6 puntos al azar ✔")
        with st.expander("🪜 ¿Qué regla se aplica? (desglose)", expanded=True):
            for l_ in A.explicar_derivada(f):
                st.latex(l_)
    st.subheader("Recta tangente")
    a = entrada_num("en x₀ =", "0", "der_a")
    if a is not None:
        try:
            fa, m, rect = A.recta_tangente(f, a)
            st.latex(rf"y - f(x_0) = f'(x_0)(x - x_0) \Rightarrow y - {L(fa)} = {L(m)}\,(x - {L(a)}) \Rightarrow y = {L(rect)}")
            rg = _rango("der")
            if rg:
                fig = figura_base()
                trazar(fig, f, *rg, "f(x)")
                trazar(fig, rect, *rg, "tangente", color=LILA, ancho=2, guion="dash")
                fa_f = A.a_float(fa)
                if fa_f is not None:
                    punto(fig, A.a_float(a), fa_f, "x₀")
                st.plotly_chart(fig, width="stretch")
        except Exception as exc:  # noqa: BLE001
            st.warning(f"No hay recta tangente ahí. {exc}")
    with st.expander("📐 Tabla de derivadas"):
        st.markdown(r"""
| $f$ | $f'$ | $f$ | $f'$ |
|---|---|---|---|
| $x^r$ | $r x^{r-1}$ | $\operatorname{sen} u$ | $u'\cos u$ |
| $e^u$ | $u' e^u$ | $\cos u$ | $-u'\operatorname{sen} u$ |
| $a^u$ | $u' a^u \ln a$ | $\operatorname{tg} u$ | $u'(1+\operatorname{tg}^2 u)$ |
| $\ln u$ | $u'/u$ | $\arcsin u$ | $u'/\sqrt{1-u^2}$ |
| $\log_a u$ | $u'/(u\ln a)$ | $\operatorname{arctg} u$ | $u'/(1+u^2)$ |
| $u\cdot v$ | $u'v+uv'$ | $u/v$ | $(u'v-uv')/v^2$ |
""")


# =================================================================== INTEGRALES
def pagina_integrales():
    analogia("integrar es <b>sumar trocitos</b>: el área bajo la curva es como medir un terreno cortándolo en tiras "
             "finísimas y sumando sus áreas. La primitiva es la «máquina del tiempo» que deshace la derivada.")
    f = entrada_expr("f(x) =", "x*e^x", "int_f")
    if f is None:
        return
    tipo = st.radio("Tipo", ["Indefinida (primitiva)", "Definida / impropia"], horizontal=True, key="int_t")
    if tipo.startswith("Indef"):
        with st.spinner("Integrando…"):
            I = A.integral(f)
        if I.primitiva.has(sp.Integral):
            st.warning("No tiene primitiva elemental (o SymPy no la encuentra). Ejemplos famosos: e^(−x²), sen(x)/x.")
        else:
            st.latex(rf"\int {L(f)}\,dx = {L(I.primitiva)} + C")
            verificado(I.comprobacion, "Comprobado: al derivar la primitiva sale exactamente f ✔")
        with st.expander("🧰 ¿Qué método usar?"):
            st.markdown(r"""
- **Inmediata / casi inmediata**: busca la forma $\int u'\,g(u)\,dx$ (p. ej. $\frac{u'}{u}\to\ln|u|$).
- **Por partes** $\int u\,dv = uv - \int v\,du$: producto de tipos distintos. Regla **ALPES** para elegir $u$:
  Arcos, Logaritmos, Polinomios, Exponenciales, Senos/cosenos (el primero que aparezca es $u$).
- **Racionales** $\frac{P}{Q}$: si gr P ≥ gr Q, divide primero; luego fracciones simples según las raíces de Q.
- **Cambio de variable**: cuando ves una función y su derivada (o raíces molestas).
""")
    else:
        c1, c2 = st.columns(2)
        with c1:
            a = entrada_num("desde a =", "0", "int_a")
        with c2:
            b = entrada_num("hasta b =", "1", "int_b")
        if a is None or b is None:
            return
        with st.spinner("Integrando…"):
            I = A.integral(f, a, b)
        imp = a in (sp.oo, -sp.oo) or b in (sp.oo, -sp.oo)
        if not I.primitiva.has(sp.Integral):
            st.latex(rf"F(x) = {L(I.primitiva)}")
        if I.definida.has(sp.Integral):
            st.warning("No hay forma cerrada. Valor numérico: " + (num(I.numerica, 12) if I.numerica is not None else "?"))
        else:
            st.latex(rf"\int_{{{L(a)}}}^{{{L(b)}}} {L(f)}\,dx = {L(I.definida)}" +
                     (rf"\approx {num(sp.N(I.definida), 10)}" if I.definida.is_finite and not I.definida.is_Integer else ""))
            if I.definida in (sp.oo, -sp.oo) or I.definida is sp.nan:
                st.info("La integral impropia **diverge**." if imp else "La integral no es finita.")
            elif imp:
                st.info("Impropia **convergente**: el área infinita «se acaba» porque la función decae rápido.")
            verificado(I.coincide, f"Coincide con la integración numérica independiente ({num(I.numerica, 10)}) ✔"
                       if I.numerica is not None else "")
        rg = _rango("int", float(sp.N(a)) - 1 if a.is_finite else -6, float(sp.N(b)) + 1 if b.is_finite else 6)
        if rg:
            fig = figura_base()
            xs, ys = trazar(fig, f, *rg, "f(x)")
            lo = max(rg[0], float(sp.N(a)) if a.is_finite else rg[0])
            hi = min(rg[1], float(sp.N(b)) if b.is_finite else rg[1])
            mask = (xs >= lo) & (xs <= hi)
            fig.add_trace(go.Scatter(x=np.concatenate([[lo], xs[mask], [hi]]),
                                     y=np.concatenate([[0], np.nan_to_num(ys[mask]), [0]]),
                                     fill="toself", fillcolor="rgba(231,84,128,0.25)", line=dict(width=0), name="área con signo"))
            st.plotly_chart(fig, width="stretch")
            st.caption("Ojo: la integral definida da área CON SIGNO (lo que queda bajo el eje cuenta negativo). "
                       "Para el área geométrica integra |f|.")
        with st.expander("🍰 Sumas de Riemann (de dónde sale la integral)"):
            if a.is_finite and b.is_finite:
                N = st.slider("Número de rectángulos", 2, 200, 10, key="riem")
                af, bf = float(sp.N(a)), float(sp.N(b))
                h = (bf - af) / N
                xm = np.linspace(af + h / 2, bf - h / 2, N)
                ym = A.lambdificar(f)(xm)
                st.write(f"Suma con punto medio: **{num(np.nansum(ym) * h, 10)}**"
                         + (f"  ·  valor exacto ≈ {num(sp.N(I.definida), 10)}" if not I.definida.has(sp.Integral) else ""))
                fig = figura_base(alto=320)
                fig.add_trace(go.Bar(x=xm, y=ym, width=h * 0.98, marker_color="rgba(155,107,214,0.45)", name="rectángulos"))
                trazar(fig, f, af, bf, "f(x)")
                st.plotly_chart(fig, width="stretch")
            else:
                st.write("Sólo para intervalos finitos.")


# =================================================================== TAYLOR
def pagina_taylor():
    analogia("Taylor es <b>imitar a una función con polinomios</b>, como un imitador que primero copia la posición "
             "(f(a)), luego la velocidad (f'(a)), luego la aceleración (f''(a))… Cuantos más detalles copia, más "
             "tiempo dura la imitación lejos del punto.")
    f = entrada_expr("f(x) =", "sen(x)", "tay_f")
    c1, c2 = st.columns(2)
    with c1:
        a = entrada_num("centro a =", "0", "tay_a")
    with c2:
        orden = st.slider("orden n", 0, 15, 5, key="tay_n")
    if f is None or a is None:
        return
    try:
        T, coefs, ok = A.taylor(f, a, orden)
    except Exception as exc:  # noqa: BLE001
        st.error(f"No se puede desarrollar en ese punto: {exc}")
        return
    st.latex(rf"T_{{{orden}}}(x) = \sum_{{k=0}}^{{{orden}}} \frac{{f^{{(k)}}({L(a)})}}{{k!}}(x-{L(a)})^k = {L(T)}")
    verificado(ok, "Comprobado: cada coeficiente es exactamente f⁽ᵏ⁾(a)/k! ✔")
    with st.expander("Coeficientes uno a uno"):
        st.dataframe(pd.DataFrame([{"k": k_, "f⁽ᵏ⁾(a)/k!": sp.sstr(c)} for k_, c in enumerate(coefs)]), hide_index=True)
    x0 = entrada_num("Evaluar en x =", "1", "tay_x0")
    if x0 is not None:
        try:
            ve, va = float(sp.N(f.subs(x, x0))), float(sp.N(T.subs(x, x0)))
            st.write(f"f({sp.sstr(x0)}) = {num(ve, 12)} · T({sp.sstr(x0)}) = {num(va, 12)} · error = {abs(ve - va):.3e}")
        except (TypeError, ValueError):
            st.write("No se puede evaluar ahí.")
    rg = _rango("tay", float(sp.N(a)) - 4, float(sp.N(a)) + 4)
    if rg:
        fig = figura_base()
        trazar(fig, f, *rg, "f(x)", ancho=4)
        colores = [LILA, TURQUESA, AMARILLO, GRIS]
        if st.checkbox("Ver varios órdenes a la vez", True, key="tay_varios"):
            for i, o in enumerate(sorted(set([1, 3, orden]))):
                if o <= orden:
                    To, _, _ = A.taylor(f, a, o)
                    trazar(fig, To, *rg, f"T{o}", color=colores[i % 4], ancho=2, guion="dash",
                           recorte=None)
        else:
            trazar(fig, T, *rg, f"T{orden}", color=LILA, ancho=2, guion="dash")
        fig.update_yaxes(range=[-5, 5] if "sin" in str(f) or "cos" in str(f) else None)
        st.plotly_chart(fig, width="stretch")
    ia("así calculan las calculadoras y los ordenadores e^x, sen x o ln x: con polinomios. Y la <b>aproximación "
       "de orden 2</b> (con la segunda derivada) es la idea del método de Newton para optimizar en machine learning.")


# =================================================================== SERIES
def herr_sucesiones():
    an = entrada_expr("aₙ =", "(1+1/n)^n", "suc_a", "Usa n como variable")
    if an is not None:
        an = an.subs(x, n_sym)
        try:
            lim = A.limite_sucesion(an)
            if lim is None:
                raise ValueError("No he podido calcular este límite.")
            if lim is sp.nan:
                st.error("Las subsucesiones par e impar van a sitios distintos ⇒ el límite no existe.")
            st.latex(rf"\lim_{{n\to\infty}} {L(an)} = {L(lim)}")
            vals = [(i, A.evaluar(an.subs(n_sym, x), i)) for i in [1, 2, 5, 10, 100, 1000, 10 ** 4, 10 ** 6]]
            st.dataframe(pd.DataFrame([{"n": i, "aₙ": num(v, 12) if v is not None else "—"} for i, v in vals]).T.astype(str),
                         width="stretch")
            ok = A._compara(lim, [vals[-1][1], vals[-2][1]])
            verificado(ok, "Los valores numéricos se acercan al límite ✔",
                       "Los valores numéricos no se ven claramente cerca del límite (puede converger muy lento).")
            fig = figura_base("Primeros 60 términos")
            ys = [A.evaluar(an.subs(n_sym, x), i) for i in range(1, 61)]
            fig.add_trace(go.Scatter(x=list(range(1, 61)), y=ys, mode="markers", marker=dict(color=ROSA)))
            if lim is not sp.nan and lim.is_finite:
                fig.add_hline(y=float(sp.N(lim)), line_dash="dash", line_color=GRIS)
            st.plotly_chart(fig, width="stretch")
        except Exception as exc:  # noqa: BLE001
            st.error(str(exc))



def herr_series():
    an = entrada_expr("Término general aₙ =", "1/n^2", "ser_a", "Usa n como variable; p.ej. 1/n^2, 2^n/factorial(n), (-1)^n/n")
    ini = st.number_input("n empieza en", value=1, step=1, key="ser_i")
    if an is not None:
        an = an.subs(x, n_sym)
        with st.spinner("Estudiando la serie…"):
            try:
                S = A.estudiar_serie(an, int(ini))
            except Exception as exc:  # noqa: BLE001
                st.error(str(exc))
                return
        for l_ in S.explicacion:
            st.latex(l_)
        if S.convergente is True:
            st.success("La serie **CONVERGE**." + (f"  Suma = ${L(S.suma)}$ ≈ {num(sp.N(S.suma), 10)}" if S.suma is not None else ""))
        elif S.convergente is False:
            st.error("La serie **DIVERGE**.")
        else:
            st.info("No he podido decidir automáticamente. Prueba comparación con 1/n^p, condensación o Leibniz (alternadas).")
        if S.parciales:
            fig = figura_base("Sumas parciales Sₙ")
            fig.add_trace(go.Scatter(x=[p[0] for p in S.parciales], y=[p[1] for p in S.parciales], mode="lines",
                                     line=dict(color=ROSA)))
            if S.suma is not None and S.suma.is_finite:
                fig.add_hline(y=float(sp.N(S.suma)), line_dash="dash", line_color=GRIS, annotation_text="suma")
            st.plotly_chart(fig, width="stretch")
            if S.suma is not None and S.suma.is_finite and len(S.parciales) > 150:
                verificado(abs(S.parciales[-1][1] - float(sp.N(S.suma))) < 0.05 * max(1, abs(float(sp.N(S.suma)))),
                           "Las sumas parciales se acercan al valor de la suma ✔",
                           "Las sumas parciales aún están lejos (convergencia lenta).")
        with st.expander("📋 Criterios"):
            st.markdown(r"""
1. **Condición necesaria**: si $a_n \not\to 0$, diverge. (Si $\to 0$, no dice nada: $\sum 1/n$ diverge.)
2. **Serie geométrica** $\sum r^n$: converge ⇔ $|r|<1$, suma $\frac{\text{primer término}}{1-r}$.
3. **p-series** $\sum 1/n^p$: converge ⇔ $p > 1$.
4. **Cociente (D'Alembert)** y **raíz (Cauchy)**: $L<1$ converge, $L>1$ diverge, $L=1$ no decide.
5. **Comparación** (directa o por paso al límite) con una serie conocida.
6. **Leibniz** (alternadas): $|a_n|$ decreciente y $\to 0$ ⇒ converge.
""")


# =================================================================== INECUACIONES Y COMPLEJOS
def herr_inecuaciones():
    analogia("|x − a| < r es la <b>distancia</b> de x a a menor que r: todos los puntos a menos de r pasos de a.")
    txt = st.text_input("Inecuación", "|x-1| < 3", key="ineq", help="Usa <, >, <=, >=; p. ej. (x-1)/(x+2) >= 0")
    try:
        rel = leer(txt)
        if not isinstance(rel, sp.core.relational.Relational):
            st.error("Escribe una desigualdad (con <, >, <= o >=).")
        else:
            S = A.inecuacion(rel)
            st.latex(L(rel) + r"\iff x \in " + _intervalo_tex(S))
            pruebas = np.linspace(-20, 20, 4001)
            malos = 0
            for t in pruebas:
                try:
                    v = rel.subs(x, sp.Float(t))
                    dentro = bool(S.contains(sp.Float(t)))
                    if v in (sp.true, sp.false) and bool(v) != dentro:
                        malos += 1
                except Exception:  # noqa: BLE001
                    pass
            verificado(malos == 0, "Comprobado en 4001 puntos de [−20, 20] ✔")
    except ErrorLectura as exc:
        st.error(str(exc))



def herr_complejos_basico():
    analogia("un complejo es una <b>flecha en el plano</b>: forma binómica = «cuánto a la derecha y cuánto arriba»; "
             "forma polar = «cuánto mide y hacia dónde apunta». Multiplicar = multiplicar longitudes y SUMAR ángulos.")
    txt = st.text_input("z =", "1 + I*sqrt(3)", key="cz", help="Usa I para la unidad imaginaria")
    try:
        z = sp.sympify(leer(txt.replace("i", "I") if "I" not in txt else txt))
        re_, im_, mod, arg = A.complejo_formas(z)
        st.latex(rf"z = {L(re_)} + {L(im_)}\,i \quad |z| = {L(mod)} \quad \arg z = {L(arg) if arg is not None else '—'}")
        if arg is not None:
            st.latex(rf"z = {L(mod)}_{{{L(arg)}}} = {L(mod)}\left(\cos {L(arg)} + i\,\operatorname{{sen}} {L(arg)}\right) = "
                     rf"{L(mod)}\,e^{{i {L(arg)}}}")
        nr = st.number_input("Raíces n-ésimas: n =", value=3, min_value=1, max_value=12, key="cz_n")
        rr = A.raices_n(z, int(nr))
        fig = figura_base(alto=380)
        fig.update_yaxes(scaleanchor="x")
        puntos_r = []
        for kk, item in enumerate(rr):
            if isinstance(item, tuple):
                r_, ang = item
                w = sp.N(r_ * sp.exp(sp.I * ang))
                st.latex(rf"w_{kk} = {L(r_)}_{{{L(ang)}}} \approx {num(sp.re(w), 6)} {'+' if sp.im(w) >= 0 else '-'} {num(abs(sp.im(w)), 6)}\,i")
                puntos_r.append(complex(w))
        ok = all(abs(w ** int(nr) - complex(sp.N(z))) < 1e-8 * max(1, abs(complex(sp.N(z)))) for w in puntos_r)
        verificado(ok, f"Comprobado: cada raíz elevada a {int(nr)} da z ✔")
        th = np.linspace(0, 2 * np.pi, 300)
        if puntos_r:
            rad = abs(puntos_r[0])
            fig.add_trace(go.Scatter(x=rad * np.cos(th), y=rad * np.sin(th), mode="lines", line=dict(color=GRIS, dash="dot"),
                                     name="circunferencia"))
            fig.add_trace(go.Scatter(x=[w.real for w in puntos_r], y=[w.imag for w in puntos_r], mode="markers",
                                     marker=dict(size=11, color=LILA), name="raíces"))
        zc = complex(sp.N(z))
        fig.add_trace(go.Scatter(x=[0, zc.real], y=[0, zc.imag], mode="lines+markers", line=dict(color=ROSA, width=3), name="z"))
        st.plotly_chart(fig, width="stretch")
        st.caption("Las n raíces forman un polígono regular: mismo módulo ⁿ√|z| y ángulos separados 2π/n.")
    except Exception as exc:  # noqa: BLE001
        st.error(f"No lo entiendo: {exc}")


# =================================================================== NUMÉRICOS
def pagina_numericos():
    analogia("<b>bisección</b> es el juego de «adivina el número»: «¿mayor o menor?» y partes el intervalo a la mitad "
             "cada vez. <b>Newton</b> es más listo: usa la tangente como un tobogán que te deja directamente cerca de "
             "la raíz (pero si la pendiente es casi plana, te lanza lejísimos).")
    f = entrada_expr("f(x) =", "x^3 - x - 2", "num_f")
    if f is None:
        return
    t1, t2 = st.tabs(["Bisección", "Newton–Raphson"])
    with t1:
        c1, c2, c3 = st.columns(3)
        a = c1.number_input("a", value=1.0, key="bis_a")
        b = c2.number_input("b", value=2.0, key="bis_b")
        tol = c3.select_slider("tolerancia", [1e-2, 1e-4, 1e-6, 1e-8, 1e-10], value=1e-6, key="bis_t")
        try:
            filas = A.biseccion(f, a, b, tol)
            st.success(f"f({a}) y f({b}) tienen signos opuestos ⇒ por **Bolzano** hay al menos una raíz en ({a}, {b}).")
            st.dataframe(pd.DataFrame(filas, columns=["it", "a", "b", "c = (a+b)/2", "f(c)", "error ≤"]), hide_index=True,
                         width="stretch")
            st.markdown(f"Raíz ≈ **{num(filas[-1][3], 12)}** tras {len(filas)} iteraciones "
                        f"(cada una divide el error entre 2: hacen falta ⌈log₂((b−a)/tol)⌉ = "
                        f"{math.ceil(math.log2((b - a) / tol))}).")
        except ValueError as exc:
            st.error(str(exc))
    with t2:
        c1, c2 = st.columns(2)
        x0 = c1.number_input("x₀", value=1.0, key="new_x0")
        st.latex(r"x_{k+1} = x_k - \frac{f(x_k)}{f'(x_k)},\qquad f'(x) = " + L(sp.diff(f, x)))
        try:
            filas = A.newton(f, x0)
            st.dataframe(pd.DataFrame(filas, columns=["it", "xₖ", "f(xₖ)", "f'(xₖ)", "xₖ₊₁", "|xₖ₊₁ − xₖ|"]),
                         hide_index=True, width="stretch")
            raiz = filas[-1][4]
            fr = A.evaluar(f, raiz)
            st.markdown(f"Raíz ≈ **{num(raiz, 15)}**  (f = {fr:.2e})")
            verificado(fr is not None and abs(fr) < 1e-8, "Comprobado: f(raíz) ≈ 0 ✔",
                       "No ha convergido: prueba otro x₀ (más cerca de la raíz).")
            st.caption("Fíjate en la última columna: cerca de la raíz el número de cifras correctas se DUPLICA en cada paso "
                       "(convergencia cuadrática). Bisección sólo gana un bit por paso.")
            fig = figura_base()
            xs_it = [r[1] for r in filas] + [raiz]
            lo, hi = min(xs_it) - 1, max(xs_it) + 1
            trazar(fig, f, lo, hi, "f(x)")
            for r in filas[:6]:
                xk, fx, dfx, xn = r[1], r[2], r[3], r[4]
                fig.add_trace(go.Scatter(x=[xk, xn], y=[fx, 0], mode="lines+markers", line=dict(color=LILA, dash="dot"),
                                         showlegend=False))
            st.plotly_chart(fig, width="stretch")
        except ValueError as exc:
            st.error(str(exc))
