from ui.teoria import Tema, S

TEMA = Tema("f6", "Matemática Finita", 6, "Aritmética de polinomios",
            "Operaciones, grado y orden, división euclídea, teorema de la raíz y Ruffini, mcd y mcm, irreducibles.", [

S("operaciones", "6.1 Polinomios: operaciones, grado y orden", "Apartados 176–179", [
    ("idea", "Los polinomios se comportan como los enteros", r"""
Con polinomios puedes sumar, restar, multiplicar y **dividir con resto**, igual que con los enteros. Por eso todo el tema 5 (mcd,
Euclides, Bézout, irreducibles = primos) se repite aquí casi palabra por palabra. El «tamaño» de un polinomio es su **grado**."""),
    ("def", "Polinomios, grado, orden", r"""
$K[x]$ (con $K=\mathbb Z,\mathbb Q,\mathbb R,\mathbb C$ o $\mathbb Z_p$) son las expresiones $a_0+a_1x+\dots+a_nx^n$.
- **Grado** $\partial p=\max\{k: a_k\neq0\}$ (el exponente más alto). Convenio: $\partial 0=-\infty$.
- **Orden** $\theta(p)=\min\{k: a_k\neq0\}$ (el exponente más bajo). Convenio: $\theta(0)=+\infty$.
- Suma: $\sum(a_i+b_i)x^i$. Producto: $\left(\sum a_ix^i\right)\left(\sum b_jx^j\right)=\sum_k\Big(\sum_{i+j=k}a_ib_j\Big)x^k$."""),
    ("teo", "Propiedades (179)", r"""
- $\partial(p+q)\le\max(\partial p,\partial q)$ y $\theta(p+q)\ge\min(\theta p,\theta q)$.
- Si $p,q\neq0$: $\partial(pq)=\partial p+\partial q$ y $\theta(pq)=\theta p+\theta q$.
- $pq=0\iff p=0$ o $q=0$ (no hay divisores de cero en $K[x]$ si $K$ no los tiene)."""),
    ("errata", "Apartado 178", r"""El PDF pone $\theta(0)=-\infty$; para que $\theta(pq)=\theta p+\theta q$ siga valiendo hay que tomar $\theta(0)=+\infty$
(el orden es un mínimo: el del polinomio 0 «no existe por abajo»)."""),
], "Operaciones y grado"),

S("division", "6.2 División euclídea de polinomios", "Apartados 180–182", [
    ("idea", "Repartir caramelos", r"""El cociente es cuántos le tocan a cada uno y el resto lo que sobra y ya no llega para otra ronda.
En polinomios «no llega» significa **grado del resto < grado del divisor**."""),
    ("teo", "División euclídea (180)", r"""
Si $K$ es un **cuerpo** ($\mathbb Q,\mathbb R,\mathbb C,\mathbb Z_p$) y $q\neq0$, existen **únicos** $c(x)$, $r(x)$ con
$$p(x)=q(x)\,c(x)+r(x),\qquad \partial r<\partial q.$$
Algoritmo: divide el término líder del resto entre el líder de $q$, multiplica por $q$, resta; repite mientras $\partial r\ge\partial q$."""),
    ("ojo", "¿Por qué un cuerpo?", r"""Hay que dividir entre el coeficiente líder de $q$. En $\mathbb Z[x]$, $x^2\div 2x$ no se puede hacer con coeficientes enteros.
En $\mathbb Z_6$ tampoco siempre ($2$ no tiene inverso): por eso la app sólo deja $\mathbb Z_p$ con $p$ primo."""),
    ("ej", "Ejercicio 181", r"""
- $(2x^6-3x^3+2)\div(x^2-3x+1)$ en $\mathbb Q[x]$.
- $x^{10}\div(x-1)$: cociente $x^9+x^8+\dots+1$, resto $1$ (teorema del resto: $1^{10}=1$).
- $(2x^3+2x^2+4x+1)\div(3x+4)$ en $\mathbb R[x]$: salen fracciones, y está bien.

Hazlos en la pestaña de **Polinomios** con el paso a paso."""),
], "Calculadora de polinomios"),

S("ruffini", "6.3 Raíces, teorema del resto y Ruffini", "Apartados 183–184", [
    ("teo", "Teorema de la raíz (183)", r"""
$$(x-r)\mid p(x)\iff p(r)=0.$$
Al dividir entre $x-r$ el resto es una constante $\rho$ (grado $<1$), y evaluando $p(x)=c(x)(x-r)+\rho$ en $x=r$ sale $\rho=p(r)$
(**teorema del resto**)."""),
    ("teo", "Raíces racionales", r"""
Si $p(x)$ tiene coeficientes **enteros** y $\frac pq$ (irreducible) es raíz, entonces $p\mid a_0$ (término independiente) y $q\mid a_n$
(coeficiente líder). Así se obtiene una lista finita de candidatos que se prueban con Ruffini; en particular, las raíces **enteras** dividen
al término independiente."""),
    ("truco", "Ruffini en tres movimientos", r"""Baja el primer coeficiente; multiplícalo por $r$ y súmalo al siguiente; repite. La última casilla es el resto $p(r)$
y las demás, el cociente. Si da 0, ¡raíz!, y sigues con el cociente."""),
    ("errata", "Apartado 184", r"""«Ruffini para encontrar todas las raíces enteras de $p\in\mathbb R[x]$» necesita **coeficientes enteros** (si no, el
criterio de los divisores del término independiente no tiene sentido)."""),
], "Raíces racionales"),

S("mcd_pol", "6.4 Divisibilidad, mcd y mcm de polinomios", "Apartados 185–189", [
    ("def", "Divisor, múltiplo, mónico, asociados", r"""
- $d\mid f$ si $f=d\cdot q$. $\langle f\rangle=f\cdot K[x]$ son los múltiplos de $f$.
- **Mónico**: coeficiente líder 1. Cada $f\neq0$ tiene un único mónico asociado $\tilde f$ (dividir entre el líder).
- **Asociados** $f\sim g$: se diferencian en una constante no nula (es una relación de equivalencia; el cociente son los mónicos ∪ {0})."""),
    ("teo", "mcd y mcm (188–189)", r"""
$\operatorname{Div}(f)\cap\operatorname{Div}(g)=\operatorname{Div}(m)$ para algún $m$: es el **mcd**, único salvo constante, y único si se pide **mónico**.
Los múltiplos comunes son los múltiplos de un $M$: el **mcm**. Se calcula con **Euclides** (último resto no nulo, hecho mónico) y
hay identidad de **Bézout**: $\operatorname{mcd}(f,g)=s(x)f(x)+t(x)g(x)$. Además $\operatorname{mcm}=\frac{fg}{\operatorname{mcd}}$ (salvo constante)."""),
    ("ej", "El ejercicio que hiciste en clase", r"""
$A=x^{10}+11x^8+46x^6+90x^4+81x^2+27$, $B=x^{10}+9x^8+30x^6+46x^4+33x^2+9$.
$A=1\cdot B+(2x^8+16x^6+44x^4+48x^2+18)$; $\ B=\left(\tfrac12x^2+\tfrac12\right)\cdot r+0$.
$\operatorname{mcd}=x^8+8x^6+22x^4+24x^2+9=(x^2+1)^2(x^2+3)^2$."""),
    ("teo", "Preorden de divisibilidad (186–187)", r"""En $K[x]$, $\mid$ es un **preorden** (no antisimétrico: $x\mid2x$ y $2x\mid x$). Restringido a los **mónicos** es un orden (parcial)."""),
    ("errata", "Apartado 188 (d)", r"""Los múltiplos comunes son $\langle f\rangle\cap\langle g\rangle=\langle M\rangle$ (intersección), no la unión."""),
], "Calculadora de polinomios"),

S("irreducibles", "6.5 Polinomios irreducibles", "Apartados 190–194", [
    ("idea", "Los «primos» de los polinomios", r"""Un irreducible no se puede partir en dos polinomios de grado menor. Si se puede o no **depende del cuerpo**:
$x^2-2$ es irreducible en $\mathbb Q$ pero en $\mathbb R$ es $(x-\sqrt2)(x+\sqrt2)$; $x^2+1$ lo es en $\mathbb R$ pero no en $\mathbb C$."""),
    ("def", "Irreducible y primo (190–191)", r"""
$f$ es **irreducible** si sus únicos divisores son las constantes no nulas y sus asociados. Es **primo** si $f\mid ab\Rightarrow f\mid a$ o
$f\mid b$. En $K[x]$ las dos nociones coinciden (como en $\mathbb Z$)."""),
    ("resumen", "¿Quién es irreducible?", r"""
| Cuerpo | Irreducibles | Por qué |
|---|---|---|
| todos | grado 1 | (192) cualquier factor propio tendría grado 0 |
| $\mathbb C$ | **sólo** grado 1 | Teorema Fundamental del Álgebra: todo polinomio tiene raíz |
| $\mathbb R$ | grado 1 y grado 2 **sin raíces reales** ($b^2-4ac<0$) | grado impar ⇒ raíz real por Bolzano (194) |
| $\mathbb Q$ | de **cualquier** grado ($x^n-2$) | grado 2 o 3: irreducible ⇔ sin raíces racionales |
| $\mathbb Z_p$ | depende: grado 2 o 3 ⇔ sin raíces en $\mathbb Z_p$ | $x^2+1$: irreducible en $\mathbb Z_3$, no en $\mathbb Z_5$ ($2^2+1=5\equiv0$) |"""),
    ("ojo", "Grado 4 sin raíces no es irreducible", r"""$x^4+1$ no tiene raíces reales y, sin embargo, en $\mathbb R$ es $(x^2+\sqrt2x+1)(x^2-\sqrt2x+1)$. El truco «sin raíces ⇒
irreducible» sólo vale para grados 2 y 3."""),
], "Irreducibles"),
])
