"""Lógica proposicional y de predicados (Tema 1 de Matemática Finita).

- Analizador propio de fórmulas: admite ¬ ∧ ∨ → ↔ ⊕ y también no/y/o/->/<->/=>/<=>…
- Tabla de verdad con TODAS las subfórmulas como columnas (así se ve el porqué).
- Clasificación (tautología, contradicción, contingencia), equivalencias, FND/FNC.
- Negación de enunciados con cuantificadores, paso a paso.
- Comprobador de demostraciones por inducción (sumas y divisibilidad).
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import product
import re
import sympy as sp

# ============================================================ AST
@dataclass(frozen=True)
class Var:
    nombre: str


@dataclass(frozen=True)
class Const:
    valor: bool


@dataclass(frozen=True)
class No:
    a: object


@dataclass(frozen=True)
class Bin:
    op: str      # '∧', '∨', '→', '↔', '⊕'
    a: object
    b: object


PRECEDENCIA = {"↔": 1, "→": 2, "∨": 3, "⊕": 3, "∧": 4}


class ErrorFormula(ValueError):
    pass


_SINONIMOS = [
    (r"<->|<=>|⇔|\bsii\b|\biff\b", " ↔ "),
    (r"->|=>|⇒|\bentonces\b|\bimplica\b", " → "),
    (r"\bxor\b|\^", " ⊕ "),
    (r"&&|&|\band\b|\by\b|·|\*", " ∧ "),
    (r"\|\||\||\bor\b|\bo\b|\+", " ∨ "),
    (r"~|!|\bnot\b|\bno\b|¬", " ¬ "),
    (r"⊤|\bV\b|\bT\b|\btrue\b|\bverdadero\b", " ⊤ "),
    (r"⊥|\bF\b|\bfalse\b|\bfalso\b", " ⊥ "),
]


def _tokens(texto: str) -> list[str]:
    t = texto
    for patron, rep in _SINONIMOS:
        t = re.sub(patron, rep, t)
    toks = re.findall(r"[a-zA-Z_][a-zA-Z0-9_]*|[¬∧∨→↔⊕⊤⊥()]", t)
    resto = re.sub(r"[a-zA-Z_][a-zA-Z0-9_]*|[¬∧∨→↔⊕⊤⊥()\s]", "", t)
    if resto:
        raise ErrorFormula(f"No reconozco estos símbolos: «{resto}».")
    if not toks:
        raise ErrorFormula("La fórmula está vacía.")
    return toks


def leer_formula(texto: str):
    toks = _tokens(texto)
    pos = [0]

    def ver():
        return toks[pos[0]] if pos[0] < len(toks) else None

    def comer(esperado=None):
        t = ver()
        if t is None:
            raise ErrorFormula("La fórmula termina de golpe: ¿falta algo al final?")
        if esperado and t != esperado:
            raise ErrorFormula(f"Esperaba «{esperado}» y encontré «{t}».")
        pos[0] += 1
        return t

    def atomo():
        t = ver()
        if t == "¬":
            comer()
            return No(atomo())
        if t == "(":
            comer()
            e = expr(0)
            comer(")")
            return e
        if t == "⊤":
            comer()
            return Const(True)
        if t == "⊥":
            comer()
            return Const(False)
        if t is not None and re.match(r"[a-zA-Z_]", t):
            comer()
            return Var(t)
        raise ErrorFormula(f"Esperaba una variable, «¬» o «(» y encontré «{t}».")

    def expr(prec_min):
        izq = atomo()
        while True:
            op = ver()
            if op not in PRECEDENCIA or PRECEDENCIA[op] < prec_min:
                break
            p = PRECEDENCIA[op]
            comer()
            # → es asociativa por la derecha; el resto, por la izquierda
            der = expr(p if op == "→" else p + 1)
            izq = Bin(op, izq, der)
        return izq

    e = expr(0)
    if pos[0] != len(toks):
        raise ErrorFormula(f"Sobra algo a partir de «{toks[pos[0]]}» (¿falta un operador o un paréntesis?).")
    return e


# ============================================================ evaluación
def variables(f) -> list[str]:
    out = set()

    def rec(g):
        if isinstance(g, Var):
            out.add(g.nombre)
        elif isinstance(g, No):
            rec(g.a)
        elif isinstance(g, Bin):
            rec(g.a)
            rec(g.b)
    rec(f)
    return sorted(out)


def evaluar(f, asignacion: dict) -> bool:
    if isinstance(f, Const):
        return f.valor
    if isinstance(f, Var):
        return asignacion[f.nombre]
    if isinstance(f, No):
        return not evaluar(f.a, asignacion)
    a, b = evaluar(f.a, asignacion), evaluar(f.b, asignacion)
    return {"∧": a and b, "∨": a or b, "→": (not a) or b, "↔": a == b, "⊕": a != b}[f.op]


def texto(f, padre_prec: int = 0) -> str:
    if isinstance(f, Const):
        return "⊤" if f.valor else "⊥"
    if isinstance(f, Var):
        return f.nombre
    if isinstance(f, No):
        return "¬" + texto(f.a, 10)
    p = PRECEDENCIA[f.op]
    s = f"{texto(f.a, p + (1 if f.op == '→' else 0))} {f.op} {texto(f.b, p + (0 if f.op == '→' else 1))}"
    return f"({s})" if p < padre_prec else s


def subformulas(f) -> list:
    """Subfórmulas en orden de construcción (de dentro hacia fuera), sin repetir."""
    out = []

    def rec(g):
        if isinstance(g, No):
            rec(g.a)
        elif isinstance(g, Bin):
            rec(g.a)
            rec(g.b)
        if not isinstance(g, (Var, Const)) and g not in out:
            out.append(g)
    rec(f)
    return out


@dataclass
class Tabla:
    variables: list[str]
    columnas: list[str]                   # textos de las subfórmulas
    filas: list[tuple[list[bool], list[bool]]]
    clase: str                             # 'tautología', 'contradicción', 'contingencia'


def tabla_verdad(f, orden_vars: list[str] | None = None) -> Tabla:
    vs = orden_vars or variables(f)
    if len(vs) > 8:
        raise ErrorFormula("Con más de 8 variables la tabla tendría más de 256 filas; simplifica la fórmula.")
    subs = subformulas(f) or [f]
    filas = []
    for valores in product([True, False], repeat=len(vs)):
        asig = dict(zip(vs, valores))
        filas.append((list(valores), [evaluar(s, asig) for s in subs]))
    finales = [r[1][-1] for r in filas]
    clase = "tautología" if all(finales) else ("contradicción" if not any(finales) else "contingencia")
    return Tabla(vs, [texto(s) for s in subs], filas, clase)


def equivalentes(f, g) -> tuple[bool, dict | None]:
    vs = sorted(set(variables(f)) | set(variables(g)))
    for valores in product([True, False], repeat=len(vs)):
        asig = dict(zip(vs, valores))
        if evaluar(f, asig) != evaluar(g, asig):
            return False, asig
    return True, None


def a_sympy(f):
    if isinstance(f, Const):
        return sp.true if f.valor else sp.false
    if isinstance(f, Var):
        return sp.Symbol(f.nombre)
    if isinstance(f, No):
        return sp.Not(a_sympy(f.a))
    a, b = a_sympy(f.a), a_sympy(f.b)
    return {"∧": sp.And, "∨": sp.Or, "→": sp.Implies, "↔": sp.Equivalent, "⊕": sp.Xor}[f.op](a, b)


def sympy_a_texto(e) -> str:
    if e is sp.true:
        return "⊤"
    if e is sp.false:
        return "⊥"
    if isinstance(e, sp.Symbol):
        return str(e)
    if isinstance(e, sp.Not):
        return "¬" + sympy_a_texto(e.args[0])
    if isinstance(e, sp.And):
        return " ∧ ".join(_par(a, sp.Or) for a in sorted(e.args, key=str))
    if isinstance(e, sp.Or):
        return " ∨ ".join(_par(a, sp.And) for a in sorted(e.args, key=str))
    return str(e)


def _par(a, tipo):
    s = sympy_a_texto(a)
    return f"({s})" if isinstance(a, tipo) else s


def formas_normales(f) -> dict:
    e = a_sympy(f)
    return {
        "simplificada": sympy_a_texto(sp.simplify_logic(e)),
        "FND (disyuntiva)": sympy_a_texto(sp.to_dnf(e, simplify=True)),
        "FNC (conjuntiva)": sympy_a_texto(sp.to_cnf(e, simplify=True)),
    }


def negar_paso_a_paso(f) -> list[tuple[str, str]]:
    """Empuja una negación hacia dentro con De Morgan, ¬(p→q) ≡ p∧¬q, etc. Devuelve (fórmula, regla)."""
    pasos = [(texto(No(f)), "punto de partida")]

    def neg(g):
        if isinstance(g, Var):
            return No(g), None
        if isinstance(g, Const):
            return Const(not g.valor), "¬⊤ ≡ ⊥, ¬⊥ ≡ ⊤"
        if isinstance(g, No):
            return g.a, "doble negación ¬¬p ≡ p"
        if g.op == "∧":
            return Bin("∨", neg(g.a)[0], neg(g.b)[0]), "De Morgan: ¬(p ∧ q) ≡ ¬p ∨ ¬q"
        if g.op == "∨":
            return Bin("∧", neg(g.a)[0], neg(g.b)[0]), "De Morgan: ¬(p ∨ q) ≡ ¬p ∧ ¬q"
        if g.op == "→":
            return Bin("∧", g.a, neg(g.b)[0]), "¬(p → q) ≡ p ∧ ¬q"
        if g.op == "↔":
            return Bin("⊕", g.a, g.b), "¬(p ↔ q) ≡ p ⊕ q (exactamente una es verdad)"
        return Bin("↔", g.a, g.b), "¬(p ⊕ q) ≡ p ↔ q"

    r, regla = neg(f)
    pasos.append((texto(r), regla or "la negación ya está pegada a una variable"))
    return pasos


# ============================================================ cuantificadores
_REL_NEG = [("≤", ">"), ("≥", "<"), ("<", "≥"), (">", "≤"), ("≠", "="), ("=", "≠"), ("∉", "∈"), ("∈", "∉"),
            ("∤", "|"), ("|", "∤"), ("⊈", "⊆"), ("⊆", "⊈")]


def _normalizar_cuant(t: str) -> str:
    rep = [(r"<=", "≤"), (r">=", "≥"), (r"!=|=/=", "≠"), (r"->|=>|⇒", "→"), (r"<->|<=>|⇔", "↔"),
           (r"\bpara todo\b|\bforall\b|\bpt\b", "∀"), (r"\bexiste\b|\bexists\b", "∃"),
           (r"\ben\b(?=\s*[A-Zℕℤℚℝℂ])", "∈"), (r"\band\b|&", "∧"), (r"\bor\b", "∨"), (r"\bnot\b|~", "¬")]
    for a, b in rep:
        t = re.sub(a, b, t)
    return t


def _split_top(s: str, op: str):
    nivel = 0
    for i, c in enumerate(s):
        if c in "([{":
            nivel += 1
        elif c in ")]}":
            nivel -= 1
        elif nivel == 0 and s.startswith(op, i):
            return s[:i].strip(), s[i + len(op):].strip()
    return None


def _quitar_par(s: str) -> str:
    s = s.strip()
    while s.startswith("(") and s.endswith(")"):
        nivel = 0
        ok = True
        for i, c in enumerate(s):
            nivel += c == "("
            nivel -= c == ")"
            if nivel == 0 and i < len(s) - 1:
                ok = False
                break
        if not ok:
            break
        s = s[1:-1].strip()
    return s


_RELS = ["≤", "≥", "≠", "∉", "∈", "<", ">", "="]


def _rels_top(s: str):
    """Posiciones de relaciones de primer nivel (fuera de paréntesis)."""
    out = []
    nivel = 0
    i = 0
    while i < len(s):
        c = s[i]
        if c in "([{":
            nivel += 1
        elif c in ")]}":
            nivel -= 1
        elif nivel == 0:
            for r in _RELS:
                if s.startswith(r, i):
                    out.append((i, r))
                    break
        i += 1
    return out


def _negar_atomo(s: str, pasos: list) -> str:
    s = _quitar_par(s)
    if s.startswith("¬"):
        pasos.append("doble negación: ¬¬P ≡ P")
        return _quitar_par(s[1:])
    rels = _rels_top(s)
    neg = dict(_REL_NEG)
    if len(rels) >= 2:
        # cadena a < x < b  ≡  (a < x) ∧ (x < b)  ⇒ su negación es (a ≥ x) ∨ (x ≥ b)
        trozos = []
        ini = 0
        for i, r in rels:
            trozos.append(s[ini:i].strip())
            ini = i + len(r)
        trozos.append(s[ini:].strip())
        partes = [f"{trozos[j]} {neg[r]} {trozos[j + 1]}" for j, (_, r) in enumerate(rels)]
        pasos.append("desigualdad encadenada: a < x < b significa (a < x) ∧ (x < b); su negación es (a ≥ x) ∨ (x ≥ b)")
        return " ∨ ".join(partes)
    # valor absoluto |x| no debe confundirse con «divide»: solo tratamos | como divide si va entre espacios
    for a, b in _REL_NEG:
        if a == "|":
            m = re.search(r"\s\|\s", s)
            if m:
                return s[:m.start()] + " ∤ " + s[m.end():]
            continue
        idx = _buscar_rel(s, a)
        if idx is not None:
            pasos.append(f"se niega la relación: «{a}» pasa a «{b}»")
            return s[:idx] + b + s[idx + len(a):]
    return f"¬({s})"


def _buscar_rel(s: str, rel: str):
    nivel = 0
    i = 0
    while i < len(s):
        c = s[i]
        if c in "([{":
            nivel += 1
        elif c in ")]}":
            nivel -= 1
        elif nivel == 0 and s.startswith(rel, i):
            # evitar confundir < dentro de ≤ ya tratado
            return i
        i += 1
    return None


def _negar_cuerpo(s: str, pasos: list) -> str:
    s = _quitar_par(s.strip().lstrip(",:").strip())
    m = re.match(r"^([∀∃])\s*([^,:]+?)\s*[,:]\s*(.+)$", s)
    if m:
        q, var, resto = m.groups()
        nq = "∃" if q == "∀" else "∀"
        pasos.append(f"«{q}{var}» pasa a «{nq}{var}» (la negación atraviesa el cuantificador; el dominio no cambia)")
        return f"{nq}{var}, " + _negar_cuerpo(resto, pasos)
    for op, nuevo, regla in (("↔", None, None), ("→", "∧", "¬(P → Q) ≡ P ∧ ¬Q (la hipótesis se queda, se niega la tesis)"),
                             ("∨", "∧", "De Morgan: ¬(P ∨ Q) ≡ ¬P ∧ ¬Q"), ("∧", "∨", "De Morgan: ¬(P ∧ Q) ≡ ¬P ∨ ¬Q")):
        partes = _split_top(s, op)
        if partes:
            a, b = partes
            if op == "↔":
                pasos.append("¬(P ↔ Q) ≡ (P ∧ ¬Q) ∨ (Q ∧ ¬P)")
                return f"({a} ∧ {_negar_cuerpo(b, [])}) ∨ ({b} ∧ {_negar_cuerpo(a, [])})"
            pasos.append(regla)
            if op == "→":
                return f"({a}) ∧ ({_negar_cuerpo(b, pasos)})"
            return f"({_negar_cuerpo(a, pasos)}) {nuevo} ({_negar_cuerpo(b, pasos)})"
    return _negar_atomo(s, pasos)


def negar_cuantificado(enunciado: str) -> tuple[str, list[str]]:
    """Niega un enunciado tipo «∀ε>0 ∃δ>0 ∀x, (|x−a|<δ → |f(x)−L|<ε)».
    Los cuantificadores se separan del resto con coma o dos puntos."""
    s = _normalizar_cuant(enunciado.strip())
    # admitir «∀ε>0 ∃δ>0 ∀x∈A, cuerpo»: insertamos comas entre cuantificadores pegados
    s = re.sub(r"(?<![,:(\s])\s*(?=[∀∃])", ", ", s)
    s = re.sub(r"\s+(?=[∀∃])", " ", s)
    pasos: list[str] = []
    res = _negar_cuerpo(s, pasos)
    res = re.sub(r",\s*,", ",", res)
    return res, pasos


EJEMPLOS_CUANT = {
    "Límite de una función": "∀ε>0, ∃δ>0, ∀x∈A, (0<|x−a|<δ → |f(x)−L|<ε)",
    "Continuidad en a": "∀ε>0, ∃δ>0, ∀x∈A, (|x−a|<δ → |f(x)−f(a)|<ε)",
    "Continuidad uniforme": "∀ε>0, ∃δ>0, ∀x∈A, ∀y∈A, (|x−y|<δ → |f(x)−f(y)|<ε)",
    "Límite de una sucesión": "∀ε>0, ∃n0∈ℕ, ∀n∈ℕ, (n≥n0 → |a_n−L|<ε)",
    "Sucesión de Cauchy": "∀ε>0, ∃n0∈ℕ, ∀n∈ℕ, ∀m∈ℕ, (n≥n0 ∧ m≥n0 → |a_n−a_m|<ε)",
    "Acotada superiormente": "∃M∈ℝ, ∀x∈A, x≤M",
    "f inyectiva": "∀x∈A, ∀y∈A, (f(x)=f(y) → x=y)",
    "f sobreyectiva": "∀y∈B, ∃x∈A, f(x)=y",
    "Convergencia uniforme": "∀ε>0, ∃n0∈ℕ, ∀n∈ℕ, ∀x∈A, (n≥n0 → |f_n(x)−f(x)|<ε)",
    "Infinitos primos": "∀n∈ℕ, ∃p∈ℕ, (p>n ∧ p es primo)",
}


# ============================================================ inducción
@dataclass
class Induccion:
    base_n: int
    base_ok: bool
    base_detalle: str
    paso_ok: bool | None
    paso_detalle: list[str]
    numerico_ok: bool


def induccion_suma(termino: str, formula: str, n0: int = 1):
    """Comprueba Σ_{k=n0}^{n} termino(k) = formula(n) por inducción (con SymPy)."""
    from .parsing import leer
    n, k = sp.symbols("n k", integer=True)
    t = leer(termino).subs(sp.Symbol("k", integer=True, positive=True), k).subs(sp.Symbol("x", real=True), k)
    t = t.subs({s: k for s in t.free_symbols if s.name == "k"})
    F = leer(formula)
    F = F.subs({s: n for s in F.free_symbols if s.name == "n"})
    base_izq = t.subs(k, n0)
    base_der = F.subs(n, n0)
    base_ok = sp.simplify(base_izq - base_der) == 0
    hip = F
    paso_izq = sp.simplify(hip + t.subs(k, n + 1))
    obj = sp.simplify(F.subs(n, n + 1))
    paso_ok = sp.simplify(sp.expand(paso_izq - obj)) == 0
    detalle = [
        rf"\text{{Hipótesis de inducción: }} \sum_{{k={n0}}}^{{n}} {sp.latex(t)} = {sp.latex(F)}",
        rf"\sum_{{k={n0}}}^{{n+1}} {sp.latex(t)} = \underbrace{{{sp.latex(F)}}}_{{\text{{hipótesis}}}} + {sp.latex(t.subs(k, n + 1))}",
        rf"= {sp.latex(sp.factor(paso_izq))}",
        rf"\text{{Queremos llegar a }} F(n+1) = {sp.latex(F.subs(n, n + 1))} = {sp.latex(sp.factor(obj))}",
    ]
    num_ok = all(sp.simplify(sum(t.subs(k, j) for j in range(n0, m + 1)) - F.subs(n, m)) == 0 for m in range(n0, n0 + 25))
    return Induccion(n0, base_ok, f"{sp.sstr(base_izq)} = {sp.sstr(base_der)}", paso_ok, detalle, num_ok), t, F


def induccion_divisibilidad(expr: str, d: int, n0: int = 1):
    """Comprueba d | expr(n) para n ≥ n0: base y que expr(n+1) − expr(n) es múltiplo de d."""
    from .parsing import leer
    n = sp.Symbol("n", integer=True)
    E = leer(expr)
    E = E.subs({s: n for s in E.free_symbols if s.name == "n"})
    base = E.subs(n, n0)
    base_ok = sp.Integer(base) % d == 0
    def multiplo(expr_):
        expr_ = sp.expand(expr_)
        if expr_.is_polynomial(n):
            return all(sp.Integer(c) % d == 0 for c in sp.Poly(expr_, n).all_coeffs())
        return None

    # Probamos E(n+1) = c·E(n) + R(n) con c = 1 o c = base de alguna exponencial b^n de E.
    candidatos = [sp.Integer(1)]
    for pw in sp.expand(E).atoms(sp.Pow):
        if pw.exp == n and pw.base.is_Integer:
            candidatos.append(pw.base)
    paso_ok, detalle = None, []
    for c in candidatos:
        R = sp.expand(sp.expand_power_exp(E.subs(n, n + 1)) - c * E)
        ok = multiplo(R)
        if ok is not None:
            paso_ok = ok
            cociente = sp.expand(R / d)
            detalle = [rf"E(n+1) = {sp.latex(sp.expand_power_exp(E.subs(n, n + 1)))}",
                       rf"E(n+1) = {sp.latex(c)}\cdot \underbrace{{E(n)}}_{{\text{{múltiplo de }}{d}\text{{ (hipótesis)}}}} + "
                       rf"\underbrace{{{sp.latex(R)}}}_{{= {d}\cdot({sp.latex(cociente)})}}"]
            if not ok:
                detalle[-1] = rf"E(n+1) = {sp.latex(c)}\cdot E(n) + {sp.latex(R)} \quad\text{{y }} {sp.latex(R)} \text{{ no es múltiplo de }} {d}"
            break
    if paso_ok is None:
        detalle = [r"\text{No he encontrado una descomposición automática: revisa el paso a mano (abajo, la comprobación numérica).}"]
    num_ok = all(sp.Integer(E.subs(n, m)) % d == 0 for m in range(n0, n0 + 40))
    return Induccion(n0, base_ok, f"E({n0}) = {base}", paso_ok, detalle, num_ok), E
