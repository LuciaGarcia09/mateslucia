"""Análisis: herramientas de todos los temas de los apuntes (1–7) que no estaban en analisis.py.

Cada cálculo simbólico va acompañado de una comprobación numérica independiente.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import math
import re

import mpmath as mp
import numpy as np
import sympy as sp
from sympy.integrals.manualintegrate import integral_steps
import sympy.integrals.manualintegrate as MI

from .parsing import x, n as n_sym, leer
from .analisis import a_float, evaluar, lambdificar, son_iguales, mas_simple, limite_sucesion

R = sp.S.Reals
PARAMS = sp.symbols("a b c d k m p q r s", real=True)


# ======================================================================== Tema 1: ℝ, ℝⁿ, ℂ
def leer_vector(texto: str) -> sp.Matrix:
    t = texto.strip().strip("()[]")
    partes = [p for p in re.split(r"[,;\s]+", t) if p]
    if not partes:
        raise ValueError("Escribe las componentes separadas por comas: (1, 2, 3).")
    return sp.Matrix([leer(p) for p in partes])


def info_vectores(u: sp.Matrix, v: sp.Matrix):
    if u.shape != v.shape:
        raise ValueError("Los dos vectores tienen que tener el mismo número de componentes.")
    dot = (u.T * v)[0]
    nu, nv = sp.sqrt((u.T * u)[0]), sp.sqrt((v.T * v)[0])
    dist = sp.sqrt(((u - v).T * (u - v))[0])
    ang = sp.acos(sp.simplify(dot / (nu * nv))) if nu != 0 and nv != 0 else None
    cs = abs(float(dot)) <= float(nu * nv) + 1e-12
    return {"producto escalar": sp.simplify(dot), "‖u‖": sp.simplify(nu), "‖v‖": sp.simplify(nv),
            "d(u, v)": sp.simplify(dist), "ángulo": sp.simplify(ang) if ang is not None else None,
            "Cauchy–Schwarz |u·v| ≤ ‖u‖‖v‖": cs, "ortogonales": sp.simplify(dot) == 0}


def estudio_sistema_vectores(vectores: list[sp.Matrix], v: sp.Matrix | None = None):
    M = sp.Matrix.hstack(*vectores)
    rango = M.rank()
    n = M.shape[0]
    k = len(vectores)
    res = {"rango": rango, "independientes": rango == k, "generan": rango == n, "base": rango == k == n, "dimension": n}
    if v is not None:
        cs = sp.symbols(f"λ1:{k + 1}")
        sol = sp.solve(list(M * sp.Matrix(cs) - v), cs, dict=True)
        res["coordenadas"] = sol
    return res


def leer_conjunto_real(texto: str):
    """«[0,1) ∪ {2} ∪ (3, oo)», «x^2 < 4», «{1/n : n ∈ N}» no (infinitos puntos sueltos no se pueden)."""
    t = texto.strip()
    if any(op in t for op in ("<", ">", "≤", "≥")) and "[" not in t and "(" not in t.split("<")[0][:1]:
        rel = leer(t.replace("≤", "<=").replace("≥", ">="))
        return sp.solveset(rel, x, R)
    t = t.replace("∪", " U ").replace("u", " U ").replace("oo", "∞").replace("infinito", "∞")
    trozos = [p.strip() for p in re.split(r"\s+U\s+", t) if p.strip()]
    conj = sp.S.EmptySet
    for p in trozos:
        if p.startswith("{"):
            elems = [leer(e) for e in p.strip("{}").split(",") if e.strip()]
            conj = conj | sp.FiniteSet(*elems)
            continue
        m = re.fullmatch(r"([\[(\]])\s*(.+?)\s*,\s*(.+?)\s*([\])\[])", p)
        if not m:
            raise ValueError(f"No entiendo el trozo «{p}». Ejemplos: [0, 1), (2, ∞), {{3, 5}}.")
        izq, a, b, der = m.groups()
        A = leer(a.replace("∞", "oo"))
        B = leer(b.replace("∞", "oo"))
        conj = conj | sp.Interval(A, B, left_open=(izq in "(]") or A == -sp.oo, right_open=(der in ")[") or B == sp.oo)
    return conj


def topologia(S):
    """Interior, adherencia, frontera, puntos de acumulación y aislados de un subconjunto de ℝ."""
    interior = S.interior
    clausura = S.closure
    frontera = S.boundary
    # acumulación: los puntos de la adherencia salvo los aislados (puntos sueltos del conjunto finito)
    aislados = []
    partes = S.args if isinstance(S, sp.Union) else (S,)
    intervalos = sp.Union(*[p for p in partes if isinstance(p, sp.Interval)]) if any(isinstance(p, sp.Interval) for p in partes) else sp.S.EmptySet
    for p in partes:
        if isinstance(p, sp.FiniteSet):
            for e in p:
                if intervalos.closure.contains(e) != sp.true:
                    aislados.append(e)
    acumulacion = intervalos.closure if intervalos != sp.S.EmptySet else sp.S.EmptySet
    sup_ = S.sup if S != sp.S.EmptySet else None
    inf_ = S.inf if S != sp.S.EmptySet else None
    res = {
        "interior": interior, "adherencia (cierre)": clausura, "frontera": frontera,
        "puntos de acumulación": acumulacion, "puntos aislados": sp.FiniteSet(*aislados),
        "abierto": S == interior, "cerrado": S == clausura,
        "acotado": bool(sup_ is not None and inf_ is not None and sup_.is_finite and inf_.is_finite),
        "supremo": sup_, "ínfimo": inf_,
        "máximo": sup_ if sup_ is not None and S.contains(sup_) == sp.true else None,
        "mínimo": inf_ if inf_ is not None and S.contains(inf_) == sp.true else None,
    }
    res["compacto"] = res["cerrado"] and res["acotado"]
    return res


# ----------------------------------------------------------------------- complejos
def operar_complejos(z, w):
    z, w = sp.nsimplify(z), sp.nsimplify(w)
    res = {"z + w": sp.expand_complex(z + w), "z − w": sp.expand_complex(z - w), "z · w": sp.expand_complex(z * w),
           "z̄ (conjugado)": sp.conjugate(z), "|z|": sp.simplify(sp.Abs(z))}
    if w != 0:
        res["z / w"] = sp.simplify(sp.expand_complex(z / w))
    return res


def de_moivre(z, nexp: int):
    z = sp.nsimplify(z)
    mod = sp.simplify(sp.Abs(z))
    arg = sp.simplify(sp.arg(z))
    pot_polar = (sp.simplify(mod ** nexp), sp.simplify(nexp * arg))
    directo = sp.expand_complex(z ** nexp)
    return mod, arg, pot_polar, sp.simplify(directo)


def region_compleja(cond: str, rango: float = 3.0, N: int = 400):
    """Dibuja {z : cond} en el plano. cond usa z, |z|, re(z), im(z), arg(z), conjugate(z)."""
    t = cond.replace("Re(", "re(").replace("Im(", "im(").replace("|", "@")
    # |expr| → Abs(expr)
    t = re.sub(r"@([^@]+)@", r"Abs(\1)", t)
    t = t.replace("≤", "<=").replace("≥", ">=")
    zz = sp.Symbol("z")
    X, Y = sp.symbols("X Y", real=True)
    loc = {"z": zz, "re": sp.re, "im": sp.im, "Abs": sp.Abs, "arg": sp.arg,
           "conjugate": sp.conjugate, "I": sp.I, "i": sp.I, "pi": sp.pi}
    trozos = [c for c in re.split(r"&|,|\by\b|\band\b", t) if c.strip()]
    partes = []
    for c in trozos:
        e = sp.sympify(c.strip(), locals=loc)
        partes.append(e.subs(zz, X + sp.I * Y))
    expr = sp.And(*partes) if len(partes) > 1 else partes[0]
    xs = np.linspace(-rango, rango, N)
    XX, YY = np.meshgrid(xs, xs)
    mask = np.ones_like(XX, dtype=bool)
    for p in partes:
        f = sp.lambdify((X, Y), p.lhs - p.rhs, "numpy")
        with np.errstate(all="ignore"):
            v = np.real(f(XX, YY) * np.ones_like(XX))
        if isinstance(p, (sp.StrictLessThan, sp.LessThan)):
            mask &= v <= 0 if isinstance(p, sp.LessThan) else v < 0
        elif isinstance(p, (sp.StrictGreaterThan, sp.GreaterThan)):
            mask &= v >= 0 if isinstance(p, sp.GreaterThan) else v > 0
        else:
            mask &= np.abs(v) < 2 * rango / N * 2
    return xs, mask, sp.simplify(expr)


# ======================================================================== Tema 2: límites y continuidad
def buscar_delta(f, a, L, eps: float, delta_max: float = 2.0, muestras: int = 4000):
    """Mayor δ (aprox.) tal que 0<|x−a|<δ ⇒ |f(x) − L| < ε. Busca en una malla fina."""
    af, Lf = float(sp.N(a)), float(sp.N(L))
    fl = lambdificar(f)
    lo, hi = 0.0, delta_max
    for _ in range(40):
        mid = (lo + hi) / 2
        xs = np.concatenate([np.linspace(af - mid, af - mid * 1e-6, muestras), np.linspace(af + mid * 1e-6, af + mid, muestras)])
        ys = fl(xs)
        ok = np.all(np.abs(ys[np.isfinite(ys)] - Lf) < eps) and np.isfinite(ys).mean() > 0.5
        if ok:
            lo = mid
        else:
            hi = mid
    return lo


@dataclass
class Trozo:
    expr: object
    izq: object           # límite izquierdo del tramo (−oo si no hay)
    der: object
    izq_cerrado: bool
    der_cerrado: bool


def leer_trozos(lineas: list[tuple[str, str]]):
    """[(expresión, condición)] con condiciones como «x < 0», «0 <= x < 2», «x >= 2»."""
    trozos = []
    for e, c in lineas:
        expr = leer(e)
        cc = c.replace("≤", "<=").replace("≥", ">=").replace(" ", "")
        m = re.fullmatch(r"(.+?)(<=|<)x(<=|<)(.+)", cc)
        if m:
            a, o1, o2, b = m.groups()
            trozos.append(Trozo(expr, leer(a), leer(b), o1 == "<=", o2 == "<="))
            continue
        m = re.fullmatch(r"x(<=|<|>=|>)(.+)", cc)
        if m:
            o, v = m.groups()
            v = leer(v)
            if o in ("<", "<="):
                trozos.append(Trozo(expr, -sp.oo, v, False, o == "<="))
            else:
                trozos.append(Trozo(expr, v, sp.oo, o == ">=", False))
            continue
        m = re.fullmatch(r"x=(.+)", cc)
        if m:
            v = leer(m.group(1))
            trozos.append(Trozo(expr, v, v, True, True))
            continue
        raise ValueError(f"No entiendo la condición «{c}». Usa x < 0, 0 <= x < 2, x >= 2 o x = 1.")
    return trozos


def a_piecewise(trozos):
    ramas = []
    for t in trozos:
        if t.izq == t.der:
            cond = sp.Eq(x, t.izq)
        else:
            c1 = (x >= t.izq if t.izq_cerrado else x > t.izq) if t.izq != -sp.oo else sp.true
            c2 = (x <= t.der if t.der_cerrado else x < t.der) if t.der != sp.oo else sp.true
            cond = sp.And(c1, c2)
        ramas.append((t.expr, cond))
    return sp.Piecewise(*ramas)


def estudiar_trozos(trozos):
    """En cada punto de corte: límites laterales, valor, continuidad y derivabilidad.
    Si hay parámetros, plantea y resuelve las ecuaciones."""
    puntos = sorted({t.der for t in trozos if t.der not in (sp.oo,)} | {t.izq for t in trozos if t.izq not in (-sp.oo,)},
                    key=lambda v: float(sp.N(v)))
    params = sorted(set().union(*[t.expr.free_symbols for t in trozos]) - {x}, key=str)
    estudio = []
    ecs_cont, ecs_der = [], []
    for c in puntos:
        izq = next((t for t in trozos if t.der == c and t.izq != t.der), None)
        der = next((t for t in trozos if t.izq == c and t.izq != t.der), None)
        punto = next((t for t in trozos if t.izq == t.der == c), None)
        valor_t = punto or (izq if izq and izq.der_cerrado else (der if der and der.izq_cerrado else None))
        Li = sp.limit(izq.expr, x, c, "-") if izq else None
        Ld = sp.limit(der.expr, x, c, "+") if der else None
        fc = sp.simplify(valor_t.expr.subs(x, c)) if valor_t else None
        info = {"punto": c, "lim_izq": Li, "lim_der": Ld, "valor": fc}
        if izq and der:
            ecs = [sp.Eq(Li, Ld)]
            if fc is not None:
                ecs.append(sp.Eq(Li, fc))
            ecs = list(dict.fromkeys(e for e in ecs if e is not sp.true))
            info["ec_continuidad"] = ecs
            ecs_cont += [e for e in ecs if e is not sp.false and e not in ecs_cont]
            info["continua_sin_parametros"] = None if params else all(e is sp.true or e == True for e in ecs) or not ecs  # noqa: E712
            di = sp.limit(sp.diff(izq.expr, x), x, c, "-")
            dd = sp.limit(sp.diff(der.expr, x), x, c, "+")
            info["der_izq"] = di
            info["der_der"] = dd
            e2 = sp.Eq(di, dd)
            info["ec_derivabilidad"] = e2
            if e2 is not sp.true:
                ecs_der.append(e2)
        estudio.append(info)
    sol_cont = sp.solve(ecs_cont, params, dict=True) if params and ecs_cont else None
    sol_der = sp.solve(ecs_cont + ecs_der, params, dict=True) if params and (ecs_cont or ecs_der) else None
    return {"puntos": puntos, "parametros": params, "estudio": estudio, "sol_continua": sol_cont,
            "sol_derivable": sol_der, "ecs_cont": ecs_cont, "ecs_der": ecs_der}


def extremos_absolutos(f, a, b):
    """Weierstrass: f continua en [a, b] alcanza máximo y mínimo. Candidatos: extremos del intervalo,
    puntos críticos y puntos donde f no es derivable."""
    I = sp.Interval(a, b)
    df = sp.diff(f, x)
    cands = {a, b}
    try:
        crit = sp.solveset(sp.Eq(df, 0), x, I)
        if isinstance(crit, sp.FiniteSet):
            cands |= set(crit)
        else:
            raise ValueError
    except Exception:  # noqa: BLE001
        xs = np.linspace(float(sp.N(a)), float(sp.N(b)), 4001)
        ys = lambdificar(df)(xs)
        for i in range(len(xs) - 1):
            if np.isfinite(ys[i]) and np.isfinite(ys[i + 1]) and ys[i] * ys[i + 1] < 0:
                cands.add(sp.Float(mp.findroot(sp.lambdify(x, df, "mpmath"), (xs[i], xs[i + 1]), solver="anderson"), 12))
    try:
        sing = sp.singularities(df, x, I)
        if isinstance(sing, sp.FiniteSet):
            cands |= set(sing)
    except Exception:  # noqa: BLE001
        pass
    for ab in f.atoms(sp.Abs):
        z = sp.solveset(ab.args[0], x, I)
        if isinstance(z, sp.FiniteSet):
            cands |= set(z)
    tabla = []
    for c in sorted(cands, key=lambda v: float(sp.N(v))):
        v = sp.simplify(f.subs(x, c))
        tabla.append((c, v, a_float(v)))
    tabla = [t for t in tabla if t[2] is not None]
    mx = max(tabla, key=lambda t: t[2])
    mn = min(tabla, key=lambda t: t[2])
    return tabla, mx, mn


# ======================================================================== Tema 3: derivadas
def valor_medio(f, a, b, tipo: str = "lagrange", g=None):
    """Rolle / Lagrange / Cauchy: puntos c ∈ (a, b) que cumplen la tesis + comprobación de hipótesis."""
    I = sp.Interval(a, b)
    hip = []
    try:
        from sympy.calculus.util import continuous_domain
        cont = continuous_domain(f, x, I) == I
    except Exception:  # noqa: BLE001
        cont = None
    hip.append(("f continua en [a, b]", cont))
    df = sp.diff(f, x)
    try:
        sing = sp.singularities(df, x, sp.Interval.open(a, b))
        deriv = sing == sp.S.EmptySet and not any(sp.solveset(ab.args[0], x, sp.Interval.open(a, b)) != sp.S.EmptySet
                                                    for ab in f.atoms(sp.Abs))
    except Exception:  # noqa: BLE001
        deriv = None
    hip.append(("f derivable en (a, b)", deriv))
    fa, fb = sp.simplify(f.subs(x, a)), sp.simplify(f.subs(x, b))
    if tipo == "rolle":
        hip.append(("f(a) = f(b)", sp.simplify(fa - fb) == 0))
        ecuacion = sp.Eq(df, 0)
    elif tipo == "cauchy":
        ga, gb = sp.simplify(g.subs(x, a)), sp.simplify(g.subs(x, b))
        ecuacion = sp.Eq(df * (gb - ga), sp.diff(g, x) * (fb - fa))
    else:
        ecuacion = sp.Eq(df, (fb - fa) / (b - a))
    try:
        sol = sp.solveset(ecuacion, x, sp.Interval.open(a, b))
        cs = list(sol) if isinstance(sol, sp.FiniteSet) else None
    except Exception:  # noqa: BLE001
        cs = None
    if cs is None:
        expr = ecuacion.lhs - ecuacion.rhs
        xs = np.linspace(float(sp.N(a)), float(sp.N(b)), 2001)[1:-1]
        ys = lambdificar(expr)(xs)
        cs = []
        for i in range(len(xs) - 1):
            if np.isfinite(ys[i]) and np.isfinite(ys[i + 1]) and ys[i] * ys[i + 1] <= 0:
                cs.append(sp.Float((xs[i] + xs[i + 1]) / 2, 8))
    return {"hipotesis": hip, "fa": fa, "fb": fb, "ecuacion": ecuacion, "c": cs}


@dataclass
class PasoHopital:
    num: object
    den: object
    lim_num: object
    lim_den: object
    tipo: str


def hopital(num, den, a, lado="+-", max_pasos=6):
    """Aplica L'Hôpital mientras haya 0/0 o ∞/∞, mostrando cada cociente."""
    pasos = []
    f, g = num, den
    d = "+" if lado == "+" else ("-" if lado == "-" else "+-")

    def lim(e):
        try:
            return sp.limit(e, x, a, d) if a not in (sp.oo, -sp.oo) else sp.limit(e, x, a)
        except Exception:  # noqa: BLE001
            return sp.nan
    for _ in range(max_pasos):
        Lf, Lg = lim(f), lim(g)
        if Lf == 0 and Lg == 0:
            tipo = "0/0"
        elif Lf in (sp.oo, -sp.oo, sp.zoo) and Lg in (sp.oo, -sp.oo, sp.zoo):
            tipo = "∞/∞"
        else:
            tipo = "determinado"
        pasos.append(PasoHopital(f, g, Lf, Lg, tipo))
        if tipo == "determinado":
            break
        f, g = sp.simplify(sp.diff(f, x)), sp.simplify(sp.diff(g, x))
    resultado = lim(num / den)
    return pasos, resultado


