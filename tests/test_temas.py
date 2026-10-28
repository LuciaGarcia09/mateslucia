"""Cada calculadora de cada tema, la teoría de cada sección y la práctica se ejecutan sin errores."""
import pytest
from streamlit.testing.v1 import AppTest

from ui.temas import TEMAS

HERRAMIENTAS = [(m.TEMA.id, i, n) for m, _, h in TEMAS for i, (n, _) in enumerate(h)]
SECCIONES = [(m.TEMA.id, s.id) for m, _, _ in TEMAS for s in m.TEMA.secciones]


def _app(codigo):
    at = AppTest.from_string("import sys; sys.path.insert(0, '.')\nimport core\n" + codigo, default_timeout=240)
    at.run()
    return at


def _sin_errores(at, ctx):
    assert not at.exception, (ctx, [e.value for e in at.exception])
    errores = [e.value for e in at.error]
    assert not errores, (ctx, errores)


@pytest.mark.parametrize("tid,i,nombre", HERRAMIENTAS)
def test_herramienta(tid, i, nombre):
    at = _app(f"from ui.temas import TEMAS\nm = [t for t in TEMAS if t[0].TEMA.id == '{tid}'][0]\nm[2][{i}][1]()\n")
    _sin_errores(at, nombre)


@pytest.mark.parametrize("tid,sid", SECCIONES)
def test_seccion_teoria(tid, sid):
    at = _app(f"import streamlit as st\nst.session_state['sec_{tid}'] = '{sid}'\n"
              f"from ui.temas import TEMAS\nfrom ui.teoria import mostrar_tema\n"
              f"m = [t for t in TEMAS if t[0].TEMA.id == '{tid}'][0]\nmostrar_tema(m[0].TEMA)\n")
    _sin_errores(at, sid)


@pytest.mark.parametrize("tid", [m.TEMA.id for m, _, _ in TEMAS])
def test_pagina_tema_y_practica(tid):
    at = _app(f"from ui.temas import TEMAS, pagina_tema\nm = [t for t in TEMAS if t[0].TEMA.id == '{tid}'][0]\npagina_tema(*m)\n")
    _sin_errores(at, tid)
    at.tabs[0]  # existe


def test_pagina_examenes_todas_las_pestanas():
    for tab in ["📚 Por examen", "🗺️ Qué cae más", "⏱️ Simulacro"]:
        at = _app(f"import streamlit as st\nst.session_state['exr_tabs'] = '{tab}'\nfrom ui.examenes import pagina_examenes\npagina_examenes()\n")
        _sin_errores(at, tab)


@pytest.mark.parametrize("eid", list("ABCDEFGHJ"))
def test_cada_examen(eid):
    at = _app(f"import streamlit as st\nst.session_state['exr_sel'] = '{eid}'\nst.session_state['sim_sel'] = '{eid}'\n"
              f"st.session_state['sim_fin_{eid}'] = True\nfrom ui.examenes import pagina_examenes, _simulacro\npagina_examenes()\n_simulacro()\n")
    _sin_errores(at, eid)


def test_herramientas_de_examenes_existen():
    from contenido.examenes import EXAMENES
    tabs = {(m.TEMA.id, n) for m, _, h in TEMAS for n, _ in h}
    for e in EXAMENES:
        for p in e.preguntas:
            if p.herramienta:
                assert p.herramienta in tabs, (e.id, p.num, p.herramienta)
