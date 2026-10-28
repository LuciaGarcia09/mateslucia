"""Generador de ejercicios tipo examen con corrección automática.

Cada ejercicio se construye AL REVÉS (primero la solución, luego el enunciado),
así la solución es correcta por construcción y además se recalcula con el
núcleo para comprobarla.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import random
from math import gcd, comb
import sympy as sp

from .parsing import x, leer, ErrorLectura
from . import polinomios as P
from . import enteros as E
from . import combinatoria as C


@dataclass
class Ejercicio:
    tema: str
    enunciado: str                         # markdown con LaTeX
    campos: list[tuple[str, str]]          # (etiqueta, clave)
    solucion: list[str]                    # líneas markdown/LaTeX
    _correctas: dict = field(default_factory=dict)
    _comprobador: object = None

    def corregir(self, respuestas: dict) -> tuple[bool, str]:
        try:
            return self._comprobador(respuestas)
        except ErrorLectura as exc:
            return False, str(exc)
        except Exception as exc:  # noqa: BLE001
            return False, f"No he podido leer tu respuesta: {exc}"


def _iguales(expr_txt: str, correcta) -> bool:
    from .analisis import son_iguales
    v = leer(expr_txt)
    if isinstance(v, sp.core.relational.Relational):
        raise ErrorLectura("Escribe sólo el resultado, sin «=».")
    return son_iguales(v, correcta)


def _poly_aleatorio(rnd, grado, coef=5, monico=False):
    c = [rnd.randint(-coef, coef) for _ in range(grado + 1)]
    c[0] = 1 if monico else rnd.choice([v for v in range(-3, 4) if v != 0])
    return sp.expand(sum(ci * x ** (grado - i) for i, ci in enumerate(c)))


# ----------------------------------------------------------------- finita
def ej_division(rnd) -> Ejercicio:
    K = P.Cuerpo()
    B = _poly_aleatorio(rnd, rnd.choice([1, 2]), 4, monico=True)
    Q = _poly_aleatorio(rnd, rnd.choice([2, 3]), 4)
    gB = sp.degree(B, x)
    R = _poly_aleatorio(rnd, gB - 1, 6) if gB > 1 else sp.Integer(rnd.randint(-9, 9))
    A = sp.expand(Q * B + R)
    d = P.division(P.desde_expr(A, K), P.desde_expr(B, K), K)
    assert P.a_expr(d.cociente) == sp.expand(Q) and P.a_expr(d.resto) == sp.expand(R)
    sol = [f"Cociente $q(x) = {sp.latex(Q)}$, resto $r(x) = {sp.latex(R)}$."]
    for i, paso in enumerate(d.pasos, 1):
        t = paso.termino_coef * x ** paso.termino_grado
        sol.append(f"Paso {i}: líder del resto ÷ líder del divisor $= {sp.latex(t)}$; restamos "
                   f"${sp.latex(t)}\\cdot({sp.latex(B)}) = {sp.latex(P.a_expr(paso.restado))}$ "
                   f"y queda ${sp.latex(P.a_expr(paso.resto_despues))}$.")
    sol.append(f"Comprobación: $q\\cdot B + r = {sp.latex(sp.expand(Q * B + R))} = A$ ✔")

    def comp(r):
        ok_q = _iguales(r["q"], Q)
        ok_r = _iguales(r["r"], R)
        if ok_q and ok_r:
            return True, "¡Perfecto! Cociente y resto correctos."
        return False, ("El cociente está bien pero el resto no." if ok_q else
                       "El resto está bien pero el cociente no." if ok_r else
                       "Ni cociente ni resto coinciden. Revisa el primer paso de la división.")
    return Ejercicio("División euclídea de polinomios",
                     f"Calcula el cociente y el resto de dividir $A(x) = {sp.latex(A)}$ entre $B(x) = {sp.latex(B)}$ en $\\mathbb{{Q}}[x]$.",
                     [("Cociente q(x)", "q"), ("Resto r(x)", "r")], sol, {"q": Q, "r": R}, comp)


def ej_mcd_polinomios(rnd) -> Ejercicio:
    K = P.Cuerpo()
    raices = rnd.sample(range(-4, 5), 4)
    G = sp.expand(sp.prod([x - r for r in raices[:2]]))
    A = sp.expand(G * (x - raices[2]) * rnd.choice([1, 2, -1]))
    B = sp.expand(G * (x ** 2 + rnd.randint(1, 4)))
    res = P.mcd_extendido(P.desde_expr(A, K), P.desde_expr(B, K), K)
    assert P.a_expr(res.mcd) == G
    sol = [f"$\\operatorname{{mcd}}(A,B) = {sp.latex(G)} = {sp.latex(sp.factor(G))}$ (mónico)."]
    for i, f in enumerate(res.filas, 1):
        sol.append(f"División {i}: ${sp.latex(P.a_expr(f.dividendo))} = ({sp.latex(P.a_expr(f.cociente))})"
                   f"\\cdot({sp.latex(P.a_expr(f.divisor))}) + ({sp.latex(P.a_expr(f.resto))})$")
    sol.append("El último resto no nulo, dividido entre su coeficiente líder, es el mcd.")
    sol.append(f"Atajo para comprobar: $A = {sp.latex(sp.factor(A))}$, $B = {sp.latex(sp.factor(B))}$.")

    def comp(r):
        v = sp.Poly(leer(r["mcd"]), x)
        if v.is_zero:
            return False, "El mcd no puede ser 0."
        if sp.expand(v.monic().as_expr() - G) == 0:
            if v.LC() != 1:
                return True, "Correcto salvo constante; recuerda que el convenio es darlo MÓNICO (coef. líder 1)."
            return True, "¡Correcto!"
        return False, "No es el mcd. Comprueba que tu polinomio divide a A y a B."
    return Ejercicio("MCD de polinomios",
                     f"Calcula el máximo común divisor de $A(x) = {sp.latex(A)}$ y $B(x) = {sp.latex(B)}$ "
                     f"con el algoritmo de Euclides.",
                     [("mcd(A, B)", "mcd")], sol, {"mcd": G}, comp)


def ej_bezout(rnd) -> Ejercicio:
    while True:
        a, b = rnd.randint(40, 400), rnd.randint(20, 300)
        if a != b and gcd(a, b) not in (a, b):
            break
    ee = E.euclides_extendido(a, b)
    sol = [f"$d = \\operatorname{{mcd}}({a},{b}) = {ee.d}$ y una identidad de Bézout es "
           f"${ee.d} = ({ee.s})\\cdot {a} + ({ee.t})\\cdot {b}$."]
    sol.append("| a | b | q | r | s | t |\n|---|---|---|---|---|---|\n" +
               "\n".join(f"| {f.a} | {f.b} | {f.q} | {f.r} | {f.s} | {f.t} |" for f in ee.filas))
    sol.append(f"Hay infinitas parejas: $s + {b // ee.d}\\lambda,\\ t - {a // ee.d}\\lambda$.")

    def comp(r):
        d, s, t = int(leer(r["d"])), int(leer(r["s"])), int(leer(r["t"]))
        if d != ee.d:
            return False, f"El mcd no es {d}."
        if s * a + t * b != d:
            return False, f"El mcd está bien, pero {s}·{a} + {t}·{b} = {s * a + t * b} ≠ {d}."
        return True, "¡Correcto! (cualquier pareja (s, t) válida cuenta)."
    return Ejercicio("Euclides extendido (enteros)",
                     f"Calcula $d = \\operatorname{{mcd}}({a}, {b})$ y enteros $s, t$ con $d = s\\cdot {a} + t\\cdot {b}$.",
                     [("d", "d"), ("s", "s"), ("t", "t")], sol, {"d": ee.d, "s": ee.s, "t": ee.t}, comp)


def ej_congruencia(rnd) -> Ejercicio:
    m = rnd.choice([12, 15, 18, 20, 21, 24, 26, 28, 35, 36])
    a = rnd.randint(2, m - 1)
    d = gcd(a, m)
    x0 = rnd.randint(0, m - 1)
    b = (a * x0) % m  # garantiza solución
    c = E.congruencia_lineal(a, b, m)
    sols = c.soluciones
    sol = [f"$\\operatorname{{mcd}}({a},{m}) = {d}$ divide a ${b}$, así que hay ${d}$ soluciones módulo ${m}$."]
    if d > 1:
        sol.append(f"Dividimos todo entre {d}: ${a // d}x \\equiv {b // d} \\pmod{{{m // d}}}$.")
    sol.append(f"Inverso de ${a // d}$ módulo ${m // d}$: ${c.inverso}$ (porque ${a // d}\\cdot{c.inverso} \\equiv 1$).")
    sol.append(f"$x \\equiv {c.sol_base} \\pmod{{{m // d}}}$, es decir $x \\in \\{{{', '.join(map(str, sols))}\\}}$ módulo ${m}$.")

    def comp(r):
        trozos = [t for t in r["x"].replace(";", ",").split(",") if t.strip()]
        if not trozos:
            return False, "Escribe al menos una solución."
        dadas = sorted(set(int(leer(t)) % m for t in trozos))
        if dadas == sorted(sols):
            return True, "¡Correcto, todas las soluciones!"
        faltan = sorted(set(sols) - set(dadas))
        sobran = sorted(set(dadas) - set(sols))
        msg = []
        if faltan:
            msg.append(f"te faltan {len(faltan)} solución(es)")
        if sobran:
            msg.append(f"sobran {sobran} (no cumplen la congruencia)")
        return False, "Casi: " + " y ".join(msg) + "."
    return Ejercicio("Congruencia lineal",
                     f"Resuelve ${a}x \\equiv {b} \\pmod{{{m}}}$. Da TODAS las soluciones entre 0 y {m - 1}, separadas por comas.",
                     [("Soluciones", "x")], sol, {"x": ", ".join(map(str, sols))}, comp)


def ej_tcr(rnd) -> Ejercicio:
    mods = rnd.choice([[3, 5, 7], [4, 5, 9], [5, 7, 8], [3, 7, 11], [4, 9, 5], [7, 9, 10]])
    X = rnd.randint(1, mods[0] * mods[1] * mods[2] - 1)
    restos = [X % m for m in mods]
    t = E.chino_del_resto(restos, mods)
    assert t.x == X
    M = mods[0] * mods[1] * mods[2]
    sol = [f"Los módulos son coprimos dos a dos, solución única módulo ${M}$: $x \\equiv {X} \\pmod{{{M}}}$."]
    sol += [f"- {p.explicacion}" for p in t.pasos]
    sistema = " \\\\ ".join(f"x \\equiv {a} \\pmod{{{m}}}" for a, m in zip(restos, mods))

    def comp(r):
        v = int(leer(r["x"]))
        if all(v % m == a for a, m in zip(restos, mods)):
            return True, f"¡Correcto! (la solución general es {X} + {M}k)."
        return False, "Ese número no cumple todas las congruencias."
    return Ejercicio("Teorema chino del resto",
                     f"Resuelve el sistema $\\begin{{cases}} {sistema} \\end{{cases}}$",
                     [("x", "x")], sol, {"x": X}, comp)


_HISTORIAS = {
    # (objetos distintos, cajas distintas, condición): plantilla
    (True, True, "libre"): "¿De cuántas formas se pueden repartir {k} libros DISTINTOS entre {n} estudiantes (alguno puede quedarse sin ninguno)?",
    (True, True, "inyectiva"): "¿De cuántas formas se pueden sentar {k} personas en {n} sillas numeradas (una persona por silla)?",
    (True, True, "sobreyectiva"): "¿De cuántas formas se pueden asignar {k} tareas DISTINTAS a {n} becarios si todos deben recibir al menos una?",
    (True, False, "sobreyectiva"): "¿De cuántas formas se pueden dividir {k} personas en {n} grupos de trabajo (sin nombre) no vacíos?",
    (True, False, "libre"): "¿De cuántas formas se pueden meter {k} canicas de colores DISTINTOS en {n} bolsas IGUALES (puede haber bolsas vacías)?",
    (False, True, "libre"): "¿De cuántas formas se pueden repartir {k} caramelos IGUALES entre {n} niños?",
    (False, True, "sobreyectiva"): "¿De cuántas formas se pueden repartir {k} caramelos IGUALES entre {n} niños si cada niño recibe al menos uno?",
    (False, True, "inyectiva"): "¿De cuántas formas se pueden colocar {k} fichas IGUALES en un tablero de {n} casillas (como mucho una por casilla)?",
    (False, False, "sobreyectiva"): "¿De cuántas formas se puede escribir {k} como suma de exactamente {n} enteros positivos (sin importar el orden)?",
}


def ej_combinatoria(rnd) -> Ejercicio:
    clave = rnd.choice(list(_HISTORIAS))
    D, Cj, cond = clave
    if cond == "inyectiva":
        n = rnd.randint(5, 9)
        k = rnd.randint(2, n - 1)
    elif cond == "sobreyectiva":
        n = rnd.randint(2, 4)
        k = rnd.randint(n + 1, n + 4)
    else:
        n = rnd.randint(2, 5)
        k = rnd.randint(3, 7)
    caso = C.doce_formas(k, n, D, Cj, cond)
    fb = C.doce_formas_fuerza_bruta(k, n, D, Cj, cond)
    assert fb is None or fb == caso.numero
    sol = [f"**{caso.nombre}**: ${caso.formula_tex}$ con $k = {k}$ objetos y $n = {n}$ cajas → **{caso.numero}**.",
           f"Por qué: {caso.porque}", f"Por qué no otra: {caso.otras}"]
    if fb is not None:
        sol.append(f"Comprobado enumerando todos los casos por ordenador: {fb} ✔")

    def comp(r):
        v = leer(r["N"])
        if sp.simplify(v - caso.numero) == 0:
            return True, "¡Correcto!"
        return False, "No es esa cifra. Pregúntate: ¿los objetos se distinguen? ¿las cajas? ¿puede quedar alguna vacía?"
    return Ejercicio("Combinatoria", _HISTORIAS[clave].format(k=k, n=n), [("Número de formas", "N")], sol, {"N": caso.numero}, comp)


# ----------------------------------------------------------------- análisis
def ej_limite(rnd) -> Ejercicio:
    a = rnd.choice([1, 2, 3, -1, -2])
    b = rnd.choice([2, 3, 4, 5])
    c = rnd.choice([2, 3, 5])
    plantillas = [
        ((x ** 2 - a ** 2) / (x - a), a, "Indeterminación 0/0: factoriza el numerador (diferencia de cuadrados) y simplifica."),
        (sp.sin(b * x) / (c * x), 0, "Usa el límite notable $\\lim_{t\\to0}\\frac{\\operatorname{sen} t}{t} = 1$ (o equivalencias: sen(bx) ~ bx)."),
        ((1 + sp.Integer(b) / x) ** x, sp.oo, "Indeterminación $1^\\infty$: $\\lim (1 + b/x)^x = e^b$."),
        ((c * x ** 2 + b * x) / (b * x ** 2 - 1), sp.oo, "Cociente de polinomios del mismo grado: cociente de coeficientes líderes."),
        ((sp.exp(b * x) - 1) / x, 0, "Equivalencia $e^t - 1 \\sim t$ cuando $t \\to 0$, o L'Hôpital."),
        ((sp.sqrt(x + c ** 2) - c) / x, 0, "Multiplica y divide por el conjugado $\\sqrt{x + c^2} + c$."),
        (sp.log(1 + b * x) / (c * x), 0, "Equivalencia $\\ln(1+t) \\sim t$."),
        ((1 - sp.cos(x)) / x ** 2, 0, "Equivalencia $1 - \\cos t \\sim t^2/2$."),
    ]
    f, p, pista = rnd.choice(plantillas)
    L = sp.limit(f, x, p)
    p_tex = "+\\infty" if p == sp.oo else sp.latex(p)
    sol = [f"$\\displaystyle\\lim_{{x\\to {p_tex}}} {sp.latex(f)} = {sp.latex(L)}$", f"Idea: {pista}"]

    def comp(r):
        if _iguales(r["L"], L):
            return True, "¡Correcto!"
        return False, "No. " + pista
    return Ejercicio("Límites", f"Calcula $\\displaystyle\\lim_{{x\\to {p_tex}}} {sp.latex(f)}$", [("Límite", "L")], sol, {"L": L}, comp)


def ej_derivada(rnd) -> Ejercicio:
    a = rnd.randint(2, 5)
    b = rnd.randint(1, 4)
    plantillas = [
        x ** a * sp.exp(b * x),
        sp.log(x ** 2 + b),
        sp.sin(a * x) * sp.cos(b * x),
        (x ** 2 + b) / (x - a),
        sp.atan(a * x),
        sp.sqrt(x ** 2 + b) * x,
        sp.exp(sp.sin(b * x)),
    ]
    f = rnd.choice(plantillas)
    from .analisis import explicar_derivada, mas_simple
    df = mas_simple(sp.diff(f, x))
    sol = [f"$f'(x) = {sp.latex(df)}$"] + [f"${l}$" for l in explicar_derivada(f, 0, 1)]

    def comp(r):
        if _iguales(r["d"], df):
            return True, "¡Correcto! (da igual cómo la hayas simplificado)."
        return False, "No coincide. Identifica primero la regla principal: ¿suma, producto, cociente o cadena?"
    return Ejercicio("Derivadas", f"Deriva $f(x) = {sp.latex(f)}$", [("f'(x)", "d")], sol, {"d": df}, comp)


def ej_integral(rnd) -> Ejercicio:
    a = rnd.randint(1, 4)
    b = rnd.randint(1, 3)
    plantillas = [
        (x * sp.exp(a * x), 0, 1, "Por partes: $u = x$, $dv = e^{ax}dx$."),
        (x ** 2 + b * x, 0, a, "Polinomio: integral inmediata término a término (regla de Barrow)."),
        (1 / (x + a), 0, b, "Inmediata tipo logaritmo: $\\int \\frac{dx}{x+a} = \\ln|x+a|$."),
        (x * sp.cos(x), 0, sp.pi, "Por partes: $u = x$, $dv = \\cos x\\,dx$."),
        (2 * x / (x ** 2 + a), 0, 1, "Cambio $t = x^2 + a$: es $\\frac{u'}{u}$."),
        (sp.exp(-x), 0, sp.oo, "Impropia: calcula $\\lim_{M\\to\\infty}\\int_0^M e^{-x}dx$."),
    ]
    f, lo, hi, pista = rnd.choice(plantillas)
    F = sp.integrate(f, x)
    V = sp.simplify(sp.integrate(f, (x, lo, hi)))
    hi_tex = "+\\infty" if hi == sp.oo else sp.latex(hi)
    sol = [f"Primitiva: $F(x) = {sp.latex(F)}$", f"$\\displaystyle\\int_{{{sp.latex(lo)}}}^{{{hi_tex}}} {sp.latex(f)}\\,dx = {sp.latex(V)}$",
           f"Idea: {pista}"]

    def comp(r):
        if _iguales(r["I"], V):
            return True, "¡Correcto!"
        return False, "No. " + pista
    return Ejercicio("Integrales", f"Calcula $\\displaystyle\\int_{{{sp.latex(lo)}}}^{{{hi_tex}}} {sp.latex(f)}\\,dx$",
                     [("Valor", "I")], sol, {"I": V}, comp)


def ej_taylor(rnd) -> Ejercicio:
    f = rnd.choice([sp.exp(x), sp.sin(x), sp.cos(x), sp.log(1 + x), 1 / (1 - x), sp.sqrt(1 + x)])
    orden = rnd.choice([3, 4])
    T = sp.series(f, x, 0, orden + 1).removeO()
    sol = [f"$T_{orden}(x) = {sp.latex(T)}$",
           f"Coeficientes: $\\dfrac{{f^{{(k)}}(0)}}{{k!}}$ para $k = 0, …, {orden}$."]

    def comp(r):
        if _iguales(r["T"], T):
            return True, "¡Correcto!"
        return False, "No coincide. Calcula f(0), f'(0), f''(0)… y divide cada una entre k!."
    return Ejercicio("Taylor", f"Escribe el polinomio de Taylor de orden {orden} de $f(x) = {sp.latex(f)}$ en $x = 0$.",
                     [(f"T_{orden}(x)", "T")], sol, {"T": T}, comp)


GENERADORES = {
    "Matemática finita": {
        "División de polinomios": ej_division,
        "MCD de polinomios": ej_mcd_polinomios,
        "Euclides extendido / Bézout": ej_bezout,
        "Congruencias lineales": ej_congruencia,
        "Teorema chino del resto": ej_tcr,
        "Combinatoria (12 formas)": ej_combinatoria,
    },
    "Análisis": {
        "Límites": ej_limite,
        "Derivadas": ej_derivada,
        "Integrales": ej_integral,
        "Polinomios de Taylor": ej_taylor,
    },
}


def _registrar_nuevos():
    from .ejercicios2 import NUEVOS
    for asig, d in NUEVOS.items():
        GENERADORES[asig].update(d)


_registrar_nuevos()

# Qué ejercicios se practican en cada tema (id del tema → nombres de GENERADORES)
POR_TEMA = {
    "f1": ["Lógica proposicional"],
    "f2": ["Aplicaciones"],
    "f3": ["Relaciones binarias"],
    "f4": ["Combinatoria (12 formas)", "Inclusión–exclusión"],
    "f5": ["Euclides extendido / Bézout", "Sistemas de numeración"],
    "f6": ["División de polinomios", "MCD de polinomios"],
    "f7": ["Ecuaciones diofánticas", "Congruencias lineales", "Inversos en ℤₙ", "Fermat y Euler", "Teorema chino del resto"],
    "a1": ["Números complejos"],
    "a2": ["Límites"],
    "a3": ["Derivadas", "Polinomios de Taylor"],
    "a4": ["Integrales", "Área entre curvas", "Integrales impropias"],
    "a5": ["Límites de sucesiones", "Sucesiones recurrentes"],
    "a6": ["Carácter de una serie"],
    "a7": ["Radio de convergencia"],
}


def generar(asignatura: str, tema: str, semilla: int | None = None) -> Ejercicio:
    rnd = random.Random(semilla)
    return GENERADORES[asignatura][tema](rnd)