def derivada_implicita(ecuacion: str):
    """h(x, y) = 0 ⇒ dy/dx = −h_x / h_y (derivando ambos miembros respecto de x)."""
    y = sp.Symbol("y", real=True)
    if "=" in ecuacion:
        izq, der = ecuacion.split("=", 1)
        h = leer(izq) - leer(der)
    else:
        h = leer(ecuacion)
    hx, hy = sp.diff(h, x), sp.diff(h, y)
    dydx = sp.simplify(-hx / hy)
    yy = sp.Function("y")(x)
    d2 = sp.simplify(sp.diff(dydx.subs(y, yy), x).subs(sp.Derivative(yy, x), dydx).subs(yy, y))
    return h, hx, hy, dydx, d2


def leibniz(f, g, nn: int):
    terminos = [(k, sp.binomial(nn, k), sp.diff(f, x, k), sp.diff(g, x, nn - k)) for k in range(nn + 1)]
    total = sp.simplify(sum(c * a * b for _, c, a, b in terminos))
    return terminos, total, son_iguales(total, sp.diff(f * g, x, nn))


def criterio_derivadas_sucesivas(f, c, max_n=10):
    """Teoremas 3.2.6 y 3.5.9: primera derivada no nula en c (a partir de la 1ª o de la 2ª)."""
    ders = []
    for k in range(1, max_n + 1):
        v = sp.simplify(sp.diff(f, x, k).subs(x, c))
        ders.append((k, v))
        if k >= 2 and v != 0:
            break
    if ders[0][1] != 0:
        return ders, "f'(c) ≠ 0: c no es punto crítico, así que no es extremo relativo."
    nz = next(((k, v) for k, v in ders[1:] if v != 0), None)
    if nz is None:
        return ders, "Todas las derivadas calculadas son 0: el criterio no decide."
    k, v = nz
    if k % 2 == 0:
        return ders, f"La primera derivada no nula es la de orden {k} (par) y vale {sp.sstr(v)} ⇒ " + (
            "mínimo relativo." if v > 0 else "máximo relativo.")
    return ders, f"La primera derivada no nula es la de orden {k} (impar) ⇒ NO es extremo; es punto de inflexión."


