"""Rincón Datos e IA: dónde se usa lo que estudias en primero."""
from __future__ import annotations

from math import comb, gcd, prod
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import sympy as sp

from core import analisis as A
from core import enteros as E
from core.parsing import x
from ui.estilo import cabecera
from ui.comun import (L, entrada_expr, verificado, analogia, figura_base, trazar, num, ROSA, LILA, TURQUESA, GRIS)


def pagina_ia():
    cabecera("🤖", "Rincón Datos e IA", "Lo que estudias en Análisis y Matemática finita, funcionando dentro de la IA de verdad.",
             etiqueta="Practicar", chips=["descenso de gradiente", "RSA", "hash y cumpleaños", "activaciones"])
    t1, t2, t3, t4 = st.tabs(["⛰️ Descenso de gradiente", "🔐 RSA de juguete", "🎂 Colisiones y cumpleaños",
                              "🧠 Funciones de activación"])

    # ------------------------------------------------------------ gradiente
    with t1:
        analogia("estás en una montaña con niebla y quieres bajar al valle: no ves el mapa, sólo notas la "
                 "<b>pendiente bajo tus pies</b> (la derivada). Das un paso cuesta abajo, vuelves a mirar, otro paso… "
                 "El tamaño del paso es la <b>tasa de aprendizaje</b>. Así se entrenan TODAS las redes neuronales.")
        f = entrada_expr("Función de error f(x) =", "x^4 - 3x^2 + x", "gd_f")
        c1, c2, c3 = st.columns(3)
        x0 = c1.number_input("Punto de partida x₀", value=2.0, key="gd_x0")
        lr = c2.select_slider("Tasa de aprendizaje η", [0.001, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.3, 0.5], value=0.05, key="gd_lr")
        pasos = c3.slider("Pasos", 1, 200, 40, key="gd_n")
        if f is not None:
            st.latex(r"x_{k+1} = x_k - \eta\, f'(x_k),\qquad f'(x) = " + L(sp.diff(f, x)))
            df = sp.lambdify(x, sp.diff(f, x), "numpy")
            fn = sp.lambdify(x, f, "numpy")
            xs = [x0]
            diverge = False
            for _ in range(pasos):
                with np.errstate(all="ignore"):
                    nuevo = xs[-1] - lr * float(df(xs[-1]))
                if not np.isfinite(nuevo) or abs(nuevo) > 1e6:
                    diverge = True
                    break
                xs.append(nuevo)
            ys = [float(fn(v)) for v in xs]
            if diverge:
                st.error("💥 ¡Ha divergido! La tasa de aprendizaje es demasiado grande: cada paso se pasa del valle "
                         "y acaba más arriba. Esto pasa de verdad al entrenar redes.")
            else:
                st.success(f"Tras {len(xs) - 1} pasos: x ≈ {num(xs[-1], 8)}, f(x) ≈ {num(ys[-1], 8)}, "
                           f"f'(x) ≈ {num(float(df(xs[-1])), 3)}")
            lo, hi = min(xs + [-2.5]) - 0.5, max(xs + [2.5]) + 0.5
            fig = figura_base()
            trazar(fig, f, lo, hi, "f(x) = error")
            fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines+markers", name="recorrido",
                                     marker=dict(color=np.arange(len(xs)), colorscale="Purp", size=8),
                                     line=dict(color=LILA, width=1)))
            st.plotly_chart(fig, width="stretch")
            st.markdown("🔎 **Experimenta:** con x₀ = 2 cae en un mínimo *local*; con x₀ = −2 en el *global*. "
                        "Sube η a 0,3 y mira cómo se vuelve loco. Eso es lo que hace tan difícil entrenar modelos: "
                        "el mínimo que encuentras depende de dónde empiezas.")

    # ------------------------------------------------------------ RSA
    with t2:
        analogia("RSA es un <b>buzón con candado</b>: cualquiera puede cerrar el candado (clave pública), pero sólo "
                 "quien tiene la llave (clave privada) lo abre. La «magia» es Euclides extendido + potencias modulares + "
                 "lo difícil que es factorizar números enormes.")
        c1, c2, c3 = st.columns(3)
        p = int(c1.number_input("primo p", value=61, min_value=3, step=1, key="rsa_p"))
        q = int(c2.number_input("primo q", value=53, min_value=3, step=1, key="rsa_q"))
        e = int(c3.number_input("exponente público e", value=17, min_value=3, step=2, key="rsa_e"))
        if not (sp.isprime(p) and sp.isprime(q)) or p == q:
            st.error("p y q tienen que ser primos distintos.")
        else:
            nmod, ph = p * q, (p - 1) * (q - 1)
            if gcd(e, ph) != 1:
                st.error(f"mcd(e, φ(n)) = mcd({e}, {ph}) = {gcd(e, ph)} ≠ 1: e no tiene inverso. Prueba otro e.")
            else:
                ee = E.euclides_extendido(e, ph)
                d = ee.s % ph
                st.markdown(f"1. n = p·q = **{nmod}**  ·  φ(n) = (p−1)(q−1) = **{ph}**")
                st.markdown(f"2. Clave pública: **(n, e) = ({nmod}, {e})**")
                st.markdown(f"3. Clave privada d = e⁻¹ mod φ(n). Con Euclides extendido: "
                            f"{ee.d} = ({ee.s})·{e} + ({ee.t})·{ph} ⇒ d ≡ {ee.s} ≡ **{d}** (mod {ph})")
                msg = st.text_input("Mensaje (texto corto)", "Hola Lucía", key="rsa_msg")
                cod = [ord(ch) for ch in msg]
                if any(c >= nmod for c in cod):
                    st.warning("Algún carácter tiene código ≥ n: usa primos más grandes.")
                else:
                    cif = [pow(c, e, nmod) for c in cod]
                    desc = [pow(c, d, nmod) for c in cif]
                    df = pd.DataFrame({"letra": list(msg), "m (código)": cod, "c = mᵉ mod n": cif, "cᵈ mod n": desc})
                    st.dataframe(df.T.astype(str), width="stretch")
                    texto = "".join(chr(v) for v in desc)
                    st.markdown(f"Descifrado: **{texto}**")
                    verificado(texto == msg, "El mensaje vuelve intacto: (mᵉ)ᵈ ≡ m (mod n) por Euler–Fermat ✔")

    # ------------------------------------------------------------ cumpleaños
    with t3:
        analogia("en una clase de 23 personas hay más de un 50 % de probabilidad de que dos cumplan años el mismo día. "
                 "Parece imposible porque piensas en «alguien que cumpla el MISMO día que yo», pero cuentan todas las "
                 "<b>parejas</b>: C(23, 2) = 253.")
        c1, c2 = st.columns(2)
        N = int(c1.number_input("Valores posibles (días, cubos de un hash…)", value=365, min_value=2, key="bd_N"))
        k = int(c2.number_input("Elementos (personas, datos…)", value=23, min_value=1, key="bd_k"))
        if k > N:
            pr = 1.0
        else:
            prob_no = 1.0
            for i in range(k):
                prob_no *= (N - i) / N
            pr = 1 - prob_no
        st.latex(rf"P(\text{{alguna coincidencia}}) = 1 - \frac{{V_{{{N},{k}}}}}{{{N}^{{{k}}}}} = "
                 rf"1 - \frac{{{N}\cdot{N - 1}\cdots{max(N - k + 1, 0)}}}{{{N}^{{{k}}}}} \approx {pr:.4f}")
        st.caption("Casos favorables a «ninguna coincidencia» = variaciones sin repetición; casos totales = variaciones "
                   "con repetición. ¡Combinatoria pura!")
        ks = list(range(1, min(4 * int(np.sqrt(N)) + 20, 3 * N) + 1))
        probs = []
        acc = 1.0
        for i in ks:
            acc *= max(N - (i - 1), 0) / N
            probs.append(1 - acc)
        fig = figura_base("Probabilidad de colisión")
        fig.add_trace(go.Scatter(x=ks, y=probs, mode="lines", line=dict(color=ROSA, width=3)))
        fig.add_hline(y=0.5, line_dash="dash", line_color=GRIS)
        st.plotly_chart(fig, width="stretch")
        st.markdown(f"Regla práctica: aparecen colisiones con unos √N ≈ **{num(np.sqrt(N), 4)}** elementos. "
                    "Por eso los <b>hashes</b> y los identificadores únicos (UUID) necesitan espacios ENORMES.",
                    unsafe_allow_html=True)

    # ------------------------------------------------------------ activaciones
    with t4:
        analogia("una neurona artificial es un <b>interruptor con regulador</b>: suma lo que le llega y la función "
                 "de activación decide cuánto «se enciende». Para aprender por descenso de gradiente, necesitamos su "
                 "<b>derivada</b>.")
        opciones = {
            "Sigmoide σ(x) = 1/(1+e^(−x))": 1 / (1 + sp.exp(-x)),
            "Tangente hiperbólica tanh(x)": sp.tanh(x),
            "Softplus ln(1+e^x)": sp.log(1 + sp.exp(x)),
            "Gaussiana e^(−x²)": sp.exp(-x ** 2),
            "ReLU max(0, x)": sp.Max(0, x),
        }
        eleccion = st.selectbox("Función", list(opciones), key="act")
        g = opciones[eleccion]
        dg = A.mas_simple(sp.diff(g, x))
        st.latex(rf"g(x) = {L(g)},\qquad g'(x) = {L(dg)}")
        if "Sigmoide" in eleccion:
            st.latex(r"\sigma'(x) = \sigma(x)\,\bigl(1-\sigma(x)\bigr)")
            ok = A.son_iguales(dg, g * (1 - g))
            verificado(ok, "Comprobado: σ' = σ(1 − σ) ✔ (por eso es tan barata de calcular)")
            st.caption("Lejos de 0, σ' ≈ 0: el gradiente «se apaga» (problema del desvanecimiento del gradiente).")
        if "ReLU" in eleccion:
            st.caption("ReLU no es derivable en 0 (pico como |x|): en la práctica se toma g'(0) = 0. Su derivada vale 1 "
                       "para x > 0, así que el gradiente no se apaga.")
        fig = figura_base()
        trazar(fig, g, -6, 6, "g(x)")
        trazar(fig, sp.Piecewise((0, x < 0), (1, True)) if "ReLU" in eleccion else dg, -6, 6, "g'(x)",
               color=LILA, ancho=2, guion="dash")
        st.plotly_chart(fig, width="stretch")
