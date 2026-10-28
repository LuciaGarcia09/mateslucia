"""Exámenes reales de Matemática Finita I: enunciados, pistas, soluciones explicadas, qué cae más y simulacro."""
from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from contenido.examenes import EXAMENES, frecuencia_temas
from ui.estilo import cabecera, caja, ROSA, LILA
from ui.temas import TODOS, ICONO

NOMBRE = {t.id: f"T{t.numero}. {t.titulo}" for t in TODOS}


def _ir(tid, tab=None):
    from ui import extras
    if tab:
        st.session_state["_pestaña_sugerida"] = tab
    st.switch_page(extras.PAGINAS[tid])


def _pregunta(e, p, mostrar_sol=True, px="ex"):
    with st.container(border=True):
        chips = " ".join(f"<span class='sello sello-ok'>{ICONO[t]} T{t[1]}</span>" for t in p.temas)
        st.markdown(f"##### Pregunta {p.num} · {p.puntos} puntos &nbsp; {chips}", unsafe_allow_html=True)
        st.markdown(p.enunciado)
        if not mostrar_sol:
            return
        with st.expander("💡 Pista (sin destripar la solución)"):
            st.markdown(p.pista)
        with st.expander("✅ Solución explicada paso a paso"):
            st.markdown(p.solucion)
        if p.errata:
            with caja("errata", "Ojo con este enunciado o con su solución oficial", clave=f"err-{px}-{e.id}-{p.num}"):
                st.markdown(p.errata)
        if p.herramienta:
            tid, tab = p.herramienta
            c1, c2 = st.columns([3, 1])
            c1.caption(f"🧪 Compruébalo en {ICONO[tid]} {NOMBRE[tid]} → pestaña «🧪 {tab}»")
            if c2.button("Ir al tema →", key=f"ir_{px}_{e.id}_{p.num}", width="stretch"):
                _ir(tid, tab)


def _info(e):
    chips = [e.tipo, e.fecha, e.tiempo, f"{e.total} puntos", f"aprobado en {e.aprobado}"]
    if e.oficial:
        chips.append("soluciones oficiales revisadas")
    st.markdown(" ".join(f"<span class='sello sello-ok'>{c}</span>" for c in chips), unsafe_allow_html=True)


def pagina_examenes():
    n_preg = sum(len(e.preguntas) for e in EXAMENES)
    n_err = sum(1 for e in EXAMENES for p in e.preguntas if p.errata)
    cabecera("🏆", "Exámenes reales de Matemática Finita", "Los 9 modelos del curso 2025/26 resueltos y explicados como en clase, "
             "con pistas, enlace a la calculadora de cada pregunta y las erratas que tienen.",
             etiqueta="Practicar", chips=[f"{len(EXAMENES)} exámenes", f"{n_preg} preguntas resueltas", f"{n_err} erratas avisadas",
                                         "simulacro con nota"])
    t1, t2, t3 = st.tabs(["📚 Por examen", "🗺️ Qué cae más", "⏱️ Simulacro"], key="exr_tabs", on_change="rerun")

    if t1.open:
        with t1:
            ids = [e.id for e in EXAMENES]
            eid = st.pills("Examen", ids, format_func=lambda i: next(e.modelo.split(" (")[0] for e in EXAMENES if e.id == i),
                           default="J", key="exr_sel") or "J"
            e = next(e for e in EXAMENES if e.id == eid)
            st.markdown(f"### {e.modelo} · {e.tipo}")
            _info(e)
            st.write("")
            for p in e.preguntas:
                _pregunta(e, p)

    if t2.open:
        with t2:
            fr = frecuencia_temas()
            total = sum(fr.values())
            fig = go.Figure(go.Bar(x=[v / total * 100 for v in fr.values()], y=[NOMBRE[t] for t in fr], orientation="h",
                                   marker_color=[ROSA if i % 2 == 0 else LILA for i in range(len(fr))],
                                   text=[f"{v / total * 100:.0f} %" for v in fr.values()], textposition="outside"))
            fig.update_layout(height=380, margin=dict(l=10, r=40, t=30, b=10), yaxis=dict(autorange="reversed"),
                              xaxis_title="% de los puntos de los 9 exámenes", plot_bgcolor="rgba(0,0,0,0)",
                              paper_bgcolor="rgba(0,0,0,0)", title="¿Qué temas dan más puntos?")
            st.plotly_chart(fig, width="stretch")
            with caja("idea", "Cómo leerlo"):
                st.markdown("Cada pregunta reparte sus puntos entre los temas que toca. Los **Parciales I** (A–D) son de los temas 1–4 "
                            "(lógica, inducción, conjuntos, relaciones, combinatoria); el **Parcial II** (F, H) es de los temas 5–8 "
                            "(aritmética, polinomios, congruencias y **grupos y anillos**, que ahora tienes en el tema 8), y los **finales y la "
                            "recuperación** (E, G, J) mezclan las dos partes.")
            # preguntas repetidas
            vistas: dict[str, list[str]] = {}
            for e in EXAMENES:
                for p in e.preguntas:
                    vistas.setdefault(p.solucion, []).append(f"{e.modelo.split(' (')[0]} · P{p.num}")
            rep = [(k, v) for k, v in vistas.items() if len(v) > 1]
            with caja("truco", f"Preguntas que se han repetido ({len(rep)})"):
                st.markdown("El profesor **repite** preguntas entre modelos. Estas han salido más de una vez: llévalas dominadas.\n\n" +
                            "\n".join(f"- {', '.join(v)}: *{_titulo(k)}*" for k, v in rep))
            filas = [{"Modelo": e.modelo.split(" (")[0], "Tipo": e.tipo, "Fecha": e.fecha, "Preguntas": len(e.preguntas),
                      "Puntos": e.total, "Temas": ", ".join(sorted({f"T{t[1]}" for p in e.preguntas for t in p.temas}))} for e in EXAMENES]
            st.dataframe(pd.DataFrame(filas), hide_index=True, width="stretch")

    if t3.open:
        with t3:
            _simulacro()