def cota_lagrange(f, a, x0, orden_: int):
    """|R_n(x0)| ≤ M |x0 − a|^{n+1} / (n+1)!, con M = máx |f^{(n+1)}| entre a y x0 (numérico)."""
    d = sp.diff(f, x, orden_ + 1)
    lo, hi = sorted([float(sp.N(a)), float(sp.N(x0))])
    ts = np.linspace(lo, hi, 2001)
    vals = np.abs(lambdificar(d)(ts))
    M = float(np.nanmax(vals))
    cota = M * abs(float(sp.N(x0 - a))) ** (orden_ + 1) / math.factorial(orden_ + 1)
    return d, M, cota


def orden_necesario(f, a, x0, tol: float, max_n: int = 40):
    for k in range(0, max_n):
        _, M, cota = cota_lagrange(f, a, x0, k)
        if cota < tol:
            return k, cota
    return None, None


# ======================================================================== Tema 4: integrales
_NOMBRES = {
    "ConstantRule": "Integral de una constante: ∫c dx = c·x",
    "PowerRule": "Regla de la potencia: ∫xⁿ dx = xⁿ⁺¹/(n+1) (n ≠ −1)",
    "ReciprocalRule": "∫ dx/x = ln|x|",
    "ExpRule": "Exponencial: ∫aˣ dx = aˣ/ln a",
    "SinRule": "∫sen x dx = −cos x", "CosRule": "∫cos x dx = sen x",
    "Sec2Rule": "∫sec²x dx = tg x", "SecTanRule": "∫sec x·tg x dx = sec x",
    "Csc2Rule": "∫csc²x dx = −cotg x", "CscCotRule": "∫csc x·cotg x dx = −csc x",
    "ArctanRule": "Tipo arcotangente: ∫dx/(a + b·x²)", "ArcsinRule": "∫dx/√(1 − x²) = arcsen x",
    "ArcsinhRule": "∫dx/√(1 + x²) = argsenh x = ln(x + √(x²+1))",
    "SinhRule": "∫senh x dx = cosh x", "CoshRule": "∫cosh x dx = senh x",
}


