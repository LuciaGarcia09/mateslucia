"""Grupos, anillos y cuerpos finitos: permutaciones, ℤₙ y cocientes 𝔽ₚ[x]/(f)."""
from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from math import gcd, lcm
import re

import sympy as sp


# ======================================================================= permutaciones
class ErrorPermutacion(ValueError):
    pass


def leer_permutacion(texto: str, n: int | None = None) -> tuple[int, ...]:
    """Acepta notación de una línea «2314» / «2 3 1 4» o ciclos «(1 2 3)(4 5)». Devuelve la imagen de 1..n."""
    t = texto.strip()
    if not t:
        raise ErrorPermutacion("Escribe una permutación.")
    if "(" in t:
        ciclos = re.findall(r"\(([^()]*)\)", t)
        nums = [[int(v) for v in re.split(r"[\s,]+", c.strip()) if v] for c in ciclos]
        maxi = max([n or 0] + [v for c in nums for v in c])
        img = list(range(1, maxi + 1))
        vistos = set()
        # se componen de derecha a izquierda, como funciones
        for c in reversed(nums):
            if len(set(c)) != len(c):
                raise ErrorPermutacion(f"El ciclo ({' '.join(map(str, c))}) repite un número.")
            if any(v < 1 for v in c):
                raise ErrorPermutacion("Los elementos van de 1 a n.")
            ciclo = {c[i]: c[(i + 1) % len(c)] for i in range(len(c))}
            img = [ciclo.get(v, v) for v in img]
            vistos |= set(c)
        return tuple(img)
    partes = re.split(r"[\s,]+", t) if re.search(r"[\s,]", t) else list(t)
    try:
        img = [int(v) for v in partes if v]
    except ValueError as exc:
        raise ErrorPermutacion("Usa números: «2314» o ciclos «(1 2 3)».") from exc
    m = len(img)
    if sorted(img) != list(range(1, m + 1)):
        raise ErrorPermutacion(f"En notación de una línea tienen que aparecer 1, …, {m} una vez cada uno.")
    if n and n > m:
        img += list(range(m + 1, n + 1))
    return tuple(img)


def componer(f, g):
    """(f ∘ g)(i) = f(g(i)): primero g, luego f."""
    n = max(len(f), len(g))
    F = list(f) + list(range(len(f) + 1, n + 1))
    G = list(g) + list(range(len(g) + 1, n + 1))
    return tuple(F[G[i] - 1] for i in range(n))


def inversa(f):
    inv = [0] * len(f)
    for i, v in enumerate(f, 1):
        inv[v - 1] = i
    return tuple(inv)


def ciclos(f) -> list[tuple[int, ...]]:
    vistos, out = set(), []
    for i in range(1, len(f) + 1):
        if i in vistos:
            continue
        c, j = [], i
        while j not in vistos:
            vistos.add(j)
            c.append(j)
            j = f[j - 1]
        out.append(tuple(c))
    return out


def orden_permutacion(f) -> int:
    return lcm(*[len(c) for c in ciclos(f)])


def signo(f) -> int:
    return (-1) ** sum(len(c) - 1 for c in ciclos(f))


def texto_ciclos(f) -> str:
    cs = [c for c in ciclos(f) if len(c) > 1]
    return "".join("(" + " ".join(map(str, c)) + ")" for c in cs) or "id"


def potencias(f):
    out, p = [], tuple(range(1, len(f) + 1))
    while True:
        p = componer(f, p)
        out.append(p)
        if p == tuple(range(1, len(f) + 1)):
            return out


def ordenes_en_Sn(n: int) -> dict[int, int]:
    """Cuántos elementos de Sₙ tienen cada orden (por fuerza bruta, n ≤ 7)."""
    from itertools import permutations
    cuenta: dict[int, int] = {}
    for p in permutations(range(1, n + 1)):
        o = orden_permutacion(p)
        cuenta[o] = cuenta.get(o, 0) + 1
    return dict(sorted(cuenta.items()))


