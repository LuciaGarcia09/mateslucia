"""Análisis matemático de una variable real.

Regla de oro: cada resultado simbólico se contrasta con un cálculo NUMÉRICO
independiente (tablas de valores, diferencias finitas, integración numérica).
Si no coinciden, la app lo dice en lugar de dar un resultado dudoso.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import math
import random

import mpmath as mp
import numpy as np
import sympy as sp
from sympy.calculus.util import continuous_domain

from .parsing import x, n as n_sym

R = sp.S.Reals


# ------------------------------------------------------------------ utilidades
def a_float(v) -> float | None:
    try:
        c = complex(sp.N(v, 30))
    except (TypeError, ValueError):
        return None
    if abs(c.imag) > 1e-9 * max(1.0, abs(c.real)):
        return None
    return c.real


def evaluar(f, x0: float) -> float | None:
    try:
        v = f.subs(x, sp.Float(x0, 30)).evalf(30)
        return a_float(v)
    except Exception:  # noqa: BLE001
        return None


def lambdificar(f):
    g = sp.lambdify(x, f, modules=["numpy"])

    def seguro(xs):
        with np.errstate(all="ignore"):
            try:
                ys = g(xs)
            except Exception:  # noqa: BLE001
                ys = np.array([evaluar(f, float(t)) if evaluar(f, float(t)) is not None else np.nan for t in xs])
            ys = np.asarray(ys, dtype=complex) if np.iscomplexobj(ys) else np.asarray(ys, dtype=float)
            if np.iscomplexobj(ys):
                ys = np.where(np.abs(ys.imag) < 1e-12, ys.real, np.nan).astype(float)
            if ys.shape == ():
                ys = np.full_like(xs, float(ys), dtype=float)
        return ys
    return seguro


def puntos_grafica(f, a: float, b: float, num: int = 1500, recorte: float | None = None):
    xs = np.linspace(a, b, num)
    ys = lambdificar(f)(xs)
    ys = np.where(np.isfinite(ys), ys, np.nan)
    finitos = ys[np.isfinite(ys)]
    if recorte is None and finitos.size:
        q1, q99 = np.percentile(finitos, [2, 98])
        span = max(q99 - q1, 1.0)
        recorte = max(abs(q1), abs(q99)) + 3 * span
    if recorte is not None:
        ys = np.where(np.abs(ys) > recorte, np.nan, ys)
    # cortar la línea en saltos enormes (asíntotas verticales)
    dif = np.abs(np.diff(ys))
    if np.isfinite(dif).any():
        umbral = np.nanpercentile(dif, 99) * 20 + 1e-9
        saltos = np.where(dif > umbral)[0]
        ys[saltos] = np.nan
    return xs, ys


def conjunto_a_lista(S, maximo=40):
    """Lista de valores reales de un conjunto de sympy si es finito; None si no se puede."""
    if isinstance(S, sp.FiniteSet):
        return sorted([v for v in S if v.is_real is not False], key=lambda v: float(sp.N(v)))
    if isinstance(S, sp.Union):
        out = []
        for a in S.args:
            l = conjunto_a_lista(a, maximo)
            if l is None:
                return None
            out += l
        return sorted(out, key=lambda v: float(sp.N(v)))
    if S == sp.S.EmptySet:
        return []
    return None


def resolver_real(ecuacion, intervalo=R):
    try:
        return sp.solveset(ecuacion, x, intervalo)
    except Exception:  # noqa: BLE001
        return None


def mas_simple(e):
    """Forma más corta de e SIN introducir funciones que no estaban (p. ej. cosh al simplificar exponenciales)."""
    hiper = (sp.sinh, sp.cosh, sp.tanh)
    tenia = any(e.has(h) for h in hiper)
    candidatos = [e]
    for fn in (sp.simplify, sp.factor, sp.together, sp.cancel):
        try:
            candidatos.append(fn(e))
        except Exception:  # noqa: BLE001
            pass
    validos = [c for c in candidatos if tenia or not any(c.has(h) for h in hiper)]
    return min(validos or candidatos, key=lambda c: (sp.count_ops(c), len(str(c))))


def son_iguales(a, b, var=None) -> bool:
    """¿a = b como expresiones? Simbólico y, si no concluye, numérico en 8 puntos con 30 cifras."""
    d = sp.sympify(a) - sp.sympify(b)
    try:
        if sp.simplify(d) == 0 or sp.simplify(d.rewrite(sp.exp)) == 0:
            return True
    except Exception:  # noqa: BLE001
        pass
    libres = list(d.free_symbols)
    if not libres:
        try:
            return abs(complex(sp.N(d, 30))) < 1e-20
        except (TypeError, ValueError):
            return False
    rnd = random.Random(7)
    probados = 0
    for _ in range(60):
        val = {s_: sp.Float(rnd.uniform(0.3, 2.7), 30) if not s_.is_integer else rnd.randint(2, 9) for s_ in libres}
        try:
            v = complex(sp.N(d.subs(val), 30))
        except (TypeError, ValueError, ZeroDivisionError):
            continue
        if not (math.isfinite(v.real) and math.isfinite(v.imag)):
            continue
        probados += 1
        if abs(v) > 1e-15:
            return False
        if probados >= 8:
            return True
    return False


# ------------------------------------------------------------------ límites
@dataclass
class Limite:
    valor: object
    lado: str
    tabla: list = field(default_factory=list)   # (x, f(x))
    coincide_numerico: bool | None = None
    laterales: tuple | None = None


def limite(f, a, lado: str = "+-") -> Limite:
    """lado: '+-' (bilateral), '+' (por la derecha), '-' (por la izquierda)."""
    if a in (sp.oo, -sp.oo):
        val = sp.limit(f, x, a)
        tabla = []
        for e in range(1, 7):
            xv = (10 ** e) * (1 if a == sp.oo else -1)
            tabla.append((xv, evaluar(f, xv)))
        return Limite(val, "∞", tabla, _compara(val, [t[1] for t in tabla[-3:]]))
    if lado == "+-":
        der = sp.limit(f, x, a, "+")
        izq = sp.limit(f, x, a, "-")
        val = der if sp.simplify(der - izq) == 0 or der == izq else sp.nan
        tabla = []
        af = a_float(a)
        for e in range(1, 7):
            h = 10.0 ** (-e)
            tabla.append((af - h, evaluar(f, af - h)))
            tabla.append((af + h, evaluar(f, af + h)))
        ok = None
        if val is not sp.nan:
            ok = _compara(val, [tabla[-1][1], tabla[-2][1]])
        return Limite(val, "bilateral", tabla, ok, (izq, der))
    val = sp.limit(f, x, a, lado)
    af = a_float(a)
    sgn = 1 if lado == "+" else -1
    tabla = [(af + sgn * 10.0 ** (-e), evaluar(f, af + sgn * 10.0 ** (-e))) for e in range(1, 7)]
    return Limite(val, "derecha" if lado == "+" else "izquierda", tabla, _compara(val, [tabla[-1][1]]))


def _compara(simbolico, numericos) -> bool | None:
    nums = [v for v in numericos if v is not None]
    if not nums:
        return None
    if simbolico in (sp.oo, -sp.oo):
        return all(abs(v) > 1e3 and math.copysign(1, v) == (1 if simbolico == sp.oo else -1) for v in nums)
    if simbolico is sp.nan or simbolico == sp.zoo or isinstance(simbolico, sp.AccumBounds):
        return None
    s = a_float(simbolico)
    if s is None:
        return None
    return all(abs(v - s) < 1e-2 * max(1, abs(s)) for v in nums)


# ------------------------------------------------------------------ derivadas
def explicar_derivada(f, profundidad: int = 0, max_prof: int = 2) -> list[str]:
    """Explica (en LaTeX) qué regla de derivación se aplica, desglosando un par de niveles."""
    L = sp.latex
    d = lambda g: sp.simplify(sp.diff(g, x))  # noqa: E731
    lineas = []
    pre = r"\quad " * profundidad
    if not f.has(x):
        return [pre + rf"\left({L(f)}\right)' = 0 \quad\text{{(constante)}}"]
    if f == x:
        return [pre + r"(x)' = 1"]
    if isinstance(f, sp.Add):
        lineas.append(pre + r"\text{Regla de la suma: se deriva término a término}")
        lineas.append(pre + r"\left(" + L(f) + r"\right)' = " + " + ".join(rf"\left({L(t)}\right)'" for t in f.args))
        if profundidad < max_prof:
            for t in f.args:
                lineas += explicar_derivada(t, profundidad + 1, max_prof)
    elif isinstance(f, sp.Mul):
        c, resto = f.as_independent(x)
        if c != 1:
            lineas.append(pre + rf"\text{{Constante por función: }}\left({L(f)}\right)' = {L(c)}\cdot\left({L(resto)}\right)'")
            if profundidad < max_prof:
                lineas += explicar_derivada(resto, profundidad + 1, max_prof)
        else:
            num, den = sp.fraction(f)
            if den.has(x) and den != 1:
                lineas.append(pre + r"\text{Regla del cociente: } \left(\frac{u}{v}\right)' = \frac{u'v-uv'}{v^2}")
                lineas.append(pre + rf"u = {L(num)},\; u' = {L(d(num))};\quad v = {L(den)},\; v' = {L(d(den))}")
            else:
                u = f.args[0]
                v = sp.Mul(*f.args[1:])
                lineas.append(pre + r"\text{Regla del producto: } (uv)' = u'v + uv'")
                lineas.append(pre + rf"u = {L(u)},\; u' = {L(d(u))};\quad v = {L(v)},\; v' = {L(d(v))}")
    elif isinstance(f, sp.Pow):
        b, e = f.args
        if not e.has(x):
            if b == x:
                lineas.append(pre + rf"\text{{Potencia: }} (x^{{r}})' = r\,x^{{r-1}} \Rightarrow \left({L(f)}\right)' = {L(d(f))}")
            else:
                lineas.append(pre + r"\text{Potencia + regla de la cadena: } (u^r)' = r\,u^{r-1}\,u'")
                lineas.append(pre + rf"u = {L(b)},\; u' = {L(d(b))}")
                if profundidad < max_prof:
                    lineas += explicar_derivada(b, profundidad + 1, max_prof)
        elif not b.has(x):
            lineas.append(pre + r"\text{Exponencial: } (a^{u})' = a^{u}\ln a \cdot u'")
            lineas.append(pre + rf"u = {L(e)},\; u' = {L(d(e))}")
        else:
            lineas.append(pre + r"\text{Base y exponente con } x\text{: derivación logarítmica } (u^v)' = u^v\left(v'\ln u + v\frac{u'}{u}\right)")
    elif isinstance(f, sp.Function):
        u = f.args[0]
        nombre = type(f).__name__
        tabla = {
            "sin": r"(\operatorname{sen} u)' = \cos u \cdot u'",
            "cos": r"(\cos u)' = -\operatorname{sen} u \cdot u'",
            "tan": r"(\operatorname{tg} u)' = (1+\operatorname{tg}^2 u)\, u'",
            "exp": r"(e^u)' = e^u \cdot u'",
            "log": r"(\ln u)' = \dfrac{u'}{u}",
            "asin": r"(\arcsin u)' = \dfrac{u'}{\sqrt{1-u^2}}",
            "acos": r"(\arccos u)' = \dfrac{-u'}{\sqrt{1-u^2}}",
            "atan": r"(\operatorname{arctg} u)' = \dfrac{u'}{1+u^2}",
            "sinh": r"(\operatorname{senh} u)' = \cosh u \cdot u'",
            "cosh": r"(\cosh u)' = \operatorname{senh} u \cdot u'",
        }
        regla = tabla.get(nombre, r"\text{regla de la cadena: } (g(u))' = g'(u)\,u'")
        lineas.append(pre + regla + (r"\quad\text{(regla de la cadena)}" if u != x else ""))
        if u != x:
            lineas.append(pre + rf"u = {L(u)},\; u' = {L(d(u))}")
            if profundidad < max_prof:
                lineas += explicar_derivada(u, profundidad + 1, max_prof)
    return lineas


def comprobar_derivada(f, df, puntos: int = 6) -> bool | None:
    """Compara f' simbólica con la diferencia centrada (f(x+h)-f(x-h))/2h en puntos aleatorios del dominio."""
    rnd = random.Random(1)
    ok = 0
    probados = 0
    intentos = 0
    while probados < puntos and intentos < 200:
        intentos += 1
        x0 = rnd.uniform(-3, 3)
        v = evaluar(df, x0)
        if v is None or not math.isfinite(v):
            continue
        h = 1e-6
        mp.mp.dps = 30
        try:
            fl = sp.lambdify(x, f, modules="mpmath")
            num = mp.diff(fl, mp.mpf(x0))
            num = float(mp.re(num)) if abs(mp.im(num)) < 1e-12 else None
        except Exception:  # noqa: BLE001
            a1, a2 = evaluar(f, x0 + h), evaluar(f, x0 - h)
            num = None if a1 is None or a2 is None else (a1 - a2) / (2 * h)
        if num is None:
            continue
        probados += 1
        if abs(num - v) <= 1e-5 * max(1.0, abs(v)):
            ok += 1
    if probados == 0:
        return None
    return ok == probados


