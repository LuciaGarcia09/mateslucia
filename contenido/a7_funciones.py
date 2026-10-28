from ui.teoria import Tema, S

TEMA = Tema("a7", "Análisis", 7, "Sucesiones y series de funciones",
            "Convergencia puntual y uniforme, criterio M de Weierstrass, continuidad, integración y derivación del límite, series de potencias y funciones analíticas.", [

S("puntual", "7.1 Convergencia puntual", "§7.1 (Definiciones 7.1.1–7.1.4, Ejemplos 7.1.5–7.1.9)", [
    ("idea", "Una película de funciones", r"""Una sucesión de funciones $f_1,f_2,\dots$ es como los fotogramas de una película. **Puntual**: cada píxel ($x$) acaba
quieto en su color final… pero cada uno a su ritmo, y algunos pueden tardar muchísimo."""),
    ("def", "Definición 7.1.2 y Observación 7.1.3", r"""$f_n\to f$ **puntualmente** en $A$ si $f(x)=\lim f_n(x)$ para cada $x\in A$: dados $x$ y $\varepsilon$ existe $n_0$ **(que depende de $x$ y de $\varepsilon$)**
con $|f_n(x)-f(x)|<\varepsilon$ para $n\ge n_0$. Para series: $\sum f_n$ converge puntualmente si lo hacen sus sumas parciales; el conjunto
donde converge es el **campo de convergencia**."""),
    ("ojo", "La pregunta del tema", r"""¿Hereda $f$ las propiedades de las $f_n$? Con convergencia puntual **no**: es intercambiar dos límites, y el orden importa
(Ej. 7.1.5: $\frac m{m+n}$ da 1 en un orden y 0 en el otro)."""),
    ("ej", "Los contraejemplos de los apuntes", r"""
- **7.1.6**: $\sum\frac{x^2}{(1+x^2)^n}$ es $1+x^2$ si $x\neq0$ y $0$ en $x=0$: funciones continuas con suma **discontinua**.
- **7.1.7**: $\lim_m\lim_n(\cos m!\pi x)^{2n}$ es 1 en racionales y 0 en irracionales: **no integrable**.
- **7.1.8**: $\frac{\operatorname{sen}nx}{\sqrt n}\to0$ pero las derivadas $\sqrt n\cos nx$ **no** tienden a 0.
- **7.1.9**: $n^2x(1-x^2)^n\to0$ en $[0,1]$ pero $\int_0^1f_n=\frac{n^2}{2n+2}\to\infty$: el límite de las integrales **no** es la integral del límite.
- **Clásico**: $x^n$ en $[0,1]$ tiende a 0 si $x<1$ y a 1 en $x=1$."""),
], "Puntual vs uniforme"),

S("uniforme", "7.2 Convergencia uniforme", "§7.2 (7.2.1–7.2.7)", [
    ("idea", "Todos los píxeles a la vez", r"""**Uniforme**: el mismo $n_0$ sirve para **todos** los $x$. Gráficamente: a partir de $n_0$ toda la gráfica de $f_n$ cabe en una
**banda de anchura $\varepsilon$** alrededor de la de $f$ (un «tubo»)."""),
    ("def", "Definición 7.2.1", r"""$\forall\varepsilon>0\ \exists n_0$: $n\ge n_0\Rightarrow|f_n(x)-f(x)|<\varepsilon$ **para todo $x\in A$**. Uniforme ⇒ puntual, no al revés."""),
    ("teo", "Criterio del supremo (7.2.4)", r"""$f_n\to f$ uniformemente ⇔ $M_n=\sup_{x\in A}|f_n(x)-f(x)|\to0$. **Es el que se usa en la práctica**: calcula el límite puntual, el sup (derivando)
y mira si tiende a 0."""),
    ("ej", "Ejemplo 7.2.7", r"""$f_n(x)=nx(1-x)^n$ en $[0,1]$ → 0 puntualmente. El máximo está en $x=\frac1{n+1}$ y vale $\left(\frac n{n+1}\right)^{n+1}\to\frac1e\neq0$ ⇒ **no uniforme**.
(La «joroba» no baja: sólo se desplaza hacia 0.)"""),
    ("teo", "Cauchy uniforme (7.2.3) y criterio M de Weierstrass (7.2.5)", r"""
- Converge uniformemente ⇔ $\forall\varepsilon\ \exists n_0$: $|f_n(x)-f_m(x)|<\varepsilon$ para $n,m\ge n_0$ y **todo** $x$.
- **M de Weierstrass**: si $|f_n(x)|\le M_n$ para todo $x\in A$ y $\sum M_n$ converge, entonces $\sum f_n$ converge **uniforme y absolutamente** en $A$.
Ej.: $\sum\frac{\cos nx}{n^2}$: $M_n=\frac1{n^2}$ ⇒ uniforme en ℝ."""),
], "Criterio M"),

S("propiedades", "7.3 Qué se hereda con convergencia uniforme", "§7.3–7.6 (7.3.1–7.5.3)", [
    ("teo", "Continuidad (7.3.1–7.3.2)", r"""Límite uniforme de funciones **continuas** es **continuo**: $\lim_{t\to x}\lim_nf_n(t)=\lim_n\lim_{t\to x}f_n(t)$.
Consecuencia útil: si el límite puntual de funciones continuas es **discontinuo**, la convergencia **no puede ser uniforme** ($x^n$ en $[0,1]$)."""),
    ("ojo", "Ejemplo 7.3.3", r"""El recíproco falla: puede haber límite continuo sin convergencia uniforme (una «joroba» de altura 1 que se desplaza hacia la derecha
en $[0,\infty)$ tiende a 0 en cada punto, pero el sup siempre vale 1)."""),
    ("teo", "Dini (7.3.5)", r"""En un **compacto** $K$, si $f_n$ continuas convergen puntualmente a $f$ **continua** y **monótonamente** ($f_n\ge f_{n+1}$), la convergencia es uniforme."""),
    ("teo", "Integración (7.4.1–7.4.2)", r"""$f_n\to f$ uniformemente en $[a,b]$ ⇒ $f$ integrable y $\int_a^bf=\lim\int_a^bf_n$. Para series: se **integra término a término**."""),
    ("teo", "Derivación (7.5.1)", r"""Si $f_n\in C^1[a,b]$, $(f_n(x_0))$ converge en algún punto y **las derivadas $f_n'$ convergen uniformemente**, entonces $f_n\to f$ uniformemente
y $f'=\lim f_n'$. (Ojo: lo que tiene que ser uniforme es la convergencia de las **derivadas**.)"""),
    ("teo", "Weierstrass (7.5.2–7.5.3)", r"""Existe una función **continua en todo ℝ y no derivable en ningún punto**: $\sum a^n\cos(b^n\pi x)$ para ciertos $a,b$ (una serie uniformemente
convergente de cosenos cada vez más rápidos). Continuidad no implica suavidad."""),
    ("resumen", "Tabla resumen", r"""
| Las $f_n$ son… | y la convergencia es… | ⇒ el límite $f$ es… |
|---|---|---|
| continuas | puntual | **puede no** ser continua |
| continuas | uniforme | continua |
| integrables | uniforme | integrable, $\int f=\lim\int f_n$ |
| $C^1$ | $f_n'$ uniforme (+ un punto) | derivable, $f'=\lim f_n'$ |"""),
], "Puntual vs uniforme"),

S("potencias", "7.4 Series de potencias", "§7.7 (7.7.1–7.7.3)", [
    ("idea", "Polinomios infinitos", r"""Una serie de potencias $\sum c_n(x-a)^n$ es un «polinomio de grado infinito». Converge en un **intervalo centrado en $a$**:
dentro manda la serie geométrica, fuera los términos crecen sin control."""),
    ("teo", "Cauchy–Hadamard (7.7.1–7.7.2)", r"""
$$\frac1R=\limsup\sqrt[n]{|c_n|}\qquad\left(\text{o }\frac1R=\lim\left|\frac{c_{n+1}}{c_n}\right|\text{ si existe}\right).$$
- $|x-a|<R$: converge **absolutamente**. $\ |x-a|>R$: **no** converge.
- $|x-a|=R$: hay que estudiar **cada extremo a mano** (con los criterios del tema 6)."""),
    ("ej", "Los tres comportamientos en los extremos", r"""$\sum x^n$ ($R=1$): diverge en $\pm1$. $\ \sum\frac{x^n}n$: diverge en 1, converge en $-1$ (Leibniz). $\ \sum\frac{x^n}{n^2}$: converge en los dos."""),
    ("teo", "Operaciones término a término (7.7.3)", r"""En $[a-r,a+r]$ con $r<R$ la convergencia es **uniforme** (criterio M), así que se puede **derivar e integrar término a término**, y el radio
no cambia. La suma es $C^\infty$ en $|x-a|<R$.
Ej.: integrando $\frac1{1+t^2}=\sum(-1)^nt^{2n}$ sale $\operatorname{arctg}x=\sum\frac{(-1)^nx^{2n+1}}{2n+1}$ ($|x|<1$)."""),
], "Series de potencias"),

S("analiticas", "7.5 Funciones analíticas", "§7.7 (7.7.4–7.7.6)", [
    ("def", "Definición 7.7.4", r"""$f$ es **analítica** en $a$ si coincide con una serie de potencias en un entorno $|x-a|<R$. Entonces esa serie es **su serie de Taylor**:
$c_n=\frac{f^{(n)}(a)}{n!}$."""),
    ("teo", "Proposición 7.7.5", r"""Analítica ⇒ $C^\infty$. **El recíproco es falso**: $f(x)=e^{-1/x^2}$ ($f(0)=0$) es $C^\infty$, todas sus derivadas en 0 valen 0, su serie de Taylor
es la serie nula… y **no coincide** con $f$ fuera de 0. (Es tan plana en 0 que ningún polinomio la «ve».)"""),
    ("teo", "Cómo obtener desarrollos (7.7.6)", r"""
1. Derivadas sucesivas (fórmula de Taylor) y comprobar que el **resto tiende a 0**.
2. A partir de series conocidas: geométrica $\frac1{1-x}=\sum x^n$, sustituyendo $x$ por $-x^2$, $2x$…
3. Derivando o integrando término a término.
4. Operando (sumas, productos de Cauchy) con series ya conocidas."""),
    ("errata", "§7.7, primer párrafo", r"""Dice que las series de potencias prolongan lo visto «en el **Tema 2** sobre los polinomios de Taylor»; los polinomios de Taylor
están en el **Tema 3** (§3.4)."""),
    ("ia", None, r"""Las funciones de activación (sigmoide, tanh, GELU) y la softmax se evalúan con aproximaciones polinómicas/racionales sacadas de estas series,
y la «linealización» de un modelo alrededor de un punto es quedarse con el término de grado 1."""),
], "Funciones analíticas"),
])
