from ui.teoria import Tema, S

TEMA = Tema("a5", "Análisis", 5, "Sucesiones de números reales",
            "Límite, acotación, monotonía, subsucesiones, Bolzano–Weierstrass, Cauchy, Stolz, equivalencias y límites superior e inferior.", [

S("convergencia", "5.1 Sucesiones convergentes", "§5.1–5.2 (Definiciones 5.2.1–5.2.8)", [
    ("idea", "Una sucesión es una función que va dando saltos", r"""Es una lista infinita $a_1,a_2,a_3,\dots$: una función $\mathbb N\to\mathbb R$. Converge a $\ell$ si, por estrecha que sea la franja alrededor
de $\ell$, **a partir de un momento** todos los términos se quedan dentro."""),
    ("def", "Límite (5.2.2 y 5.2.5)", r"""
$\lim a_n=\ell$: $\ \forall\varepsilon>0\ \exists n_0\ \forall n>n_0,\ |a_n-\ell|<\varepsilon$. $\quad\lim a_n=+\infty$: $\forall M>0\ \exists n_0\ \forall n>n_0,\ a_n>M$.
Es el límite en $\infty$ de la función $n\mapsto a_n$, así que todo lo del tema 2 (álgebra de límites, indeterminaciones) vale aquí."""),
    ("teo", "Propiedades (5.2.4–5.2.11)", r"""
- El límite es **único**.
- **Sándwich**: $a_n\le b_n\le c_n$ y $a_n,c_n\to\ell$ ⇒ $b_n\to\ell$ (también con $\ell=\pm\infty$).
- Convergente ⇒ **acotada** (el recíproco falla: $(-1)^n$).
- **Acotada × infinitésimo → 0**: $\frac{\operatorname{sen}n}{n}\to0$."""),
    ("ia", None, r"""Entrenar un modelo con **descenso de gradiente** produce una sucesión de parámetros $\theta_n$. Que el entrenamiento «funcione» es exactamente
que esa sucesión converja (introducción del tema 5 de tus apuntes). Pruébalo en el **Rincón Datos e IA**."""),
], "Límite de una sucesión"),

S("monotonas", "5.2 Monotonía, subsucesiones, Bolzano–Weierstrass y Cauchy", "§5.2 (5.2.12–5.2.20)", [
    ("teo", "Monótona y acotada ⇒ convergente (5.2.13)", r"""Creciente y acotada superiormente ⇒ converge a $\sup\{a_n\}$; decreciente y acotada inferiormente ⇒ a $\inf\{a_n\}$.
Es la herramienta de las **sucesiones recurrentes**: (1) acotada por inducción, (2) monótona por inducción, (3) el límite cumple $\ell=g(\ell)$."""),
    ("ej", r"Problema 5.4: $x_1=1$, $x_n=\sqrt{2+x_{n-1}}$", r"""Por inducción $x_n<2$ y $x_{n+1}>x_n$ ⇒ converge; el límite cumple $\ell=\sqrt{2+\ell}$ ⇒ $\ell^2-\ell-2=0$ ⇒ $\ell=2$ (el $-1$ no vale porque $x_n>0$).
Problema 5.8: $x_{n+1}=\frac12\left(x_n+\frac\alpha{x_n}\right)\to\sqrt\alpha$ (el método de Herón para raíces cuadradas, ¡que es Newton!)."""),
    ("teo", "Subsucesiones (5.2.14–5.2.16)", r"""Si $a_n\to\ell$, **toda** subsucesión $a_{n_k}\to\ell$. Por tanto, si dos subsucesiones tienen límites distintos (o una no converge), la sucesión
**no converge**: $(-1)^n$ (pares → 1, impares → −1)."""),
    ("teo", "Bolzano–Weierstrass (5.2.17)", r"""**Toda sucesión acotada tiene una subsucesión convergente.** (Se parte el intervalo por la mitad quedándose siempre con la mitad que
tiene infinitos términos: intervalos encajados que se cierran sobre un punto.)"""),
    ("teo", "Criterio de Cauchy (5.2.18–5.2.19)", r"""$(a_n)$ es **de Cauchy** si $\forall\varepsilon\ \exists n_0$: $n,m\ge n_0\Rightarrow|a_n-a_m|<\varepsilon$ (los términos se juntan entre sí).
**En ℝ, convergente ⇔ de Cauchy.** Ventaja: sirve para probar convergencia sin conocer el límite. (En ℚ falla: los decimales de $\sqrt2$.)"""),
    ("teo", "Criterio secuencial (5.2.20)", r"""$\lim_{x\to a}f(x)=\ell$ ⇔ $f(x_n)\to\ell$ para toda $x_n\to a$ con $x_n\neq a$. Conecta funciones y sucesiones."""),
], "Recurrentes"),

S("practica", "5.3 Cálculo práctico: Stolz, equivalencias y Stirling", "§5.3 (5.3.1–5.3.9)", [
    ("teo", "Criterio de Stolz (5.3.1)", r"""Si $(b_n)$ es estrictamente monótona y divergente (o $a_n,b_n\to0$ con $b_n$ estrictamente monótona):
$$\lim\frac{a_n-a_{n-1}}{b_n-b_{n-1}}=\ell\ \Rightarrow\ \lim\frac{a_n}{b_n}=\ell.$$
Es el **L'Hôpital de las sucesiones**: se «derivan» numerador y denominador restando el término anterior."""),
    ("teo", "Consecuencias (5.3.2)", r"""
- **Media aritmética**: $a_n\to\ell\Rightarrow\frac{a_1+\dots+a_n}n\to\ell$.
- **Media geométrica**: $a_n>0$, $a_n\to\ell\Rightarrow\sqrt[n]{a_1\cdots a_n}\to\ell$.
- **Raíz y cociente**: $a_n>0$ y $\frac{a_{n+1}}{a_n}\to\ell\Rightarrow\sqrt[n]{a_n}\to\ell$. Ej.: $\sqrt[n]{n!}/n\to1/e$."""),
    ("ej", "Problema 5.2", r"""$\displaystyle\lim\frac{1+\frac12+\dots+\frac1n}{\ln n}$: Stolz con $b_n=\ln n$: $\frac{1/n}{\ln n-\ln(n-1)}=\frac{1/n}{-\ln(1-1/n)}\to1$ (equivalencia $\ln(1-1/n)\equiv-1/n$)."""),
    ("teo", "Equivalencias (5.3.4–5.3.9) y Stirling (5.3.7)", r"""
Si $x_n\to0$, valen las mismas equivalencias que en funciones: $\operatorname{sen}x_n\equiv x_n$, $1-\cos x_n\equiv\frac{x_n^2}2$, $\ln(1+x_n)\equiv x_n$… y se usan **sólo en productos y cocientes**.
**Stirling**: $n!\equiv n^ne^{-n}\sqrt{2\pi n}$. Ej. 5.3.6: $\frac{\operatorname{sen}(1/n)\operatorname{tg}(1/n)}{1-\cos(1/n)}\to2$."""),
    ("ia", None, r"""Stirling aparece al estimar **probabilidades binomiales** y la entropía; y la media aritmética de Stolz es la idea de los promedios
móviles que suavizan las curvas de pérdida durante el entrenamiento."""),
], "Stolz"),

S("limsup", "5.4 Límite superior e inferior", "§5.4 (5.4.1–5.4.5)", [
    ("idea", "El techo y el suelo a largo plazo", r"""Aunque una sucesión no converja, se puede preguntar a qué altura máxima y mínima **sigue volviendo** a largo plazo.
$\limsup$ es el mayor valor al que se acerca infinitas veces y $\liminf$ el menor. **Siempre existen** (quizá $\pm\infty$)."""),
    ("def", "Definición 5.4.1", r"""$s_n=\sup\{a_k:k\ge n\}$ (decreciente), $i_n=\inf\{a_k:k\ge n\}$ (creciente); $\limsup a_n=\lim s_n=\inf_ns_n$ y $\liminf a_n=\lim i_n=\sup_ni_n$."""),
    ("teo", "Propiedades (5.4.3–5.4.5)", r"""
- $(a_n)$ acotada ⇔ $\limsup$ y $\liminf$ finitos; entonces son el **mayor y el menor límite de subsucesiones**.
- Siempre $\liminf\le\limsup$, y $a_n\to\ell\iff\liminf=\limsup=\ell$.
- Si son finitos, a partir de un momento $a_n<\limsup+\varepsilon$ y $a_n>\liminf-\varepsilon$."""),
    ("ej", r"$a_n=(-1)^n\frac{n}{n+1}$", r"""Pares → 1, impares → −1: $\limsup=1$, $\liminf=-1$; no converge. (Problema 5.3: recurrencias que alternan dos reglas.)"""),
], "lím sup / lím inf"),
])