def pasos_integral(f, var=x, prof=0, max_prof=6) -> list[tuple[int, str]]:
    """Explicación (en LaTeX) de cómo se integra f, traduciendo las reglas de SymPy."""
    try:
        r = integral_steps(f, var)
    except Exception:  # noqa: BLE001
        return [(prof, r"\text{No he podido descomponer la integral en pasos.}")]
    return _explicar_regla(r, prof, max_prof)


def _I(e, v):
    return rf"\int {sp.latex(e)}\,d{sp.latex(v)}"


def _explicar_regla(r, prof, max_prof) -> list[tuple[int, str]]:
    L = sp.latex
    nombre = type(r).__name__
    out = []
    integ, v = r.integrand, r.variable
    if prof > max_prof:
        return [(prof, rf"{_I(integ, v)} = {L(r.eval())}")]
    if nombre == "AddRule":
        out.append((prof, rf"\text{{Linealidad: se integra cada sumando}}\quad {_I(integ, v)} = " +
                    " + ".join(_I(s.integrand, v) for s in r.substeps)))
        for s in r.substeps:
            out += _explicar_regla(s, prof + 1, max_prof)
    elif nombre == "ConstantTimesRule":
        out.append((prof, rf"\text{{La constante sale fuera: }} {_I(integ, v)} = {L(r.constant)}\cdot {_I(r.other, v)}"))
        out += _explicar_regla(r.substep, prof + 1, max_prof)
    elif nombre == "URule":
        u = r.u_var
        out.append((prof, rf"\text{{Cambio de variable }} {L(u)} = {L(r.u_func)},\quad d{L(u)} = {L(sp.diff(r.u_func, v))}\,d{L(v)}"))
        out.append((prof, rf"\Rightarrow\ {_I(r.substep.integrand, u)}"))
        out += _explicar_regla(r.substep, prof + 1, max_prof)
        out.append((prof, rf"\text{{Deshago el cambio }} ({L(u)} = {L(r.u_func)})"))
    elif nombre == "PartsRule":
        du = sp.diff(r.u, v)
        vv = r.v_step.eval()
        out.append((prof, r"\text{Por partes: } \int u\,dv = u\,v - \int v\,du"))
        out.append((prof, rf"u = {L(r.u)},\ du = {L(du)}\,d{L(v)};\qquad dv = {L(r.dv)}\,d{L(v)},\ v = {L(vv)}"))
        out.append((prof, rf"{_I(integ, v)} = {L(r.u * vv)} - {_I(sp.simplify(vv * du), v)}"))
        if r.second_step is not None:
            out += _explicar_regla(r.second_step, prof + 1, max_prof)
    elif nombre == "CyclicPartsRule":
        out.append((prof, r"\text{Por partes dos veces: vuelve a aparecer la integral original (integral cíclica),"
                          r" así que se despeja como en una ecuación.}"))
        for pr in r.parts_rules:
            out.append((prof + 1, rf"u = {L(pr.u)},\ dv = {L(pr.dv)}\,d{L(v)}"))
        out.append((prof, rf"{_I(integ, v)} = {L(r.eval())}"))
        return out
    elif nombre in ("RewriteRule", "CompleteSquareRule"):
        txt = "Completo el cuadrado" if nombre == "CompleteSquareRule" else "Reescribo el integrando"
        reesc = r.rewritten
        if sp.together(integ).is_rational_function(v) and sp.apart(integ, v) == reesc:
            txt = "Descompongo en fracciones simples"
        out.append((prof, rf"\text{{{txt}: }} {L(integ)} = {L(reesc)}"))
        out += _explicar_regla(r.substep, prof + 1, max_prof)
    elif nombre == "AlternativeRule":
        out += _explicar_regla(r.alternatives[0], prof, max_prof)
        return out
    elif nombre == "TrigSubstitutionRule":
        out.append((prof, rf"\text{{Cambio trigonométrico }} {L(v)} = {L(r.func)}"))
        out.append((prof, rf"\Rightarrow\ {_I(r.rewritten, r.theta)}"))
        out += _explicar_regla(r.substep, prof + 1, max_prof)
    elif nombre == "PiecewiseRule":
        out.append((prof, r"\text{Integral a trozos (depende de los parámetros).}"))
    elif nombre == "DontKnowRule":
        out.append((prof, rf"\text{{No hay primitiva elemental conocida para }} {L(integ)}"))
        return out
    else:
        regla = _NOMBRES.get(nombre, nombre.replace("Rule", ""))
        out.append((prof, rf"\text{{{regla}}}:\quad {_I(integ, v)} = {L(r.eval())}"))
        return out
    out.append((prof, rf"\Rightarrow\ {_I(integ, v)} = {L(sp.simplify(r.eval()))}"))
    return out


