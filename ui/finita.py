"""Páginas de Matemática finita."""
from __future__ import annotations

from itertools import combinations
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import sympy as sp

from core import polinomios as P
from core import enteros as E
from core import combinatoria as C
from core.parsing import x, leer, ErrorLectura
from ui.comun import (L, entrada_expr, verificado, analogia, ia, figura_base, ROSA, LILA, TURQUESA)


# =================================================================== POLINOMIOS
def _cuerpo_selector(clave):
    c1, c2 = st.columns([2, 1])
    with c1:
        tipo = st.radio("¿Dónde trabajamos?", ["ℚ (racionales)", "ℤ_p (módulo un primo p)"], horizontal=True, key=f"{clave}_k")
    p = None
    if tipo.startswith("ℤ"):
        with c2:
            p = st.number_input("p (primo)", value=5, min_value=2, step=1, key=f"{clave}_p")
    try:
        return P.Cuerpo(int(p) if p else None)
    except ValueError as exc:
        st.error(str(exc))
        return None


def _poly(K, txt_expr):
    try:
        return P.desde_expr(txt_expr, K)
    except ValueError as exc:
        st.error(str(exc))
        return None


def pagina_polinomios():
    analogia("dividir polinomios es como repartir caramelos: el cociente es cuántos le tocan a cada uno y el resto lo "
             "que sobra y ya no llega para otra ronda completa. En polinomios «no llega» significa que el resto tiene "
             "<b>grado menor</b> que el divisor.")
    K = _cuerpo_selector("pol")
    if K is None:
        return
    c1, c2 = st.columns(2)
    with c1:
        A_e = entrada_expr("A(x)", "x^10+11x^8+46x^6+90x^4+81x^2+27", "pol_A")
    with c2:
        B_e = entrada_expr("B(x)", "x^10+9x^8+30x^6+46x^4+33x^2+9", "pol_B")
    if A_e is None or B_e is None:
        return
    A, B = _poly(K, A_e), _poly(K, B_e)
    if A is None or B is None:
        return
    eq = "\\equiv" if K.p else "="
    t1, t2, t3, t4, t5 = st.tabs(["➗ División euclídea", "🔗 MCD y Bézout", "🧩 mcm", "📋 Ruffini", "🌱 Factorizar y raíces"])

    with t1:
        if P.es_cero(B):
            st.error("No se puede dividir entre el polinomio 0.")
        else:
            d = P.division(A, B, K)
            st.latex(rf"A(x) {eq} q(x)\cdot B(x) + r(x)")
            st.latex(rf"\textbf{{Cociente: }}\ q(x) {eq} {P.mostrar(d.cociente, K)}")
            st.latex(rf"\textbf{{Resto: }}\ r(x) {eq} {P.mostrar(d.resto, K)}")
            m1, m2 = st.columns(2)
            m1.metric("Grado del cociente", P.grado(d.cociente) if not P.es_cero(d.cociente) else "—")
            m2.metric("Grado del resto", P.grado(d.resto) if not P.es_cero(d.resto) else "—  (resto 0: B divide a A)")
            verificado(P.verificar_division(d, K),
                       "Comprobado: q·B + r reproduce A exactamente y gr(r) < gr(B) ✔")
            st.subheader("Paso a paso")
            st.caption("En cada paso: (1) divido el término líder del resto entre el líder de B, "
                       "(2) multiplico ese término por B, (3) lo resto. Paro cuando el grado del resto es menor que el de B.")
            for i, paso in enumerate(d.pasos, 1):
                t = paso.termino_coef * x ** paso.termino_grado
                with st.expander(f"Paso {i}: término del cociente  {sp.sstr(t)}", expanded=len(d.pasos) <= 4):
                    lider_R = paso.resto_antes[0] * x ** P.grado(paso.resto_antes)
                    lider_B = B[0] * x ** P.grado(B)
                    st.latex(rf"\frac{{{L(lider_R)}}}{{{L(lider_B)}}} {eq} {L(t)}")
                    st.latex(rf"{L(t)}\cdot\left({P.mostrar(B, K)}\right) {eq} {P.mostrar(paso.restado, K)}")
                    st.latex(rf"\left({P.mostrar(paso.resto_antes, K)}\right) - \left({P.mostrar(paso.restado, K)}\right) {eq} "
                             rf"\mathbf{{{P.mostrar(paso.resto_despues, K)}}}")
            if not d.pasos:
                st.info("gr(A) < gr(B): el cociente es 0 y el resto es el propio A.")

    with t2:
        if P.es_cero(A) and P.es_cero(B):
            st.error("mcd(0, 0) no está definido.")
        else:
            res = P.mcd_extendido(A, B, K)
            st.latex(rf"\operatorname{{mcd}}(A,B) = {P.mostrar(res.mcd, K)}")
            try:
                st.latex(r"= " + L(P.factorizar(P.a_expr(res.mcd), K)))
            except Exception:  # noqa: BLE001
                pass
            checks = P.verificar_mcd(res, K)
            verificado(all(checks.values()), "Comprobado: divide a A y a B, cumple Bézout y coincide con SymPy ✔")
            with st.expander("Detalle de las comprobaciones"):
                for k_, v_ in checks.items():
                    st.write(("✅ " if v_ else "❌ ") + k_)
            st.subheader("Algoritmo de Euclides")
            analogia("es como buscar la baldosa más grande que cubre a la vez dos pasillos: recortas el largo con el corto, "
                     "luego el corto con lo que sobró… hasta que un trozo encaja exacto. Ese trozo es el mcd.")
            for i, f in enumerate(res.filas, 1):
                st.latex(rf"\text{{({i})}}\quad {P.mostrar(f.dividendo, K)} {eq} \left({P.mostrar(f.cociente, K)}\right)"
                         rf"\left({P.mostrar(f.divisor, K)}\right) + \left({P.mostrar(f.resto, K)}\right)")
            lc = res.ultimo_resto[0]
            st.markdown(f"El último resto **no nulo** es $r = {P.mostrar(res.ultimo_resto, K)}$. "
                        + (f"Lo divido entre su coeficiente líder ${L(lc)}$ para hacerlo **mónico**."
                           if lc != 1 else "Ya es mónico."))
            st.subheader("Identidad de Bézout")
            st.latex(rf"\underbrace{{\left({P.mostrar(res.s, K)}\right)}}_{{s(x)}}A(x) + "
                     rf"\underbrace{{\left({P.mostrar(res.t, K)}\right)}}_{{t(x)}}B(x) {eq} {P.mostrar(res.mcd, K)}")
            with st.expander("Tabla del algoritmo extendido (rᵢ = sᵢ·A + tᵢ·B)"):
                filas = [{"i": 0, "rᵢ": sp.sstr(P.a_expr(res.A)), "sᵢ": "1", "tᵢ": "0", "qᵢ": ""},
                         {"i": 1, "rᵢ": sp.sstr(P.a_expr(res.B)), "sᵢ": "0", "tᵢ": "1", "qᵢ": ""}]
                for i, f in enumerate(res.filas, 2):
                    filas.append({"i": i, "rᵢ": sp.sstr(P.a_expr(f.resto)), "sᵢ": sp.sstr(P.a_expr(f.s)),
                                  "tᵢ": sp.sstr(P.a_expr(f.t)), "qᵢ": sp.sstr(P.a_expr(f.cociente))})
                st.dataframe(pd.DataFrame(filas), hide_index=True, width="stretch")
                st.caption("Cada fila nueva: rᵢ = rᵢ₋₂ − qᵢ·rᵢ₋₁, y lo mismo con s y t.")

    with t3:
        if P.es_cero(A) or P.es_cero(B):
            st.latex(r"\operatorname{mcm} = 0")
        else:
            m = P.mcm(A, B, K)
            st.latex(rf"\operatorname{{mcm}}(A,B) = \frac{{A\cdot B}}{{\operatorname{{mcd}}(A,B)}} = {P.mostrar(m, K)}")
            try:
                st.latex("= " + L(P.factorizar(P.a_expr(m), K)))
            except Exception:  # noqa: BLE001
                pass
            ok = P.es_cero(P.division(m, A, K).resto) and P.es_cero(P.division(m, B, K).resto)
            verificado(ok, "Comprobado: A y B dividen al mcm ✔")

    with t4:
        st.caption("Ruffini = dividir entre (x − a) de forma rápida. El resto es P(a) (teorema del resto).")
        a_txt = st.text_input("a (divido A entre x − a)", "-1", key="ruf_a")
        try:
            a = leer(a_txt)
            rf = P.ruffini(A, a, K)
            cols = [L(c) for c in rf.coef]
            tabla = (r"\begin{array}{c|" + "c" * len(cols) + r"}"
                     + " & " + " & ".join(cols) + r"\\ "
                     + L(rf.a) + " & " + " & ".join(L(v) if i else "" for i, v in enumerate(rf.fila_media)) + r"\\ \hline "
                     + " & " + " & ".join(L(v) for v in rf.fila_baja[:-1]) + r" & \boxed{" + L(rf.resto) + r"}\end{array}")
            st.latex(tabla)
            st.latex(rf"A(x) {eq} (x - ({L(rf.a)}))\left({P.mostrar(rf.cociente, K)}\right) + {L(rf.resto)}")
            st.markdown(f"Resto = A({sp.sstr(rf.a)}) = **{sp.sstr(rf.resto)}** → "
                        + ("**es raíz** 🎯" if rf.resto == 0 else "no es raíz."))
            d = P.division(A, P.desde_expr(x - a, K), K)
            verificado(d.cociente == rf.cociente and (d.resto == [rf.resto]), "Coincide con la división larga ✔")
        except (ErrorLectura, ValueError) as exc:
            st.error(str(exc))

    with t5:
        for nombre, poli in (("A", A), ("B", B)):
            st.markdown(f"**{nombre}(x)**")
            if P.es_cero(poli):
                st.write("Es el polinomio 0.")
                continue
            ex = P.a_expr(poli)
            st.latex(rf"{nombre}(x) {eq} {L(P.factorizar(ex, K))}")
            r = P.raices(poli, K)
            if K.p:
                st.write("Raíces en " + K.nombre + ": " +
                         (", ".join(f"{v} (mult. {m})" for v, m in r["en el cuerpo"].items()) or "ninguna"))
            else:
                st.write("Raíces racionales: " + (", ".join(f"{sp.sstr(v)} (mult. {m})" for v, m in r["racionales"].items()) or "ninguna"))
                st.write("Raíces reales: " + (", ".join(f"{sp.sstr(v)} ≈ {float(sp.N(v)):.6g} (mult. {m})"
                                                       for v, m in r["reales"].items()) or "ninguna"))
                st.write("Raíces complejas no reales: " + (", ".join(f"{sp.sstr(sp.N(v, 6))} (mult. {m})"
                                                                     for v, m in r["complejas"].items()) or "ninguna"))
            if K.p is None:
                st.caption("Truco de examen (raíces racionales): si p/q es raíz de un polinomio con coeficientes enteros, "
                           "p divide al término independiente y q al coeficiente líder.")
    ia("los polinomios en ℤ_p son la base de los <b>códigos correctores de errores</b> (CRC, Reed–Solomon en QR y "
       "discos) y de la criptografía; y el algoritmo de Euclides es el mismo que se usa para invertir en ℤ_p.")


