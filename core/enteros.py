"""Aritmética entera y modular con todos los pasos."""
from __future__ import annotations

from dataclasses import dataclass
from math import gcd
import sympy as sp
from itertools import product


# ------------------------------------------------------ Euclides extendido
@dataclass
class FilaEE:
    a: int
    b: int
    q: int
    r: int
    s: int
    t: int


@dataclass
class EuclidesExt:
    a: int
    b: int
    filas: list[FilaEE]
    d: int
    s: int
    t: int   # d = s*a + t*b


def euclides_extendido(a: int, b: int) -> EuclidesExt:
    if a == 0 and b == 0:
        raise ValueError("mcd(0, 0) no está definido.")
    A, B = abs(a), abs(b)
    r0, s0, t0 = A, 1, 0
    r1, s1, t1 = B, 0, 1
    filas = []
    while r1 != 0:
        q, r = divmod(r0, r1)
        s2, t2 = s0 - q * s1, t0 - q * t1
        filas.append(FilaEE(r0, r1, q, r, s2, t2))
        r0, s0, t0, r1, s1, t1 = r1, s1, t1, r, s2, t2
    # ajustar signos para a, b originales
    s = s0 * (1 if a >= 0 else -1)
    t = t0 * (1 if b >= 0 else -1)
    return EuclidesExt(a, b, filas, r0, s, t)


def mcm(a: int, b: int) -> int:
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // gcd(a, b)


def mcd_lista(nums: list[int]) -> int:
    g = 0
    for v in nums:
        g = gcd(g, v)
    return g


def mcm_lista(nums: list[int]) -> int:
    m = 1
    for v in nums:
        m = mcm(m, v)
    return m


# ------------------------------------------------------ ecuación diofántica
@dataclass
class Diofantica:
    a: int
    b: int
    c: int
    d: int
    tiene_solucion: bool
    x0: int | None = None
    y0: int | None = None
    paso_x: int | None = None   # x = x0 + paso_x * λ
    paso_y: int | None = None   # y = y0 + paso_y * λ
    ee: EuclidesExt | None = None


