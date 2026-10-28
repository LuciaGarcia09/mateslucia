from ui.teoria import Tema, S

TEMA = Tema("a2", "Análisis", 2, "Límites y continuidad",
            "Definición ε–δ, laterales, propiedades, indeterminaciones, equivalencias, continuidad, Bolzano, Weierstrass y continuidad uniforme.", [

S("definicion", "2.1 Límite de una función en un punto", "§2.1 (Definiciones 2.1.1–2.1.3, Teoremas 2.1.7–2.1.8)", [
    ("idea", "El juego del ε y el δ", r"""
Tú me retas con una franja de anchura $\varepsilon$ alrededor de $L$ (por pequeña que sea). Yo gano si encuentro un $\delta$ tal que,
siempre que $x$ esté a menos de $\delta$ de $a$ (sin ser $a$), $f(x)$ cae dentro de tu franja. **$\lim_{x\to a}f(x)=L$ significa que
yo gano siempre.** Lo que pase justo en $a$ da igual: $f$ ni siquiera tiene que estar definida ahí."""),
    ("def", "Definición 2.1.1", r"""
$a$ punto de acumulación de $A$. $\displaystyle\lim_{x\to a}f(x)=L$ si
$$\forall\varepsilon>0\ \exists\delta>0:\ x\in(a-\delta,a+\delta)^*\cap A\ \Rightarrow\ |f(x)-L|<\varepsilon.$$
**Límite infinito** (2.1.2): $\forall m>0\ \exists\delta>0$: $f(x)>m$. **En el infinito** (2.1.3): se cambia «$x$ cerca de $a$» por «$x>K$»."""),
    ("teo", "Unicidad y acotación (2.1.4–2.1.5)", r"""El límite, si existe, es **único** (con $\varepsilon=|L_1-L_2|/3$ las franjas serían disjuntas) y si es finito $f$ está
**acotada** en un entorno reducido de $a$."""),
    ("teo", "Laterales (2.1.6–2.1.7)", r"""$\lim_{x\to a}f(x)=L\iff$ existen los dos laterales y valen $L$. Es sobre todo un **criterio negativo**: si los laterales
difieren o alguno no existe, no hay límite. (Y no hace falta calcular laterales cuando la función es igual a los dos lados.)"""),
    ("teo", "Criterio secuencial (2.1.8)", r"""$\lim_{x\to a}f(x)=L\iff$ para **toda** sucesión $x_n\to a$ ($x_n\neq a$) se tiene $f(x_n)\to L$.
Para ver que **no** hay límite basta encontrar dos sucesiones que den límites distintos: $\operatorname{sen}(1/x)$ con $x_n=\frac1{n\pi}$ y $y_n=\frac1{2n\pi+\pi/2}$."""),
], "ε–δ"),

S("propiedades", "2.2 Propiedades e indeterminaciones", "§2.2 (2.2.1–2.2.8)", [
    ("teo", "Álgebra de límites (2.2.1)", r"""Si $f\to\ell$ y $g\to m$ (finitos): $|f|\to|\ell|$, $f+g\to\ell+m$, $fg\to\ell m$, $f/g\to\ell/m$ si $m\neq0$,
$\log_u f\to\log_u\ell$ si $\ell>0$ y $f^g\to\ell^m$ si $\ell>0$."""),
    ("resumen", "Las 7 indeterminaciones (2.2.4)", r"""
$$\infty-\infty,\quad\frac\infty\infty,\quad0\cdot\infty,\quad\frac00,\quad\infty^0,\quad0^0,\quad1^\infty$$
En ellas el límite puede ser cualquier cosa: hay que **transformar** la expresión."""),
    ("teo", "Sándwich (2.2.5) y acotada por infinitésimo (2.2.8)", r"""
- Si $f\le g\le h$ cerca de $a$ y $f,h\to L$, entonces $g\to L$.
- Si $f$ está **acotada** y $g\to0$, entonces $fg\to0$. Ej. 2.2.6: $x\operatorname{sen}(1/x)\to0$ aunque $\operatorname{sen}(1/x)$ no tenga límite.
- Si $f$ acotada y $|g|\to\infty$, $f/g\to0$ (2.2.3)."""),
    ("truco", r"El caso $1^\infty$ (Ejemplo 2.4.6)", r"""Si $f\to1$ y $g\to\infty$: $\displaystyle\lim f^g=e^{\lim g\,(f-1)}$. Ej.: $\lim\left(1+\frac3x\right)^x=e^{\lim x\cdot3/x}=e^3$."""),
], "Límites"),

S("equivalencias", "2.3 Notación de Landau y equivalencias", "§2.3 (2.3.1–2.3.8)", [
    ("def", "O grande, o pequeña, equivalentes", r"""
- $f=O(g)$ en $a$: $|f|\le M|g|$ cerca de $a$ («$f$ no crece más que $g$»).
- $f=o(g)$ en $a$: $f/g\to0$ («$f$ es despreciable frente a $g$»).
- $f\equiv_a g$ (**equivalentes**): $\lim_{x\to a}f/g=1$."""),
    ("teo", "Cuándo se puede sustituir (2.3.4)", r"""Si $f\equiv g$, se puede cambiar $f$ por $g$ **en productos y cocientes**, pero **nunca en sumas o restas**."""),
    ("ojo", "El error que más se repite", r"""$\displaystyle\lim_{x\to0}\frac{x-\operatorname{sen}x}{x^3}$: si cambias $\operatorname{sen}x$ por $x$ sale $0/x^3=0$, **mal**. La resta no se puede
tocar; hay que usar la equivalencia de la diferencia entera, $x-\operatorname{sen}x\equiv x^3/6$, y el límite es $1/6$."""),
    ("ej", "Ejemplo 2.3.5", r"""$\displaystyle\lim_{x\to0}\frac{1-\cos2x}{\operatorname{sen}^2(x/2)}=\lim\frac{(2x)^2/2}{(x/2)^2}=\lim\frac{2x^2}{x^2/4}=8.$"""),
    ("teo", "Órdenes de infinitud (2.3.6)", r"""En $+\infty$: $(\log x)^\beta\ll x^m\ll c^x\ll x^{rx}$ (de menos a más rápido; $\ll$ significa cociente $\to0$).
Ej. 2.3.7: $x-\ln x\equiv x\to\infty$."""),
    ("resumen", "Tabla de equivalencias (2.3.8)", r"""
En $x\to0$: $\operatorname{sen}x\equiv\operatorname{tg}x\equiv\arcsin x\equiv\operatorname{arctg}x\equiv\ln(1+x)\equiv e^x-1\equiv x$;
$\ 1-\cos x\equiv\frac{x^2}2$; $\ a^x-1\equiv x\ln a$; $\ (1+x)^a-1\equiv ax$; $\ x-\operatorname{sen}x\equiv\frac{x^3}6$; $\ x-\operatorname{tg}x\equiv-\frac{x^3}3$;
$\ x-\ln(1+x)\equiv\frac{x^2}2$; $\ \ln\cos x\equiv-\frac{x^2}2$; $\ \ln\frac{\operatorname{sen}x}x\equiv-\frac{x^2}6$.
En $x\to1$: $\ln x\equiv x-1$, $\ x^a-1\equiv a(x-1)$. **Vale con cualquier $u(x)\to0$ en lugar de $x$.**"""),
], "Equivalencias"),

S("continuidad", "2.4 Continuidad", "§2.4 (2.4.1–2.4.12)", [
    ("idea", "Dibujar sin levantar el lápiz", r"""Continua en $a$ = «el valor que tiene coincide con el que anuncia»: $\lim_{x\to a}f(x)=f(a)$. Tres cosas: que exista $f(a)$,
que exista el límite y que coincidan."""),
    ("def", "Definición 2.4.1", r"""$f$ continua en $a\in A$: $\forall\varepsilon>0\ \exists\delta>0$: $|x-a|<\delta\Rightarrow|f(x)-f(a)|<\varepsilon$.
Si $a$ es de acumulación equivale a $\lim_{x\to a}f(x)=f(a)$; en un punto aislado siempre es continua. **El δ depende de ε y de a.**"""),
    ("teo", "Propiedades (2.4.2–2.4.4)", r"""
- Continua en $a$ ⇒ acotada cerca de $a$, y si $f(a)\neq0$ **conserva el signo** cerca de $a$.
- Sumas, productos, $|f|$, $\lambda f$ y cocientes (si $g(a)\neq0$) de continuas son continuas.
- **Composición**: $f$ continua en $a$ y $g$ en $f(a)$ ⇒ $g\circ f$ continua en $a$. Así $\lim e^{u(x)}=e^{\lim u(x)}$ (Ej. 2.4.5)."""),
    ("teo", "Bolzano (2.4.7)", r"""$f$ continua en $[a,b]$ y $f(a)f(b)<0$ ⇒ existe $c\in(a,b)$ con $f(c)=0$. (Si vas de un lado del río al otro sin saltar,
cruzas el río.) Sin continuidad falla: el escalón $-1/1$ (Ej. 2.4.9)."""),
    ("teo", "Darboux / valores intermedios (2.4.8)", r"""$f$ continua en $[a,b]$ toma **todos** los valores entre $f(a)$ y $f(b)$ (aplica Bolzano a $f-\lambda$)."""),
    ("teo", "Weierstrass (2.4.11)", r"""$f$ continua en un **cerrado y acotado** $[a,b]$ ⇒ alcanza **máximo y mínimo absolutos** (y está acotada). Falla si quitas
algo: $1/x$ en $(0,1]$ no está acotada; $f(x)=x$ con $f(0)=1$ en $[0,1]$ no alcanza el mínimo (Ej. 2.4.12)."""),
    ("truco", "Extremos absolutos en [a, b]", r"""Candidatos: **los extremos $a$ y $b$**, los **puntos críticos** ($f'=0$) y los puntos donde **$f$ no es derivable**. Evalúa $f$ en
todos y quédate con el mayor y el menor."""),
    ("ej", "Problemas 2.7, 2.12 y 2.13", r"""
- $60x^4+16x^3-167x^2-18x+45$ tiene 4 raíces en $[-2,2]$: busca 5 puntos con signos alternos y aplica Bolzano 4 veces.
- **Punto fijo**: $f:[0,1]\to[0,1]$ continua ⇒ existe $x$ con $f(x)=x$ (Bolzano a $g(x)=f(x)-x$: $g(0)\ge0\ge g(1)$).
- $f$ continua en $[0,2]$ con $f(0)=f(2)$ ⇒ hay $x,y$ con $|x-y|=1$ y $f(x)=f(y)$ (Bolzano a $g(x)=f(x+1)-f(x)$ en $[0,1]$)."""),
], "Funciones a trozos"),

S("uniforme", "2.5 Continuidad uniforme", "§2.5 (2.5.1–2.5.7)", [
    ("idea", "Un mismo δ para todo el mundo", r"""En la continuidad normal, cada punto tiene su propio δ. En la **uniforme**, un único δ sirve en **todos** los puntos a la vez.
$1/x$ en $(0,1)$ es continua, pero cerca de 0 se empina tanto que ningún δ fijo sirve: no es uniformemente continua."""),
    ("def", "Definición 2.5.1", r"""$\forall\varepsilon>0\ \exists\delta>0$: **para todos** $x,y\in A$, $|x-y|<\delta\Rightarrow|f(x)-f(y)|<\varepsilon$.
Es una propiedad de la función **en un conjunto**, no en un punto."""),
    ("teo", "Heine–Cantor (2.5.2)", r"""Continua en un intervalo **cerrado y acotado** $[a,b]$ ⇒ **uniformemente continua**."""),
    ("teo", "Criterio secuencial (2.5.4) y Lipschitz (2.5.5)", r"""
- **No** uniforme ⇔ hay $\varepsilon_0>0$ y $x_n,y_n$ con $|x_n-y_n|\to0$ pero $|f(x_n)-f(y_n)|\ge\varepsilon_0$. (1/x: $x_n=\frac1n$, $y_n=\frac1{n+1}$.)
- **Lipschitz**: $|f(x)-f(y)|\le L|x-y|$ ⇒ uniformemente continua ($\delta=\varepsilon/L$). Si $|f'|\le L$, $f$ es Lipschitz (valor medio).
- No al revés: $\sqrt x$ es uniformemente continua en $[0,1]$ pero no Lipschitz (pendiente infinita en 0)."""),
], "Continuidad uniforme"),
])
