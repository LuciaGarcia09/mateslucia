"""Páginas de estudio: portada, buscador, erratas, progreso y chuleta."""
from __future__ import annotations

import streamlit as st

from core.ejercicios import GENERADORES
from ui.estilo import cabecera, caja, tarjeta
from ui.teoria import buscar, progreso_tema, marcar, _cargar, _guardar
from ui.temas import TEMAS, TODOS, ICONO

PAGINAS: dict = {}     # id de tema → st.Page (lo rellena app.py)


def _ir(tema_id: str, seccion_id: str | None = None):
    if seccion_id:
        st.session_state[f"sec_{tema_id}"] = seccion_id
        st.session_state.pop(f"pills_{tema_id}", None)
        st.session_state.pop(f"tabs_{tema_id}", None)
    st.switch_page(PAGINAS[tema_id])


# ======================================================================== portada
def inicio():
    total_sec = sum(len(t.secciones) for t in TODOS)
    total_herr = sum(len(h) for _, _, h in TEMAS)
    hechas = sum(progreso_tema(t) * len(t.secciones) for t in TODOS)
    cabecera("🌸", "MatesLucía", "Tu laboratorio de Matemática Finita y Análisis · 1º de Ingeniería de Datos e IA. "
             "Teoría explicada con analogías, calculadoras que enseñan el paso a paso y ejercicios que se corrigen solos.",
             etiqueta="Hola, Lucía 💗",
             chips=[f"{len(TODOS)} temas", f"{total_sec} secciones de teoría", f"{total_herr} calculadoras",
                    f"{sum(len(d) for d in GENERADORES.values())} tipos de ejercicio", "todo comprobado dos veces"])
    c1, c2, c3 = st.columns(3)
    with c1:
        tarjeta("Teoría entendida", f"{hechas:.0f} de {total_sec} secciones marcadas con 💗", f"{100 * hechas / total_sec:.0f} %",
                hechas / total_sec, alto=175)
    with c2:
        ss = st.session_state
        n, a = ss.get("ex_intentos", 0), ss.get("ex_aciertos", 0)
        tarjeta("Ejercicios de hoy", f"{a} aciertos de {n} intentos" if n else "Aún no has hecho ninguno: ¡a por el primero!",
                f"{10 * a / n:.1f}" if n else "—", a / n if n else 0, alto=175)
    with c3:
        siguiente = next(((t, s) for t in TODOS for s in t.secciones if not _cargar().get(f"{t.id}/{s.id}")), None)
        tarjeta("Para seguir", f"{siguiente[0].asignatura} · Tema {siguiente[0].numero}<br><b>{siguiente[1].titulo}</b>"
                if siguiente else "¡Lo has marcado todo! Ahora, modo examen 💪", "→", alto=175)
        if siguiente and st.button("Seguir estudiando", type="primary", width="stretch"):
            _ir(siguiente[0].id, siguiente[1].id)
    st.write("")
    for asig, cols in (("Matemática Finita", "f"), ("Análisis", "a")):
        st.markdown(f"### {'📐' if cols == 'f' else '📈'} {asig}")
        temas = [t for t in TODOS if t.id.startswith(cols)]
        for fila in [temas[i:i + 4] for i in range(0, len(temas), 4)]:
            cs = st.columns(4)
            for c, t in zip(cs, fila):
                with c:
                    tarjeta(f"{ICONO[t.id]} {t.titulo}", t.resumen, f"T{t.numero}", progreso_tema(t), alto=385)
                    if st.button("Abrir", key=f"abrir_{t.id}", width="stretch"):
                        _ir(t.id)
    st.divider()
    with caja("truco", "Cómo escribir en las calculadoras"):
        st.markdown("""
| Quiero | Escribo | | Quiero | Escribo |
|---|---|---|---|---|
| x² + 3x | `x^2 + 3x` | | √x | `raiz(x)` |
| sen, cos, tg | `sen(x)`, `cos(x)`, `tg(x)` | | arcotangente | `arctg(x)` |
| ln x | `ln(x)` | | eˣ | `e^x` |
| \\|x − 1\\| | `\\|x-1\\|` | | ∞ | `oo` o `infinito` |
| π | `pi` | | n! | `factorial(n)` |
| fracción | `(x+1)/(x-2)` | | i (complejos) | `I` |
""")
    with caja("idea", "Cómo sacarle partido"):
        st.markdown("1. Lee la **teoría** del tema (cada sección empieza con una analogía) y márcala con 💗 cuando la entiendas.\n"
                    "2. Haz el ejercicio **en papel** y compruébalo con la **calculadora** del tema: te enseña el paso a paso y un "
                    "sello ✅ cuando un segundo método independiente da lo mismo.\n"
                    "3. Termina con la pestaña **✍️ Practica** o el **Modo examen**, que te pone nota y te dice qué repasar.")


