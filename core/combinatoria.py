"""Combinatoria: las 12 formas de contar (Rota), selecciones, Stirling,
inclusión–exclusión y recurrencias. Cada fórmula se puede comprobar por
FUERZA BRUTA (enumerando todos los casos) cuando los números son pequeños."""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from itertools import (combinations, combinations_with_replacement, permutations,
                       product)
from math import comb, factorial, perm
import sympy as sp


# ------------------------------------------------------------ números básicos
@lru_cache(maxsize=None)
def stirling2(n: int, k: int) -> int:
    """Formas de partir un conjunto de n elementos en k bloques no vacíos."""
    if n == k == 0:
        return 1
    if n == 0 or k == 0 or k > n:
        return 0
    return k * stirling2(n - 1, k) + stirling2(n - 1, k - 1)


@lru_cache(maxsize=None)
def stirling1(n: int, k: int) -> int:
    """(sin signo) Permutaciones de n elementos con exactamente k ciclos."""
    if n == k == 0:
        return 1
    if n == 0 or k == 0 or k > n:
        return 0
    return (n - 1) * stirling1(n - 1, k) + stirling1(n - 1, k - 1)


def bell(n: int) -> int:
    return sum(stirling2(n, j) for j in range(n + 1))


@lru_cache(maxsize=None)
def particiones_exactas(n: int, k: int) -> int:
    """Formas de escribir n como suma de exactamente k enteros positivos (sin orden)."""
    if n == k == 0:
        return 1
    if n <= 0 or k <= 0 or k > n:
        return 0
    # o hay una parte igual a 1, o restamos 1 a cada una de las k partes
    return particiones_exactas(n - 1, k - 1) + particiones_exactas(n - k, k)


def particiones_hasta(n: int, k: int) -> int:
    """n como suma de a lo sumo k partes positivas."""
    return sum(particiones_exactas(n, j) for j in range(k + 1))


def sobreyecciones(k: int, n: int) -> int:
    """Aplicaciones sobreyectivas de un conjunto de k elementos en uno de n (inclusión-exclusión)."""
    return sum((-1) ** i * comb(n, i) * (n - i) ** k for i in range(n + 1))