# =================================================================== ENTEROS
def herr_euclides():
    c1, c2 = st.columns(2)
    a = c1.number_input("a", value=240, step=1, key="ee_a")
    b = c2.number_input("b", value=46, step=1, key="ee_b")
    try:
        ee = E.euclides_extendido(int(a), int(b))
        st.latex(rf"\operatorname{{mcd}}({int(a)},{int(b)}) = {ee.d}\qquad \operatorname{{mcm}} = {E.mcm(int(a), int(b))}")
        st.latex(rf"{ee.d} = ({ee.s})\cdot {int(a)} + ({ee.t})\cdot {int(b)}")
        verificado(ee.s * int(a) + ee.t * int(b) == ee.d and sp.gcd(int(a), int(b)) == ee.d,
                   "Comprobado: la identidad cuadra y el mcd coincide con SymPy ✔")
        df = pd.DataFrame([{"dividendo": f.a, "divisor": f.b, "cociente q": f.q, "resto r": f.r, "s": f.s, "t": f.t}
                           for f in ee.filas])
        st.dataframe(df, hide_index=True, width="stretch")
        st.caption("Cada resto r se escribe como r = s·|a| + t·|b|. La última fila con resto ≠ 0 da el mcd.")
        if ee.d == 1:
            st.info(f"Son coprimos: {ee.s % abs(int(b)) if b else '—'} es el inverso de {int(a)} módulo {abs(int(b))}.")
    except ValueError as exc:
        st.error(str(exc))
    lista = st.text_input("mcd y mcm de varios números (separados por comas)", "12, 18, 30", key="lista_mcd")
    try:
        nums = [int(leer(t)) for t in lista.split(",") if t.strip()]
        st.write(f"mcd = **{E.mcd_lista(nums)}**,  mcm = **{E.mcm_lista(nums)}**")
    except Exception as exc:  # noqa: BLE001
        st.error(f"Lista no válida: {exc}")



