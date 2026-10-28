"""Ejecuta cada página de la app con los valores por defecto y comprueba que no hay errores."""
import pytest
from streamlit.testing.v1 import AppTest

PAGINAS = [
    ("ui.examen", "pagina_examen"), ("ui.ia", "pagina_ia"),
    ("ui.extras", "inicio"), ("ui.extras", "buscador"), ("ui.extras", "erratas"), ("ui.extras", "mi_progreso"),
    ("ui.extras", "chuleta"),
]


def correr(mod, fn, preparar=None):
    codigo = f"import sys; sys.path.insert(0, '.')\nimport core\nfrom {mod} import {fn}\n{fn}()\n"
    at = AppTest.from_string(codigo, default_timeout=180)
    at.run()
    if preparar:
        preparar(at)
        at.run()
    return at


@pytest.mark.parametrize("mod,fn", PAGINAS)
def test_pagina_sin_errores(mod, fn):
    at = correr(mod, fn)
    assert not at.exception, [e.value for e in at.exception]
    errores = [e.value for e in at.error]
    assert not errores, errores


def test_app_completa_arranca():
    at = AppTest.from_file("../app.py", default_timeout=120)
    at.run()
    assert not at.exception, [e.value for e in at.exception]
    assert not at.error, [e.value for e in at.error]


def test_estudio_otras_funciones():
    for f in ["x^3-3x", "ln(x)/x", "|x^2-4|", "sen(x)", "x*e^(-x)", "sqrt(4-x^2)", "x^(2/3)", "1/(x^2-1)"]:
        at = correr("ui.analisis", "pagina_estudio", lambda a, f=f: a.text_input(key="est_f").set_value(f))
        assert not at.exception, (f, [e.value for e in at.exception])
        assert not at.error, (f, [e.value for e in at.error])


def test_polinomios_en_Zp():
    def prep(at):
        at.radio(key="pol_k").set_value("ℤ_p (módulo un primo p)")
    at = correr("ui.finita", "pagina_polinomios", prep)
    assert not at.exception and not at.error, [e.value for e in at.error]


def test_examen_corrige_desde_la_interfaz():
    import streamlit as st  # noqa: F401
    from core.ejercicios import generar
    at = correr("ui.examen", "pagina_examen")
    at.selectbox(key="ex_mf_tema").set_value("División de polinomios")
    at.run()
    semilla = at.session_state["ex_mf_semilla"]
    ej = generar("Matemática finita", "División de polinomios", semilla)
    import sympy as sp
    at.text_input(key="ex_mf_resp_q").set_value(sp.sstr(ej._correctas["q"]))
    at.text_input(key="ex_mf_resp_r").set_value(sp.sstr(ej._correctas["r"]))
    [b for b in at.button if "Corregir" in b.label][0].click()
    at.run()
    assert any("Perfecto" in s.value for s in at.success), [s.value for s in at.success]
    assert at.session_state["ex_aciertos"] == 1


def test_interacciones_variadas():
    casos = [
        ("ui.analisis", "pagina_limites", [("lim_f", "1/x"), ("lim_a", "0")]),
        ("ui.analisis", "pagina_limites", [("lim_f", "(x^2-9)/(x-3)"), ("lim_a", "3")]),
        ("ui.analisis", "pagina_derivadas", [("der_f", "x^x")]),
        ("ui.analisis", "pagina_taylor", [("tay_f", "ln(1+x)"), ("tay_a", "0")]),
        ("ui.analisis", "herr_series", [("ser_a", "(-1)^n/n")]),
        ("ui.analisis", "herr_inecuaciones", [("ineq", "(x-1)/(x+2) >= 0")]),
        ("ui.analisis", "herr_complejos_basico", [("cz", "-8")]),
        ("ui.finita", "herr_chino", [("tcr_r", "1, 2"), ("tcr_m", "4, 6")]),
        ("ui.finita", "pagina_recurrencias", [("rec_c", "1, 1"), ("rec_i", "0, 1")]),
        ("ui.finita", "pagina_polinomios", [("pol_A", "x^4-1"), ("pol_B", "x^2+x")]),
    ]
    for mod, fn, entradas in casos:
        def prep(at, entradas=entradas):
            for k, v in entradas:
                at.text_input(key=k).set_value(v)
        at = correr(mod, fn, prep)
        assert not at.exception, (fn, entradas, [e.value for e in at.exception])
        # errores esperables: límite que no existe / sistema incompatible
        errs = [e.value for e in at.error]
        assert all("no existe" in e or "incompatible" in e for e in errs), (fn, entradas, errs)