def recta_tangente(f, a):
    fa = sp.simplify(f.subs(x, a))
    m = sp.simplify(sp.diff(f, x).subs(x, a))
    for v, nombre in ((fa, "f"), (m, "f'")):
        if v.has(sp.zoo, sp.nan, sp.oo, -sp.oo) or v.is_real is False:
            raise ValueError(f"{nombre} no está definida (o es infinita) en x₀ = {sp.sstr(a)}: elige otro punto.")
    return fa, m, sp.expand(fa + m * (x - a))


# --------------------------------------------------------------- estudio de función
@dataclass
class Estudio:
    f: object
    dominio: object
    corte_y: object
    cortes_x: object
    paridad: str
    asintotas_v: list
    asintota_h: dict
    asintota_o: dict
    df: object
    criticos: list
    monotonia: list      # (intervalo_texto, '↗'/'↘')
    extremos: list       # (x, y, 'máximo'/'mínimo')
    d2f: object
    inflexion: list
    curvatura: list      # (intervalo_texto, '∪ convexa'/'∩ cóncava')
    avisos: list


def _intervalos_signo(g, puntos_corte: list[float], dominio, a_min=-1e6, a_max=1e6):
    """Signo de g en cada tramo entre puntos de corte, sólo en tramos dentro del dominio."""
    pts = sorted(set(p for p in puntos_corte if math.isfinite(p)))
    bordes = [-math.inf] + pts + [math.inf]
    out = []
    for izq, der in zip(bordes[:-1], bordes[1:]):
        if izq == -math.inf and der == math.inf:
            prueba = [0.0, 1.0, -1.0, 2.5]
        elif izq == -math.inf:
            prueba = [der - 1.0, der - 0.25, der - 10]
        elif der == math.inf:
            prueba = [izq + 1.0, izq + 0.25, izq + 10]
        else:
            m = (izq + der) / 2
            prueba = [m, izq + (der - izq) / 4, izq + 3 * (der - izq) / 4]
        signo = None
        for t in prueba:
            try:
                if dominio is not None and not bool(dominio.contains(sp.Float(t))):
                    continue
            except Exception:  # noqa: BLE001
                pass
            v = evaluar(g, t)
            if v is None or not math.isfinite(v):
                continue
            if abs(v) < 1e-14:
                continue
            signo = 1 if v > 0 else -1
            break
        out.append((izq, der, signo))
    return out