def herr_diofanticas():
    st.latex(r"a\,x + b\,y = c,\quad x,y\in\mathbb{Z}")
    c1, c2, c3 = st.columns(3)
    a = int(c1.number_input("a", value=12, step=1, key="dio_a"))
    b = int(c2.number_input("b", value=42, step=1, key="dio_b"))
    c = int(c3.number_input("c", value=30, step=1, key="dio_c"))
    try:
        d = E.diofantica(a, b, c)
        st.markdown(f"**Paso 1.** mcd({a}, {b}) = {d.d}.")
        if not d.tiene_solucion:
            st.error(f"{d.d} no divide a {c} ⇒ **no hay soluciones enteras**.")
        else:
            st.markdown(f"**Paso 2.** {d.d} divide a {c} ⇒ hay infinitas soluciones.")
            st.markdown(f"**Paso 3.** Bézout: {d.d} = ({d.ee.s})·{a} + ({d.ee.t})·{b}. "
                        f"Multiplico por {c}/{d.d} = {c // d.d}:")
            st.latex(rf"x_0 = {d.x0},\quad y_0 = {d.y0}")
            st.markdown("**Paso 4.** Solución general (λ ∈ ℤ):")
            st.latex(rf"x = {d.x0} {'+' if d.paso_x >= 0 else '-'} {abs(d.paso_x)}\lambda,\qquad "
                     rf"y = {d.y0} {'+' if d.paso_y >= 0 else '-'} {abs(d.paso_y)}\lambda")
            ok = all(a * (d.x0 + d.paso_x * l) + b * (d.y0 + d.paso_y * l) == c for l in range(-5, 6))
            verificado(ok, "Comprobado sustituyendo λ = −5, …, 5 ✔")
            filas = [{"λ": l, "x": d.x0 + d.paso_x * l, "y": d.y0 + d.paso_y * l} for l in range(-3, 4)]
            st.dataframe(pd.DataFrame(filas), hide_index=True)
            st.caption("Si te piden soluciones positivas: impón x > 0 e y > 0 y despeja qué λ valen.")
    except ValueError as exc:
        st.error(str(exc))