def diofantica(a: int, b: int, c: int) -> Diofantica:
    """a·x + b·y = c en enteros."""
    if a == 0 and b == 0:
        raise ValueError("Con a = b = 0 la ecuación no tiene variables.")
    ee = euclides_extendido(a, b)
    d = ee.d
    if c % d != 0:
        return Diofantica(a, b, c, d, False, ee=ee)
    f = c // d
    x0, y0 = ee.s * f, ee.t * f
    return Diofantica(a, b, c, d, True, x0, y0, b // d, -(a // d), ee)


# ------------------------------------------------------ congruencias
@dataclass
class Congruencia:
    a: int
    b: int
    m: int
    d: int
    tiene_solucion: bool
    soluciones: list[int]        # representantes en [0, m)
    sol_base: int | None = None  # x ≡ sol_base (mod m/d)
    modulo_reducido: int | None = None
    inverso: int | None = None   # inverso de a/d módulo m/d


def congruencia_lineal(a: int, b: int, m: int) -> Congruencia:
    """a·x ≡ b (mod m)."""
    if m <= 0:
        raise ValueError("El módulo tiene que ser un entero positivo.")
    a %= m
    b %= m
    d = gcd(a, m)
    if d == 0:  # a ≡ 0 y m... no ocurre porque m>0
        d = m
    if b % d != 0:
        return Congruencia(a, b, m, d, False, [])
    m2 = m // d
    a2, b2 = a // d, b // d
    if m2 == 1:
        return Congruencia(a, b, m, d, True, list(range(m)), 0, 1, 0)
    inv = pow(a2, -1, m2)
    x0 = (b2 * inv) % m2
    sols = [x0 + i * m2 for i in range(d)]
    return Congruencia(a, b, m, d, True, sols, x0, m2, inv)


def inverso_modular(a: int, m: int) -> int | None:
    if m <= 0:
        raise ValueError("El módulo tiene que ser positivo.")
    if gcd(a, m) != 1:
        return None
    return pow(a, -1, m)


# ------------------------------------------------------ teorema chino del resto
@dataclass
class PasoTCR:
    x_antes: int
    M_antes: int
    a: int
    m: int
    x_despues: int
    M_despues: int
    explicacion: str


@dataclass
class TCR:
    tiene_solucion: bool
    x: int | None
    M: int | None
    pasos: list[PasoTCR]
    motivo: str = ""


def chino_del_resto(restos: list[int], modulos: list[int]) -> TCR:
    """Resuelve x ≡ a_i (mod m_i). Funciona aunque los módulos NO sean coprimos."""
    if len(restos) != len(modulos) or not restos:
        raise ValueError("Necesito el mismo número de restos que de módulos (al menos uno).")
    if any(m <= 0 for m in modulos):
        raise ValueError("Los módulos tienen que ser positivos.")
    x, M = restos[0] % modulos[0], modulos[0]
    pasos = []
    for a, m in zip(restos[1:], modulos[1:]):
        a %= m
        g = gcd(M, m)
        if (a - x) % g != 0:
            return TCR(False, None, None, pasos,
                       f"x ≡ {x} (mod {M}) y x ≡ {a} (mod {m}) son incompatibles: "
                       f"mcd({M}, {m}) = {g} no divide a {a} − {x} = {a - x}.")
        # x + M·k ≡ a (mod m)  ->  (M/g)·k ≡ (a-x)/g (mod m/g)
        m_g = m // g
        k = ((a - x) // g * pow(M // g, -1, m_g)) % m_g if m_g > 1 else 0
        nuevo_x = x + M * k
        nuevo_M = M * m_g
        nuevo_x %= nuevo_M
        pasos.append(PasoTCR(x, M, a, m, nuevo_x, nuevo_M,
                             f"x = {x} + {M}·k ; imponemos {x} + {M}k ≡ {a} (mod {m}) ⇒ k ≡ {k} (mod {m_g}) "
                             f"⇒ x ≡ {nuevo_x} (mod {nuevo_M})"))
        x, M = nuevo_x, nuevo_M
    return TCR(True, x, M, pasos)


# ------------------------------------------------------ potencias modulares
@dataclass
class PasoPotencia:
    bit: int
    base: int
    acumulado: int


def potencia_modular(base: int, exp: int, m: int):
    """Exponenciación rápida (cuadrado y multiplica) con pasos."""
    if m <= 0:
        raise ValueError("El módulo tiene que ser positivo.")
    if exp < 0:
        inv = inverso_modular(base, m)
        if inv is None:
            raise ValueError(f"{base} no tiene inverso módulo {m}, así que no existe {base}^{exp}.")
        base, exp = inv, -exp
    pasos = []
    res, b, e = 1 % m, base % m, exp
    while e > 0:
        bit = e & 1
        if bit:
            res = (res * b) % m
        pasos.append(PasoPotencia(bit, b, res))
        b = (b * b) % m
        e >>= 1
    return res, pasos, bin(exp)[2:]


# ------------------------------------------------------ teoría de números básica
def factorizacion(n: int) -> dict[int, int]:
    if n == 0:
        raise ValueError("0 no tiene factorización en primos.")
    return sp.factorint(abs(n))


def phi(n: int) -> int:
    if n <= 0:
        raise ValueError("φ(n) se define para n ≥ 1.")
    return int(sp.totient(n))


def divisores(n: int) -> list[int]:
    if n == 0:
        raise ValueError("Todo entero divide a 0.")
    return sp.divisors(abs(n))


def tabla_inversos(m: int) -> list[tuple[int, int | None]]:
    return [(a, inverso_modular(a, m)) for a in range(m)]


# ====================================================== división entera (también negativos)
def division_entera(a: int, b: int):
    """a = q·b + r con 0 ≤ r < |b| (convenio euclídeo: el resto nunca es negativo)."""
    if b == 0:
        raise ValueError("No se puede dividir entre 0.")
    q, r = divmod(a, b)
    if r < 0:          # Python ya da r ≥ 0 si b > 0; con b < 0 lo corregimos
        q, r = q + 1, r - b
    return q, r


def division_por_restas(n: int, m: int):
    """El algoritmo del apartado 150 (corregido: while resto ≥ m)."""
    pasos = []
    c, r = 0, n
    while r >= m:
        r -= m
        c += 1
        pasos.append((c, r))
    return c, r, pasos


# ====================================================== criba de Eratóstenes
def criba(N: int):
    """Devuelve (primos, pasos) con pasos[k] = números tachados al usar k."""
    if N < 2:
        return [], []
    es = [True] * (N + 1)
    es[0] = es[1] = False
    pasos = []
    k = 2
    while k * k <= N:
        if es[k]:
            tachados = list(range(k * k, N + 1, k))
            nuevos = [t for t in tachados if es[t]]
            for t in tachados:
                es[t] = False
            pasos.append((k, nuevos))
        k += 1
    return [i for i in range(N + 1) if es[i]], pasos


# ====================================================== sistemas de numeración
DIGITOS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def a_base(m: int, b: int):
    """Divisiones sucesivas entre b: los restos leídos de abajo arriba son las cifras."""
    if not 2 <= b <= 36:
        raise ValueError("La base tiene que estar entre 2 y 36.")
    if m == 0:
        return "0", [(0, 0, 0)]
    neg = m < 0
    x = abs(m)
    pasos = []
    cifras = []
    while x > 0:
        q, r = divmod(x, b)
        pasos.append((x, q, r))
        cifras.append(DIGITOS[r])
        x = q
    return ("-" if neg else "") + "".join(reversed(cifras)), pasos


def desde_base(texto: str, b: int):
    """Σ cᵢ·bⁱ (método de Horner) con los pasos."""
    t = texto.strip().upper()
    neg = t.startswith("-")
    t = t.lstrip("-")
    if not t:
        raise ValueError("Escribe un número.")
    valor = 0
    pasos = []
    for ch in t:
        d = DIGITOS.find(ch)
        if d < 0 or d >= b:
            raise ValueError(f"La cifra «{ch}» no existe en base {b} (las cifras van de 0 a {DIGITOS[b - 1]}).")
        nuevo = valor * b + d
        pasos.append((valor, d, nuevo))
        valor = nuevo
    return (-valor if neg else valor), pasos


def dividir_en_base(cifras: str, b: int, d: int):
    """Divide un número escrito en base b entre d (< b) cifra a cifra, SIN pasar por base 10
    (como en el apartado 166). Devuelve (cociente en base b, resto, pasos)."""
    cociente = []
    resto = 0
    pasos = []
    for ch in cifras.upper():
        c = DIGITOS.index(ch)
        actual = resto * b + c
        q, resto = divmod(actual, d)
        pasos.append((ch, actual, q, resto))
        cociente.append(DIGITOS[q])
    s = "".join(cociente).lstrip("0") or "0"
    return s, resto, pasos


def cambiar_base_directo(cifras: str, b1: int, b2: int):
    """Pasa de base b1 a base b2 dividiendo repetidamente entre b2 DENTRO de la base b1 (requiere b2 < b1)."""
    if b2 >= b1:
        raise ValueError("Este método directo necesita que la base de llegada sea menor que la de partida.")
    restos = []
    pasos_tot = []
    actual = cifras.upper().lstrip("0") or "0"
    while actual != "0":
        q, r, pasos = dividir_en_base(actual, b1, b2)
        pasos_tot.append((actual, q, r, pasos))
        restos.append(DIGITOS[r])
        actual = q
    return "".join(reversed(restos)) or "0", pasos_tot


def sumar_en_base(x: str, y: str, b: int):
    """Suma en columna con llevadas, toda en base b."""
    X, Y = x.upper()[::-1], y.upper()[::-1]
    out, llevadas, lleva = [], [], 0
    for i in range(max(len(X), len(Y))):
        a = DIGITOS.index(X[i]) if i < len(X) else 0
        c = DIGITOS.index(Y[i]) if i < len(Y) else 0
        s = a + c + lleva
        out.append(DIGITOS[s % b])
        llevadas.append(lleva)
        lleva = s // b
    if lleva:
        out.append(DIGITOS[lleva])
    return "".join(reversed(out)), llevadas


def tabla_base(b: int, op: str = "+"):
    return [[a_base(i + j if op == "+" else i * j, b)[0] for j in range(b)] for i in range(b)]


# ====================================================== divisores
def info_divisores(n: int):
    """Número, suma y producto de divisores con las fórmulas del apartado 157."""
    fac = factorizacion(n)
    numero = 1
    suma = 1
    for p, e in fac.items():
        numero *= e + 1
        suma *= (p ** (e + 1) - 1) // (p - 1)
    divs = divisores(n)
    prod_formula = sp.sqrt(sp.Integer(n) ** numero)   # √(n^{d(n)})
    prod_real = 1
    for d in divs:
        prod_real *= d
    return {"factorizacion": fac, "numero": numero, "suma": suma, "producto": prod_formula,
            "divisores": divs, "comprobacion": numero == len(divs) and suma == sum(divs) and prod_formula == prod_real}


def mcd_mcm_factorizacion(m: int, n: int):
    """mcd = ∏ p^min, mcm = ∏ p^max (apartado 160)."""
    fm, fn = factorizacion(m), factorizacion(n)
    primos = sorted(set(fm) | set(fn))
    filas = [(p, fm.get(p, 0), fn.get(p, 0), min(fm.get(p, 0), fn.get(p, 0)), max(fm.get(p, 0), fn.get(p, 0))) for p in primos]
    d = 1
    M = 1
    for p, a, b, mi, ma in filas:
        d *= p ** mi
        M *= p ** ma
    return filas, d, M


def libre_de_cuadrados(m: int):
    fac = factorizacion(m)
    malos = [p for p, e in fac.items() if e >= 2]
    return not malos, malos


# ====================================================== Z_n
def tabla_zn(n: int, op: str):
    return [[(a + b) % n if op == "+" else (a * b) % n for b in range(n)] for a in range(n)]


def unidades(n: int):
    return [a for a in range(1, n) if gcd(a, n) == 1] if n > 1 else []


def divisores_de_cero(n: int):
    return [a for a in range(1, n) if any((a * b) % n == 0 for b in range(1, n))]


def orden_multiplicativo(a: int, n: int):
    if gcd(a, n) != 1:
        return None
    k, x = 1, a % n
    while x != 1 % n:
        x = (x * a) % n
        k += 1
    return k


def wilson(n: int):
    f = 1
    for i in range(1, n):
        f = (f * i) % n
    return f, (f == n - 1)


def ultimas_cifras(base: int, exp: int, cifras: int):
    m = 10 ** cifras
    return pow(base, exp, m)


# ====================================================== sistemas lineales módulo p
def gauss_mod_p(A: list[list[int]], b: list[int], p: int):
    """Eliminación de Gauss–Jordan en Z_p. Devuelve dict con rango, compatibilidad, solución particular,
    base del núcleo, número de soluciones y los pasos."""
    if not sp.isprime(p):
        raise ValueError(f"{p} no es primo: en Z_{p} no se puede dividir siempre (no es un cuerpo).")
    m = len(A)
    nvar = len(A[0]) if A else 0
    M = [[x % p for x in fila] + [bi % p] for fila, bi in zip(A, b)]
    pasos = [("Matriz ampliada inicial", [r[:] for r in M])]
    fila = 0
    pivotes = []
    for col in range(nvar):
        piv = next((r for r in range(fila, m) if M[r][col] % p), None)
        if piv is None:
            continue
        if piv != fila:
            M[fila], M[piv] = M[piv], M[fila]
            pasos.append((f"Intercambio F{fila + 1} ↔ F{piv + 1}", [r[:] for r in M]))
        inv = pow(M[fila][col], -1, p)
        if inv != 1:
            M[fila] = [(v * inv) % p for v in M[fila]]
            pasos.append((f"F{fila + 1} ← {inv}·F{fila + 1}  (multiplico por el inverso del pivote)", [r[:] for r in M]))
        for r in range(m):
            if r != fila and M[r][col] % p:
                f = M[r][col]
                M[r] = [(M[r][j] - f * M[fila][j]) % p for j in range(nvar + 1)]
                pasos.append((f"F{r + 1} ← F{r + 1} − {f}·F{fila + 1}", [rr[:] for rr in M]))
        pivotes.append(col)
        fila += 1
        if fila == m:
            break
    rango = len(pivotes)
    incompatible = any(all(v == 0 for v in M[r][:nvar]) and M[r][nvar] != 0 for r in range(m))
    res = {"rango": rango, "rango_ampliada": rango + (1 if incompatible else 0), "compatible": not incompatible,
           "pasos": pasos, "pivotes": pivotes, "nvar": nvar}
    if incompatible:
        return res
    libres = [j for j in range(nvar) if j not in pivotes]
    x0 = [0] * nvar
    for i, c in enumerate(pivotes):
        x0[c] = M[i][nvar]
    base = []
    for lj in libres:
        v = [0] * nvar
        v[lj] = 1
        for i, c in enumerate(pivotes):
            v[c] = (-M[i][lj]) % p
        base.append(v)
    res.update({"particular": x0, "libres": libres, "nucleo": base, "num_soluciones": p ** len(libres)})
    # comprobación
    res["comprobado"] = all(sum(A[i][j] * x0[j] for j in range(nvar)) % p == b[i] % p for i in range(m))
    return res


def congruencia_varias(coefs: list[int], b: int, m: int, max_fuerza_bruta: int = 200_000):
    """a₁X₁+…+aₙXₙ ≡ b (mód m): hay solución ⇔ g = mcd(a₁,…,aₙ,m) | b, y entonces g·mⁿ⁻¹ soluciones (apartado 232)."""
    g = m
    for a in coefs:
        g = gcd(g, a)
    nsol = g * m ** (len(coefs) - 1) if b % g == 0 else 0
    fb = None
    if m ** len(coefs) <= max_fuerza_bruta:
        fb = sum(1 for xs in product(range(m), repeat=len(coefs)) if sum(a * x for a, x in zip(coefs, xs)) % m == b % m)
    # una solución particular (Bézout encadenado)
    part = None
    if b % g == 0:
        # g = Σ λᵢaᵢ + μm
        lam = []
        acc = 0
        cur = 0
        for a in coefs:
            ee = euclides_extendido(cur, a) if (cur or a) else None
            if ee is None:
                lam.append(0)
                continue
            lam = [l * ee.s for l in lam] + [ee.t]
            cur = ee.d
        ee = euclides_extendido(cur, m) if (cur or m) else None
        if ee:
            lam = [l * ee.s for l in lam]
            f = b // g
            part = [(l * f) % m for l in lam]
            if sum(a * x for a, x in zip(coefs, part)) % m != b % m:
                part = None
    return {"g": g, "compatible": b % g == 0, "num_soluciones": nsol, "fuerza_bruta": fb, "particular": part}


def diofantica_n(coefs: list[int], c: int):
    """a₁x₁ + … + aₙxₙ = c en ℤ: solución ⇔ mcd(a₁,…,aₙ) | c (apartado 197), con una particular."""
    g = 0
    for a in coefs:
        g = gcd(g, a)
    if g == 0:
        return {"g": 0, "compatible": c == 0, "particular": [0] * len(coefs) if c == 0 else None}
    if c % g:
        return {"g": g, "compatible": False, "particular": None}
    lam = []
    cur = 0
    for a in coefs:
        ee = euclides_extendido(cur, a)
        lam = [l * ee.s for l in lam] + [ee.t]
        cur = ee.d
    f = c // g
    part = [l * f for l in lam]
    assert sum(a * x for a, x in zip(coefs, part)) == c
    return {"g": g, "compatible": True, "particular": part}


def congruencia_por_primos(coefs: list[int], b: int, m: int):
    """Si m es libre de cuadrados, la congruencia mód m equivale a una congruencia mód cada primo (TCR)."""
    libre, _ = libre_de_cuadrados(m)
    if not libre:
        return None
    out = []
    for p in factorizacion(m):
        out.append((p, [a % p for a in coefs], b % p))
    return out
