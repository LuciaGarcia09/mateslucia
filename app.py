"""MatesLucía · tu asistente de Matemática Finita y Análisis (1º Ingeniería de Datos e IA).

Arranque:  streamlit run app.py
"""
import streamlit as st

import core  # noqa: F401  (activa la notación ln en LaTeX)
from ui import examen, ia, extras, examenes
from ui.estilo import aplicar_estilo
from ui.temas import paginas_de

st.set_page_config(page_title="MatesLucía", page_icon="🌸", layout="wide")
aplicar_estilo()


def _seguro(func):
    """Ninguna página deja la app en blanco: si algo falla, lo explica."""
    def envoltura():
        try:
            func()
        except Exception as exc:  # noqa: BLE001
            if type(exc).__name__ in ("RerunException", "StopException", "SwitchPageException"):
                raise
            st.error(f"Algo ha fallado en esta página: {exc}. Revisa lo que has escrito o prueba otro ejemplo.")
            with st.expander("Detalles técnicos"):
                st.exception(exc)
    envoltura.__name__ = func.__name__
    return envoltura


def _p(func, titulo, icono, url=None, **kw):
    return st.Page(_seguro(func), title=titulo, icon=icono, url_path=url or func.__name__, **kw)


def _temas(asig):
    out = []
    for f, titulo, icono, url in paginas_de(asig):
        pg = _p(f, titulo, icono, url)
        extras.PAGINAS[url.removeprefix("tema_")] = pg
        out.append(pg)
    return out


paginas = {
    "": [_p(extras.inicio, "Inicio", "🏠", default=True)],
    "Matemática finita": _temas("Matemática Finita"),
    "Análisis": _temas("Análisis"),
    "Practicar": [
        _p(examenes.pagina_examenes, "Exámenes reales", "🏆"),
        _p(examen.pagina_examen, "Modo examen", "📝"),
        _p(ia.pagina_ia, "Rincón Datos e IA", "🤖"),
    ],
    "Estudiar": [
        _p(extras.buscador, "Buscador", "🔎"),
        _p(extras.chuleta, "Chuleta", "📚"),
        _p(extras.erratas, "Erratas", "🛠️"),
        _p(extras.mi_progreso, "Mi progreso", "💗"),
    ],
}

pagina = st.navigation(paginas, expanded=True)

with st.sidebar:
    st.caption("Resultados exactos con SymPy y comprobados por un segundo método. "
               "Si ves ⚠️, revisa a mano: es la app avisándote, no fallando en silencio.")

pagina.run()