def herr_congruencias():
    st.latex(r"a\,x \equiv b \pmod m")
    c1, c2, c3 = st.columns(3)
    a = int(c1.number_input("a", value=6, step=1, key="cg_a"))
    b = int(c2.number_input("b", value=4, step=1, key="cg_b"))
    m = int(c3.number_input("m", value=10, min_value=1, step=1, key="cg_m"))
    try:
        cg = E.congruencia_lineal(a, b, m)
        st.markdown(f"**Paso 1.** d = mcd({a % m}, {m}) = {cg.d}.")
        if not cg.tiene_solucion:
            st.error(f"{cg.d} no divide a {b % m} ⇒ **no tiene solución**.")
        else:
            if cg.d > 1:
                st.markdown(f"**Paso 2.** {cg.d} divide a {b % m} ⇒ hay exactamente **{cg.d}** soluciones módulo {m}. "
                            f"Divido todo entre {cg.d}:")
                st.latex(rf"{(a % m) // cg.d}\,x \equiv {(b % m) // cg.d} \pmod{{{m // cg.d}}}")
            else:
                st.markdown(f"**Paso 2.** Son coprimos ⇒ solución única módulo {m}.")
            if cg.modulo_reducido > 1:
                st.markdown(f"**Paso 3.** Inverso de {(a % m) // cg.d} módulo {cg.modulo_reducido}: "
                            f"**{cg.inverso}** (porque {(a % m) // cg.d}·{cg.inverso} = "
                            f"{(a % m) // cg.d * cg.inverso} ≡ 1). Multiplico por él:")
            st.latex(rf"x \equiv {cg.sol_base} \pmod{{{cg.modulo_reducido}}}")
            st.markdown("Soluciones módulo " + str(m) + ": **" + ", ".join(map(str, cg.soluciones)) + "**")
            ok = sorted(cg.soluciones) == [v for v in range(m) if (a * v - b) % m == 0]
            verificado(ok, f"Comprobado probando los {m} valores 0…{m - 1} uno a uno ✔")
    except ValueError as exc:
        st.error(str(exc))
    with st.expander("Tabla de inversos módulo m"):
        mm = int(st.number_input("m", value=11, min_value=2, max_value=200, key="tinv_m"))
        filas = E.tabla_inversos(mm)
        st.dataframe(pd.DataFrame([{"a": a_, "a⁻¹": inv if inv is not None else "no existe"} for a_, inv in filas]).T.astype(str),
                     width="stretch")
        st.caption("a tiene inverso módulo m ⇔ mcd(a, m) = 1. Si m es primo, todos menos el 0 lo tienen (ℤ_m es un cuerpo).")