# ======================================================================== buscador
def buscador():
    cabecera("🔎", "Buscador", f"Busca cualquier concepto en la teoría de los {len(TODOS)} temas (sin preocuparte por las tildes).",
             etiqueta="Estudiar")
    q = st.text_input("¿Qué buscas?", placeholder="p. ej. Bézout, Raabe, palomar, convergencia uniforme, Stirling…", key="bus_q")
    if not q:
        st.caption("Ideas: `inverso`, `hasse`, `taylor`, `leibniz`, `impropia`, `stolz`, `wilson`, `sobreyectiva`.")
        return
    res = buscar(TODOS, q)
    if not res:
        st.info("No encuentro nada con todas esas palabras. Prueba con menos palabras o un sinónimo.")
        return
    st.caption(f"{len(res)} resultado(s)")
    for k, (_, t, s, frag) in enumerate(res):
        with st.container(border=True):
            c1, c2 = st.columns([5, 1])
            c1.markdown(f"**{ICONO[t.id]} {t.asignatura} · Tema {t.numero}** — {s.titulo}  \n"
                        f"<span class='mini'>…{frag}…</span>", unsafe_allow_html=True)
            if c2.button("Ir →", key=f"bus_{k}", width="stretch"):
                _ir(t.id, s.id)


# ======================================================================== erratas
def erratas():
    cabecera("🛠️", "Erratas de los apuntes", "Lo que he encontrado revisando tus apuntes, la guía y los exámenes, comprobado a mano sobre las "
             "páginas originales. En la teoría de la app ya está corregido.", etiqueta="Estudiar")
    n = 0
    st.markdown("### En los apuntes y la guía")
    for t in TODOS:
        for s in t.secciones:
            for b in s.bloques:
                if b[0] == "errata":
                    n += 1
                    tit = b[1] if len(b) == 3 else None
                    with caja("errata", f"{t.asignatura} · Tema {t.numero} · {tit or s.titulo}"):
                        st.markdown(b[-1])
                        st.caption(f"📎 {s.referencia}")
                        if st.button("Ver en la teoría", key=f"err_{n}"):
                            _ir(t.id, s.id)
    from contenido.examenes import EXAMENES
    st.markdown("### En los exámenes y sus soluciones oficiales")
    for e in EXAMENES:
        for p in e.preguntas:
            if p.errata:
                n += 1
                with caja("errata", f"{e.modelo.split(' (')[0]} · {e.tipo} · Pregunta {p.num}"):
                    st.markdown(p.errata)
    if not n:
        st.success("No hay erratas registradas.")


# ======================================================================== progreso
def mi_progreso():
    cabecera("💗", "Mi progreso", "Qué secciones has marcado como entendidas y cómo vas en los ejercicios.", etiqueta="Estudiar")
    p = _cargar()
    for asig in ("Matemática Finita", "Análisis"):
        st.markdown(f"#### {asig}")
        for t in [t for t in TODOS if t.asignatura == asig]:
            c1, c2 = st.columns([3, 2])
            c1.markdown(f"{ICONO[t.id]} **Tema {t.numero}.** {t.titulo}")
            c2.progress(progreso_tema(t), text=f"{sum(1 for s in t.secciones if p.get(f'{t.id}/{s.id}'))}/{len(t.secciones)}")
    st.divider()
    ss = st.session_state
    st.markdown("#### Ejercicios (esta sesión)")
    n, a = ss.get("ex_intentos", 0), ss.get("ex_aciertos", 0)
    st.write(f"{a} aciertos de {n} intentos" + (f" · nota {10 * a / n:.1f}" if n else ""))
    if st.button("Borrar mi progreso de teoría"):
        ss.progreso = {}
        _guardar()
        st.rerun()
