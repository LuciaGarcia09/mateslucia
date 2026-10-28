"""Más generadores de ejercicios (uno o varios por tema), construidos al revés y comprobados.

Cada generador recibe un random.Random y devuelve un Ejercicio (ver ejercicios.py).
"""
from __future__ import annotations

from math import gcd, comb
import re
import sympy as sp

from .parsing import x, leer, ErrorLectura
from .ejercicios import Ejercicio, _iguales
from . import logica as L
from . import conjuntos as CJ
from . import enteros as E

n = sp.Symbol("n", integer=True, positive=True)


def _si_no(txt: str) -> bool:
    t = txt.strip().lower()
    if t in ("s", "si", "sí", "y", "yes", "v", "verdadero", "1", "true"):
        return True
    if t in ("n", "no", "f", "falso", "0", "false"):
        return False
    raise ErrorLectura("Responde «sí» o «no».")


def _entero(txt: str) -> int:
    v = leer(txt)
    if not (v.is_integer):
        raise ErrorLectura("Escribe un número entero.")
    return int(v)


# ======================================================================= FINITA
_FORMULAS = [
    "p -> (q -> p)", "(p -> q) <-> (¬q -> ¬p)", "(p ∧ q) -> p", "p ∧ ¬p", "(p -> q) ∧ (q -> r) -> (p -> r)",
    "(p ∨ q) -> p", "¬(p ∧ q) <-> (¬p ∨ ¬q)", "(p -> q) <-> (q -> p)", "(p ∧ (p -> q)) -> q",
    "(p ∨ q) ∧ (¬p ∨ r) -> (q ∨ r)", "(p <-> q) ∧ (p ⊕ q)", "((p -> q) -> p) -> p", "(p -> q) ∧ ¬q ∧ p",
    "(p ∨ q) ∧ ¬(p ∧ q)",
]


def ej_logica(rnd) -> Ejercicio:
    txt = rnd.choice(_FORMULAS)
    f = L.leer_formula(txt)
    t = L.tabla_verdad(f)
    vs = t.variables
    filas = "\n".join("| " + " | ".join("V" if v else "F" for v in vals) + " | " + ("V" if res[-1] else "F") + " |"
                      for vals, res in t.filas)
    tabla = "| " + " | ".join(vs) + " | fórmula |\n|" + "---|" * (len(vs) + 1) + "\n" + filas
    sol = [f"Es una **{t.clase}**.", tabla,
           "Tautología: V en todas las filas · contradicción: F en todas · contingencia: de todo."]

    def comp(r):
        d = r["c"].strip().lower().replace("í", "i").replace("ó", "o").rstrip(".")
        for clase in ("tautologia", "contradiccion", "contingencia"):
            if d == clase:
                ok = clase == t.clase.replace("í", "i").replace("ó", "o")
                return ok, "¡Correcto!" if ok else "No. Haz la tabla de verdad y mira la última columna."
        raise ErrorLectura("Responde «tautología», «contradicción» o «contingencia».")
    return Ejercicio("Lógica proposicional", f"Clasifica la fórmula $\\;{L.texto(f)}\\;$ como tautología, contradicción o contingencia.",
                     [("Clase", "c")], sol, {"c": t.clase}, comp)


_REGLAS = [("a ≡ b mod 3", "a \\equiv b \\pmod 3"), ("a | b", "a \\mid b"), ("a <= b", "a\\le b"),
           ("a + b es par", "a+b\\ \\text{es par}"), ("a < b", "a<b"), ("a*b > 0", "ab>0"),
           ("abs(a - b) <= 1", "|a-b|\\le1"), ("a ≡ b mod 2", "a\\equiv b\\pmod 2")]