def herr_chino():
    st.caption("Escribe un sistema x ≡ aᵢ (mod mᵢ). Funciona aunque los módulos no sean coprimos (te dice si es incompatible).")
    rs = st.text_input("Restos a₁, a₂, …", "2, 3, 2", key="tcr_r")
    ms = st.text_input("Módulos m₁, m₂, …", "3, 5, 7", key="tcr_m")
    try:
        restos = [int(leer(t)) for t in rs.split(",") if t.strip()]
        mods = [int(leer(t)) for t in ms.split(",") if t.strip()]
        st.latex(r"\begin{cases}" + r"\\".join(rf"x\equiv {a}\pmod{{{m}}}" for a, m in zip(restos, mods)) + r"\end{cases}")
        t = E.chino_del_resto(restos, mods)
        if not t.tiene_solucion:
            st.error("Sistema **incompatible**: " + t.motivo)
        else:
            for p in t.pasos:
                st.markdown("- " + p.explicacion)
            st.latex(rf"x \equiv {t.x} \pmod{{{t.M}}}")
            verificado(all(t.x % m == a % m for a, m in zip(restos, mods)), "Comprobado: cumple todas las congruencias ✔")
            if all(sp.gcd(m1, m2) == 1 for m1, m2 in combinations(mods, 2)):
                with st.expander("Método de la fórmula (Mᵢ y sus inversos)"):
                    M = 1
                    for m in mods:
                        M *= m
                    filas, total = [], 0
                    for a, m in zip(restos, mods):
                        Mi = M // m
                        yi = pow(Mi, -1, m)
                        total += a * Mi * yi
                        filas.append({"aᵢ": a, "mᵢ": m, "Mᵢ = M/mᵢ": Mi, "yᵢ = Mᵢ⁻¹ mod mᵢ": yi, "aᵢMᵢyᵢ": a * Mi * yi})
                    st.dataframe(pd.DataFrame(filas), hide_index=True)
                    st.latex(rf"x \equiv \sum a_i M_i y_i = {total} \equiv {total % M} \pmod{{{M}}}")
    except ValueError as exc:
        st.error(str(exc))



def herr_potencias():
    c1, c2, c3 = st.columns(3)
    base = int(c1.number_input("base", value=7, step=1, key="pm_b"))
    ex = int(c2.number_input("exponente", value=222, step=1, key="pm_e"))
    m = int(c3.number_input("módulo", value=13, min_value=1, step=1, key="pm_m"))
    try:
        r, pasos, binario = E.potencia_modular(base, ex, m)
        st.latex(rf"{base}^{{{ex}}} \equiv {r} \pmod{{{m}}}")
        verificado(r == pow(base, ex, m) if ex >= 0 else None, "Coincide con pow() de Python ✔")
        st.markdown(f"**Exponenciación rápida:** {abs(ex)} en binario es `{binario}` (se leen los bits de derecha a izquierda).")
        st.dataframe(pd.DataFrame([{"bit": p.bit, "potencia actual (base^(2^i))": p.base, "acumulado": p.acumulado}
                                   for p in pasos]), hide_index=True)
        if m > 1 and sp.gcd(base, m) == 1:
            ph = E.phi(m)
            st.markdown(f"**Atajo de Euler–Fermat:** como mcd({base}, {m}) = 1, {base}^φ({m}) = {base}^{ph} ≡ 1, "
                        f"así que puedo reducir el exponente módulo {ph}: {ex} ≡ {ex % ph} ⇒ "
                        f"{base}^{ex} ≡ {base}^{ex % ph} ≡ {pow(base, ex % ph, m)} (mod {m}).")
    except ValueError as exc:
        st.error(str(exc))



def herr_primos_phi():
    nn = int(st.number_input("n", value=360, min_value=1, step=1, key="pr_n"))
    fac = E.factorizacion(nn)
    st.latex(rf"{nn} = " + (r"\cdot ".join(f"{p}^{{{e}}}" if e > 1 else str(p) for p, e in fac.items()) if fac else "1"))
    divs = E.divisores(nn)
    st.markdown(f"**¿Primo?** {'sí ✨' if sp.isprime(nn) else 'no'}  ·  **Nº de divisores:** {len(divs)}  ·  "
                f"**Suma de divisores:** {sum(divs)}  ·  **φ({nn}) = {E.phi(nn)}**")
    if fac:
        st.latex(r"\varphi(n) = n\prod_{p\mid n}\left(1-\tfrac1p\right) = " + str(nn) + "".join(
            rf"\left(1-\tfrac1{{{p}}}\right)" for p in fac) + f" = {E.phi(nn)}")
    st.caption("Divisores: " + ", ".join(map(str, divs[:200])) + (" …" if len(divs) > 200 else ""))