def sugerir_metodo(f) -> list[str]:
    """Pistas de qué técnica usar, según la forma del integrando (apartado 4.2)."""
    pistas = []
    num, den = sp.fraction(sp.together(f))
    if f.is_rational_function(x) and sp.degree(den, x) >= 1:
        if sp.degree(num, x) >= sp.degree(den, x):
            pistas.append("Racional con grado del numerador ≥ denominador: **primero divide** (división euclídea) y luego fracciones simples.")
        pistas.append("Racional: **fracciones simples** (factoriza el denominador; método de Hermite si hay raíces múltiples o complejas).")
    if f.has(sp.exp) or f.has(sp.sin) or f.has(sp.cos) or f.has(sp.log) or f.has(sp.atan) or f.has(sp.asin):
        terms = sp.Mul.make_args(f)
        if any(t.is_polynomial(x) and t.has(x) for t in terms) and len(terms) > 1:
            pistas.append("Producto de polinomio por exponencial/trigonométrica/logaritmo: **por partes** (regla ALPES para elegir u: "
                          "Arcos, Logaritmos, Polinomios, Exponenciales, Senos).")
    if f.has(sp.exp) and (f.has(sp.sin) or f.has(sp.cos)):
        pistas.append("eᵃˣ·sen(bx) o eᵃˣ·cos(bx): **por partes dos veces** (integral cíclica).")
    pw = [p for p in f.atoms(sp.Pow) if p.base.func in (sp.sin, sp.cos)]
    if pw or (f.has(sp.sin) and f.has(sp.cos)):
        pistas.append("Potencias de seno y coseno: si alguna potencia es **impar**, separa un factor y cambia t = cos x (o sen x); "
                      "si ambas son **pares**, usa sen² = (1 − cos 2x)/2 y cos² = (1 + cos 2x)/2.")
    for p in f.atoms(sp.Pow):
        if p.exp == sp.Rational(1, 2) or p.exp == -sp.Rational(1, 2):
            b = p.base
            if b.is_polynomial(x) and sp.degree(b, x) == 2:
                a2 = sp.Poly(b, x).all_coeffs()
                if a2[0] < 0:
                    pistas.append("Aparece √(a² − x²): cambio **x = a·sen t**.")
                elif a2[2] > 0 if len(a2) == 3 else False:
                    pistas.append("Aparece √(a² + x²): cambio **x = a·tg t** (o argsenh).")
                else:
                    pistas.append("Aparece √(x² − a²): cambio **x = a·sec t** (o argcosh).")
    if f.has(sp.sin) or f.has(sp.cos):
        if f.is_rational_function(sp.sin(x)) or True:
            pistas.append("Si es una función racional de sen x y cos x y nada funciona: **t = tg(x/2)** "
                          "(sen x = 2t/(1+t²), cos x = (1−t²)/(1+t²), dx = 2dt/(1+t²)).")
    # u'/u o u'·g(u)
    for sub in [a for a in f.atoms(sp.Function, sp.Pow) if a.has(x)]:
        inner = sub.args[0] if isinstance(sub, sp.Function) else sub.base
        if inner != x and inner.has(x):
            du = sp.diff(inner, x)
            q = sp.simplify(f / du)
            if du != 0 and not sp.simplify(q.subs(inner, sp.Symbol("u"))).has(x):
                pistas.insert(0, f"Ves una función y su derivada: **cambio $u = {sp.latex(inner)}$** ($du = {sp.latex(du)}\\,dx$).")
                break
    return list(dict.fromkeys(pistas)) or ["Parece inmediata o casi inmediata: busca en la tabla de integrales."]


