"""Las 14 páginas de tema: teoría + calculadoras + práctica, en pestañas que sólo se ejecutan al abrirlas."""
from __future__ import annotations

import streamlit as st

from contenido import (f1_logica, f2_conjuntos, f3_relaciones, f4_combinatoria, f5_enteros, f6_polinomios, f7_modular, f8_algebra,
                       a1_numeros, a2_limites, a3_derivadas, a4_integrales, a5_sucesiones, a6_series, a7_funciones)
from core.ejercicios import POR_TEMA
from ui import finita as F, analisis as A, herr_finita as HF, herr_analisis as HA, herr_algebra as HG
from ui.estilo import cabecera
from ui.examen import bloque_practica
from ui.teoria import mostrar_tema, progreso_tema


def _taylor():
    A.pagina_taylor()
    st.divider()
    HA.herr_taylor_resto()


def _primos():
    HF.herr_criba()
    st.divider()
    F.herr_primos_phi()


# (módulo de contenido, icono, [(pestaña, función)])
TEMAS = [
    (f1_logica, "🧠", [("Tabla de verdad", HF.herr_tabla_verdad), ("Equivalencias", HF.herr_equivalencias),
                       ("Negar cuantificadores", HF.herr_cuantificadores)]),
    (f2_conjuntos, "🫧", [("Conjuntos y Venn", HF.herr_conjuntos), ("Partes y producto", HF.herr_partes_producto),
                          ("Aplicaciones", HF.herr_aplicaciones), ("Contar aplicaciones", HF.herr_contar_aplicaciones),
                          ("Inducción", HF.herr_induccion)]),
    (f3_relaciones, "🔗", [("Analizar una relación", HF.herr_relacion), ("Equivalencia y clases", HF.herr_equivalencia),
                           ("Orden y Hasse", HF.herr_orden), ("Clausuras", HF.herr_clausuras),
                           ("Lexicográfico", HF.herr_lexicografico)]),
    (f4_combinatoria, "🎲", [("Asistente: ¿qué fórmula uso?", F.herr_selecciones), ("Repartos (las 12 formas)", F.herr_doce_formas),
                             ("Números especiales", F.herr_numeros_especiales), ("Inclusión–exclusión", F.herr_inclusion_exclusion),
                             ("Palomar", HF.herr_palomar), ("Particiones", HF.herr_particiones), ("Binomio", HF.herr_binomio),
                             ("Recurrencias", F.pagina_recurrencias)]),
    (f5_enteros, "🔢", [("División entera", HF.herr_division_entera), ("Criba y primos", _primos), ("Bases", HF.herr_bases),
                        ("Divisores y factorización", HF.herr_divisores), ("mcd, mcm y Bézout", F.herr_euclides)]),
    (f6_polinomios, "🧮", [("Calculadora de polinomios", F.pagina_polinomios), ("Operaciones y grado", HF.herr_poli_operaciones),
                           ("Raíces racionales", HF.herr_raices_racionales), ("Irreducibles", HF.herr_irreducibles)]),
    (f7_modular, "🕐", [("Diofánticas", F.herr_diofanticas), ("Congruencias", F.herr_congruencias),
                        ("ℤₙ: tablas y unidades", HF.herr_zn), ("Fermat, Euler y Wilson", HF.herr_fermat_euler),
                        ("Potencias", F.herr_potencias), ("Chino del resto", F.herr_chino),
                        ("Sistemas mód p", HF.herr_sistemas_p), ("Varias variables", HF.herr_congruencia_varias)]),
    (f8_algebra, "💎", [("Permutaciones", HG.herr_permutaciones), ("ℤₙ: anillo e ideales", HG.herr_zn_anillo),
                        ("Cocientes de polinomios", HG.herr_cocientes)]),
    (a1_numeros, "🌀", [("Desigualdades y valor absoluto", A.herr_inecuaciones), ("Supremo, ínfimo y topología", HA.herr_topologia),
                        ("Vectores de ℝⁿ", HA.herr_vectores), ("Complejos", HA.herr_complejos),
                        ("Regiones del plano complejo", HA.herr_region_compleja), ("Funciones", HA.herr_funciones_reales)]),
    (a2_limites, "🎯", [("Límites", A.pagina_limites), ("ε–δ", HA.herr_epsilon_delta), ("Equivalencias", HA.herr_equivalencias),
                        ("Funciones a trozos", HA.herr_trozos), ("Bolzano y Weierstrass", HA.herr_weierstrass),
                        ("Continuidad uniforme", HA.herr_uniforme)]),
    (a3_derivadas, "📉", [("Derivadas", A.pagina_derivadas), ("Rolle y valor medio", HA.herr_valor_medio),
                          ("L'Hôpital", HA.herr_hopital), ("Implícita y Leibniz", HA.herr_implicita), ("Taylor", _taylor),
                          ("Extremos", HA.herr_extremos_derivadas), ("Estudio completo", A.pagina_estudio),
                          ("Newton", A.pagina_numericos)]),
    (a4_integrales, "➰", [("Primitivas paso a paso", HA.herr_pasos_integral), ("Integral definida", A.pagina_integrales),
                          ("Riemann y Darboux", HA.herr_darboux), ("TFC", HA.herr_tfc), ("Áreas", HA.herr_areas),
                          ("Longitud y volumen", HA.herr_volumenes), ("Paramétricas y polares", HA.herr_parametricas),
                          ("Impropias", HA.herr_impropias), ("Beta y Gamma", HA.herr_beta_gamma)]),
    (a5_sucesiones, "🪜", [("Límite de una sucesión", A.herr_sucesiones), ("Recurrentes", HA.herr_recurrentes),
                           ("lím sup / lím inf", HA.herr_limsup), ("Stolz", HA.herr_stolz)]),
    (a6_series, "♾️", [("Estudio de una serie", A.herr_series), ("Más criterios", HA.herr_criterios_series),
                       ("Sumar series", HA.herr_sumar_series), ("Producto de Cauchy", HA.herr_producto_cauchy),
                       ("Reordenación de Riemann", HA.herr_riemann)]),
    (a7_funciones, "🌊", [("Puntual vs uniforme", HA.herr_puntual_uniforme), ("Criterio M", HA.herr_criterio_m),
                          ("Series de potencias", HA.herr_potencias), ("Funciones analíticas", HA.herr_analiticas)]),
]

