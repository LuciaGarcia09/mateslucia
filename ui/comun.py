"""Piezas de interfaz compartidas."""
from __future__ import annotations

import numpy as np
import plotly.graph_objects as go
import streamlit as st
import sympy as sp

from core.parsing import leer, leer_numero, leer_entero, ErrorLectura, x

ROSA = "#e75480"
ROSA_SUAVE = "#f7c6d9"
LILA = "#8e5bd6"
TURQUESA = "#1fa595"
AMARILLO = "#e0a21b"
GRIS = "#9a8f96"


def L(e) -> str:
    return sp.latex(e)


def entrada_expr(etiqueta: str, defecto: str, clave: str, ayuda: str | None = None):
    txt = st.text_input(etiqueta, defecto, key=clave, help=ayuda or
                        "Escribe como en clase: x^2 + 3x, sen(x), ln(x), e^x, raiz(x), |x|, pi")
    try:
        return leer(txt)
    except ErrorLectura as exc:
        st.error(str(exc))
        return None


def entrada_num(etiqueta: str, defecto: str, clave: str, ayuda: str | None = None):
    txt = st.text_input(etiqueta, defecto, key=clave, help=ayuda or "Admite 1/2, pi, e, oo (infinito), -oo")
    try:
        return leer_numero(txt)
    except ErrorLectura as exc:
        st.error(str(exc))
        return None


def entrada_entero(etiqueta: str, defecto: int, clave: str, minimo=None, maximo=None, ayuda=None):
    return st.number_input(etiqueta, value=defecto, step=1, key=clave, min_value=minimo, max_value=maximo,
                           help=ayuda, format="%d")


def verificado(ok, texto_ok="Comprobado de forma independiente ✔", texto_mal=None):
    """Muestra el sello de comprobación."""
    if ok is True:
        st.success(texto_ok, icon="✅")
    elif ok is False:
        st.error(texto_mal or "La comprobación independiente NO cuadra: no te fíes de este resultado y revísalo a mano.",
                 icon="⚠️")
    else:
        st.info("No he podido hacer una comprobación independiente de este resultado.", icon="ℹ️")


def _md(texto: str) -> str:
    """Las analogías antiguas usaban <b>…</b>: lo pasamos a markdown para que funcione el LaTeX."""
    return texto.replace("<b>", "**").replace("</b>", "**")


def analogia(texto: str, titulo: str = "Analogía"):
    from ui.estilo import caja
    with caja("idea", titulo):
        st.markdown(_md(texto))


def ia(texto: str):
    from ui.estilo import caja
    with caja("ia"):
        st.markdown(_md(texto))


def figura_base(titulo: str = "", alto: int = 430) -> go.Figure:
    fig = go.Figure()
    fig.update_layout(
        title=titulo, height=alto, margin=dict(l=10, r=10, t=40 if titulo else 10, b=10),
        template="plotly_white", hovermode="x unified", paper_bgcolor="rgba(255,255,255,0.85)",
        plot_bgcolor="#fffafc", font=dict(family="Nunito, sans-serif", color="#2b1b24"),
        colorway=[ROSA, LILA, TURQUESA, AMARILLO, GRIS],
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
    )
    fig.update_xaxes(zeroline=True, zerolinewidth=1.5, zerolinecolor="#c9a9b8", showspikes=True, gridcolor="#f6e3ec")
    fig.update_yaxes(zeroline=True, zerolinewidth=1.5, zerolinecolor="#c9a9b8", gridcolor="#f6e3ec")
    return fig


def trazar(fig, f, a, b, nombre, color=ROSA, ancho=3, guion=None, recorte=None):
    from core.analisis import puntos_grafica
    xs, ys = puntos_grafica(f, a, b, recorte=recorte)
    fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines", name=nombre,
                             line=dict(color=color, width=ancho, dash=guion), connectgaps=False))
    return xs, ys


def punto(fig, px, py, nombre, color=LILA, simbolo="circle"):
    fig.add_trace(go.Scatter(x=[px], y=[py], mode="markers+text", name=nombre, text=[nombre],
                             textposition="top center", marker=dict(size=11, color=color, symbol=simbolo)))


def num(v, cifras=8) -> str:
    try:
        f = float(v)
    except (TypeError, ValueError):
        return str(v)
    if f == int(f) and abs(f) < 1e15:
        return str(int(f))
    return f"{f:.{cifras}g}"


def calcular(fn, *args, segundos: float = 15, **kw):
    """Ejecuta un cálculo simbólico con límite de tiempo; si falla, muestra el error y devuelve None."""
    from core.tiempo import con_tiempo, Tarda
    try:
        return con_tiempo(fn, *args, segundos=segundos, **kw)
    except Tarda as exc:
        st.warning(f"⏳ {exc}")
    except (ErrorLectura, ValueError, ZeroDivisionError) as exc:
        st.error(str(exc))
    except Exception as exc:  # noqa: BLE001
        st.error(f"No he podido hacer este cálculo: {exc}")
    return None


def ok_no(v) -> str:
    if v is True:
        return "<span class='sello sello-ok'>sí ✓</span>"
    if v is False:
        return "<span class='sello sello-no'>no ✗</span>"
    return "<span class='sello'>?</span>"