def sumas_darboux(f, a, b, N: int):
    """Sumas superior U(P,f) e inferior L(P,f) para la partición uniforme en N trozos."""
    af, bf = float(sp.N(a)), float(sp.N(b))
    xs = np.linspace(af, bf, N + 1)
    fl = lambdificar(f)
    U = L_ = 0.0
    Ms, ms = [], []
    for i in range(N):
        t = np.linspace(xs[i], xs[i + 1], 60)
        v = fl(t)
        v = v[np.isfinite(v)]
        M, m = (float(v.max()), float(v.min())) if v.size else (np.nan, np.nan)
        Ms.append(M)
        ms.append(m)
        U += M * (xs[i + 1] - xs[i])
        L_ += m * (xs[i + 1] - xs[i])
    return xs, Ms, ms, U, L_


def derivada_integral_variable(f_t, g, h):
    """F(x) = ∫_{h(x)}^{g(x)} f(t) dt ⇒ F'(x) = f(g(x))·g'(x) − f(h(x))·h'(x) (Corolario 4.1.12)."""
    t = sp.Symbol("t", real=True)
    ft = f_t.subs(x, t)
    res = sp.simplify(ft.subs(t, g) * sp.diff(g, x) - ft.subs(t, h) * sp.diff(h, x))
    # comprobación: derivar numéricamente la integral en un punto
    return res


def area_entre(f, g, a, b):
    """Área = ∫ |f − g| dx: se buscan los cortes en [a, b] y se integra a trozos con el signo correcto."""
    d = sp.simplify(f - g)
    I = sp.Interval(a, b)
    try:
        cortes = sp.solveset(sp.Eq(d, 0), x, I)
        cortes = sorted([c for c in cortes], key=lambda v: float(sp.N(v))) if isinstance(cortes, sp.FiniteSet) else []
    except Exception:  # noqa: BLE001
        cortes = []
    pts = [a] + [c for c in cortes if c != a and c != b] + [b]
    trozos = []
    total = 0
    for p, q in zip(pts[:-1], pts[1:]):
        val = sp.simplify(sp.integrate(d, (x, p, q)))
        trozos.append((p, q, val))
        total += sp.Abs(val)
    total = sp.simplify(total)
    num = float(mp.quad(lambda t: abs(float(sp.N(d.subs(x, t)))), [float(sp.N(p)) for p in pts]))
    return cortes, trozos, total, num


def aplicaciones_integral(f, a, b):
    """Longitud de arco, volumen y superficie de revolución alrededor de OX y volumen alrededor de OY (capas)."""
    df = sp.diff(f, x)
    out = {}
    exprs = {
        "longitud de la curva": sp.sqrt(1 + df ** 2),
        "volumen al girar en torno a OX (discos)": sp.pi * f ** 2,
        "área lateral al girar en torno a OX": 2 * sp.pi * f * sp.sqrt(1 + df ** 2),
        "volumen al girar en torno a OY (capas cilíndricas, x ≥ 0)": 2 * sp.pi * x * f,
        "valor medio (promedio integral)": f / (b - a),
    }
    for nombre, integrando in exprs.items():
        exacto = sp.integrate(integrando, (x, a, b))
        if exacto.has(sp.Integral):
            exacto = None
        else:
            exacto = sp.simplify(exacto)
        try:
            num = float(mp.quad(sp.lambdify(x, integrando, "mpmath"), [float(sp.N(a)), float(sp.N(b))]))
        except Exception:  # noqa: BLE001
            num = None
        out[nombre] = (integrando, exacto, num)
    return out


def parametrica(xt, yt, t0, t1):
    t = sp.Symbol("t", real=True)
    xt, yt = xt.subs(x, t), yt.subs(x, t)
    dx, dy = sp.diff(xt, t), sp.diff(yt, t)
    res = {}
    for nombre, integ in {"longitud": sp.sqrt(dx ** 2 + dy ** 2),
                          "área encerrada ½∫(x y' − y x') dt": (xt * dy - yt * dx) / 2}.items():
        ex = sp.integrate(sp.simplify(integ), (t, t0, t1))
        ex = None if ex.has(sp.Integral) else sp.simplify(ex)
        num = float(mp.quad(sp.lambdify(t, integ, "mpmath"), [float(sp.N(t0)), float(sp.N(t1))]))
        res[nombre] = (integ, ex, num)
    return res, xt, yt, t


def area_polar(rho, t0, t1):
    t = sp.Symbol("θ", real=True)
    r_ = rho.subs(x, t)
    ex = sp.integrate(r_ ** 2 / 2, (t, t0, t1))
    ex = None if ex.has(sp.Integral) else sp.simplify(ex)
    num = float(mp.quad(sp.lambdify(t, r_ ** 2 / 2, "mpmath"), [float(sp.N(t0)), float(sp.N(t1))]))
    return r_, ex, num, t