def desarreglos(n: int) -> int:
    """Permutaciones sin puntos fijos: n! Σ (-1)^i / i!."""
    return sum((-1) ** i * factorial(n) // factorial(i) for i in range(n + 1))


def multinomial(ns: list[int]) -> int:
    total = factorial(sum(ns))
    for v in ns:
        total //= factorial(v)
    return total


def comb_rep(n: int, k: int) -> int:
    """C(n+k-1, k) con el caso n = 0 bien definido (sólo k = 0 da 1)."""
    if n == 0:
        return 1 if k == 0 else 0
    return comb(n + k - 1, k)


def catalan(n: int) -> int:
    return comb(2 * n, n) // (n + 1)


# ------------------------------------------------------- las 12 formas de contar
@dataclass
class Caso12:
    numero: int
    formula_tex: str
    nombre: str
    porque: str
    otras: str          # por qué NO valen las fórmulas de los casos vecinos


def doce_formas(k: int, n: int, objetos_distintos: bool, cajas_distintas: bool,
                condicion: str) -> Caso12:
    """Repartir k objetos en n cajas.
    condicion: 'libre' (cualquier reparto), 'inyectiva' (≤1 por caja), 'sobreyectiva' (ninguna vacía)."""
    if k < 0 or n < 0:
        raise ValueError("k y n tienen que ser ≥ 0.")
    D, C = objetos_distintos, cajas_distintas
    if condicion == "libre":
        if D and C:
            return Caso12(n ** k, r"n^k", "Variaciones con repetición / todas las aplicaciones",
                          f"Cada uno de los {k} objetos elige su caja con libertad entre {n}: "
                          f"principio del producto, {n}·{n}·…·{n} ({k} veces).",
                          "No es C(n+k−1,k) porque los objetos se distinguen (no basta con contar cuántos hay en cada caja). "
                          "No es Stirling porque las cajas tienen nombre.")
        if D and not C:
            return Caso12(sum(stirling2(k, j) for j in range(n + 1)),
                          r"\sum_{j=0}^{n} S(k,j)",
                          "Particiones de un conjunto en a lo sumo n bloques",
                          "Como las cajas no tienen nombre, un reparto es una partición del conjunto de objetos "
                          "en bloques; puede haber cajas vacías, así que sumamos los casos con j = 0, 1, …, n bloques usados.",
                          "No es n^k: eso cuenta como distintos repartos que sólo cambian el nombre de las cajas. "
                          "No es sólo S(k,n): eso exigiría usar todas las cajas.")
        if not D and C:
            return Caso12(comb_rep(n, k), r"\binom{n+k-1}{k}",
                          "Combinaciones con repetición (estrellas y barras)",
                          f"Sólo importa cuántos objetos hay en cada caja: x₁+…+x_{n} = {k} con xᵢ ≥ 0. "
                          f"Son {k} estrellas y {n}−1 barras ordenadas: elegir dónde van las {k} estrellas entre {n + k - 1} huecos.",
                          "No es n^k porque al ser iguales los objetos no importa quién va a cada caja. "
                          "No es C(k−1,n−1) porque se permiten cajas vacías.")
        return Caso12(particiones_hasta(k, n), r"\sum_{j=0}^{n} p_j(k)",
                      "Particiones del número k en a lo sumo n sumandos",
                      "Objetos y cajas iguales: un reparto es sólo la lista ordenada (de mayor a menor) de cuántos hay en cada caja "
                      "no vacía, es decir, una partición del número k en como mucho n partes.",
                      "No es C(n+k−1,k): ahí 3+1 y 1+3 serían distintos porque las cajas tienen nombre.")
    if condicion == "inyectiva":
        if k > n:
            return Caso12(0, r"0 \quad (k>n)", "Imposible",
                          f"Hay más objetos ({k}) que cajas ({n}) y en cada caja cabe como mucho uno (principio del palomar).",
                          "—")
        if D and C:
            return Caso12(perm(n, k), r"V_{n,k}=\dfrac{n!}{(n-k)!}", "Variaciones sin repetición / aplicaciones inyectivas",
                          f"El primer objeto tiene {n} cajas, el segundo {n}−1, …: n·(n−1)·…·(n−k+1).",
                          "No es n^k porque dos objetos no pueden compartir caja. No es C(n,k) porque los objetos se distinguen "
                          "(importa cuál va en cada caja).")
        if not D and C:
            return Caso12(comb(n, k), r"\binom{n}{k}", "Combinaciones sin repetición",
                          f"Sólo hay que decidir qué {k} cajas de las {n} quedan ocupadas.",
                          "No es V(n,k) porque al ser iguales los objetos no hay orden entre ellos.")
        return Caso12(1, r"1 \quad (k\le n)", "Una única forma",
                      "Cajas iguales y como mucho un objeto por caja: todos los repartos se ven igual.",
                      "—")
    if condicion == "sobreyectiva":
        if D and C:
            return Caso12(sobreyecciones(k, n),
                          r"n!\,S(k,n)=\sum_{i=0}^{n}(-1)^i\binom{n}{i}(n-i)^k",
                          "Aplicaciones sobreyectivas",
                          "Partimos los objetos en n bloques no vacíos (S(k,n)) y damos nombre de caja a cada bloque (n!). "
                          "Equivale a inclusión–exclusión quitando los repartos que dejan alguna caja vacía.",
                          "No es n^k porque ahí entran repartos con cajas vacías. No es S(k,n) a secas porque las cajas tienen nombre.")
        if D and not C:
            return Caso12(stirling2(k, n), r"S(k,n)", "Número de Stirling de 2ª especie",
                          "Repartir objetos distintos en n cajas iguales sin dejar ninguna vacía es exactamente partir el conjunto en n bloques.",
                          "No es n!·S(k,n) porque las cajas no tienen nombre (no se ordenan los bloques). "
                          "No es Stirling de 1ª especie: esa cuenta permutaciones con n ciclos, no particiones.")
        if not D and C:
            return Caso12(comb(k - 1, n - 1) if k >= 1 and n >= 1 else int(k == n == 0),
                          r"\binom{k-1}{n-1}", "Estrellas y barras con cajas no vacías",
                          f"x₁+…+x_{n} = {k} con xᵢ ≥ 1. Ponemos un objeto en cada caja y repartimos los {k}−{n} restantes libremente: "
                          f"C(({k}−{n})+{n}−1, {k}−{n}) = C({k}−1, {n}−1). O bien: elegir {n}−1 cortes entre los {k}−1 huecos.",
                          "No es C(n+k−1,k) porque ese incluye repartos con cajas vacías.")
        return Caso12(particiones_exactas(k, n), r"p_n(k)", "Particiones de k en exactamente n sumandos",
                      "Objetos y cajas iguales y ninguna vacía: escribir k como suma de n enteros positivos sin importar el orden.",
                      "No es C(k−1,n−1) porque ahí el orden de los sumandos importaría (cajas con nombre).")
    raise ValueError("Condición desconocida.")


def doce_formas_fuerza_bruta(k: int, n: int, objetos_distintos: bool, cajas_distintas: bool,
                             condicion: str, limite: int = 300_000) -> int | None:
    """Enumera TODAS las aplicaciones objetos→cajas y cuenta las clases de equivalencia. None si es demasiado grande."""
    if n ** k > limite:
        return None
    vistos = set()
    for f in product(range(n), repeat=k):
        ocup = [0] * n
        for c in f:
            ocup[c] += 1
        if condicion == "inyectiva" and any(o > 1 for o in ocup):
            continue
        if condicion == "sobreyectiva" and any(o == 0 for o in ocup):
            continue
        if objetos_distintos and cajas_distintas:
            clave = f
        elif not objetos_distintos and cajas_distintas:
            clave = tuple(ocup)
        elif objetos_distintos and not cajas_distintas:
            bloques = {}
            for obj, c in enumerate(f):
                bloques.setdefault(c, []).append(obj)
            clave = frozenset(frozenset(b) for b in bloques.values())
        else:
            clave = tuple(sorted(ocup))
        vistos.add(clave)
    if k == 0:
        # una única aplicación vacía; válida salvo sobreyectiva con n>0
        return 1 if not (condicion == "sobreyectiva" and n > 0) else 0
    return len(vistos)


# ------------------------------------------------------------- selecciones
@dataclass
class Seleccion:
    numero: int
    formula_tex: str
    nombre: str
    porque: str


def seleccion(n: int, k: int, importa_orden: bool, con_repeticion: bool) -> Seleccion:
    """Elegir k elementos de un conjunto de n."""
    if n < 0 or k < 0:
        raise ValueError("n y k tienen que ser ≥ 0.")
    if importa_orden and con_repeticion:
        return Seleccion(n ** k, r"VR_{n,k}=n^k", "Variaciones con repetición",
                         f"Cada una de las {k} posiciones admite cualquiera de los {n} elementos.")
    if importa_orden:
        return Seleccion(perm(n, k) if k <= n else 0, r"V_{n,k}=\dfrac{n!}{(n-k)!}", "Variaciones sin repetición",
                         f"{n} opciones para la 1ª posición, {n}−1 para la 2ª, … hasta {k} posiciones."
                         + (" Si k = n son permutaciones: n!." if k == n else ""))
    if con_repeticion:
        return Seleccion(comb_rep(n, k), r"CR_{n,k}=\binom{n+k-1}{k}", "Combinaciones con repetición",
                         f"Sólo importa cuántas veces sale cada elemento: x₁+…+x_{n} = {k}, xᵢ ≥ 0 (estrellas y barras).")
    return Seleccion(comb(n, k), r"C_{n,k}=\binom{n}{k}=\dfrac{n!}{k!(n-k)!}", "Combinaciones",
                     f"Las variaciones V(n,k) cuentan cada grupo k! veces (una por cada orden), así que dividimos entre k!.")


def seleccion_fuerza_bruta(n: int, k: int, importa_orden: bool, con_repeticion: bool, limite=300_000):
    universo = range(n)
    total_max = n ** k if k else 1
    if total_max > limite:
        return None
    if importa_orden and con_repeticion:
        it = product(universo, repeat=k)
    elif importa_orden:
        it = permutations(universo, k)
    elif con_repeticion:
        it = combinations_with_replacement(universo, k)
    else:
        it = combinations(universo, k)
    return sum(1 for _ in it)


def ejemplos_seleccion(elementos: list[str], k: int, importa_orden: bool, con_repeticion: bool, maximo=30):
    if importa_orden and con_repeticion:
        it = product(elementos, repeat=k)
    elif importa_orden:
        it = permutations(elementos, k)
    elif con_repeticion:
        it = combinations_with_replacement(elementos, k)
    else:
        it = combinations(elementos, k)
    out = []
    for t in it:
        out.append(t)
        if len(out) >= maximo:
            break
    return out


# ------------------------------------------------------ inclusión–exclusión
def inclusion_exclusion(tamanos_intersecciones: dict[frozenset, int], m: int) -> tuple[int, list[str]]:
    """|A1 ∪ … ∪ Am| a partir de |∩_{i∈S} Ai| para todo S no vacío."""
    total = 0
    pasos = []
    for r in range(1, m + 1):
        s = sum(tamanos_intersecciones[frozenset(S)] for S in combinations(range(m), r))
        signo = 1 if r % 2 == 1 else -1
        total += signo * s
        pasos.append(f"{'+' if signo > 0 else '−'} (suma de intersecciones de {r} conjuntos) = {'+' if signo > 0 else '−'}{s}")
    return total, pasos


def inclusion_exclusion_simetrico(m: int, tam_interseccion_r) -> int:
    """Cuando |intersección de r conjuntos| sólo depende de r: Σ (-1)^{r+1} C(m,r) N_r."""
    return sum((-1) ** (r + 1) * comb(m, r) * tam_interseccion_r(r) for r in range(1, m + 1))


# ------------------------------------------------------------- recurrencias
def resolver_recurrencia(coefs: list, f_n, iniciales: list):
    """a_n = c1 a_{n-1} + … + cr a_{n-r} + f(n).
    Devuelve (forma cerrada, ecuación característica, raíces, primeros términos por iteración)."""
    nn = sp.Symbol("n", integer=True, nonnegative=True)
    a = sp.Function("a")
    r = len(coefs)
    if r == 0:
        raise ValueError("Necesito al menos un coeficiente.")
    if len(iniciales) != r:
        raise ValueError(f"Una recurrencia de orden {r} necesita {r} condiciones iniciales (a_0 … a_{r - 1}).")
    lam = sp.Symbol("λ")
    caract = sp.Eq(lam ** r - sum(c * lam ** (r - 1 - i) for i, c in enumerate(coefs)), 0)
    raices = sp.roots(sp.Poly(caract.lhs, lam))
    f_expr = sp.sympify(f_n).subs(sp.Symbol("n"), nn)
    ecu = a(nn) - sum(c * a(nn - 1 - i) for i, c in enumerate(coefs)) - f_expr
    ini = {a(i): v for i, v in enumerate(iniciales)}
    try:
        cerrada = sp.rsolve(ecu, a(nn), ini)
    except Exception:  # noqa: BLE001
        cerrada = None
    # iteración directa (para comprobar)
    terms = list(iniciales)
    for i in range(r, 15):
        terms.append(sp.nsimplify(sum(c * terms[i - 1 - j] for j, c in enumerate(coefs)) + f_expr.subs(nn, i)))
    if cerrada is not None:
        cerrada = sp.simplify(cerrada)
        comprob = all(sp.simplify(cerrada.subs(nn, i) - terms[i]) == 0 for i in range(len(terms)))
        if not comprob:
            cerrada = None
    else:
        comprob = False
    return cerrada, caract, raices, terms, comprob, nn


# ------------------------------------------------------------- particiones (listados)
def particiones_numero(n: int, k: int | None = None, maximo: int = 400):
    """Lista las particiones de n (no crecientes); si k, sólo las de exactamente k sumandos."""
    out = []

    def rec(resto, maxp, actual):
        if len(out) >= maximo:
            return
        if resto == 0:
            if k is None or len(actual) == k:
                out.append(tuple(actual))
            return
        if k is not None and len(actual) >= k:
            return
        for p in range(min(resto, maxp), 0, -1):
            rec(resto - p, p, actual + [p])
    rec(n, n, [])
    return out


def conjugada(part: tuple) -> tuple:
    """Partición conjugada (trasponer el diagrama de Ferrers)."""
    if not part:
        return ()
    return tuple(sum(1 for p in part if p > i) for i in range(part[0]))


def particiones_conjunto(elementos: list, k: int | None = None, maximo: int = 300):
    """Particiones de un conjunto en bloques (si k, en exactamente k bloques)."""
    out = []

    def rec(i, bloques):
        if len(out) >= maximo:
            return
        if i == len(elementos):
            if k is None or len(bloques) == k:
                out.append([list(b) for b in bloques])
            return
        if k is not None and len(bloques) > k:
            return
        x = elementos[i]
        for b in bloques:
            b.append(x)
            rec(i + 1, bloques)
            b.pop()
        bloques.append([x])
        rec(i + 1, bloques)
        bloques.pop()
    rec(0, [])
    return out


def nu(n: int, J: list[int]) -> int:
    """ν(n; J): particiones de n con sumandos en J y en las que aparecen TODOS los de J (apartados 144–147)."""
    J = sorted(set(J))
    if not J or n <= 0:
        return 0

    def NU(r, j):
        if r <= 0:
            return 0
        if j == 1:
            return 1 if r % J[0] == 0 else 0
        return sum(NU(r - kk * J[j - 1], j - 1) for kk in range(1, r // J[j - 1] + 1))
    return NU(n, len(J))


def nu_fuerza_bruta(n: int, J: list[int]) -> int:
    J = sorted(set(J))
    return sum(1 for p in particiones_numero(n, maximo=10 ** 6) if set(p) == set(J))


def palomar(objetos: int, cajas: int) -> int:
    """Alguna caja tiene al menos ⌈N/k⌉ objetos."""
    return -(-objetos // cajas)


def multiplos_inclusion_exclusion(N: int, divisores: list[int]):
    """¿Cuántos de 1..N son múltiplos de alguno de los divisores? (con todos los términos)."""
    from math import lcm
    terminos = []
    total = 0
    for r in range(1, len(divisores) + 1):
        for S in combinations(divisores, r):
            m = 1
            for d in S:
                m = lcm(m, d)
            c = N // m
            signo = 1 if r % 2 else -1
            total += signo * c
            terminos.append((S, m, c, signo))
    directo = sum(1 for x in range(1, N + 1) if any(x % d == 0 for d in divisores))
    return total, terminos, directo


def circulares(m: int) -> int:
    return factorial(m - 1) if m >= 1 else 1
