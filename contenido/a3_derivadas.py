from ui.teoria import Tema, S

TEMA = Tema("a3", "Análisis", 3, "Derivabilidad",
            "Derivada y diferencial, reglas, Fermat y Rolle, valor medio, L'Hôpital, Taylor, convexidad y representación de funciones.", [

S("derivada", "3.1 La derivada", "§3.1 (Definiciones 3.1.1–3.1.15, Teoremas 3.1.5–3.1.17)", [
    ("idea", "El velocímetro", r"""
La derivada no dice dónde estás, sino **lo rápido que cambias en ese instante**. Geométricamente es la pendiente de la
**tangente**: el límite de las pendientes de las secantes cuando el segundo punto se acerca al primero."""),
    ("def", "Derivada (3.1.1) y laterales (3.1.2–3.1.3)", r"""
$$f'(a)=\lim_{x\to a}\frac{f(x)-f(a)}{x-a}=\lim_{h\to0}\frac{f(a+h)-f(a)}{h}.$$
Laterales $f'(a^-)$, $f'(a^+)$ con $h\to0^\mp$. **Existe $f'(a)$ ⇔ existen las laterales y coinciden.**"""),
    ("def", "Diferencial (3.1.4–3.1.5)", r"""$df(a)(dx)=f'(a)\,dx$ es la aplicación **lineal** que mejor aproxima $f(a+dx)-f(a)$: si $f'(a)\neq0$, son equivalentes cuando $dx\to0$."""),
    ("teo", "Derivable ⇒ continua (3.1.6)", r"""$f(x)=f(a)+(x-a)\frac{f(x)-f(a)}{x-a}\to f(a)+0\cdot f'(a)$. **El recíproco es falso**: $|x|$ es continua en 0 y no derivable
(laterales $-1$ y $1$). Si existen las derivadas laterales, aunque distintas, $f$ es continua (3.1.7)."""),
    ("teo", "Reglas (3.1.8–3.1.11)", r"""
$(f+g)'=f'+g'$, $\ (\lambda f)'=\lambda f'$, $\ (fg)'=f'g+fg'$, $\ \left(\frac fg\right)'=\frac{f'g-fg'}{g^2}$,
**cadena** $(g\circ f)'(a)=g'(f(a))\,f'(a)$, **inversa** $(f^{-1})'(f(a))=\frac1{f'(a)}$ si $f'(a)\neq0$."""),
    ("ojo", "Observación 3.1.12", r"""$f(x)=x^3$ es biyectiva y derivable, pero $f'(0)=0$ y su inversa $\sqrt[3]{y}$ **no es derivable en 0** (pendiente vertical). La hipótesis $f'(a)\neq0$ es imprescindible."""),
    ("ojo", "Observación 3.1.16: derivada lateral vs límite de la derivada", r"""
$\lim_{x\to a^+}f'(x)$ **no** es siempre $f'(a^+)$. Sí lo es si **$f$ es continua en $a$** (y derivable a cada lado): entonces las laterales existen y
coinciden con esos límites. Por eso en las funciones a trozos **primero se comprueba la continuidad**."""),
    ("teo", "Leibniz (3.1.17) y derivación implícita (3.1.18)", r"""
$(fg)^{(n)}=\sum_{k=0}^n\binom nk f^{(k)}g^{(n-k)}$ (como el binomio).
Implícita: si $h(x,y)=0$ define $y(x)$, derivo los dos miembros respecto de $x$ con la regla de la cadena y despejo $y'$.
Ej.: $y^3+y^2-5y-x^2+4=0\Rightarrow y'=\dfrac{2x}{3y^2+2y-5}$."""),
    ("resumen", "Tabla de derivadas", r"""
$(x^r)'=rx^{r-1}$, $\ (e^u)'=u'e^u$, $\ (a^u)'=u'a^u\ln a$, $\ (\ln u)'=\frac{u'}u$, $\ (\log_b u)'=\frac{u'}{u\ln b}$,
$(\operatorname{sen}u)'=u'\cos u$, $\ (\cos u)'=-u'\operatorname{sen}u$, $\ (\operatorname{tg}u)'=u'(1+\operatorname{tg}^2u)$,
$(\arcsin u)'=\frac{u'}{\sqrt{1-u^2}}$, $\ (\operatorname{arctg}u)'=\frac{u'}{1+u^2}$."""),
], "Derivadas"),

S("extremos", "3.2 Extremos, Fermat y Rolle", "§3.2 (3.2.1–3.2.7)", [
    ("def", "Extremos relativos y absolutos (3.2.1)", r"""$a$ es **máximo relativo** si $f(a)\ge f(x)$ en un entorno de $a$; **absoluto** si lo es en todo el dominio. Igual para mínimos."""),
    ("teo", "Fermat (3.2.2)", r"""Si $f$ tiene un extremo relativo en un punto **interior** $c$ y es **derivable** en $c$, entonces $f'(c)=0$.
(A la derecha los cocientes son $\le0$, a la izquierda $\ge0$; si existe el límite, es 0.)"""),
    ("ojo", "Fermat no es un «si y sólo si»", r"""Puede haber extremo sin derivada ($|x|$ en 0) y derivada nula sin extremo ($x^3$ en 0). Los puntos con $f'=0$ son sólo **candidatos**."""),
    ("teo", "Rolle (3.2.4)", r"""$f$ continua en $[a,b]$, derivable en $(a,b)$ y $f(a)=f(b)$ ⇒ existe $c\in(a,b)$ con $f'(c)=0$.
(Si subes y vuelves a la misma altura, en algún momento ibas en horizontal.) Las hipótesis no se pueden quitar: $|x|$ en $[-1,1]$; $1/x$ con $f(0)=1$."""),
    ("teo", "Condición suficiente con derivadas sucesivas (3.2.6)", r"""
Si $f'(c)=\dots=f^{(n-1)}(c)=0$ y $f^{(n)}(c)\neq0$: **$n$ par** y $f^{(n)}(c)>0$ ⇒ mínimo; $n$ par y $<0$ ⇒ máximo; **$n$ impar** ⇒ no hay extremo.
(Con $n=2$ es el criterio de la segunda derivada.)"""),
], "Extremos"),

S("valor_medio", "3.3 Teoremas del valor medio y L'Hôpital", "§3.3 (3.3.1–3.3.11)", [
    ("idea", "Si haces 100 km en una hora…", r"""…en algún instante el velocímetro marcó exactamente 100 km/h. Eso es el **valor medio**: la velocidad instantánea coincide en
algún momento con la media. Geométricamente: hay un punto donde la tangente es **paralela a la cuerda**."""),
    ("teo", "Lagrange (3.3.1)", r"""$f$ continua en $[a,b]$ y derivable en $(a,b)$ ⇒ existe $c\in(a,b)$ con $f'(c)=\dfrac{f(b)-f(a)}{b-a}$.
(Se prueba aplicando Rolle a $f$ menos la recta de la cuerda.)"""),
    ("teo", "Consecuencias (3.3.2–3.3.5)", r"""
- $f'>0$ en $(a,b)$ ⇒ estrictamente creciente; $f'<0$ ⇒ estrictamente decreciente; con $\ge$ / $\le$, en sentido amplio.
- $f'=0$ en un **intervalo** ⇒ $f$ constante; $f'=g'$ ⇒ $f-g$ constante. ¡En un intervalo! (Obs. 3.3.5: en $(-\infty,0)\cup(0,\infty)$ falla.)"""),
    ("teo", "Cauchy (3.3.6) y Darboux para derivadas (3.3.7–3.3.9)", r"""
- Existe $c$ con $f'(c)(g(b)-g(a))=g'(c)(f(b)-f(a))$.
- Las derivadas tienen la propiedad del **valor intermedio** aunque no sean continuas ⇒ **una derivada nunca tiene discontinuidades de salto**."""),
    ("teo", "L'Hôpital (3.3.10)", r"""Si $\frac{f}{g}$ da $\frac00$ o $\frac\infty\infty$ y **existe** $\lim\frac{f'}{g'}=\ell$ (finito o infinito), entonces $\lim\frac fg=\ell$.
Vale para $a$ finito, infinito y laterales."""),
    ("ojo", "Nota 3.3.11", r"""Es condición **suficiente, no necesaria**: $\lim_{x\to\infty}\frac{x+\operatorname{sen}x}{x}=1$ pero $\frac{1+\cos x}{1}$ no tiene límite.
Y se derivan numerador y denominador **por separado** (no es la regla del cociente). Antes de usarla, mira si una equivalencia es más rápida."""),
], "Rolle y valor medio"),

S("taylor", "3.4 Fórmula de Taylor", "§3.4 (3.4.1–3.4.5)", [
    ("idea", "Imitar a una función con un polinomio", r"""Un imitador copia primero la posición $f(a)$, luego la velocidad $f'(a)$, luego la aceleración $f''(a)$… Cuantas más cosas copia,
mejor se parece **cerca de $a$**. Taylor es una aproximación **local**."""),
    ("teo", "Polinomio de Taylor (3.4.1–3.4.2)", r"""
Existe un **único** polinomio de grado $\le n$ con las mismas derivadas que $f$ en $a$ hasta orden $n$:
$$T_n(f,a)(x)=\sum_{k=0}^n\frac{f^{(k)}(a)}{k!}(x-a)^k\qquad(\text{Maclaurin si }a=0).$$"""),
    ("teo", "Resto (3.4.3–3.4.5)", r"""
$R_n=f-T_n=o((x-a)^n)$ (Peano). Con más regularidad hay $\xi$ entre $a$ y $x$ con
$$R_n(x)=\frac{f^{(n+1)}(\xi)}{(n+1)!}(x-a)^{n+1}\ \ (\text{Lagrange}),\qquad R_n(x)=\frac{f^{(n+1)}(\eta)}{n!}(x-a)(x-\eta)^n\ \ (\text{Cauchy}).$$
**Cota del error**: si $|f^{(n+1)}|\le M$ entre $a$ y $x$, $\ |R_n(x)|\le\dfrac{M|x-a|^{n+1}}{(n+1)!}$."""),
    ("ej", "El ejemplo de los apuntes", r"""$\operatorname{sen}0{,}1\approx0{,}1-\frac{0{,}1^3}{3!}+\frac{0{,}1^5}{5!}-\frac{0{,}1^7}{7!}$ con error $<\frac{0{,}1^8}{8!}\approx2{,}48\cdot10^{-13}$
(cota $M=1$ porque $|\operatorname{sen}|,|\cos|\le1$)."""),
    ("resumen", "Desarrollos que hay que saber", r"""
$e^x=\sum\frac{x^k}{k!}$, $\ \operatorname{sen}x=x-\frac{x^3}{3!}+\frac{x^5}{5!}-\cdots$, $\ \cos x=1-\frac{x^2}{2!}+\frac{x^4}{4!}-\cdots$,
$\ \ln(1+x)=x-\frac{x^2}2+\frac{x^3}3-\cdots$, $\ \frac1{1-x}=1+x+x^2+\cdots$, $\ (1+x)^a=1+ax+\binom a2x^2+\cdots$"""),
    ("ia", None, r"""Las calculadoras evalúan $e^x$, $\operatorname{sen}x$ o $\ln x$ con polinomios así. Y la aproximación de **orden 2** (gradiente + hessiana) es la idea
de los métodos de optimización de segundo orden que se usan para entrenar modelos."""),
], "Taylor"),

S("convexidad", "3.5 Concavidad, convexidad e inflexión", "§3.5 (3.5.1–3.5.9)", [
    ("idea", "Sonrisa o ceño", r"""**Convexa** ∪ (sonrisa): la cuerda entre dos puntos queda **por encima** de la gráfica y la gráfica **por encima** de sus tangentes.
**Cóncava** ∩ (ceño): al revés. Es el convenio de tus apuntes."""),
    ("def", "Definición 3.5.1 y Nota 3.5.2", r"""$f$ convexa en $I$ si $f(\lambda x+(1-\lambda)y)\le\lambda f(x)+(1-\lambda)f(y)$ para $\lambda\in[0,1]$. Equivale a que las pendientes
de las secantes **crezcan**: $\frac{f(x)-f(a)}{x-a}\le\frac{f(b)-f(a)}{b-a}\le\frac{f(b)-f(x)}{b-x}$ para $a<x<b$."""),
    ("teo", "Con derivadas (3.5.6–3.5.7)", r"""Si $f$ es derivable: convexa ⇔ $f'$ creciente. Si existe $f''$: $f''\ge0$ ⇒ convexa, $\ f''\le0$ ⇒ cóncava."""),
    ("def", "Punto de inflexión (3.5.8)", r"""$x_0\in D(f)$ donde $f$ **cambia** de cóncava a convexa o al revés. ($f''(x_0)=0$ es sólo candidato: $x^4$ tiene $f''(0)=0$ y no es inflexión.)"""),
    ("teo", "Teorema 3.5.9", r"""Si $f'(x_0)=\dots=f^{(n-1)}(x_0)=0\neq f^{(n)}(x_0)$: $n$ par ⇒ extremo (mín si $>0$, máx si $<0$); $n$ impar ⇒ no es extremo y,
si $f^{(n)}$ es continua en $x_0$, es punto de inflexión."""),
    ("errata", "Teorema 3.5.9 (iii)", r"""La parte de la inflexión necesita $n\ge3$: con $n=1$ ($f'(x_0)\neq0$) la prueba usa $(x-x_0)^{n-2}$ con exponente $-1$ y la conclusión
falla ($f(x)=x$ no tiene inflexión en 0). Además, para la inflexión basta $f''(x_0)=\dots=f^{(n-1)}(x_0)=0\neq f^{(n)}(x_0)$ con $n$ impar $\ge3$;
no hace falta que $f'(x_0)=0$."""),
    ("resumen", "Representación de una función (3.5.10)", r"""
1. Dominio. 2. Cortes con los ejes. 3. Periodicidad. 4. Simetrías (par $f(-x)=f(x)$, impar $f(-x)=-f(x)$).
5. Asíntotas: **horizontal** si $\lim_{x\to\pm\infty}f$ es finito; **vertical** en $a$ si algún lateral es infinito; **oblicua** $y=mx+n$ con
$m=\lim\frac{f(x)}x\neq0$ y $n=\lim(f(x)-mx)$.
6. Crecimiento y extremos (signo de $f'$). 7. Concavidad e inflexión (signo de $f''$). La pestaña **Estudio completo** lo hace todo."""),
], "Estudio completo"),
])