# =================================================================== COMBINATORIA
def herr_selecciones():
    analogia("elegir de un conjunto es como <b>pedir helado</b>: ¿importa el orden de las bolas (cono: abajo/arriba) "
             "o no (tarrina)? ¿puedes repetir sabor? Las 4 respuestas dan las 4 fórmulas.")
    c1, c2, c3, c4 = st.columns(4)
    nn = int(c1.number_input("n (elementos disponibles)", value=5, min_value=0, step=1, key="sel_n"))
    kk = int(c2.number_input("k (cuántos elijo)", value=3, min_value=0, step=1, key="sel_k"))
    orden = c3.radio("¿Importa el orden?", ["Sí", "No"], key="sel_o") == "Sí"
    rep = c4.radio("¿Se puede repetir?", ["Sí", "No"], key="sel_r", index=1) == "Sí"
    s = C.seleccion(nn, kk, orden, rep)
    st.subheader(f"{s.nombre}: {s.numero:,}".replace(",", "."))
    st.latex(s.formula_tex + f" = {s.numero}")
    st.markdown("**Por qué:** " + s.porque)
    fb = C.seleccion_fuerza_bruta(nn, kk, orden, rep)
    if fb is not None:
        verificado(fb == s.numero, f"Comprobado listando por ordenador las {fb} posibilidades una a una ✔")
    else:
        st.caption("(Demasiados casos para listarlos uno a uno; la fórmula está verificada en los tests con casos pequeños.)")
    if nn <= 8 and kk <= 4:
        elem = list("ABCDEFGH"[:nn])
        ejs = C.ejemplos_seleccion(elem, kk, orden, rep, 40)
        st.caption("Ejemplos con " + "{" + ", ".join(elem) + "}: " + "  ".join("".join(t) or "∅" for t in ejs)
                   + (" …" if s.numero > 40 else ""))
    with st.expander("¿Y si son permutaciones con elementos repetidos? (MISSISSIPPI)"):
        palabra = st.text_input("Palabra o lista de repeticiones (p. ej. 1,4,4,2)", "MISSISSIPPI", key="multi")
        try:
            if any(ch.isdigit() for ch in palabra):
                reps = [int(t) for t in palabra.split(",") if t.strip()]
            else:
                reps = [palabra.count(ch) for ch in dict.fromkeys(palabra)]
            denominador = "!\\,".join(map(str, reps))
            st.latex(rf"\frac{{{sum(reps)}!}}{{{denominador}!}} = {C.multinomial(reps)}")
            st.caption("Ordeno todas las letras como si fueran distintas (n!) y divido por las formas de ordenar "
                       "las repetidas entre sí, que no se distinguen.")
        except ValueError:
            st.error("Escribe una palabra o números separados por comas.")



def herr_doce_formas():
    st.markdown("Repartir **k objetos** en **n cajas**. Contesta las tres preguntas y te digo modelo, fórmula, "
                "justificación y **por qué no valen las otras**.")
    c1, c2 = st.columns(2)
    kk = int(c1.number_input("k (objetos)", value=5, min_value=0, step=1, key="tw_k"))
    nn = int(c2.number_input("n (cajas)", value=3, min_value=0, step=1, key="tw_n"))
    c1, c2, c3 = st.columns(3)
    D = c1.radio("¿Los objetos se distinguen?", ["Sí (bolas numeradas)", "No (bolas iguales)"], key="tw_d").startswith("Sí")
    Cj = c2.radio("¿Las cajas se distinguen?", ["Sí (cajas con nombre)", "No (cajas iguales)"], key="tw_c").startswith("Sí")
    cond = c3.radio("Condición", ["Sin restricción", "Como mucho 1 por caja", "Ninguna caja vacía"], key="tw_cond")
    cond_k = {"Sin restricción": "libre", "Como mucho 1 por caja": "inyectiva", "Ninguna caja vacía": "sobreyectiva"}[cond]
    caso = C.doce_formas(kk, nn, D, Cj, cond_k)
    st.subheader(f"{caso.nombre}: {caso.numero:,}".replace(",", "."))
    st.latex(caso.formula_tex + f" = {caso.numero}")
    st.markdown("**Por qué esta fórmula:** " + caso.porque)
    st.markdown("**Por qué NO las otras:** " + caso.otras)
    fb = C.doce_formas_fuerza_bruta(kk, nn, D, Cj, cond_k)
    if fb is not None:
        verificado(fb == caso.numero, f"Comprobado enumerando las {nn}^{kk} = {nn ** kk} aplicaciones y "
                                      f"agrupando las que son «el mismo reparto»: {fb} ✔")
    with st.expander("📋 Tabla completa de las 12 formas para estos k y n"):
        filas = []
        for d_ in (True, False):
            for c_ in (True, False):
                fila = {"objetos": "distintos" if d_ else "iguales", "cajas": "distintas" if c_ else "iguales"}
                for nombre, ck in (("sin restricción", "libre"), ("≤ 1 por caja", "inyectiva"), ("sin cajas vacías", "sobreyectiva")):
                    fila[nombre] = C.doce_formas(kk, nn, d_, c_, ck).numero
                filas.append(fila)
        st.dataframe(pd.DataFrame(filas), hide_index=True, width="stretch")
    analogia("<b>objetos distintos + cajas distintas</b> = mandar cartas con nombre a buzones con número; "
             "<b>objetos iguales</b> = repartir caramelos idénticos (sólo importa cuántos); "
             "<b>cajas iguales</b> = hacer grupos de trabajo sin nombre (sólo importa quién va con quién).")



