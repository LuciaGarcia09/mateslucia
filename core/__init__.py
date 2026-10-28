"""Núcleo matemático de MatesLucía (sin interfaz: se puede usar y testear por separado)."""
import sympy as _sp

_latex_original = _sp.latex


def _latex_es(expr, **kw):
    # Notación de clase: ln en lugar de log
    kw.setdefault("ln_notation", True)
    return _latex_original(expr, **kw)


if getattr(_sp.latex, "__name__", "") != "_latex_es":
    _sp.latex = _latex_es

import warnings as _w

try:
    from sympy.utilities.exceptions import SymPyDeprecationWarning as _SDW
    _w.filterwarnings("ignore", category=_SDW)
except Exception:  # noqa: BLE001
    pass
_w.filterwarnings("ignore", category=RuntimeWarning)