def _titulo(sol: str) -> str:
    for e in EXAMENES:
        for p in e.preguntas:
            if p.solucion == sol:
                t = p.enunciado.replace("\n", " ")
                return (t[:90] + "…") if len(t) > 90 else t
    return ""


def _simulacro():
    ss = st.session_state
    with caja("idea", "Como el día del examen"):
        st.markdown("Elige un modelo, coge papel y pon un cronómetro con el tiempo del examen. Cuando termines, pulsa **Terminar**: "
                    "verás las soluciones y podrás puntuarte cada pregunta. Recuerda que en este profesor **la mera solución numérica vale 0**: "
                    "explica cada paso.")
    eid = st.selectbox("Modelo", [e.id for e in EXAMENES], index=len(EXAMENES) - 1,
                       format_func=lambda i: next(f"{e.modelo.split(' (')[0]} · {e.tipo} · {e.tiempo}" for e in EXAMENES if e.id == i),
                       key="sim_sel")
    e = next(e for e in EXAMENES if e.id == eid)
    clave = f"sim_fin_{e.id}"
    _info(e)
    terminado = ss.get(clave, False)
    for p in e.preguntas:
        _pregunta(e, p, mostrar_sol=terminado, px="sim")
    if not terminado:
        if st.button("🏁 Terminar y ver soluciones", type="primary", width="stretch", key=f"sim_btn_{e.id}"):
            ss[clave] = True
            st.rerun()
        return
    st.markdown("#### Puntúate (sé sincera 😉)")
    cols = st.columns(min(4, len(e.preguntas)))
    nota = 0
    for i, p in enumerate(e.preguntas):
        nota += cols[i % len(cols)].number_input(f"P{p.num} (de {p.puntos})", 0, p.puntos, 0, step=1, key=f"sim_p_{e.id}_{p.num}")
    sobre10 = 10 * nota / e.total
    if nota >= e.aprobado:
        st.success(f"🎉 {nota} de {e.total} puntos ⇒ **aprobado** (el aprobado está en {e.aprobado}). Sobre 10: {sobre10:.1f}")
    else:
        st.warning(f"{nota} de {e.total} puntos: te faltan {e.aprobado - nota} para el aprobado ({e.aprobado}). Repasa las preguntas que fallaste 💪")
    if st.button("🔄 Repetir este simulacro", key=f"sim_rep_{e.id}"):
        ss[clave] = False
        for p in e.preguntas:
            ss.pop(f"sim_p_{e.id}_{p.num}", None)
        st.rerun()