def ej_relaciones(rnd) -> Ejercicio:
    regla, tex = rnd.choice(_REGLAS)
    A = rnd.choice([[1, 2, 3, 4, 5, 6], [1, 2, 3, 4], [2, 3, 4, 6, 8, 12], [1, 2, 4, 8]])
    R = CJ.relacion_por_regla(A, regla)
    pr = CJ.propiedades(A, R)
    claves = ["reflexiva", "simetrica", "antisimetrica", "transitiva"]
    sol = [f"- **{pr[k].nombre}**: {'sí' if pr[k].cumple else 'no'}" + (f" (contraejemplo: {pr[k].contraejemplo})" if not pr[k].cumple else "")
           for k in claves]
    eq = pr["reflexiva"].cumple and pr["simetrica"].cumple and pr["transitiva"].cumple
    orden = pr["reflexiva"].cumple and pr["antisimetrica"].cumple and pr["transitiva"].cumple
    sol.append("Es **de equivalencia**." if eq else ("Es **de orden**." if orden else "No es ni de equivalencia ni de orden."))

    def comp(r):
        fallos = [pr[k].nombre for k in claves if _si_no(r[k]) != pr[k].cumple]
        if not fallos:
            return True, "¡Perfecto, las cuatro propiedades bien!"
        return False, "Revisa: " + ", ".join(fallos) + "."
    return Ejercicio("Relaciones binarias",
                     f"En $A=\\{{{', '.join(map(str, A))}\\}}$ se define $a\\,R\\,b \\iff {tex}$. ¿Es reflexiva, simétrica, antisimétrica, transitiva? (sí/no)",
                     [("Reflexiva", "reflexiva"), ("Simétrica", "simetrica"), ("Antisimétrica", "antisimetrica"), ("Transitiva", "transitiva")],
                     sol, {k: "sí" if pr[k].cumple else "no" for k in claves}, comp)