TODOS = [m.TEMA for m, _, _ in TEMAS]
ICONO = {m.TEMA.id: ic for m, ic, _ in TEMAS}


def pagina_tema(modulo, icono, herramientas):
    tema = modulo.TEMA
    asig = tema.asignatura
    corto = "Matemática finita" if asig.startswith("Mat") else "Análisis"
    hecho = progreso_tema(tema)
    cabecera(icono, f"Tema {tema.numero} · {tema.titulo}", tema.resumen, etiqueta=corto,
             chips=[f"{len(tema.secciones)} secciones de teoría", f"{len(herramientas)} calculadoras",
                    f"{hecho * 100:.0f} % entendido"])
    nombres = ["📖 Teoría"] + [f"🧪 {n}" for n, _ in herramientas] + ["✍️ Practica"]
    sug = st.session_state.pop("_pestaña_sugerida", None)
    defecto = None
    if sug and f"🧪 {sug}" in nombres:
        st.session_state.pop(f"tabs_{tema.id}", None)
        defecto = f"🧪 {sug}"
    pestañas = st.tabs(nombres, key=f"tabs_{tema.id}", on_change="rerun", default=defecto)
    if pestañas[0].open:
        with pestañas[0]:
            mostrar_tema(tema, [n for n, _ in herramientas])
    for (nombre, func), tab in zip(herramientas, pestañas[1:-1]):
        if tab.open:
            with tab:
                try:
                    func()
                except Exception as exc:  # noqa: BLE001
                    st.error(f"Algo ha fallado en «{nombre}»: {exc}. Revisa lo que has escrito o prueba otro ejemplo.")
                    with st.expander("Detalles técnicos"):
                        st.exception(exc)
    if pestañas[-1].open:
        with pestañas[-1]:
            st.caption("Ejercicios aleatorios de este tema, generados al revés (solución primero) y corregidos al instante. "
                       "Cuentan para tu nota del **Modo examen**.")
            bloque_practica(corto, POR_TEMA.get(tema.id, []), f"pr_{tema.id}")


def paginas_de(asignatura: str):
    """Lista de (función de página, título, icono, url) de una asignatura."""
    out = []
    for modulo, icono, herr in TEMAS:
        t = modulo.TEMA
        if t.asignatura.startswith(asignatura[:3]):
            def f(m=modulo, i=icono, h=herr):
                pagina_tema(m, i, h)
            f.__name__ = f"tema_{t.id}"
            out.append((f, f"{t.numero}. {t.titulo}", icono, f"tema_{t.id}"))
    return out
