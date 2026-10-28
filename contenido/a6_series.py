from ui.teoria import Tema, S

TEMA = Tema("a6", "Análisis", 6, "Series de números reales",
            "Convergencia, términos positivos y sus criterios, convergencia absoluta, reordenación, Abel–Dirichlet–Leibniz, series que se suman y producto de Cauchy.", [

S("definicion", "6.1 Qué es una serie", "§6.1 (Definiciones 6.1.1–6.1.4, Teoremas 6.1.5–6.1.10)", [
    ("idea", "Sumar infinitas cosas = mirar a dónde van las sumas parciales", r"""Una serie no se «suma de golpe»: se van acumulando términos $S_n=a_1+\dots+a_n$ y se mira si esa **sucesión** de sumas parciales
tiene límite. Es como llenar un vaso con gotas cada vez más pequeñas: puede rebosar (diverge) o quedarse en un nivel (converge)."""),
    ("def", "Serie, suma y carácter (6.1.1–6.1.4)", r"""$\sum a_n$ **converge** si $S_n\to S\in\mathbb R$ ($S$ es la **suma**); **diverge** si $S_n\to\pm\infty$; **oscila** si no tiene límite.
Cambiar un número finito de términos **no cambia el carácter** (sí la suma)."""),
    ("teo", "Cauchy (6.1.5) y condición necesaria (6.1.6)", r"""
Converge ⇔ $\forall\varepsilon\ \exists n_0$: $|a_{n+1}+\dots+a_{n+p}|<\varepsilon$ para $n\ge n_0$ y todo $p$.
**Si $\sum a_n$ converge, $a_n\to0$.** Por tanto, si $a_n\not\to0$, **diverge**. El recíproco es falso: $\sum\frac1n$ diverge aunque $\frac1n\to0$."""),
    ("teo", "Resto (6.1.8) y linealidad", r"""$R_n=\sum_{k>n}a_k\to0$ si la serie converge. $\sum(\lambda a_n+\mu b_n)=\lambda\sum a_n+\mu\sum b_n$ si ambas convergen."""),
    ("teo", "Serie geométrica (6.1.10)", r"""$\sum_{n\ge0}r^n$ converge ⇔ $|r|<1$, y vale $\frac1{1-r}$. En general $\sum_{n\ge n_0}r^n=\dfrac{r^{n_0}}{1-r}$ («primer término entre uno menos la razón»)."""),
    ("ej", "El clásico de las dos series", r"""$\sum_{n\ge1}\left(\frac23\right)^n=\frac{2/3}{1-2/3}=2$. $\ \sum(-1)^n$ **oscila** ($S_n$ vale $-1,0,-1,0,\dots$)."""),
], "Estudio de una serie"),

S("positivos", "6.2 Series de términos positivos", "§6.2 (6.2.1–6.2.7)", [
    ("idea", "Si todo suma, sólo hay dos opciones", r"""Con $a_n\ge0$ las sumas parciales sólo crecen: o se estabilizan (converge) o se van a $+\infty$. **Nunca oscila.**
Converge ⇔ las sumas parciales están **acotadas** (Nota 6.2.2)."""),
    ("teo", "Comparación (6.2.4) y paso al límite (6.2.5)", r"""
- $0\le a_n\le b_n$: $\sum b_n$ converge ⇒ $\sum a_n$ converge; $\sum a_n$ diverge ⇒ $\sum b_n$ diverge.
- $\lim\frac{a_n}{b_n}=\ell$: si $0<\ell<\infty$, **mismo carácter**; si $\ell=0$ y $\sum b_n$ converge, converge; si $\ell=\infty$ y $\sum b_n$ diverge, diverge.
(¡Por eso las **equivalencias** sirven en series de términos positivos!)"""),
    ("teo", "Criterio integral (6.2.6)", r"""$f$ continua, positiva y **decreciente** en $[1,\infty)$: $\sum f(n)$ y $\int_1^\infty f$ tienen el **mismo carácter**.
(Los rectángulos de altura $f(n)$ quedan encajados entre áreas bajo la curva.)"""),
    ("teo", "Armónica generalizada (6.2.7)", r"""$$\sum\frac1{n^p}\ \text{converge}\iff p>1.$$ Es **la** serie de referencia para comparar. $p=1$: la armónica, diverge (muy despacio: $S_n\approx\ln n$)."""),
    ("truco", "Receta para términos positivos", r"""
1. ¿$a_n\to0$? Si no, diverge.
2. Busca la equivalencia de $a_n$ con $\frac{C}{n^p}$ (o con algo geométrico) y compara.
3. Si hay factoriales o potencias $n$-ésimas: **cociente** o **raíz**.
4. Si cociente/raíz dan 1: **Raabe** (o logarítmico, o Pringsheim)."""),
], "Estudio de una serie"),

S("criterios", "6.3 Cociente, raíz, condensación, Pringsheim, Raabe y logarítmicos", "§6.3 (6.3.1–6.3.11)", [
    ("teo", "Cociente de D'Alembert (6.3.1) y raíz (6.3.2)", r"""
$\lambda=\lim\frac{a_{n+1}}{a_n}$ o $\lambda=\limsup\sqrt[n]{a_n}$: **$\lambda<1$ converge, $\lambda>1$ diverge, $\lambda=1$ no decide.**
La raíz es más fuerte (si decide el cociente, decide la raíz, por 5.3.2). Comparan con una geométrica de razón $\lambda$."""),
    ("teo", "Condensación de Cauchy (6.3.3)", r"""$a_n$ **decreciente** hacia 0: $\sum a_n$ y $\sum2^ka_{2^k}$ tienen el mismo carácter. Ej.: $\sum\frac1{n\ln n}$ ↔ $\sum\frac1{k\ln2}$ ⇒ **diverge**."""),
    ("teo", "Pringsheim (6.3.4–6.3.5)", r"""$\lim n^\alpha a_n=\ell$: si $\alpha>1$ y $\ell<\infty$, converge; si $\alpha\le1$ y $\ell>0$, diverge. (Es comparar con $\frac1{n^\alpha}$.)"""),
    ("teo", "Raabe (6.3.6)", r"""$\lambda=\lim n\left(1-\frac{a_{n+1}}{a_n}\right)$: **$\lambda>1$ converge, $\lambda<1$ diverge.** Se usa cuando el cociente da 1. (Compara con $\frac1{n^\lambda}$.)"""),
    ("teo", "Criterios logarítmicos (6.3.8 y 6.3.10)", r"""
$\lim\frac{-\ln a_n}{\ln n}=\lambda$ o $\lim\frac{-\ln(na_n)}{\ln\ln n}=\lambda$: **$\lambda>1$ (o $\infty$) converge, $\lambda<1$ diverge.**
(Nota 6.3.11: el numerador es $\ln\frac1{a_n}$ o $\ln\frac1{na_n}$.) El segundo distingue series como $\sum\frac1{n(\ln n)^p}$ (converge ⇔ $p>1$)."""),
    ("resumen", "¿Qué criterio uso?", r"""
| Aspecto de $a_n$ | Criterio |
|---|---|
| cocientes de polinomios, raíces | comparación / equivalencia con $1/n^p$ |
| factoriales, $a^n$, productos | cociente |
| todo elevado a $n$ | raíz |
| el cociente da 1 | Raabe |
| logaritmos ($\ln n$, $\ln\ln n$) | condensación o logarítmicos |
| $f(n)$ con $f$ fácil de integrar | integral |"""),
], "Más criterios"),

S("absoluta", "6.4 Convergencia absoluta y reordenaciones", "§6.4 (6.4.1–6.4.7)", [
    ("idea", "Una deuda y un ahorro", r"""Con signos variados, unos términos compensan a otros. **Absolutamente convergente**: incluso sin compensaciones (todo en positivo) converge.
**Condicionalmente**: sólo converge gracias a que se cancelan. Esta segunda es frágil: si cambias el orden, cambia el resultado."""),
    ("def", "Absoluta y condicional (6.4.1–6.4.3)", r"""Absoluta si $\sum|a_n|$ converge. **Absoluta ⇒ convergente** (6.4.2) y $\left|\sum a_n\right|\le\sum|a_n|$. Condicional: converge pero $\sum|a_n|$ no."""),
    ("ej", "Ejemplo 6.4.4", r"""$\sum\frac{(-1)^{n+1}}n=\ln2$ converge (Leibniz) pero $\sum\frac1n$ diverge ⇒ **condicionalmente convergente**."""),
    ("teo", "Reordenaciones (6.4.6) y teorema de Riemann (6.4.7)", r"""
- Absolutamente convergente ⇒ **cualquier reordenación** converge a la misma suma.
- Condicionalmente convergente ⇒ para **cualquier** $\alpha\in[-\infty,\infty]$ hay una reordenación que suma $\alpha$ (y otras que oscilan).
Idea: los positivos suman $+\infty$ y los negativos $-\infty$; se toman positivos hasta pasar $\alpha$, negativos hasta bajar de $\alpha$, y así."""),
    ("ia", None, r"""En un ordenador la suma con decimales **no es asociativa**: sumar en otro orden da resultados distintos (redondeo). Por eso las librerías
numéricas usan sumas «compensadas» (Kahan) y los cálculos en GPU en paralelo pueden variar en las últimas cifras."""),
], "Reordenación de Riemann"),

S("alternadas", "6.5 Abel, Dirichlet y Leibniz", "§6.5 (6.5.1–6.5.5)", [
    ("teo", "Sumación de Abel (6.5.1)", r"""Con $A_n=a_1+\dots+a_n$: $\displaystyle\sum_{k=1}^na_kb_k=A_nb_{n+1}+\sum_{k=1}^nA_k(b_k-b_{k+1})$. Es la «integración por partes» de las sumas."""),
    ("teo", "Abel (6.5.2) y Dirichlet (6.5.3)", r"""
- **Abel**: $\sum a_n$ converge y $(b_n)$ monótona y **convergente** ⇒ $\sum a_nb_n$ converge.
- **Dirichlet**: sumas parciales de $\sum a_n$ **acotadas** y $(b_n)$ monótona **hacia 0** ⇒ $\sum a_nb_n$ converge.
Ej.: $\sum\frac{\operatorname{sen}(nx)}n$ converge para todo $x$ (sumas de $\operatorname{sen}(nx)$ acotadas si $x\notin2\pi\mathbb Z$)."""),
    ("teo", "Leibniz (6.5.5)", r"""Serie **alternada** con $|a_n|$ **decreciente** y $\to0$ ⇒ converge, y el error al cortar es menor que el primer término despreciado:
$|S-S_n|\le|a_{n+1}|$."""),
    ("ojo", "Las tres hipótesis de Leibniz", r"""Alternada, decreciente en valor absoluto y con límite 0. Sin el decrecimiento puede fallar:
$\frac1{\sqrt2-1}-\frac1{\sqrt2+1}+\frac1{\sqrt3-1}-\frac1{\sqrt3+1}+\cdots$ diverge (cada pareja vale $\frac2{n-1}$)."""),
], "Estudio de una serie"),

S("sumar", "6.6 Series que sabemos sumar", "§6.6 (6.6.1–6.6.3)", [
    ("teo", "Aritmético-geométricas (6.6.1)", r"""$\sum P(n)r^n$ con $P$ polinomio: converge ⇔ $|r|<1$. Para sumarla, $S-rS$ baja el grado del polinomio; repitiendo se llega a una geométrica.
Ej.: $\sum_{n\ge1}nr^n=\dfrac{r}{(1-r)^2}$."""),
    ("teo", "Telescópicas (6.6.2)", r"""Si $a_n=b_{n+1}-b_n$ entonces $S_n=b_{n+1}-b_1$: converge ⇔ $(b_n)$ converge, y $\sum a_n=\lim b_n-b_1$.
Ej.: $\sum\frac1{n(n+1)}=\sum\left(\frac1n-\frac1{n+1}\right)=1$ (fracciones simples, como en las integrales racionales)."""),
    ("teo", "Hipergeométricas (6.6.3)", r"""$\dfrac{a_{n+1}}{a_n}=\dfrac{\alpha n+\beta}{\alpha n+\gamma}$ con $\alpha>0$: converge ⇔ $\gamma>\alpha+\beta$, y entonces
$$\sum_{n\ge1}a_n=\frac{a_1\gamma}{\gamma-\alpha-\beta}.$$ (Sale de Raabe: $\lambda=\frac{\gamma-\beta}\alpha$.)"""),
    ("errata", r"Caso $\gamma=\alpha+\beta$ en la demostración (p. 177)", r"""El texto escribe primero $a_n=\frac{a_1}{n+\delta}$ al simplificar el producto telescópico, y en la línea siguiente lo corrige
a $a_n=a_1\frac{1+\delta}{n+\delta}$ (con $\delta=\beta/\alpha$). La correcta es la segunda: $\prod_{k=1}^{n-1}\frac{k+\delta}{k+1+\delta}=\frac{1+\delta}{n+\delta}$.
La conclusión no cambia: es como $\frac Cn$ y la serie **diverge**."""),
    ("ej", "Comprobación", r"""$a_1=1$, $\frac{a_{n+1}}{a_n}=\frac{n}{n+2}$ ($\alpha=1,\beta=0,\gamma=2$): $a_n=\frac2{n(n+1)}$, suma $=2$. La fórmula: $\frac{1\cdot2}{2-1-0}=2$ ✓."""),
], "Sumar series"),

S("producto", "6.7 Producto de Cauchy", "§6.7 (6.7.1–6.7.2)", [
    ("idea", "Multiplicar series como polinomios", r"""Al multiplicar $(a_0+a_1x+\dots)(b_0+b_1x+\dots)$, el coeficiente de $x^n$ junta todos los productos $a_kb_{n-k}$. Eso es el producto de Cauchy."""),
    ("def", "Definición 6.7.1", r"""$c_n=\sum_{k=0}^na_kb_{n-k}$, y $\sum c_n$ es el **producto de Cauchy** de $\sum a_n$ y $\sum b_n$."""),
    ("teo", "Mertens (6.7.2)", r"""Si $\sum a_n=A$ converge **absolutamente** y $\sum b_n=B$ converge, entonces $\sum c_n$ converge y vale $AB$.
(Si ambas son sólo condicionales puede fallar: $\sum\frac{(-1)^n}{\sqrt{n+1}}$ por sí misma da un producto con $|c_n|\not\to0$.)"""),
    ("ej", r"$e^x\cdot e^y=e^{x+y}$", r"""$\sum\frac{x^n}{n!}\cdot\sum\frac{y^n}{n!}$: $c_n=\sum_k\frac{x^ky^{n-k}}{k!(n-k)!}=\frac{(x+y)^n}{n!}$ por el binomio de Newton (tema 4 de Finita)."""),
], "Producto de Cauchy"),
])