def chuleta():
    cabecera("📚", "Chuleta rápida", "Las fórmulas que más se usan, en una sola página.", etiqueta="Estudiar")
    t1, t2 = st.tabs(["Matemática finita", "Análisis"])
    with t1:
        st.markdown(r"""
**División euclídea**: $A = qB + r$ con $\operatorname{gr}(r) < \operatorname{gr}(B)$ (o $r = 0$). Única en un cuerpo (ℚ, ℤₚ con p primo).

**Euclides**: $\operatorname{mcd}(A,B) = \operatorname{mcd}(B, r)$. El último resto no nulo (hecho mónico) es el mcd.
**Bézout**: existen $s, t$ con $sA + tB = \operatorname{mcd}(A,B)$. $\operatorname{mcm} = \frac{AB}{\operatorname{mcd}}$.

**Teorema del resto**: el resto de dividir $P(x)$ entre $x-a$ es $P(a)$. $a$ es raíz ⇔ $(x-a) \mid P$.

**Congruencias**: $ax \equiv b \pmod m$ tiene solución ⇔ $d = \operatorname{mcd}(a,m) \mid b$; entonces hay $d$ soluciones mód $m$.
**Inverso**: $a^{-1} \bmod m$ existe ⇔ $\operatorname{mcd}(a,m) = 1$ (sale de Bézout).
**Fermat**: $p$ primo, $p\nmid a$ ⇒ $a^{p-1}\equiv 1$. **Euler**: $\operatorname{mcd}(a,n)=1$ ⇒ $a^{\varphi(n)}\equiv 1 \pmod n$.
**Chino del resto**: módulos coprimos dos a dos ⇒ solución única módulo $M = \prod m_i$.

**Combinatoria** (k elementos de n):

| | importa el orden | no importa el orden |
|---|---|---|
| **con repetición** | $n^k$ | $\binom{n+k-1}{k}$ |
| **sin repetición** | $\frac{n!}{(n-k)!}$ | $\binom{n}{k}$ |

**Sobreyecciones** $k\to n$: $n!\,S(k,n) = \sum_{i=0}^n (-1)^i\binom{n}{i}(n-i)^k$. **Desarreglos**: $D_n = n!\sum_{i=0}^n\frac{(-1)^i}{i!}$.
**Inclusión–exclusión**: $|A\cup B\cup C| = |A|+|B|+|C| - |A\cap B| - |A\cap C| - |B\cap C| + |A\cap B\cap C|$.
**Recurrencias**: $a_n = c_1a_{n-1}+c_2a_{n-2}$ → $\lambda^2 = c_1\lambda + c_2$; raíces distintas $A\lambda_1^n + B\lambda_2^n$; doble $(A + Bn)\lambda^n$.
""")
    with t2:
        st.markdown(r"""
**Límites notables**: $\frac{\operatorname{sen}x}{x}\to 1$, $\left(1+\frac1x\right)^x \to e$, $\frac{e^x-1}{x}\to 1$, $\frac{\ln(1+x)}{x}\to 1$.
**Jerarquía en ∞**: $\ln x \ll x^a \ll a^x \ll x! \ll x^x$.

**Continuidad en a**: existe $f(a)$, existe $\lim_{x\to a} f$, y coinciden.
**Bolzano**: $f$ continua en $[a,b]$ y $f(a)f(b)<0$ ⇒ hay $c\in(a,b)$ con $f(c)=0$.
**Weierstrass**: continua en $[a,b]$ ⇒ alcanza máximo y mínimo absolutos.
**Rolle**: continua en $[a,b]$, derivable en $(a,b)$, $f(a)=f(b)$ ⇒ existe $c$ con $f'(c)=0$.
**Valor medio (Lagrange)**: existe $c$ con $f'(c) = \frac{f(b)-f(a)}{b-a}$.
**L'Hôpital**: si es $\frac00$ o $\frac\infty\infty$, $\lim\frac fg = \lim\frac{f'}{g'}$ (si este existe).

**Extremos**: $f'(c)=0$ y $f''(c)>0$ ⇒ mínimo; $f''(c)<0$ ⇒ máximo; si $f''(c)=0$, mira el cambio de signo de $f'$.

**Taylor**: $f(x) = \sum_{k=0}^n \frac{f^{(k)}(a)}{k!}(x-a)^k + R_n$, $R_n = \frac{f^{(n+1)}(\xi)}{(n+1)!}(x-a)^{n+1}$.
$e^x = \sum\frac{x^k}{k!}$, $\operatorname{sen}x = x - \frac{x^3}{3!} + \frac{x^5}{5!} - \cdots$, $\cos x = 1 - \frac{x^2}{2!} + \cdots$, $\ln(1+x) = x - \frac{x^2}{2} + \frac{x^3}{3}-\cdots$

**Integral**: Barrow $\int_a^b f = F(b) - F(a)$. Partes: $\int u\,dv = uv - \int v\,du$.
**Series**: geométrica $\sum_{n\ge0} r^n = \frac{1}{1-r}$ si $|r|<1$; $\sum \frac1{n^p}$ converge ⇔ $p>1$.
""")


