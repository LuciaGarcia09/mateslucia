"""Lectura de expresiones escritas "como en clase".

Acepta:  x^2 + 3x - 1,  2(x+1),  sen(x), tg(x), ln(x), raiz(x), e^x, pi, oo (infinito)
"""
import re
import sympy as sp
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
    convert_xor,
)

x, y = sp.symbols("x y", real=True)
n, k = sp.symbols("n k", integer=True, positive=True)

TRANSFORMS = standard_transformations + (implicit_multiplication_application, convert_xor)

# Notación española -> nombres de sympy (el orden importa: primero los largos)
_ALIAS = [
    (r"\barcsen\b", "asin"),
    (r"\barccos\b", "acos"),
    (r"\barctg\b", "atan"),
    (r"\barctan\b", "atan"),
    (r"\barcsin\b", "asin"),
    (r"\bsenh\b", "sinh"),
    (r"\bcosh\b", "cosh"),
    (r"\btgh\b", "tanh"),
    (r"\bsen\b", "sin"),
    (r"\btg\b", "tan"),
    (r"\bcotg\b", "cot"),
    (r"\bln\b", "log"),
    (r"\braiz\b", "sqrt"),
    (r"\braíz\b", "sqrt"),
    (r"\binfinito\b", "oo"),
    (r"∞", "oo"),
    (r"π", "pi"),
    (r"·", "*"),
    (r"−", "-"),
    (r"√", "sqrt"),
]

LOCAL = {
    "x": x, "y": y, "n": n, "k": k,
    "e": sp.E, "E": sp.E, "pi": sp.pi, "oo": sp.oo,
    "log": sp.log, "sqrt": sp.sqrt, "exp": sp.exp,
    "sin": sp.sin, "cos": sp.cos, "tan": sp.tan, "cot": sp.cot,
    "asin": sp.asin, "acos": sp.acos, "atan": sp.atan,
    "sinh": sp.sinh, "cosh": sp.cosh, "tanh": sp.tanh,
    "Abs": sp.Abs, "abs": sp.Abs, "factorial": sp.factorial,
}


class ErrorLectura(ValueError):
    pass


def normalizar(texto: str) -> str:
    t = texto.strip()
    if not t:
        raise ErrorLectura("La expresión está vacía.")
    for patron, rep in _ALIAS:
        # \b no sirve en «2sen(x)» (2 y s son ambos caracteres de palabra): sólo exigimos que no haya LETRAS pegadas
        patron = patron.replace(r"\b", "")
        if patron[0].isalpha():
            patron = r"(?<![A-Za-zÁÉÍÓÚáéíóúñ_])" + patron + r"(?![A-Za-zÁÉÍÓÚáéíóúñ_])"
        t = re.sub(patron, rep, t)
    # |expr| -> Abs(expr) (casos simples sin anidar)
    t = re.sub(r"\|([^|]+)\|", r"Abs(\1)", t)
    return t


def leer(texto: str) -> sp.Expr:
    """Convierte texto en expresión de sympy o lanza ErrorLectura con un mensaje amable."""
    t = normalizar(texto)
    try:
        expr = parse_expr(t, local_dict=LOCAL, transformations=TRANSFORMS, evaluate=True)
    except Exception as exc:  # noqa: BLE001
        raise ErrorLectura(
            f"No he podido entender «{texto}». Revisa paréntesis y operadores "
            f"(usa ^ o ** para potencias). Detalle: {exc}"
        ) from exc
    if not isinstance(expr, sp.Basic):
        expr = sp.sympify(expr)
    return expr


def leer_numero(texto: str):
    """Lee un número (admite oo, -oo, pi, fracciones 1/2)."""
    v = leer(texto)
    if v.free_symbols:
        raise ErrorLectura(f"«{texto}» debería ser un número, no una expresión con variables.")
    return v


def leer_entero(texto: str) -> int:
    v = leer_numero(texto)
    if not v.is_integer:
        raise ErrorLectura(f"«{texto}» no es un número entero.")
    return int(v)


def leer_lista_enteros(texto: str) -> list[int]:
    partes = [p for p in re.split(r"[;,\s]+", texto.strip()) if p]
    if not partes:
        raise ErrorLectura("La lista está vacía.")
    return [leer_entero(p) for p in partes]


def tex(expr) -> str:
    return sp.latex(expr)