_EXACTOS: dict = {}


def _fmt(v):
    """Extremo de intervalo en LaTeX: exacto (2-√3) si lo conocemos, si no decimal."""
    for clave, exacto in _EXACTOS.items():
        if math.isfinite(v) and abs(clave - v) < 1e-12:
            return sp.latex(exacto)
    if v == -math.inf:
        return r"-\infty"
    if v == math.inf:
        return r"+\infty"
    return sp.latex(sp.nsimplify(v, rational=False, tolerance=1e-12)) if abs(v - round(v)) < 1e-12 else f"{v:.4g}"


VENTANA = 10


def _valor(f, c):
    v = sp.simplify(f.subs(x, c))
    if isinstance(c, sp.Float):
        v = sp.N(v, 10, chop=True)
        if abs(v) < 1e-9:
            v = sp.Integer(0)
    return v


def tiene_raiz_impar(f) -> bool:
    """x^(1/3), x^(2/5)…: SymPy usa la raíz principal (compleja para base negativa)."""
    for p in f.atoms(sp.Pow):
        e = p.exp
        if e.is_Rational and not e.is_integer and e.q % 2 == 1 and p.base.has(x):
            return True
    return False


def _ceros(g, conjunto, avisos, que):
    """Ceros reales de g en `conjunto`: exactos si se puede; si hay infinitos devuelve None;
    si sympy no sabe, los busca numéricamente en [-VENTANA, VENTANA]."""
    if not g.has(x):
        return [] if g != 0 else None
    S = resolver_real(sp.Eq(g, 0), conjunto)
    if S is not None:
        l = conjunto_a_lista(S)
        if l is not None:
            return l
        try:
            if isinstance(S, sp.ConditionSet) is False and S.is_finite_set is False:
                return None   # infinitos ceros
        except Exception:  # noqa: BLE001
            pass
    # búsqueda numérica: cambios de signo en una malla fina + refinamiento
    xs = np.linspace(-VENTANA, VENTANA, 4001)
    ys = lambdificar(g)(xs)
    encontrados = []
    for i in range(len(xs) - 1):
        a, b, fa, fb = xs[i], xs[i + 1], ys[i], ys[i + 1]
        if not (np.isfinite(fa) and np.isfinite(fb)):
            continue
        if fa == 0:
            encontrados.append(float(a))
        elif fa * fb < 0:
            try:
                r = float(mp.findroot(sp.lambdify(x, g, "mpmath"), (a, b), solver="anderson"))
            except Exception:  # noqa: BLE001
                r = (a + b) / 2
            if abs((evaluar(g, r) or 1)) < 1e-6:
                encontrados.append(r)
    try:
        encontrados = [r for r in encontrados if conjunto.contains(sp.Float(r)) == sp.true]
    except Exception:  # noqa: BLE001
        pass
    if que:
        avisos.append(f"Los {que} se han calculado numéricamente (aprox.) en [−{VENTANA}, {VENTANA}]; "
                      f"el estudio de esa parte se limita a ese intervalo.")
    return NumericoEnVentana(sp.Float(r, 10) for r in sorted(set(round(r, 10) for r in encontrados)))


