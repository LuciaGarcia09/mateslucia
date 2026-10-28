"""Polinomios en una variable sobre Q (racionales) o Z_p (enteros módulo p primo).

Todo se calcula con aritmética EXACTA (fracciones), nunca con decimales,
y cada resultado se puede comprobar con `verificar_*`.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import sympy as sp

from .parsing import x


# ---------------------------------------------------------------- cuerpos
class Cuerpo:
    """Q si p is None; Z_p si p es primo."""

    def __init__(self, p: int | None = None):
        if p is not None:
            if p < 2 or not sp.isprime(p):
                raise ValueError(f"{p} no es primo: Z_{p} no es un cuerpo y la división no siempre es posible.")
        self.p = p

    @property
    def nombre(self) -> str:
        return "ℚ" if self.p is None else f"ℤ_{self.p}"

    def norm(self, a):
        if self.p is None:
            return sp.Rational(a)
        a = sp.Rational(a)
        num = int(a.p) % self.p
        den = int(a.q) % self.p
        if den == 0:
            raise ValueError(f"El coeficiente {a} tiene denominador múltiplo de {self.p}: no existe en ℤ_{self.p}.")
        return sp.Integer((num * pow(den, -1, self.p)) % self.p)

    def inv(self, a):
        a = self.norm(a)
        if a == 0:
            raise ZeroDivisionError("División entre 0.")
        if self.p is None:
            return 1 / a
        return sp.Integer(pow(int(a), -1, self.p))

    def add(self, a, b):
        return self.norm(a + b)

    def sub(self, a, b):
        return self.norm(a - b)

    def mul(self, a, b):
        return self.norm(a * b)

    def div(self, a, b):
        return self.mul(a, self.inv(b))


# ---------------------------------------------------------- representación
# Un polinomio es una lista de coeficientes de MAYOR a MENOR grado, sin ceros a la izquierda.

def limpiar(c: list) -> list:
    i = 0
    while i < len(c) - 1 and c[i] == 0:
        i += 1
    c = c[i:]
    return c if c else [sp.Integer(0)]


def desde_expr(expr, K: Cuerpo) -> list:
    expr = sp.expand(sp.sympify(expr))
    libres = expr.free_symbols - {x}
    if libres:
        raise ValueError(f"El polinomio sólo puede depender de x (aparece {', '.join(map(str, libres))}).")
    try:
        P = sp.Poly(expr, x)
    except sp.PolynomialError as exc:
        raise ValueError("Eso no es un polinomio en x (¿hay x en un denominador, raíces o funciones?).") from exc
    coef = P.all_coeffs()
    for c in coef:
        if not c.is_rational:
            raise ValueError(f"El coeficiente {c} no es racional; esta herramienta trabaja en ℚ o ℤ_p.")
    return limpiar([K.norm(c) for c in coef])


def a_expr(c: list):
    g = len(c) - 1
    return sp.expand(sum(ci * x ** (g - i) for i, ci in enumerate(c)))


def grado(c: list) -> int:
    c = limpiar(c)
    return -1 if c == [0] else len(c) - 1  # grado de 0 = -∞, usamos -1


def es_cero(c: list) -> bool:
    return limpiar(c) == [0]


def mostrar(c: list, K: Cuerpo) -> str:
    """LaTeX del polinomio (en Z_p los coeficientes quedan en 0..p-1)."""
    return sp.latex(a_expr(c)) if not es_cero(c) else "0"


def suma(a, b, K):
    n = max(len(a), len(b))
    a = [0] * (n - len(a)) + list(a)
    b = [0] * (n - len(b)) + list(b)
    return limpiar([K.add(u, v) for u, v in zip(a, b)])


def resta(a, b, K):
    return suma(a, [K.norm(-v) for v in b], K)


def producto(a, b, K):
    if es_cero(a) or es_cero(b):
        return [sp.Integer(0)]
    r = [sp.Integer(0)] * (len(a) + len(b) - 1)
    for i, u in enumerate(a):
        for j, v in enumerate(b):
            r[i + j] = K.add(r[i + j], K.mul(u, v))
    return limpiar(r)


def monico(a, K):
    if es_cero(a):
        return a
    inv = K.inv(a[0])
    return [K.mul(c, inv) for c in a]


# ------------------------------------------------------------- división
@dataclass
class PasoDivision:
    termino_coef: object       # coeficiente del término del cociente
    termino_grado: int         # grado del término del cociente
    resto_antes: list
    restado: list              # termino * divisor
    resto_despues: list


@dataclass
class Division:
    dividendo: list
    divisor: list
    cociente: list
    resto: list
    pasos: list[PasoDivision] = field(default_factory=list)


def division(A: list, B: list, K: Cuerpo) -> Division:
    A, B = limpiar(A), limpiar(B)
    if es_cero(B):
        raise ZeroDivisionError("No se puede dividir entre el polinomio 0.")
    gB = grado(B)
    lider_inv = K.inv(B[0])
    R = list(A)
    Q = [sp.Integer(0)] * max(1, grado(A) - gB + 1)
    pasos = []
    while not es_cero(R) and grado(R) >= gB:
        gR = grado(R)
        c = K.mul(R[0], lider_inv)
        d = gR - gB
        termino = [c] + [sp.Integer(0)] * d
        restado = producto(termino, B, K)
        nuevo = resta(R, restado, K)
        pasos.append(PasoDivision(c, d, R, restado, nuevo))
        Q[len(Q) - 1 - d] = K.add(Q[len(Q) - 1 - d], c)
        R = nuevo
    return Division(A, B, limpiar(Q), limpiar(R), pasos)


# --------------------------------------------- algoritmo de Euclides (extendido)
@dataclass
class FilaEuclides:
    dividendo: list
    divisor: list
    cociente: list
    resto: list
    s: list   # resto = s*A + t*B
    t: list


@dataclass
class ResultadoMCD:
    filas: list[FilaEuclides]
    mcd: list            # mónico
    ultimo_resto: list   # sin normalizar
    s: list              # mcd = s*A + t*B
    t: list
    A: list
    B: list


def mcd_extendido(A: list, B: list, K: Cuerpo) -> ResultadoMCD:
    A, B = limpiar(A), limpiar(B)
    if es_cero(A) and es_cero(B):
        raise ValueError("mcd(0, 0) no está definido.")
    uno, cero = [sp.Integer(1)], [sp.Integer(0)]
    # invariantes: r_prev = s_prev*A + t_prev*B ; r = s*A + t*B
    r_prev, s_prev, t_prev = A, uno, cero
    r, s, t = B, cero, uno
    filas = []
    while not es_cero(r):
        d = division(r_prev, r, K)
        s_new = resta(s_prev, producto(d.cociente, s, K), K)
        t_new = resta(t_prev, producto(d.cociente, t, K), K)
        filas.append(FilaEuclides(r_prev, r, d.cociente, d.resto, s_new, t_new))
        r_prev, s_prev, t_prev = r, s, t
        r, s, t = d.resto, s_new, t_new
    # r_prev es el último resto no nulo
    inv = K.inv(r_prev[0])
    mcd = [K.mul(c, inv) for c in r_prev]
    s_f = limpiar([K.mul(c, inv) for c in s_prev])
    t_f = limpiar([K.mul(c, inv) for c in t_prev])
    return ResultadoMCD(filas, mcd, r_prev, s_f, t_f, A, B)


def mcm(A, B, K):
    if es_cero(A) or es_cero(B):
        return [sp.Integer(0)]
    g = mcd_extendido(A, B, K).mcd
    return monico(division(producto(A, B, K), g, K).cociente, K)


# ------------------------------------------------------------- Ruffini
@dataclass
class Ruffini:
    a: object
    coef: list
    fila_media: list
    fila_baja: list
    cociente: list
    resto: object


def ruffini(P: list, a, K: Cuerpo) -> Ruffini:
    a = K.norm(a)
    P = limpiar(P)
    media = [sp.Integer(0)]
    baja = [P[0]]
    for c in P[1:]:
        m = K.mul(baja[-1], a)
        media.append(m)
        baja.append(K.add(c, m))
    return Ruffini(a, P, media, baja, limpiar(baja[:-1]) if len(baja) > 1 else [sp.Integer(0)], baja[-1])


# -------------------------------------------------------- factorización y raíces
def factorizar(expr, K: Cuerpo):
    if K.p is None:
        return sp.factor(expr)
    return sp.factor(expr, modulus=K.p)


def factor_lista(expr, K: Cuerpo):
    """Lista de (factor irreducible, multiplicidad) y la constante."""
    if K.p is None:
        c, fs = sp.factor_list(expr, x)
    else:
        c, fs = sp.factor_list(expr, x, modulus=K.p)
    return c, fs


def raices(c: list, K: Cuerpo):
    """Raíces en el cuerpo (con multiplicidad). En ℚ también da reales y complejas."""
    if es_cero(c):
        raise ValueError("El polinomio 0 tiene infinitas raíces.")
    if K.p is not None:
        out = {}
        for v in range(K.p):
            m = 0
            Pc = c
            while not es_cero(Pc) and grado(Pc) >= 1:
                rf = ruffini(Pc, v, K)
                if rf.resto != 0:
                    break
                m += 1
                Pc = rf.cociente
            if m:
                out[sp.Integer(v)] = m
        return {"en el cuerpo": out}
    P = sp.Poly(a_expr(c), x)
    racionales = {r: m for r, m in sp.roots(P, filter="Q").items()}
    todas = sp.roots(P)
    if sum(todas.values()) < P.degree():
        # sympy no da forma cerrada: usar CRootOf (exacto) o numérico
        todas = {}
        for r in sp.Poly(P).all_roots():
            todas[r] = todas.get(r, 0) + 1
    reales = {r: m for r, m in todas.items() if r.is_real}
    complejas = {r: m for r, m in todas.items() if r.is_real is False}
    return {"racionales": racionales, "reales": reales, "complejas": complejas}


# --------------------------------------------------------- comprobaciones
def verificar_division(d: Division, K: Cuerpo) -> bool:
    reconstruido = suma(producto(d.cociente, d.divisor, K), d.resto, K)
    return reconstruido == limpiar(d.dividendo) and (es_cero(d.resto) or grado(d.resto) < grado(d.divisor))


def verificar_mcd(res: ResultadoMCD, K: Cuerpo) -> dict:
    g = res.mcd
    divide_A = es_cero(division(res.A, g, K).resto)
    divide_B = es_cero(division(res.B, g, K).resto)
    bezout = suma(producto(res.s, res.A, K), producto(res.t, res.B, K), K) == g
    # contra sympy
    if K.p is None:
        ref = sp.Poly(sp.gcd(a_expr(res.A), a_expr(res.B)), x)
        ref = [sp.Rational(c) for c in ref.monic().all_coeffs()]
    else:
        ref = sp.Poly(a_expr(res.A), x, modulus=K.p).gcd(sp.Poly(a_expr(res.B), x, modulus=K.p))
        ref = monico([K.norm(c) for c in ref.all_coeffs()], K)
    return {
        "mcd divide a A": divide_A,
        "mcd divide a B": divide_B,
        "identidad de Bézout s·A + t·B = mcd": bezout,
        "coincide con el cálculo independiente de SymPy": limpiar(ref) == limpiar(g),
    }


# ------------------------------------------------------------- grado y orden
def orden(c: list) -> int | None:
    """θ(p) = menor k con a_k ≠ 0 (None para el polinomio 0: por convenio θ(0) = +∞)."""
    c = limpiar(c)
    if es_cero(c):
        return None
    g = grado(c)
    for i, ci in enumerate(reversed(c)):
        if ci != 0:
            return i
    return g


# ------------------------------------------------------------- raíces racionales
def candidatos_racionales(expr):
    """Teorema de las raíces racionales: si p/q (irreducible) es raíz de un polinomio con coeficientes
    ENTEROS, p divide al término independiente y q al coeficiente líder."""
    P = sp.Poly(sp.expand(expr), x)
    coef = P.all_coeffs()
    den = sp.ilcm(*[sp.fraction(sp.Rational(c))[1] for c in coef])
    coef = [sp.Integer(sp.Rational(c) * den) for c in coef]
    while coef and coef[-1] == 0:
        coef = coef[:-1]
    cero = P.degree() - (len(coef) - 1)   # multiplicidad de la raíz 0
    if not coef:
        return [], cero
    a0, an = abs(int(coef[-1])), abs(int(coef[0]))
    ps = sp.divisors(a0) if a0 else [0]
    qs = sp.divisors(an)
    cand = sorted({sgn * sp.Rational(p_, q_) for p_ in ps for q_ in qs for sgn in (1, -1)})
    return cand, cero


def factorizar_por_ruffini(expr, K: "Cuerpo"):
    """Saca todas las raíces racionales una a una con Ruffini y deja el factor que queda."""
    c = desde_expr(expr, K)
    cand, cero = candidatos_racionales(expr) if K.p is None else (list(range(K.p)), 0)
    pasos = []
    raices_encontradas = []
    for _ in range(cero):
        rf = ruffini(c, 0, K)
        pasos.append(rf)
        raices_encontradas.append(sp.Integer(0))
        c = rf.cociente
    cambio = True
    while cambio and grado(c) >= 1:
        cambio = False
        for r in cand:
            if r == 0:
                continue
            rf = ruffini(c, r, K)
            if rf.resto == 0:
                pasos.append(rf)
                raices_encontradas.append(K.norm(r))
                c = rf.cociente
                cambio = True
                break
    return raices_encontradas, c, pasos


# ------------------------------------------------------------- irreducibilidad
def irreducible(expr, cuerpo: str, p: int | None = None):
    """cuerpo ∈ {'Q', 'R', 'C', 'Zp'}. Devuelve (irreducible?, explicación, factorización)."""
    P = sp.Poly(sp.expand(expr), x)
    n = P.degree()
    if n <= 0:
        return False, "Las constantes no se consideran irreducibles (son unidades, o el 0).", P.as_expr()
    if n == 1:
        return True, "Todo polinomio de grado 1 es irreducible (apartado 192): sus únicos divisores son las constantes y sus asociados.", P.as_expr()
    if cuerpo == "C":
        return False, ("En ℂ sólo son irreducibles los de grado 1: por el Teorema Fundamental del Álgebra todo polinomio "
                       "de grado ≥ 2 tiene una raíz r y entonces (x − r) lo divide."), sp.factor(P.as_expr(), extension=sp.I) if n <= 4 else "—"
    if cuerpo == "R":
        if n == 2:
            a, b, c = P.all_coeffs()
            disc = sp.simplify(b ** 2 - 4 * a * c)
            irr = bool(disc < 0)
            return irr, (f"Grado 2: es irreducible en ℝ ⇔ no tiene raíces reales ⇔ discriminante b² − 4ac < 0. Aquí vale {disc}."), sp.factor(P.as_expr())
        if n % 2 == 1:
            return False, ("Grado impar ≥ 3: por Bolzano, un polinomio de grado impar va de −∞ a +∞, así que tiene una raíz real "
                           "y no es irreducible (apartado 194)."), sp.factor(P.as_expr())
        return False, ("En ℝ los irreducibles son los de grado 1 y los de grado 2 sin raíces reales. Este tiene grado "
                       f"{n} ≥ 3, así que se descompone (en factores de grado 1 y 2)."), sp.factor(P.as_expr())
    if cuerpo == "Zp":
        F = sp.factor_list(P.as_expr(), x, modulus=p)
        irr = len(F[1]) == 1 and F[1][0][1] == 1 and sp.degree(F[1][0][0], x) == n
        expl = ("En ℤ_p: " + ("no tiene ningún factor propio." if irr else "se descompone.")
                + (" (Para grado 2 o 3 basta comprobar que no tiene raíces en ℤ_p.)" if n in (2, 3) else ""))
        return irr, expl, sp.factor(P.as_expr(), modulus=p)
    # Q
    F = sp.factor_list(P.as_expr(), x)
    irr = len(F[1]) == 1 and F[1][0][1] == 1 and sp.degree(F[1][0][0], x) == n
    if n in (2, 3):
        expl = ("Grado 2 o 3: es reducible en ℚ ⇔ tiene una raíz racional (si se partiera, uno de los factores tendría "
                "grado 1). " + ("No tiene raíces racionales ⇒ irreducible." if irr else "Tiene raíz racional ⇒ reducible."))
    else:
        expl = ("En ℚ hay irreducibles de cualquier grado (p. ej. xⁿ − 2, por Eisenstein). "
                + ("SymPy no encuentra factores ⇒ irreducible." if irr else "Se descompone en factores de grado menor."))
    return irr, expl, sp.factor(P.as_expr())