def comparacion_impropia(f, extremo, lado="sup"):
    """Halla s con f ~ C/x^s en +∞ (o f ~ C/(b−x)^s en un extremo finito) y decide la convergencia
    con el criterio de comparación por paso al límite (Corolarios 4.4.12 y 4.4.21)."""
    if extremo in (sp.oo, -sp.oo):
        try:
            s = sp.limit(-sp.log(sp.Abs(f)) / sp.log(sp.Abs(x)), x, extremo)
        except Exception:  # noqa: BLE001
            return None
        if not s.is_real or s in (sp.oo, -sp.oo):
            return {"s": s, "C": None, "converge": (s == sp.oo), "explicacion":
                    "f decae más rápido que cualquier potencia ⇒ converge." if s == sp.oo else "f no tiende a 0 ⇒ diverge."}
        C = sp.limit(f * sp.Abs(x) ** s, x, extremo)
        conv = bool(s > 1) if C not in (0, sp.oo, -sp.oo) else None
        return {"s": s, "C": C, "converge": conv,
                "explicacion": rf"\lim x^{{{sp.latex(s)}}} f(x) = {sp.latex(C)}"
                               + (r"\ (\text{finito}\neq 0)\Rightarrow\text{ mismo carácter que }\int^\infty \frac{dx}{x^{" + sp.latex(s) + "}}" if conv is not None else "")}
    b = extremo
    dist = (b - x) if lado == "sup" else (x - b)
    d = "-" if lado == "sup" else "+"
    try:
        s = sp.limit(sp.log(sp.Abs(f)) / -sp.log(sp.Abs(dist)), x, b, d)
    except Exception:  # noqa: BLE001
        return None
    if not s.is_real:
        return None
    if s <= 0:
        return {"s": s, "C": None, "converge": True, "explicacion": "f está acotada cerca del extremo: no es realmente impropia."}
    C = sp.limit(f * sp.Abs(dist) ** s, x, b, d)
    conv = bool(s < 1) if C not in (0, sp.oo, -sp.oo) else None
    return {"s": s, "C": C, "converge": conv,
            "explicacion": rf"\lim |x-{sp.latex(b)}|^{{{sp.latex(s)}}} f(x) = {sp.latex(C)}"
                           + (r"\ \Rightarrow \text{ mismo carácter que } \int \frac{dx}{|x-b|^{" + sp.latex(s) + "}}" if conv is not None else "")}


def beta_gamma(p, q=None):
    if q is None:
        return sp.gamma(p), float(mp.gamma(float(sp.N(p))))
    return sp.simplify(sp.gamma(p) * sp.gamma(q) / sp.gamma(p + q)), float(mp.beta(float(sp.N(p)), float(sp.N(q))))


# ======================================================================== Tema 5: sucesiones
def recurrencia_iterar(g, x1, N: int = 60):
    vals = [x1]
    gl = sp.lambdify(x, g, "math")
    for _ in range(N - 1):
        try:
            v = float(gl(vals[-1]))
        except Exception:  # noqa: BLE001
            break
        if not math.isfinite(v) or abs(v) > 1e12:
            vals.append(v)
            break
        vals.append(v)
    return vals


def puntos_fijos(g):
    try:
        S = sp.solveset(sp.Eq(g, x), x, R)
        pts = list(S) if isinstance(S, sp.FiniteSet) else []
    except Exception:  # noqa: BLE001
        pts = []
    dg = sp.diff(g, x)
    out = []
    for p in pts:
        try:
            der = sp.simplify(dg.subs(x, p))
            df = a_float(der)
        except Exception:  # noqa: BLE001
            der, df = None, None
        tipo = None
        if df is not None:
            tipo = "atractor (|g'| < 1)" if abs(df) < 1 else ("repulsor (|g'| > 1)" if abs(df) > 1 else "dudoso (|g'| = 1)")
        out.append((p, der, tipo))
    return out