class NumericoEnVentana(list):
    """Lista de ceros hallados numéricamente sólo dentro de la ventana [-VENTANA, VENTANA]."""


def estudio_funcion(f) -> Estudio:
    avisos = []
    if tiene_raiz_impar(f):
        avisos.append("Hay raíces de índice impar (p. ej. x^(1/3)). SymPy toma la raíz PRINCIPAL, que es compleja si la "
                      "base es negativa, así que el estudio sólo es fiable donde la base es ≥ 0. Para la raíz cúbica real "
                      "estudia por separado el tramo negativo usando la simetría.")
    try:
        dom = continuous_domain(f, x, R)
    except Exception:  # noqa: BLE001
        dom = None
        avisos.append("No he podido calcular el dominio de forma exacta.")
    # corte con OY
    corte_y = None
    if dom is not None and dom.contains(0) == sp.true:
        corte_y = sp.simplify(f.subs(x, 0))
    cortes = resolver_real(sp.Eq(f, 0), dom if dom is not None else R)
    # paridad
    fm = sp.simplify(f.subs(x, -x))
    if sp.simplify(fm - f) == 0:
        paridad = "par (simétrica respecto al eje OY)"
    elif sp.simplify(fm + f) == 0:
        paridad = "impar (simétrica respecto al origen)"
    else:
        paridad = "ni par ni impar"
    # asíntotas verticales: puntos frontera del dominio donde algún lateral es infinito
    av = []
    candidatos = []
    try:
        sing = sp.singularities(f, x, R)
        l = conjunto_a_lista(sing)
        if l:
            candidatos += l
    except Exception:  # noqa: BLE001
        pass
    if dom is not None:
        try:
            fr = conjunto_a_lista(dom.boundary)
            if fr:
                candidatos += fr
        except Exception:  # noqa: BLE001
            pass
    vistos = set()
    for c in candidatos:
        if c in vistos or not c.is_real:
            continue
        vistos.add(c)
        lims = []
        for lado in ("-", "+"):
            try:
                L_ = sp.limit(f, x, c, lado)
            except Exception:  # noqa: BLE001
                L_ = None
            lims.append(L_)
        if any(L_ in (sp.oo, -sp.oo) for L_ in lims if L_ is not None):
            av.append((c, lims[0], lims[1]))
    # horizontales y oblicuas
    ah, ao = {}, {}
    for inf, nombre in ((sp.oo, "+∞"), (-sp.oo, "−∞")):
        if dom is not None:
            try:
                if (inf == sp.oo and dom.sup != sp.oo) or (inf == -sp.oo and dom.inf != -sp.oo):
                    continue
            except Exception:  # noqa: BLE001
                pass
        try:
            L_ = sp.limit(f, x, inf)
        except Exception:  # noqa: BLE001
            continue
        if isinstance(L_, sp.AccumBounds):
            continue
        if L_.is_real and L_.is_finite:
            ah[nombre] = L_
        elif L_ in (sp.oo, -sp.oo):
            try:
                m = sp.limit(f / x, x, inf)
                if m.is_real and m.is_finite and m != 0:
                    b = sp.limit(f - m * x, x, inf)
                    if b.is_real and b.is_finite:
                        ao[nombre] = sp.expand(m * x + b)
            except Exception:  # noqa: BLE001
                pass
    # derivadas
    df = mas_simple(sp.diff(f, x))
    d2f = mas_simple(sp.diff(df, x))
    base = dom if dom is not None else R
    ventana = None
    criticos = _ceros(df, base, avisos, "puntos críticos")
    if criticos is None:
        ventana = (-VENTANA, VENTANA)
        criticos = _ceros(df, base.intersect(sp.Interval(-VENTANA, VENTANA)), avisos, "puntos críticos") or []
    if isinstance(criticos, NumericoEnVentana):
        ventana = (-VENTANA, VENTANA)
    # puntos donde f' no existe dentro del dominio (p.ej. |x| en 0) -> también cambian monotonía
    no_deriv = []
    for ab in f.atoms(sp.Abs):
        z = _ceros(ab.args[0], base, [], "")
        for c in z or []:
            if dom is None or dom.contains(c) == sp.true:
                no_deriv.append(c)
    try:
        sd = sp.singularities(df, x, R)
        l = conjunto_a_lista(sd) or []
        for c in l:
            if dom is not None and dom.contains(c) == sp.true:
                no_deriv.append(c)
    except Exception:  # noqa: BLE001
        pass
    av_x = [a_float(c) for c, *_ in av]
    frontera = []
    if dom is not None:
        try:
            frontera = [a_float(v) for v in (conjunto_a_lista(dom.boundary) or [])]
        except Exception:  # noqa: BLE001
            frontera = []
    cortes_mon = [a_float(c) for c in criticos + no_deriv] + av_x + frontera
    cortes_mon = [c for c in cortes_mon if c is not None]
    if ventana:
        cortes_mon += list(ventana)
    _EXACTOS.clear()
    for c in list(criticos) + no_deriv + [c for c, *_ in av] + (conjunto_a_lista(dom.boundary) or [] if dom is not None else []):
        cf = a_float(c)
        if cf is not None and not isinstance(c, sp.Float):
            _EXACTOS[cf] = c
    tramos = _intervalos_signo(df, cortes_mon, dom)
    if ventana:
        tramos = [t for t in tramos if math.isfinite(t[0]) and math.isfinite(t[1])]
    monotonia = []
    for a, b, s in tramos:
        if s is None:
            continue
        monotonia.append((rf"\left({_fmt(a)},\ {_fmt(b)}\right)", "creciente ↗" if s > 0 else "decreciente ↘"))
    # extremos: cambio de signo de f' en un punto del dominio
    extremos = []
    candidatos_ext = []
    for c in list(criticos) + no_deriv:
        if all(abs(a_float(c) - a_float(d)) > 1e-9 for d in candidatos_ext):
            candidatos_ext.append(c)
    for c in candidatos_ext:
        cf = a_float(c)
        if cf is None:
            continue
        izq = next((s for a, b, s in tramos if abs(b - cf) < 1e-12), None)
        der = next((s for a, b, s in tramos if abs(a - cf) < 1e-12), None)
        if izq is None or der is None:
            continue
        yv = _valor(f, c)
        if izq > 0 and der < 0:
            extremos.append((c, yv, "máximo relativo"))
        elif izq < 0 and der > 0:
            extremos.append((c, yv, "mínimo relativo"))
    # curvatura
    cand_inf = _ceros(d2f, base, avisos, "candidatos a inflexión")
    ventana2 = None
    if cand_inf is None:
        ventana2 = (-VENTANA, VENTANA)
        cand_inf = _ceros(d2f, base.intersect(sp.Interval(-VENTANA, VENTANA)), avisos, "candidatos a inflexión") or []
    if isinstance(cand_inf, NumericoEnVentana):
        ventana2 = (-VENTANA, VENTANA)
    cand_inf = [c for c in cand_inf if c not in no_deriv]
    cortes_cur = [a_float(c) for c in list(cand_inf) + no_deriv] + av_x + frontera
    if ventana2:
        cortes_cur += list(ventana2)
    cortes_cur = [c for c in cortes_cur if c is not None]
    for c in cand_inf:
        cf = a_float(c)
        if cf is not None and not isinstance(c, sp.Float):
            _EXACTOS[cf] = c
    tramos2 = _intervalos_signo(d2f, cortes_cur, dom)
    if ventana2:
        tramos2 = [t for t in tramos2 if math.isfinite(t[0]) and math.isfinite(t[1])]
    curvatura = [(rf"\left({_fmt(a)},\ {_fmt(b)}\right)", "convexa ∪" if s > 0 else "cóncava ∩")
                 for a, b, s in tramos2 if s is not None]
    inflexion = []
    for c in cand_inf:
        cf = a_float(c)
        izq = next((s for a, b, s in tramos2 if abs(b - cf) < 1e-12), None)
        der = next((s for a, b, s in tramos2 if abs(a - cf) < 1e-12), None)
        if izq is not None and der is not None and izq != der:
            inflexion.append((c, _valor(f, c)))
    return Estudio(f, dom, corte_y, cortes, paridad, av, ah, ao, df, criticos, monotonia, extremos,
                   d2f, inflexion, curvatura, avisos)