def herr_numeros_especiales():
    nmax = int(st.slider("Tamaño de las tablas", 4, 12, 8, key="tab_n"))
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Stirling de 2ª especie S(n, k)** — partir n elementos en k bloques no vacíos")
        st.dataframe(pd.DataFrame([[C.stirling2(i, j) for j in range(nmax + 1)] for i in range(nmax + 1)]),
                     width="stretch")
        st.latex(r"S(n,k) = k\,S(n-1,k) + S(n-1,k-1)")
        st.caption("El elemento n o va solo en un bloque nuevo (S(n−1,k−1)) o se une a uno de los k bloques ya formados (k·S(n−1,k)).")
    with c2:
        st.markdown("**Stirling de 1ª especie s(n, k)** (sin signo) — permutaciones de n con k ciclos")
        st.dataframe(pd.DataFrame([[C.stirling1(i, j) for j in range(nmax + 1)] for i in range(nmax + 1)]),
                     width="stretch")
        st.latex(r"s(n,k) = (n-1)\,s(n-1,k) + s(n-1,k-1)")
        st.caption("El elemento n o forma un ciclo él solo, o se mete detrás de cualquiera de los n−1 elementos en un ciclo existente.")
    st.warning("No las confundas: **2ª especie = particiones en bloques** (grupos, no importa el orden dentro). "
               "**1ª especie = ciclos** (importa el orden circular dentro de cada grupo). Por eso s(n,k) ≥ S(n,k).")
    st.markdown("**Triángulo de Pascal**")
    st.dataframe(pd.DataFrame([[str(sp.binomial(i, j)) if j <= i else "" for j in range(nmax + 1)] for i in range(nmax + 1)]),
                 width="stretch")
    st.write(f"Bell B₀…B_{nmax}: {[C.bell(i) for i in range(nmax + 1)]}  ·  "
             f"Desarreglos D₀…D_{nmax}: {[C.desarreglos(i) for i in range(nmax + 1)]}  ·  "
             f"Catalan: {[C.catalan(i) for i in range(nmax + 1)]}")
    st.caption("Desarreglos Dₙ = n!·Σ(−1)ⁱ/i!: el problema del amigo invisible en el que nadie se toca a sí mismo. "
               "Dₙ/n! → 1/e ≈ 0,3679.")