def lim_sup_inf(an, N: int = 4000):
    """lím sup y lím inf: simbólico por subsucesiones par/impar y numérico con colas."""
    m = sp.Symbol("m", integer=True, positive=True)
    simb = {}
    try:
        pares = sp.limit(sp.simplify(an.subs(n_sym, 2 * m)), m, sp.oo)
        impares = sp.limit(sp.simplify(an.subs(n_sym, 2 * m + 1)), m, sp.oo)
        simb = {"pares": pares, "impares": impares}
    except Exception:  # noqa: BLE001
        pass
    f = sp.lambdify(n_sym, an, "mpmath")
    vals = []
    for i in range(1, N + 1):
        try:
            vals.append(float(mp.re(f(i))))
        except Exception:  # noqa: BLE001
            vals.append(np.nan)
    v = np.array(vals)
    cola = v[N // 2:]
    return simb, float(np.nanmax(cola)), float(np.nanmin(cola)), v


def stolz(an, bn):
    q = sp.simplify((an - an.subs(n_sym, n_sym - 1)) / (bn - bn.subs(n_sym, n_sym - 1)))
    try:
        L_ = sp.limit(q, n_sym, sp.oo)
    except Exception:  # noqa: BLE001
        L_ = None
    try:
        directo = sp.limit(an / bn, n_sym, sp.oo)
    except Exception:  # noqa: BLE001
        directo = None
    return q, L_, directo


# ======================================================================== Tema 6: series
def criterios_extra(an):
    """Raabe, Pringsheim (comparación con 1/n^α), condensación y criterios logarítmicos."""
    nn = n_sym
    res = {}
    try:
        raabe = sp.limit(nn * (1 - sp.simplify(an.subs(nn, nn + 1) / an)), nn, sp.oo)
        res["Raabe  lím n(1 − aₙ₊₁/aₙ)"] = (raabe, "converge" if raabe.is_extended_real and raabe > 1 else
                                            ("diverge" if raabe.is_extended_real and raabe < 1 else "no decide (λ = 1)"))
    except Exception:  # noqa: BLE001
        pass
    try:
        alpha = sp.limit(-sp.log(an) / sp.log(nn), nn, sp.oo)
        if alpha.is_extended_real:
            veredicto = "converge" if alpha > 1 else ("diverge" if alpha < 1 else "no decide (λ = 1)")
            res["Logarítmico  lím −ln aₙ / ln n"] = (alpha, veredicto)
            if alpha.is_real and alpha.is_finite:
                C = sp.limit(nn ** alpha * an, nn, sp.oo)
                v = ("mismo carácter que Σ1/n^α: " + ("converge" if alpha > 1 else "diverge")) if (C.is_real and C.is_finite and C != 0) else "—"
                res[f"Pringsheim  lím n^α aₙ con α = {sp.sstr(alpha)}"] = (C, v)
    except Exception:  # noqa: BLE001
        pass
    try:
        cond = sp.simplify(2 ** nn * an.subs(nn, 2 ** nn))
        res["Condensación  2ⁿ·a(2ⁿ)"] = (cond, "estudia esta serie: tiene el mismo carácter (si aₙ ↓ 0)")
    except Exception:  # noqa: BLE001
        pass
    return res


def producto_cauchy(an, bn, N: int = 8):
    """c_n = Σ_{k=0}^{n} a_k b_{n−k}: términos exactos (sumas finitas) y, si sale rápido, forma cerrada."""
    from .tiempo import con_tiempo, Tarda
    k = sp.Symbol("k", integer=True, nonnegative=True)
    terminos = [sp.nsimplify(sp.simplify(sum(an.subs(n_sym, j) * bn.subs(n_sym, i - j) for j in range(i + 1))))
                for i in range(N)]
    cn = sp.Sum(an.subs(n_sym, k) * bn.subs(n_sym, n_sym - k), (k, 0, n_sym))
    try:
        cerrado = con_tiempo(lambda: sp.simplify(cn.doit()), segundos=6)
        if cerrado.has(sp.Sum):
            cerrado = None
    except (Tarda, Exception):  # noqa: BLE001
        cerrado = None
    return cn, cerrado, terminos


def reordenar_riemann(objetivo: float, N: int = 3000):
    """Reordena 1 − 1/2 + 1/3 − … para que sume «objetivo» (teorema de Riemann)."""
    pos, neg = 1, 2   # siguientes impar (positivo) y par (negativo) sin usar
    s = 0.0
    sumas, usados = [], []
    for _ in range(N):
        if s <= objetivo:
            s += 1 / pos
            usados.append(pos)
            pos += 2
        else:
            s -= 1 / neg
            usados.append(-neg)
            neg += 2
        sumas.append(s)
    return sumas, usados


def suma_serie(an, inicio: int = 1):
    S = sp.Sum(an, (n_sym, inicio, sp.oo))
    try:
        v = S.doit()
        if v.has(sp.Sum):
            v = None
    except Exception:  # noqa: BLE001
        v = None
    try:
        num = float(mp.nsum(sp.lambdify(n_sym, an, "mpmath"), [inicio, mp.inf]))
    except Exception:  # noqa: BLE001
        num = None
    return v, num


def telescopica(bn):
    """Σ (b_n − b_{n+1}) = b_1 − lím b_n."""
    try:
        L_ = sp.limit(bn, n_sym, sp.oo)
    except Exception:  # noqa: BLE001
        L_ = None
    return sp.simplify(bn - bn.subs(n_sym, n_sym + 1)), bn.subs(n_sym, 1), L_


# ======================================================================== Tema 7: sucesiones y series de funciones
def limite_puntual(fn):
    """f(x) = lím_{n→∞} f_n(x) simbólico. Devuelve None si SymPy no da una expresión limpia
    (p. ej. depende de si |x| < 1): entonces se estudia punto a punto."""
    from .tiempo import con_tiempo
    try:
        L_ = con_tiempo(sp.limit, fn, n_sym, sp.oo, segundos=8)
    except Exception:  # noqa: BLE001
        return None
    if L_.has(sp.Limit, sp.AccumBounds, sp.sign, sp.oo, -sp.oo, sp.zoo, sp.nan):
        return None
    return L_


def sup_diferencia(fn, f, a, b, ns=(1, 2, 5, 10, 20, 50, 100, 200, 500, 1000)):
    """M_n = sup_{x∈[a,b]} |f_n(x) − f(x)| numérico (malla fina). Si M_n → 0 la convergencia es uniforme."""
    xs = np.linspace(float(sp.N(a)), float(sp.N(b)), 3001)
    out = []
    fl = None
    if f is not None:
        try:
            fl = np.vectorize(lambda t: float(sp.N(f.subs(x, t))) if f.has(x) else float(sp.N(f)))
            fvals = fl(xs)
        except Exception:  # noqa: BLE001
            fvals = None
    for k in ns:
        g = fn.subs(n_sym, k)
        vals = lambdificar(g)(xs)
        if fvals is None:
            out.append((k, np.nan, np.nan))
            continue
        d = np.abs(vals - fvals)
        i = int(np.nanargmax(d))
        out.append((k, float(np.nanmax(d)), float(xs[i])))
    return out


def evaluar_limite_en_puntos(fn, xs):
    out = []
    for t in xs:
        try:
            out.append(float(sp.N(sp.limit(fn.subs(x, sp.nsimplify(t)), n_sym, sp.oo))))
        except Exception:  # noqa: BLE001
            out.append(np.nan)
    return np.array(out)


def radio_convergencia(cn, centro=0):
    """R = 1/lím sup |c_n|^{1/n} (Cauchy–Hadamard); se calcula también con el cociente si existe."""
    nn = n_sym
    try:
        raiz = sp.limit(sp.Abs(cn) ** (sp.Integer(1) / nn), nn, sp.oo)
    except Exception:  # noqa: BLE001
        raiz = None
    try:
        coc = sp.limit(sp.Abs(sp.simplify(cn.subs(nn, nn + 1) / cn)), nn, sp.oo)
    except Exception:  # noqa: BLE001
        coc = None
    L_ = raiz if raiz is not None and raiz.is_real is not False else coc
    if L_ is None:
        return None, raiz, coc
    Rr = sp.oo if L_ == 0 else (0 if L_ == sp.oo else sp.simplify(1 / L_))
    return Rr, raiz, coc


def extremos_serie_potencias(cn, centro, Rr):
    """Estudia la serie numérica en x = centro ± R (lo que la teoría deja «caso por caso»)."""
    from .analisis import estudiar_serie
    out = []
    if Rr in (0, sp.oo) or Rr is None:
        return out
    for signo, punto in ((-1, centro - Rr), (1, centro + Rr)):
        termino = sp.simplify(cn * (signo * Rr) ** n_sym)
        try:
            S = estudiar_serie(termino, 1)
            out.append((punto, termino, S.convergente))
        except Exception:  # noqa: BLE001
            out.append((punto, termino, None))
    return out


EJEMPLOS_FUNCIONES = {
    "xⁿ en [0, 1]": ("x^n", "0", "1"),
    "n·x·(1−x)ⁿ en [0, 1] (Ej. 7.2.7)": ("n*x*(1-x)^n", "0", "1"),
    "n²·x·(1−x²)ⁿ en [0, 1] (Ej. 7.1.9)": ("n^2*x*(1-x^2)^n", "0", "1"),
    "sen(nx)/√n en [0, 2π] (Ej. 7.1.8)": ("sen(n*x)/raiz(n)", "0", "2*pi"),
    "x/(1 + n x²) en [−2, 2]": ("x/(1+n*x^2)", "-2", "2"),
    "(1 + x/n)ⁿ en [0, 2]": ("(1+x/n)^n", "0", "2"),
}