# ------------------------------------------------------------------ integrales
@dataclass
class Integral:
    primitiva: object
    comprobacion: bool | None
    definida: object = None
    numerica: float | None = None
    coincide: bool | None = None


def integral(f, a=None, b=None) -> Integral:
    F = sp.integrate(f, x)
    if F.has(sp.Integral):
        comp = None
    else:
        comp = sp.simplify(sp.diff(F, x) - f) == 0
        if not comp:
            comp = comprobar_derivada(F, f)  # comprobación numérica si simplify no cierra
    if a is None:
        return Integral(F, comp)
    Def = sp.integrate(f, (x, a, b))
    num = None
    try:
        mp.mp.dps = 30
        fl = sp.lambdify(x, f, modules="mpmath")
        aa = mp.inf if a == sp.oo else (-mp.inf if a == -sp.oo else mp.mpf(str(sp.N(a, 30))))
        bb = mp.inf if b == sp.oo else (-mp.inf if b == -sp.oo else mp.mpf(str(sp.N(b, 30))))
        q = mp.quad(fl, [aa, bb])
        if abs(mp.im(q)) < 1e-12:
            num = float(mp.re(q))
    except Exception:  # noqa: BLE001
        num = None
    coincide = None
    dv = a_float(Def) if not Def.has(sp.Integral) and Def.is_finite is not False else None
    if dv is not None and num is not None and math.isfinite(num):
        coincide = abs(dv - num) < 1e-6 * max(1, abs(dv))
    return Integral(F, comp, Def, num, coincide)