def herr_inclusion_exclusion():
    analogia("contar alumnos que hablan inglés o francés: si sumas los dos grupos, los que hablan los dos idiomas "
             "los has contado dos veces, así que los restas una vez. Con 3 conjuntos te pasas restando y vuelves a "
             "sumar la intersección triple. Sumar–restar–sumar…")
    m = int(st.number_input("¿Cuántos conjuntos?", value=3, min_value=1, max_value=5, key="ie_m"))
    nombres = [chr(65 + i) for i in range(m)]
    tam = {}
    cols = st.columns(min(4, 2 ** m - 1))
    idx = 0
    defectos = {1: 30, 2: 10, 3: 4, 4: 1, 5: 0}
    for r in range(1, m + 1):
        for S in combinations(range(m), r):
            etiqueta = "|" + "∩".join(nombres[i] for i in S) + "|"
            tam[frozenset(S)] = int(cols[idx % len(cols)].number_input(etiqueta, value=defectos[r], min_value=0,
                                                                        step=1, key="ie_" + "".join(map(str, S))))
            idx += 1
    total, pasos = C.inclusion_exclusion(tam, m)
    for p_ in pasos:
        st.markdown("- " + p_)
    union = r" \cup ".join(nombres)
    st.latex(rf"\left|{union}\right| = {total}")
    coherente = all(tam[frozenset(S)] <= min(tam[frozenset(T)] for T in combinations(S, len(S) - 1)) if len(S) > 1 else True
                    for r in range(2, m + 1) for S in combinations(range(m), r))
    if not coherente:
        st.error("Ojo: algún tamaño de intersección es mayor que el de los conjuntos que la forman; los datos son imposibles.")
    u = st.number_input("Tamaño del universal |U| (para contar los que NO están en ninguno)", value=0, min_value=0, key="ie_u")
    if u:
        st.markdown(f"Fuera de todos: |U| − |∪| = {u} − {total} = **{u - total}**")
    st.caption("Aplicación estrella: sobreyecciones = nᵏ − C(n,1)(n−1)ᵏ + C(n,2)(n−2)ᵏ − … (restas los repartos que dejan "
               "alguna caja concreta vacía).")


# =================================================================== RECURRENCIAS
def pagina_recurrencias():
    analogia("una recurrencia es una <b>receta que se usa a sí misma</b>: para saber el término de hoy miras los de "
             "ayer y anteayer (como Fibonacci con los conejos). Resolverla es encontrar una fórmula para saltar "
             "directamente al día 100 sin pasar por los anteriores.")
    st.latex(r"a_n = c_1 a_{n-1} + c_2 a_{n-2} + \dots + c_r a_{n-r} + f(n)")
    c1, c2, c3 = st.columns(3)
    coefs_t = c1.text_input("Coeficientes c₁, c₂, …", "5, -6", key="rec_c")
    f_t = c2.text_input("f(n) (0 si es homogénea)", "0", key="rec_f")
    ini_t = c3.text_input("Condiciones iniciales a₀, a₁, …", "1, 4", key="rec_i")
    try:
        coefs = [leer(t) for t in coefs_t.split(",") if t.strip()]
        ini = [leer(t) for t in ini_t.split(",") if t.strip()]
        fn = leer(f_t)
        cerrada, caract, raices, terms, ok, nn = C.resolver_recurrencia(coefs, fn, ini)
        st.markdown("**1. Ecuación característica** (pruebo aₙ = λⁿ en la parte homogénea):")
        st.latex(L(caract))
        st.markdown("**2. Raíces:** " + ", ".join(f"λ = {sp.sstr(r)} (multiplicidad {m})" for r, m in raices.items()))
        partes = []
        letras = iter("ABCDEFGH")
        for r, m in raices.items():
            for j in range(m):
                partes.append(f"{next(letras)}" + (rf"\,n^{{{j}}}" if j > 1 else (r"\,n" if j == 1 else "")) + rf"\left({L(r)}\right)^n")
        st.markdown("**3. Solución general de la homogénea** (raíz doble ⇒ multiplico por n):")
        st.latex(r"a_n^{(h)} = " + " + ".join(partes))
        if fn != 0:
            st.markdown("**4.** Añado una solución particular del mismo «tipo» que f(n) (polinomio ↔ polinomio, "
                        "rⁿ ↔ rⁿ; si r es raíz característica, multiplico por n).")
        st.markdown(f"**{'5' if fn != 0 else '4'}. Impongo las condiciones iniciales** y obtengo:")
        if cerrada is not None:
            st.latex(rf"a_n = {L(cerrada)}")
            verificado(ok, "Comprobado: la fórmula da exactamente los 15 primeros términos calculados con la recurrencia ✔")
        else:
            st.warning("No he encontrado (o no he podido verificar) una forma cerrada. Te dejo los términos.")
        st.dataframe(pd.DataFrame({"n": list(range(len(terms))), "aₙ": [sp.sstr(t) for t in terms]}).T.astype(str),
                     width="stretch")
        fig = figura_base("Primeros términos")
        fig.add_trace(go.Scatter(x=list(range(len(terms))), y=[float(sp.N(t)) for t in terms], mode="lines+markers",
                                 line=dict(color=ROSA)))
        st.plotly_chart(fig, width="stretch")
    except (ErrorLectura, ValueError) as exc:
        st.error(str(exc))
    ia("las recurrencias miden el <b>coste de los algoritmos</b> (T(n) = 2T(n/2) + n en mergesort) y aparecen en "
       "modelos de series temporales (AR(p) es una recurrencia con ruido) y en las redes neuronales recurrentes.")
