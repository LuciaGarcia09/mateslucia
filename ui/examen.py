"""Modo examen y bloque de práctica por tema: ejercicios aleatorios con corrección automática."""
from __future__ import annotations

import random
import streamlit as st

from core.ejercicios import GENERADORES, generar
from ui.estilo import cabecera


def _estado(px: str):
    ss = st.session_state
    ss.setdefault(f"{px}_semilla", random.randint(0, 10 ** 9))
    ss.setdefault(f"{px}_resuelto", False)
    ss.setdefault("ex_aciertos", 0)
    ss.setdefault("ex_intentos", 0)
    ss.setdefault("ex_historial", [])   # (tema, acierto)  — compartido por toda la app
    return ss


def _nuevo(px: str):
    ss = st.session_state
    ss[f"{px}_semilla"] = random.randint(0, 10 ** 9)
    ss[f"{px}_resuelto"] = False
    for k in [k for k in ss.keys() if str(k).startswith(f"{px}_resp_")]:
        del ss[k]


def bloque_practica(asig: str, temas: list[str], px: str):
    """Un ejercicio aleatorio de los generadores `temas` de la asignatura `asig`."""
    ss = _estado(px)
    temas = [t for t in temas if t in GENERADORES[asig]]
    if not temas:
        st.info("Para este tema practica con las calculadoras de las otras pestañas.")
        return
    c1, c2 = st.columns([3, 1])
    opciones = (["🎲 Cualquiera"] if len(temas) > 1 else []) + temas
    tema = c1.selectbox("Tipo de ejercicio", opciones, key=f"{px}_tema", on_change=_nuevo, args=(px,))
    c2.button("🔄 Otro ejercicio", key=f"{px}_otro", on_click=_nuevo, args=(px,), width="stretch")
    semilla = ss[f"{px}_semilla"]
    rnd = random.Random(semilla)
    tema_real = rnd.choice(temas) if tema.startswith("🎲") else tema
    try:
        ej = generar(asig, tema_real, semilla)
    except Exception as exc:  # noqa: BLE001
        st.error(f"No he podido generar el ejercicio ({exc}). Pulsa «Otro ejercicio».")
        return
    with st.container(border=True):
        st.markdown(f"##### ✏️ {ej.tema}")
        st.markdown(ej.enunciado)
        with st.form(f"{px}_form_{semilla}_{tema_real}"):
            resp = {}
            cols = st.columns(len(ej.campos))
            for col, (etiqueta, clave) in zip(cols, ej.campos):
                resp[clave] = col.text_input(etiqueta, key=f"{px}_resp_{clave}")
            enviado = st.form_submit_button("✅ Corregir", width="stretch", type="primary")
    if enviado:
        if any(not v.strip() for v in resp.values()):
            st.warning("Rellena todos los huecos antes de corregir.")
        else:
            ok, msg = ej.corregir(resp)
            if not ss[f"{px}_resuelto"]:
                ss.ex_intentos += 1
                ss.ex_aciertos += int(ok)
                ss.ex_historial.append((ej.tema, ok))
                ss[f"{px}_resuelto"] = ok
            (st.success if ok else st.error)(("🎉 " if ok else "") + msg)
            if ok:
                st.balloons()
    with st.expander("👀 Ver la solución paso a paso"):
        for linea in ej.solucion:
            st.markdown(linea)


def marcador():
    ss = st.session_state
    ss.setdefault("ex_aciertos", 0)
    ss.setdefault("ex_intentos", 0)
    ss.setdefault("ex_historial", [])
    m1, m2, m3 = st.columns(3)
    m1.metric("Aciertos", ss.ex_aciertos)
    m2.metric("Intentos", ss.ex_intentos)
    m3.metric("Nota (sobre 10)", f"{10 * ss.ex_aciertos / ss.ex_intentos:.1f}" if ss.ex_intentos else "—")
    if ss.ex_historial:
        por_tema = {}
        for t, ok in ss.ex_historial:
            a, n = por_tema.get(t, (0, 0))
            por_tema[t] = (a + ok, n + 1)
        flojos = [t for t, (a, n) in por_tema.items() if a / n < 0.6]
        st.write("Por tipo: " + " · ".join(f"{t}: {a}/{n}" for t, (a, n) in por_tema.items()))
        if flojos:
            st.info("Te conviene repasar: **" + ", ".join(flojos) + "** 💪")
        if st.button("Reiniciar marcador"):
            ss.ex_aciertos = ss.ex_intentos = 0
            ss.ex_historial = []
            st.rerun()


def pagina_examen():
    cabecera("📝", "Modo examen", "Ejercicios nuevos cada vez, del estilo de los de clase, corregidos al momento. "
             "Escribe la respuesta como en papel (x^2 + 3x, 1/2, e^2…): da igual cómo la simplifiques.",
             etiqueta="Practicar", chips=[f"{sum(len(d) for d in GENERADORES.values())} tipos de ejercicio", "nota sobre 10"])
    asig = st.segmented_control("Asignatura", list(GENERADORES), default=list(GENERADORES)[0], key="ex_asig")
    asig = asig or list(GENERADORES)[0]
    bloque_practica(asig, list(GENERADORES[asig]), f"ex_{'mf' if asig.startswith('Mat') else 'an'}")
    st.divider()
    marcador()