# ------------------------------------------------------------------ Taylor
def taylor(f, a, orden: int):
    serie = sp.series(f, x, a, orden + 1).removeO()
    # comprobación: coeficientes = f^(k)(a)/k!
    coefs = []
    for kk in range(orden + 1):
        ck = sp.simplify(sp.diff(f, x, kk).subs(x, a) / sp.factorial(kk))
        coefs.append(ck)
    reconstruido = sp.expand(sum(c * (x - a) ** kk for kk, c in enumerate(coefs)))
    ok = sp.simplify(sp.expand(serie) - reconstruido) == 0
    return sp.expand(serie) if a == 0 else serie, coefs, ok


# ------------------------------------------------------------------ sucesiones y series
@dataclass
class Serie:
    termino: object
    limite_termino: object
    cociente: object
    raiz: object
    convergente: object      # True/False/None
    suma: object
    parciales: list
    explicacion: list


def limite_sucesion(an):
    """lim a_n cuando n→∞. Si SymPy no puede (p. ej. con (−1)^n) usa: |a_n|→0 ⇒ a_n→0,
    y si no, compara las subsucesiones par e impar."""
    nn = n_sym
    try:
        return sp.limit(an, nn, sp.oo)
    except Exception:  # noqa: BLE001
        pass
    try:
        if sp.limit(sp.Abs(an), nn, sp.oo) == 0:
            return sp.Integer(0)
    except Exception:  # noqa: BLE001
        pass
    m = sp.Symbol("m", integer=True, positive=True)
    try:
        par = sp.limit(sp.simplify(an.subs(nn, 2 * m)), m, sp.oo)
        impar = sp.limit(sp.simplify(an.subs(nn, 2 * m + 1)), m, sp.oo)
        if sp.simplify(par - impar) == 0:
            return par
        return sp.nan   # subsucesiones con límites distintos: no existe
    except Exception:  # noqa: BLE001
        return None