# ======================================================================= ℤₙ
@dataclass
class InfoZn:
    n: int
    unidades: list[int]
    divisores_cero: list[int]     # no nulos
    nilpotentes: list[int]
    idempotentes: list[int]
    es_dominio: bool
    es_cuerpo: bool
    ideales: list[tuple[int, list[int]]]      # (d, ⟨d⟩) con d | n
    maximales: list[int]


def info_zn(n: int) -> InfoZn:
    if n < 2:
        raise ValueError("Toma n ≥ 2.")
    uni = [a for a in range(1, n) if gcd(a, n) == 1]
    dz = [a for a in range(1, n) if gcd(a, n) > 1]
    nil = [a for a in range(n) if any(pow(a, k, n) == 0 for k in range(1, n + 1))]
    idem = [a for a in range(n) if a * a % n == a]
    divs = [d for d in range(1, n + 1) if n % d == 0]
    ideales = [(d, sorted({d * k % n for k in range(n)})) for d in divs]
    maxi = [d for d in divs if sp.isprime(d)]
    primo = sp.isprime(n)
    return InfoZn(n, uni, dz, nil, idem, primo, primo, ideales, maxi)


def orden_aditivo(a: int, n: int) -> int:
    return n // gcd(a % n, n) if a % n else 1


def orden_en_Q_Z(r: sp.Rational) -> int:
    """Orden de [r] en el grupo ℚ/ℤ: el denominador de r reducida."""
    return int(sp.Rational(r).q)


# ======================================================================= 𝔽ₚ[x]/(f)
from .parsing import x  # el mismo símbolo que usa el lector de expresiones


@dataclass
class Cociente:
    p: int
    f: sp.Poly
    elementos: list[sp.Poly]
    irreducible: bool
    unidades: list[sp.Poly]
    divisores_cero: list[sp.Poly]
    nilpotentes: list[sp.Poly]
    factores: list


def cociente_fp(f_expr, p: int) -> Cociente:
    if not sp.isprime(p):
        raise ValueError("p tiene que ser primo para que 𝔽ₚ sea un cuerpo.")
    f = sp.Poly(f_expr, x, modulus=p)
    d = f.degree()
    if d < 1:
        raise ValueError("El polinomio tiene que tener grado ≥ 1.")
    if p ** d > 729:
        raise ValueError(f"Saldrían {p ** d} elementos; prueba con algo más pequeño (como mucho 729).")
    elems = [sp.Poly(sum(c * x ** i for i, c in enumerate(reversed(cs))), x, modulus=p) for cs in product(range(p), repeat=d)]
    cero = sp.Poly(0, x, modulus=p)
    uno = sp.Poly(1, x, modulus=p)
    mul = lambda a, b: (a * b).rem(f)  # noqa: E731
    uni = [a for a in elems if not a.is_zero and any(mul(a, b) == uno for b in elems)]
    dz = [a for a in elems if not a.is_zero and any(not b.is_zero and mul(a, b).is_zero for b in elems)]
    nil = []
    for a in elems:
        q = a
        for _ in range(d + 1):
            if q.is_zero:
                nil.append(a)
                break
            q = mul(q, a)
    fl = sp.factor_list(f.as_expr(), x, modulus=p)
    irr = len(fl[1]) == 1 and fl[1][0][1] == 1 and sp.Poly(fl[1][0][0], x, modulus=p).degree() == d
    return Cociente(p, f, elems, irr, uni, dz, nil, fl[1])


def fmt_poly(a: sp.Poly) -> str:
    e = a.as_expr()
    # representantes 0..p-1 en lugar de negativos
    p = a.get_modulus()
    pos = sp.Poly([int(c) % p for c in a.all_coeffs()], x).as_expr() if not a.is_zero else 0
    return sp.sstr(pos if pos != 0 else e).replace("**", "^").replace("*", "")