def ej_inclusion_exclusion(rnd) -> Ejercicio:
    p, q, s = rnd.choice([(2, 3, 5), (2, 3, 7), (3, 5, 7), (2, 5, 7), (4, 6, 9)])
    N = rnd.choice([100, 120, 200, 250, 300, 500, 1000])
    real = sum(1 for k in range(1, N + 1) if k % p == 0 or k % q == 0 or k % s == 0)
    from math import lcm
    t = [N // p, N // q, N // s, N // lcm(p, q), N // lcm(p, s), N // lcm(q, s), N // lcm(p, q, s)]
    assert t[0] + t[1] + t[2] - t[3] - t[4] - t[5] + t[6] == real
    sol = [f"$|A_{{{p}}}\\cup A_{{{q}}}\\cup A_{{{s}}}| = {t[0]}+{t[1]}+{t[2]}-{t[3]}-{t[4]}-{t[5]}+{t[6]} = {real}$",
           f"Con $|A_d|=\\lfloor {N}/d\\rfloor$ y las intersecciones con el **mcm** ({lcm(p, q)}, {lcm(p, s)}, {lcm(q, s)}, {lcm(p, q, s)}).",
           f"Comprobado contando uno a uno: {real} ✔"]

    def comp(r):
        v = _entero(r["N"])
        return (True, "¡Correcto!") if v == real else (False, "No. Ojo: las intersecciones son múltiplos del **mcm**, no del producto.")
    return Ejercicio("Inclusión–exclusión", f"¿Cuántos enteros entre 1 y {N} son múltiplos de {p}, de {q} o de {s}?",
                     [("Cantidad", "N")], sol, {"N": real}, comp)


def ej_bases(rnd) -> Ejercicio:
    b = rnd.choice([2, 3, 5, 7, 8, 16])
    m = rnd.randint(40, 900)
    cif, pasos = E.a_base(m, b)
    assert int(cif, b) == m
    sol = [f"${m} = ({cif})_{{{b}}}$", "Divisiones sucesivas (los restos, de abajo arriba, son las cifras):"]
    sol += [f"- ${a} = {qq}\\cdot{b} + {rr}$" for a, qq, rr in pasos]

    def comp(r):
        t = r["c"].strip().upper().replace(" ", "")
        try:
            ok = int(t, b) == m
        except ValueError:
            return False, f"En base {b} sólo valen las cifras 0…{E.DIGITOS[b - 1]}."
        return (True, "¡Correcto!") if ok else (False, "No. Recuerda leer los restos de **abajo arriba**.")
    return Ejercicio("Sistemas de numeración", f"Escribe ${m}$ (en base 10) en base ${b}$.", [(f"Cifras en base {b}", "c")], sol, {"c": cif}, comp)


def ej_diofantica(rnd) -> Ejercicio:
    while True:
        d = rnd.choice([1, 2, 3, 4, 5, 6])
        a, b = d * rnd.randint(2, 30), d * rnd.randint(2, 30)
        if gcd(a, b) == d and a != b:
            break
    c = d * rnd.randint(-20, 40)
    D = E.diofantica(a, b, c)
    sol = [f"$\\operatorname{{mcd}}({a},{b})={d}$ divide a ${c}$ ⇒ tiene solución.",
           f"Particular (de Bézout × {c // d}): $x_0={D.x0}$, $y_0={D.y0}$.",
           f"General: $x={D.x0}+{b // d}\\lambda$, $\\ y={D.y0}-{a // d}\\lambda$, $\\lambda\\in\\mathbb Z$."]

    def comp(r):
        X, Y = _entero(r["x"]), _entero(r["y"])
        if a * X + b * Y == c:
            return True, "¡Correcto! (cualquier solución particular vale)."
        return False, f"{a}·({X}) + {b}·({Y}) = {a * X + b * Y} ≠ {c}."
    return Ejercicio("Ecuaciones diofánticas", f"Encuentra una solución entera de ${a}x + {b}y = {c}$.",
                     [("x", "x"), ("y", "y")], sol, {"x": D.x0, "y": D.y0}, comp)


def ej_inverso(rnd) -> Ejercicio:
    m = rnd.choice([7, 11, 13, 17, 19, 23, 26, 29, 31, 35, 40, 45])
    a = rnd.choice([v for v in range(2, m) if gcd(v, m) == 1])
    inv = pow(a, -1, m)
    ee = E.euclides_extendido(a, m)
    sol = [f"$\\operatorname{{mcd}}({a},{m})=1$ ⇒ existe el inverso.",
           f"Bézout: $1 = ({ee.s})\\cdot{a} + ({ee.t})\\cdot{m}$ ⇒ $\\overline{{{a}}}^{{-1}}=\\overline{{{ee.s % m}}}$.",
           f"Comprobación: ${a}\\cdot{inv} = {a * inv} \\equiv 1 \\pmod{{{m}}}$ ✔"]

    def comp(r):
        v = _entero(r["i"])
        return (True, "¡Correcto!") if (a * v) % m == 1 else (False, f"{a}·{v} = {a * v} ≡ {(a * v) % m} (mód {m}), no 1.")
    return Ejercicio("Inversos en ℤₙ", f"Calcula el inverso de $\\overline{{{a}}}$ en $\\mathbb Z_{{{m}}}$.", [("Inverso", "i")], sol, {"i": inv}, comp)


def ej_potencias(rnd) -> Ejercicio:
    m = rnd.choice([7, 9, 10, 11, 12, 13, 15, 17, 20, 100])
    a = rnd.choice([v for v in range(2, 60) if gcd(v, m) == 1])
    k = rnd.randint(50, 3000)
    from sympy import totient
    phi = int(totient(m))
    res = pow(a, k, m)
    sol = [f"$\\operatorname{{mcd}}({a},{m})=1$ y $\\varphi({m})={phi}$ ⇒ Euler: ${a}^{{{phi}}}\\equiv1$.",
           f"${k} = {k // phi}\\cdot{phi} + {k % phi}$ ⇒ ${a}^{{{k}}}\\equiv {a}^{{{k % phi}}} \\equiv {res} \\pmod{{{m}}}$."]

    def comp(r):
        v = _entero(r["r"])
        return (True, "¡Correcto!") if v % m == res else (False, f"No. Reduce el exponente módulo φ({m}) = {phi}.")
    return Ejercicio("Fermat y Euler", f"Calcula el resto de dividir ${a}^{{{k}}}$ entre ${m}$.", [("Resto", "r")], sol, {"r": res}, comp)


def ej_aplicaciones(rnd) -> Ejercicio:
    k = rnd.randint(2, 4)
    m = rnd.randint(k, 6)
    tot, iny = m ** k, sp.ff(m, k)
    sob = sum((-1) ** i * comb(m, i) * (m - i) ** k for i in range(m + 1))
    from itertools import product
    fb = list(product(range(m), repeat=k))
    assert len(fb) == tot and sum(len(set(f)) == k for f in fb) == iny and sum(len(set(f)) == m for f in fb) == sob
    sol = [f"Todas: cada uno de los ${k}$ elementos de $A$ elige imagen entre ${m}$: ${m}^{{{k}}}={tot}$.",
           f"Inyectivas: ${m}\\cdot{m - 1}\\cdots$ (${k}$ factores) $=\\frac{{{m}!}}{{{m - k}!}}={iny}$.",
           f"Sobreyectivas: {'como ' + str(k) + ' = ' + str(m) + ', son las biyectivas: ' + str(k) + '! = ' + str(sob) if k == m else 'imposible porque |A| < |B|, hay 0' if k < m else ''}.",
           f"Comprobado enumerando las {tot} aplicaciones ✔"]

    def comp(r):
        a, b, c = _entero(r["t"]), _entero(r["i"]), _entero(r["s"])
        mal = [nom for nom, v, w in (("todas", a, tot), ("inyectivas", b, iny), ("sobreyectivas", c, sob)) if v != w]
        return (True, "¡Perfecto!") if not mal else (False, "Revisa: " + ", ".join(mal) + ".")
    return Ejercicio("Aplicaciones entre conjuntos finitos",
                     f"Sean $|A|={k}$ y $|B|={m}$. ¿Cuántas aplicaciones $A\\to B$ hay? ¿Cuántas inyectivas? ¿Cuántas sobreyectivas?",
                     [("Todas", "t"), ("Inyectivas", "i"), ("Sobreyectivas", "s")], sol, {"t": tot, "i": iny, "s": sob}, comp)


# ======================================================================= ANÁLISIS
def ej_serie(rnd) -> Ejercicio:
    p = rnd.choice([sp.Rational(1, 2), 1, sp.Rational(3, 2), 2, 3])
    a = rnd.randint(1, 5)
    b = rnd.choice([2, 3, 5])
    plantillas = [
        (1 / n ** p, bool(p > 1), f"Armónica generalizada con $p={sp.latex(p)}$: converge ⇔ $p>1$."),
        ((n + a) / (n ** 3 + b), True, "Equivale a $\\frac1{n^2}$ (comparación por paso al límite) ⇒ converge."),
        ((n + a) / (n ** 2 + b), False, "Equivale a $\\frac1n$ ⇒ diverge."),
        (n ** a / b ** n, True, f"Cociente: $\\frac{{a_{{n+1}}}}{{a_n}}\\to\\frac1{{{b}}}<1$ ⇒ converge."),
        (b ** n / sp.factorial(n), True, "Cociente: $\\frac{b}{n+1}\\to0<1$ ⇒ converge."),
        (sp.factorial(n) / b ** n, False, "El término general no tiende a 0 ($\\frac{n+1}{b}\\to\\infty$) ⇒ diverge."),
        (n / (n + a), False, "El término general tiende a 1 ≠ 0 ⇒ diverge (condición necesaria)."),
        (sp.sin(sp.Integer(1) / n ** 2), True, "$\\operatorname{sen}\\frac1{n^2}\\equiv\\frac1{n^2}$ ⇒ converge."),
        (1 / (n * sp.log(n + 1)), False, "Condensación (o integral): como $\\frac1{n\\ln n}$ ⇒ diverge."),
        ((sp.Integer(a) / (a + 1)) ** n, True, f"Geométrica de razón $\\frac{{{a}}}{{{a + 1}}}<1$ ⇒ converge."),
    ]
    t, conv, pista = rnd.choice(plantillas)
    sol = [f"**{'Converge' if conv else 'Diverge'}**.", pista]

    def comp(r):
        d = r["c"].strip().lower().rstrip(".")
        if d in ("converge", "convergente", "conv"):
            v = True
        elif d in ("diverge", "divergente", "div"):
            v = False
        else:
            raise ErrorLectura("Responde «converge» o «diverge».")
        return (True, "¡Correcto!") if v == conv else (False, "No. " + pista)
    return Ejercicio("Carácter de una serie", f"Estudia el carácter de $\\displaystyle\\sum_{{n\\ge1}} {sp.latex(t)}$ (converge / diverge).",
                     [("Carácter", "c")], sol, {"c": "converge" if conv else "diverge"}, comp)


def ej_radio(rnd) -> Ejercicio:
    k = rnd.choice([2, 3, 4, 5])
    p = rnd.choice([0, 1, 2])
    tipo = rnd.choice(["k", "1/k", "inf"])
    if tipo == "k":
        c = n ** p / k ** n
        R = sp.Integer(k)
    elif tipo == "1/k":
        c = k ** n * n ** p
        R = sp.Rational(1, k)
    else:
        c = 1 / sp.factorial(n)
        R = sp.oo
    sol = [f"$R = {sp.latex(R)}$.",
           "Cauchy–Hadamard: $\\frac1R=\\lim\\sqrt[n]{|c_n|}$ (o el cociente $\\left|\\frac{c_{n+1}}{c_n}\\right|$). Los factores $n^p$ no cambian el radio."]

    def comp(r):
        v = leer(r["R"])
        ok = (v == sp.oo) if R == sp.oo else (v != sp.oo and _iguales(r["R"], R))
        return (True, "¡Correcto!") if ok else (False, "No. Calcula $\\lim|c_{n+1}/c_n|$ y toma el inverso.")
    return Ejercicio("Radio de convergencia", f"Calcula el radio de convergencia de $\\displaystyle\\sum_{{n\\ge1}} {sp.latex(c)}\\,x^n$ (escribe `oo` si es infinito).",
                     [("R", "R")], sol, {"R": R}, comp)


def ej_area(rnd) -> Ejercicio:
    a = rnd.randint(-3, 1)
    b = a + rnd.randint(2, 4)
    k = rnd.choice([1, 2, 3])
    g = sp.expand(k * x + rnd.randint(-2, 2))
    f = sp.expand(g - (x - a) * (x - b))       # f ≥ g en [a, b]
    A = sp.integrate(f - g, (x, a, b))
    assert A == sp.Rational((b - a) ** 3, 6)
    prod = sp.latex(sp.factor(f - g))
    sol = [f"Cortes: $f-g={prod}=0$ ⇒ $x={a}$, $x={b}$.",
           f"En medio $f\\ge g$: $\\displaystyle A=\\int_{{{a}}}^{{{b}}}(f-g)\\,dx=\\int_{{{a}}}^{{{b}}}{prod}\\,dx={sp.latex(A)}$"]

    def comp(r):
        return (True, "¡Correcto!") if _iguales(r["A"], A) else (False, "No. Calcula los cortes y integra (curva de arriba − curva de abajo).")
    return Ejercicio("Área entre curvas", f"Calcula el área encerrada entre $f(x)={sp.latex(f)}$ y $g(x)={sp.latex(g)}$.",
                     [("Área", "A")], sol, {"A": A}, comp)


def ej_recurrente(rnd) -> Ejercicio:
    Lm = rnd.choice([2, 3, 4, 5])
    c = Lm * Lm - Lm
    sol = [f"Converge (acotada por ${Lm}$ y creciente, ambas cosas por inducción).",
           f"El límite cumple $\\ell=\\sqrt{{{c}+\\ell}}$ ⇒ $\\ell^2-\\ell-{c}=0$ ⇒ $\\ell={Lm}$ (la otra raíz, ${1 - Lm}$, es negativa)."]

    def comp(r):
        return (True, "¡Correcto!") if _iguales(r["L"], sp.Integer(Lm)) else (False, "Plantea ℓ = g(ℓ) y descarta la raíz que no puede ser.")
    return Ejercicio("Sucesiones recurrentes", f"$x_1=1$, $x_{{n+1}}=\\sqrt{{{c}+x_n}}$. Sabiendo que converge, calcula su límite.",
                     [("Límite", "L")], sol, {"L": Lm}, comp)


def ej_limite_sucesion(rnd) -> Ejercicio:
    a = rnd.choice([1, 2, 3, -1, -2])
    b = rnd.choice([1, 2, 3])
    c = rnd.choice([2, 3, 4])
    plantillas = [
        ((1 + sp.Integer(a) / n) ** (b * n), sp.exp(a * b), "Tipo $1^\\infty$: $e^{\\lim bn\\cdot a/n}$."),
        ((c * n ** 2 + n) / (b * n ** 2 + a + 10), sp.Rational(c, b), "Cociente de polinomios del mismo grado: cociente de coeficientes líderes."),
        (sp.sqrt(n ** 2 + c * n) - n, sp.Rational(c, 2), "Multiplica y divide por el conjugado."),
        (n * sp.sin(sp.Integer(c) / n), sp.Integer(c), "Equivalencia $\\operatorname{sen}\\frac cn\\equiv\\frac cn$."),
        (((n + a + 5) / (n + b)) ** n, sp.exp(a + 5 - b), "Tipo $1^\\infty$: $e^{\\lim n(\\frac{n+a}{n+b}-1)}$."),
    ]
    t, Lv, pista = rnd.choice(plantillas)
    assert sp.simplify(sp.limit(t, n, sp.oo) - Lv) == 0
    sol = [f"$\\lim {sp.latex(t)} = {sp.latex(Lv)}$", pista]

    def comp(r):
        return (True, "¡Correcto!") if _iguales(r["L"], Lv) else (False, "No. " + pista)
    return Ejercicio("Límites de sucesiones", f"Calcula $\\displaystyle\\lim_{{n\\to\\infty}} {sp.latex(t)}$", [("Límite", "L")], sol, {"L": Lv}, comp)


def ej_impropia(rnd) -> Ejercicio:
    p = rnd.choice([sp.Rational(1, 2), 1, sp.Rational(3, 2), 2, 3, 4])
    a = rnd.choice([1, 2])
    conv = bool(p > 1)
    V = sp.integrate(x ** -p, (x, a, sp.oo)) if conv else sp.oo
    sol = [f"$\\int_{a}^\\infty x^{{-s}}dx$ converge ⇔ $s>1$; aquí $s={sp.latex(p)}$.",
           f"Valor: ${sp.latex(V)}$" if conv else "Diverge a $+\\infty$."]

    def comp(r):
        t = r["V"].strip().lower()
        if t.startswith("div") or t in ("oo", "inf", "infinito", "+oo"):
            return (True, "¡Correcto, diverge!") if not conv else (False, f"Converge, porque s = {p} > 1.")
        if not conv:
            return False, f"Diverge, porque s = {p} ≤ 1."
        return (True, "¡Correcto!") if _iguales(r["V"], V) else (False, "Converge, pero el valor no es ese: haz el límite de la primitiva.")
    return Ejercicio("Integrales impropias", f"Calcula $\\displaystyle\\int_{{{a}}}^{{+\\infty}} \\frac{{dx}}{{x^{{{sp.latex(p)}}}}}$ (escribe «diverge» si diverge).",
                     [("Valor", "V")], sol, {"V": V}, comp)


def ej_complejos(rnd) -> Ejercicio:
    a, b = rnd.choice([(1, 1), (1, -1), (-1, 1), (0, 2), (2, 0), (1, sp.sqrt(3)), (sp.sqrt(3), 1)])
    k = rnd.choice([3, 4, 6, 8])
    z = a + b * sp.I
    w = sp.simplify(sp.expand(z ** k))
    r, th = sp.Abs(z), sp.arg(z)
    sol = [f"$z={sp.latex(z)}$: módulo $r={sp.latex(r)}$, argumento $\\theta={sp.latex(th)}$.",
           f"De Moivre: $z^{{{k}}}=r^{{{k}}}(\\cos{k}\\theta+i\\operatorname{{sen}}{k}\\theta)={sp.latex(w)}$."]

    def comp(r_):
        v = leer(re.sub(r"(?<![a-zA-Z])i(?![a-zA-Z])", "I", r_["w"]))
        return (True, "¡Correcto!") if sp.simplify(sp.expand(v - w)) == 0 else (False, "No. Pasa a forma polar y usa De Moivre.")
    return Ejercicio("Números complejos", f"Calcula $({sp.latex(z)})^{{{k}}}$ en forma binómica.", [("Resultado", "w")], sol, {"w": w}, comp)


NUEVOS = {
    "Matemática finita": {
        "Lógica proposicional": ej_logica,
        "Aplicaciones": ej_aplicaciones,
        "Relaciones binarias": ej_relaciones,
        "Inclusión–exclusión": ej_inclusion_exclusion,
        "Sistemas de numeración": ej_bases,
        "Ecuaciones diofánticas": ej_diofantica,
        "Inversos en ℤₙ": ej_inverso,
        "Fermat y Euler": ej_potencias,
    },
    "Análisis": {
        "Números complejos": ej_complejos,
        "Límites de sucesiones": ej_limite_sucesion,
        "Sucesiones recurrentes": ej_recurrente,
        "Carácter de una serie": ej_serie,
        "Radio de convergencia": ej_radio,
        "Área entre curvas": ej_area,
        "Integrales impropias": ej_impropia,
    },
}