def estudiar_serie(an, inicio: int = 1) -> Serie:
    nn = n_sym
    expl = []
    lt = limite_sucesion(an)
    if lt is None:
        expl.append(r"\text{No he podido calcular } \lim a_n")
    elif lt is sp.nan:
        expl.append(r"\lim a_n \text{ no existe} \Rightarrow \text{la serie DIVERGE (condición necesaria)}")
    elif lt != 0:
        expl.append(rf"\lim a_n = {sp.latex(lt)} \neq 0 \Rightarrow \text{{la serie DIVERGE (condición necesaria)}}")
    else:
        expl.append(r"\lim a_n = 0\text{: condición necesaria cumplida (no basta para converger)}")
    try:
        coc = sp.limit(sp.Abs(sp.simplify(an.subs(nn, nn + 1) / an)), nn, sp.oo)
    except Exception:  # noqa: BLE001
        coc = None
    if coc is not None and coc.is_real:
        if coc < 1:
            expl.append(rf"\text{{Criterio del cociente: }} L = {sp.latex(coc)} < 1 \Rightarrow \text{{converge (absolutamente)}}")
        elif coc > 1 or coc == sp.oo:
            expl.append(rf"\text{{Criterio del cociente: }} L = {sp.latex(coc)} > 1 \Rightarrow \text{{diverge}}")
        else:
            expl.append(r"\text{Criterio del cociente: } L = 1 \Rightarrow \text{no decide}")
    try:
        raiz = sp.limit(sp.Abs(an) ** (sp.Integer(1) / nn), nn, sp.oo)
    except Exception:  # noqa: BLE001
        raiz = None
    if raiz is not None and raiz.is_real:
        if raiz < 1:
            expl.append(rf"\text{{Criterio de la raíz: }} L = {sp.latex(raiz)} < 1 \Rightarrow \text{{converge}}")
        elif raiz > 1 or raiz == sp.oo:
            expl.append(rf"\text{{Criterio de la raíz: }} L = {sp.latex(raiz)} > 1 \Rightarrow \text{{diverge}}")
        else:
            expl.append(r"\text{Criterio de la raíz: } L = 1 \Rightarrow \text{no decide}")
    alterna = an.has((-1) ** nn) or an.has(sp.cos(sp.pi * nn))
    if alterna and lt == 0:
        b = sp.simplify(sp.Abs(an))
        try:
            dec = all((b.subs(nn, i + 1) - b.subs(nn, i)) <= 0 for i in range(max(inicio, 1), max(inicio, 1) + 60))
        except Exception:  # noqa: BLE001
            dec = False
        if dec:
            expl.append(r"\text{Leibniz: serie alternada con } |a_n| = " + sp.latex(b)
                        + r" \text{ decreciente y} \to 0 \Rightarrow \text{converge}")
    S = sp.Sum(an, (nn, inicio, sp.oo))
    try:
        conv = S.is_convergent()
    except Exception:  # noqa: BLE001
        conv = None
    suma = None
    if conv is True or conv == sp.true:
        try:
            suma = S.doit()
            if suma.has(sp.Sum):
                suma = None
        except Exception:  # noqa: BLE001
            suma = None
    parciales = []
    acc = 0.0
    for i in range(inicio, inicio + 200):
        v = evaluar(an.subs(nn, x), i)
        if v is None:
            break
        acc += v
        parciales.append((i, acc))
    conv_val = True if conv in (True, sp.true) else (False if conv in (False, sp.false) else None)
    return Serie(an, lt, coc, raiz, conv_val, suma, parciales, expl)


