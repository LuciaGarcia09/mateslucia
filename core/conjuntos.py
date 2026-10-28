"""Conjuntos, aplicaciones y relaciones finitas (Temas 1–3 de Matemática Finita).

Todo funciona con conjuntos FINITOS que escribes tú, y cada propiedad que falla
viene con su CONTRAEJEMPLO concreto (que es lo que se pide en los exámenes).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from itertools import chain, combinations, product
from math import gcd
import re


class ErrorConjunto(ValueError):
    pass


# ============================================================ lectura de elementos
def _elemento(t: str):
    t = t.strip()
    if re.fullmatch(r"-?\d+", t):
        return int(t)
    return t


def leer_conjunto(texto: str) -> list:
    """«{1, 2, 3}», «1,2,3», «a b c» o «1..10» (rango)."""
    t = texto.strip()
    if t in ("", "{}", "∅", "vacio", "vacío"):
        return []
    t = t.strip("{}")
    m = re.fullmatch(r"\s*(-?\d+)\s*\.\.\s*(-?\d+)\s*", t)
    if m:
        a, b = int(m.group(1)), int(m.group(2))
        if b - a > 400:
            raise ErrorConjunto("El rango es demasiado grande (máximo 400 elementos).")
        return list(range(a, b + 1))
    partes = [p for p in re.split(r"[,;\s]+", t) if p]
    vistos, out = set(), []
    for p in partes:
        e = _elemento(p)
        if e not in vistos:
            vistos.add(e)
            out.append(e)
    return out


def ordenar(xs):
    try:
        return sorted(xs)
    except TypeError:
        return sorted(xs, key=lambda v: (str(type(v)), str(v)))


def fmt(conj) -> str:
    xs = ordenar(conj)
    if not xs:
        return "∅"
    return "{" + ", ".join(_fmt_el(x) for x in xs) + "}"


def _fmt_el(x):
    if isinstance(x, frozenset):
        return fmt(x)
    if isinstance(x, tuple):
        return "(" + ", ".join(_fmt_el(v) for v in x) + ")"
    return str(x)


# ============================================================ expresiones de conjuntos
_OPS = {"∪": 1, "∩": 2, "−": 1, "Δ": 1, "×": 3}


def evaluar_expresion(expr: str, conjuntos: dict[str, list], universo: list | None):
    """Evalúa p.ej. «(A ∪ B) − C'» con ∪ ∩ − Δ × y complemento ' (respecto del universo)."""
    t = expr
    for a, b in ((r"\bu\b|\bU\b(?![A-Za-z])|\|", "∪"), (r"&|\bn\b", "∩"), (r"\\|-", "−"), (r"\^|Δ|△", "Δ"),
                 (r"ᶜ|c\b(?=[\s)∪∩−Δ]|$)", "'"), (r"\bx\b|\*", "×")):
        t = re.sub(a, b, t)
    toks = re.findall(r"[A-Z][A-Za-z0-9]*|[∪∩−Δ×()']", t)
    if re.sub(r"[A-Z][A-Za-z0-9]*|[∪∩−Δ×()'\s]", "", t):
        raise ErrorConjunto("Usa nombres en mayúscula (A, B, C…), paréntesis y ∪ ∩ − Δ × '.")
    pos = [0]
    pasos: list[tuple[str, frozenset]] = []

    def ver():
        return toks[pos[0]] if pos[0] < len(toks) else None

    def atomo():
        tk = ver()
        if tk == "(":
            pos[0] += 1
            v, s = binaria(0)
            if ver() != ")":
                raise ErrorConjunto("Falta un paréntesis «)».")
            pos[0] += 1
            v_, s_ = v, f"({s})"
        elif tk and re.match(r"[A-Z]", tk):
            if tk not in conjuntos:
                raise ErrorConjunto(f"No has definido el conjunto {tk}.")
            pos[0] += 1
            v_, s_ = frozenset(conjuntos[tk]), tk
        else:
            raise ErrorConjunto(f"Esperaba un conjunto y encontré «{tk}».")
        while ver() == "'":
            pos[0] += 1
            if universo is None:
                raise ErrorConjunto("Para el complementario (A') tienes que definir el universo U.")
            v_ = frozenset(universo) - v_
            s_ = f"{s_}ᶜ"
            pasos.append((s_, v_))
        return v_, s_

    def binaria(pmin):
        izq, si = atomo()
        while ver() in _OPS and _OPS[ver()] >= pmin:
            op = ver()
            pos[0] += 1
            der, sd = binaria(_OPS[op] + 1)
            if op == "∪":
                izq = izq | der
            elif op == "∩":
                izq = izq & der
            elif op == "−":
                izq = izq - der
            elif op == "Δ":
                izq = izq ^ der
            else:
                izq = frozenset(product(ordenar(izq), ordenar(der)))
            si = f"{si} {op} {sd}"
            pasos.append((si, izq))
        return izq, si

    v, s = binaria(0)
    if pos[0] != len(toks):
        raise ErrorConjunto(f"Sobra algo a partir de «{toks[pos[0]]}».")
    return v, pasos


def partes(conj, maximo=10):
    xs = ordenar(conj)
    if len(xs) > maximo:
        raise ErrorConjunto(f"P(A) tendría 2^{len(xs)} elementos; usa conjuntos de como mucho {maximo}.")
    return [frozenset(c) for c in chain.from_iterable(combinations(xs, r) for r in range(len(xs) + 1))]


# ============================================================ aplicaciones finitas
@dataclass
class Aplicacion:
    dominio: list
    codominio: list
    regla: dict
    problemas: list = field(default_factory=list)   # por qué NO es aplicación (si falla)

    @property
    def es_aplicacion(self):
        return not self.problemas

    def imagen(self, sub=None):
        sub = self.dominio if sub is None else sub
        return frozenset(self.regla[a] for a in sub if a in self.regla)

    def contraimagen(self, sub):
        s = set(sub)
        return frozenset(a for a in self.dominio if self.regla.get(a) in s)

    def inyectiva(self):
        vistos = {}
        for a in self.dominio:
            b = self.regla[a]
            if b in vistos:
                return False, (vistos[b], a, b)
            vistos[b] = a
        return True, None

    def sobreyectiva(self):
        im = self.imagen()
        faltan = [b for b in self.codominio if b not in im]
        return (not faltan), faltan

    def inversa(self):
        if self.inyectiva()[0] and self.sobreyectiva()[0]:
            return {b: a for a, b in self.regla.items()}
        return None


def leer_aplicacion(dom: list, cod: list, texto: str) -> Aplicacion:
    """«a→1, b→2, c→1» (también admite -> y =>)."""
    regla, problemas = {}, []
    trozos = [p for p in re.split(r"[,;\n]+", texto) if p.strip()]
    for p in trozos:
        m = re.match(r"\s*(.+?)\s*(?:→|->|=>|↦|:)\s*(.+?)\s*$", p)
        if not m:
            raise ErrorConjunto(f"No entiendo «{p.strip()}»; escribe cada flecha como a→b.")
        a, b = _elemento(m.group(1)), _elemento(m.group(2))
        if a not in dom:
            problemas.append(f"{a} no está en el dominio.")
            continue
        if b not in cod:
            problemas.append(f"{a} va a {b}, que no está en el conjunto de llegada.")
            continue
        if a in regla and regla[a] != b:
            problemas.append(f"{a} tiene dos imágenes ({regla[a]} y {b}): eso no es una aplicación.")
            continue
        regla[a] = b
    for a in dom:
        if a not in regla:
            problemas.append(f"{a} no tiene imagen: en una aplicación TODO el dominio tiene que tener flecha.")
    return Aplicacion(dom, cod, regla, problemas)


def componer(f: Aplicacion, g: Aplicacion):
    """g ∘ f (primero f, luego g)."""
    if not set(f.imagen()) <= set(g.dominio):
        raise ErrorConjunto("Para hacer g∘f, la imagen de f tiene que estar dentro del dominio de g.")
    return Aplicacion(f.dominio, g.codominio, {a: g.regla[f.regla[a]] for a in f.dominio})


# ============================================================ relaciones
@dataclass
class Propiedad:
    nombre: str
    cumple: bool
    contraejemplo: str = ""


def relacion_por_regla(A: list, regla: str) -> set:
    """Construye R ⊆ A×A con una regla en a y b: «a | b», «a ≡ b mod 3», «a <= b», «a + b es par»…"""
    r = regla.strip()
    m = re.fullmatch(r"\s*a\s*(?:≡|==|=)\s*b\s*\(?\s*(?:mod|mód)\s*(\d+)\s*\)?\s*", r)
    if m:
        k = int(m.group(1))
        return {(a, b) for a in A for b in A if (a - b) % k == 0}
    if re.fullmatch(r"\s*a\s*\|\s*b\s*", r):
        return {(a, b) for a in A for b in A if (b == 0) or (a != 0 and b % a == 0)}
    py = (r.replace("≤", "<=").replace("≥", ">=").replace("≠", "!=").replace("^", "**")
          .replace(" es par", " % 2 == 0").replace(" es impar", " % 2 == 1"))
    py = re.sub(r"(?<![<>!=])=(?!=)", "==", py)
    if re.search(r"[^ab0-9+\-*/%<>=!() .,]|__", py.replace("and", "").replace("or", "").replace("not", "")
                 .replace("abs", "").replace("gcd", "").replace("max", "").replace("min", "")):
        raise ErrorConjunto("La regla sólo puede usar a, b, números y operaciones (+ − * / % ** < ≤ = | mod, «es par»).")
    entorno = {"abs": abs, "gcd": gcd, "max": max, "min": min, "__builtins__": {}}
    out = set()
    for a in A:
        for b in A:
            try:
                if eval(py, entorno, {"a": a, "b": b}):  # noqa: S307 (expresión filtrada arriba)
                    out.add((a, b))
            except ZeroDivisionError:
                pass
            except Exception as exc:  # noqa: BLE001
                raise ErrorConjunto(f"No puedo evaluar la regla: {exc}") from exc
    return out


def relacion_por_pares(A: list, texto: str) -> set:
    pares = re.findall(r"\(\s*([^,()]+?)\s*,\s*([^,()]+?)\s*\)", texto)
    R = set()
    for a, b in pares:
        a, b = _elemento(a), _elemento(b)
        if a not in A or b not in A:
            raise ErrorConjunto(f"El par ({a}, {b}) usa elementos que no están en A.")
        R.add((a, b))
    return R


def propiedades(A: list, R: set) -> dict[str, Propiedad]:
    out = {}
    falta = [a for a in A if (a, a) not in R]
    out["reflexiva"] = Propiedad("Reflexiva", not falta, f"({falta[0]}, {falta[0]}) ∉ R" if falta else "")
    sim = next(((a, b) for (a, b) in ordenar(R) if (b, a) not in R), None)
    out["simetrica"] = Propiedad("Simétrica", sim is None, f"({sim[0]}, {sim[1]}) ∈ R pero ({sim[1]}, {sim[0]}) ∉ R" if sim else "")
    anti = next(((a, b) for (a, b) in ordenar(R) if a != b and (b, a) in R), None)
    out["antisimetrica"] = Propiedad("Antisimétrica", anti is None,
                                     f"({anti[0]}, {anti[1]}) y ({anti[1]}, {anti[0]}) están en R con {anti[0]} ≠ {anti[1]}" if anti else "")
    tra = None
    for (a, b) in ordenar(R):
        for (c, d) in ordenar(R):
            if b == c and (a, d) not in R:
                tra = (a, b, d)
                break
        if tra:
            break
    out["transitiva"] = Propiedad("Transitiva", tra is None,
                                  f"({tra[0]}, {tra[1]}) ∈ R y ({tra[1]}, {tra[2]}) ∈ R pero ({tra[0]}, {tra[2]}) ∉ R" if tra else "")
    tot = next(((a, b) for a, b in combinations(A, 2) if (a, b) not in R and (b, a) not in R), None)
    out["total"] = Propiedad("Total (todos comparables)", tot is None, f"{tot[0]} y {tot[1]} no están relacionados en ningún sentido" if tot else "")
    return out


def clases_equivalencia(A: list, R: set) -> list[list]:
    clases, usados = [], set()
    for a in A:
        if a in usados:
            continue
        c = [b for b in A if (a, b) in R]
        usados |= set(c)
        clases.append(c)
    return clases


def hasse(A: list, R: set) -> set:
    """Relación de cobertura: a ⋖ b si a ≺ b y no hay c con a ≺ c ≺ b."""
    estricto = {(a, b) for (a, b) in R if a != b}
    return {(a, b) for (a, b) in estricto if not any((a, c) in estricto and (c, b) in estricto for c in A)}


def niveles_hasse(A: list, R: set) -> dict:
    cub = hasse(A, R)
    nivel = {}

    def niv(x, pila=()):
        if x in nivel:
            return nivel[x]
        if x in pila:
            return 0
        abajo = [a for (a, b) in cub if b == x]
        nivel[x] = 0 if not abajo else 1 + max(niv(a, pila + (x,)) for a in abajo)
        return nivel[x]
    for x in A:
        niv(x)
    return nivel


@dataclass
class Extremos:
    cotas_sup: list
    cotas_inf: list
    supremo: object
    infimo: object
    maximo: object
    minimo: object
    maximales: list
    minimales: list


def extremos(A: list, R: set, B: list) -> Extremos:
    def leq(x, y):
        return (x, y) in R
    cs = [c for c in A if all(leq(b, c) for b in B)]
    ci = [c for c in A if all(leq(c, b) for b in B)]
    sup = next((c for c in cs if all(leq(c, d) for d in cs)), None)
    inf = next((c for c in ci if all(leq(d, c) for d in ci)), None)
    mx = next((b for b in B if all(leq(x, b) for x in B)), None)
    mn = next((b for b in B if all(leq(b, x) for x in B)), None)
    maxl = [b for b in B if not any(leq(b, x) and x != b for x in B)]
    minl = [b for b in B if not any(leq(x, b) and x != b for x in B)]
    return Extremos(cs, ci, sup, inf, mx, mn, maxl, minl)


def bien_ordenado(A: list, R: set) -> tuple[bool, str]:
    """En un conjunto FINITO: buen orden ⇔ orden total (todo subconjunto no vacío finito de una
    cadena tiene mínimo). Si no es total, el par incomparable {a, b} no tiene mínimo."""
    props = propiedades(A, R)
    if not props["total"].cumple:
        return False, props["total"].contraejemplo + " ⇒ el subconjunto formado por esos dos no tiene mínimo"
    return True, "es un orden total en un conjunto finito, así que todo subconjunto no vacío tiene mínimo"


def clausura_reflexiva(A, R):
    return set(R) | {(a, a) for a in A}


def clausura_simetrica(R):
    return set(R) | {(b, a) for (a, b) in R}


def clausura_transitiva(A, R):
    """Algoritmo de Warshall: añade (a,c) si (a,b) y (b,c) ya están, hasta que no cambie."""
    T = set(R)
    for k in A:
        for i in A:
            if (i, k) in T:
                for j in A:
                    if (k, j) in T:
                        T.add((i, j))
    return T


def matriz(A: list, R: set) -> list[list[int]]:
    return [[1 if (a, b) in R else 0 for b in A] for a in A]


def divisores_de(n: int) -> list[int]:
    return [d for d in range(1, n + 1) if n % d == 0]


# conjuntos del ejercicio 162 (divisibilidad), listos para cargar
PRESETS_DIVISIBILIDAD = {
    "A = {n : 4 ≤ n ≤ 28}": list(range(4, 29)),
    "C = {n ≥ 4 : n | 60}": [n for n in divisores_de(60) if n >= 4],
    "D = Div(24) ∩ Div(160)": sorted(set(divisores_de(24)) & set(divisores_de(160))),
    "E = Div(42) ∪ Div(98)": sorted(set(divisores_de(42)) | set(divisores_de(98))),
    "F = Div(64) ∪ Div(125)": sorted(set(divisores_de(64)) | set(divisores_de(125))),
    "Div(36)": divisores_de(36),
    "B (hasta 60) = 6ℕ⁺ ∪ 9ℕ⁺": sorted({6 * n for n in range(1, 11)} | {9 * n for n in range(1, 7)}),
}