# ------------------------------------------------------------------ inecuaciones
def inecuacion(rel):
    return sp.solveset(rel, x, R)


# ------------------------------------------------------------------ complejos
def complejo_formas(z):
    z = sp.nsimplify(sp.expand_complex(z))
    re_, im_ = sp.re(z), sp.im(z)
    mod = sp.simplify(sp.sqrt(re_ ** 2 + im_ ** 2))
    arg = sp.simplify(sp.arg(z)) if z != 0 else None
    return re_, im_, mod, arg


def raices_n(z, nr: int):
    _, _, mod, arg = complejo_formas(z)
    if arg is None:
        return [sp.Integer(0)]
    out = []
    for kk in range(nr):
        ang = (arg + 2 * sp.pi * kk) / nr
        out.append((sp.simplify(mod ** sp.Rational(1, nr)), sp.simplify(ang)))
    return out


# ------------------------------------------------------------------ métodos numéricos
def biseccion(f, a: float, b: float, tol: float = 1e-8, max_it: int = 100):
    fa, fb = evaluar(f, a), evaluar(f, b)
    if fa is None or fb is None:
        raise ValueError("f no está definida en algún extremo del intervalo.")
    if fa * fb > 0:
        raise ValueError(f"f(a) = {fa:.6g} y f(b) = {fb:.6g} tienen el mismo signo: Bolzano no garantiza raíz.")
    filas = []
    for i in range(1, max_it + 1):
        c = (a + b) / 2
        fc = evaluar(f, c)
        if fc is None:
            raise ValueError(f"f no está definida en {c}: ¿es continua en [a, b]?")
        filas.append((i, a, b, c, fc, (b - a) / 2))
        if fc == 0 or (b - a) / 2 < tol:
            break
        if fa * fc < 0:
            b, fb = c, fc
        else:
            a, fa = c, fc
    return filas


def newton(f, x0: float, tol: float = 1e-12, max_it: int = 50):
    df = sp.diff(f, x)
    filas = []
    xk = x0
    for i in range(1, max_it + 1):
        fx, dfx = evaluar(f, xk), evaluar(df, xk)
        if fx is None or dfx is None:
            raise ValueError(f"f o f' no están definidas en x = {xk}.")
        if dfx == 0:
            raise ValueError(f"f'({xk}) = 0: Newton no puede seguir (tangente horizontal). Prueba otro x₀.")
        x_new = xk - fx / dfx
        filas.append((i, xk, fx, dfx, x_new, abs(x_new - xk)))
        if abs(x_new - xk) < tol:
            break
        xk = x_new
    return filas
