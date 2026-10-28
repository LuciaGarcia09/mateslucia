from ui.teoria import Tema, S

TEMA = Tema("a1", "Análisis", 1, "Conjuntos de números: ℝ, ℝⁿ y ℂ",
            "Axiomas de ℝ, valor absoluto, supremo, inducción, topología de ℝ, el espacio ℝⁿ, números complejos y aplicaciones.", [

S("reales", "1.1 Los números reales", "§1.1 (Teoremas 1.1.1–1.1.12)", [
    ("idea", "ℝ es la recta sin agujeros", r"""
Los racionales están por todas partes en la recta, pero dejan **agujeros**: $\sqrt2$, $\pi$… ℝ es lo que sale al **rellenar esos agujeros**.
Formalmente: ℝ es el **único cuerpo ordenado que cumple el axioma del supremo** (Teorema 1.1.12)."""),
    ("def", "Cuerpo totalmente ordenado (1.1.1 y 1.1.3)", r"""
- **Cuerpo**: $(\mathbb R,+)$ y $(\mathbb R\setminus\{0\},\cdot)$ son grupos abelianos (asociativa, conmutativa, neutro, opuesto/inverso) y hay distributiva.
- **Orden total**: reflexivo, antisimétrico, transitivo y dos números siempre se comparan.
- **Compatible**: $x\le y\Rightarrow x+z\le y+z$; $\ x\le y,\ z>0\Rightarrow xz\le yz$ (si $z<0$ **se invierte**).
- **Arquimediana**: si $0<x\le y$, existe $n\in\mathbb N$ con $nx>y$ («con pasos pequeños llego tan lejos como quiera»)."""),
    ("def", "Valor absoluto y distancia (1.1.5–1.1.9)", r"""
$|x|=x$ si $x\ge0$ y $-x$ si $x<0$. Propiedades clave: $|xy|=|x||y|$; $\ |x|\le y\iff -y\le x\le y$;
**desigualdad triangular** $|x+y|\le|x|+|y|$ y la **inversa** $\big||x|-|y|\big|\le|x-y|$. La distancia es $d(x,y)=|y-x|$."""),
    ("ojo", r"Observación 1.1.7: $\sqrt{x^2}=|x|$", r"""$\sqrt{x^2}$ **no** es $x$ ni «$\pm x$»: el símbolo $\sqrt{\ }$ es la raíz **positiva**. Si $x=-3$, $\sqrt{9}=3=|-3|$."""),
    ("def", "Cotas, supremo e ínfimo (1.1.10–1.1.11)", r"""
$E$ está **acotado superiormente** si hay $x$ con $y\le x$ para todo $y\in E$. El **supremo** es la **menor** cota superior; el **ínfimo**,
la mayor cota inferior. **Axioma del supremo**: todo $E\neq\varnothing$ acotado superiormente tiene supremo en ℝ. (En ℚ falla:
$\{q: q^2<2\}$ no tiene supremo racional.)"""),
    ("truco", "Cómo demostrar que s = sup E", r"""
1. $s$ es cota superior: $y\le s$ para todo $y\in E$.
2. Nada menor lo es: para todo $\varepsilon>0$ hay $y\in E$ con $y>s-\varepsilon$."""),
    ("ej", "Desigualdades (problema 1.2)", r"""$|x^2-4x+1|<2\iff -2<x^2-4x+1<2\iff\big(x^2-4x+3>0\big)\wedge\big(x^2-4x-1<0\big)$ ⇒
$x\in(2-\sqrt5,1)\cup(3,2+\sqrt5)$. Resuélvelas en la pestaña **Desigualdades**."""),
], "Desigualdades y valor absoluto"),

S("induccion", "1.2 El principio de inducción", "§1.1.13 (Teoremas 1.1.14–1.1.16)", [
    ("def", "Tres versiones", r"""
- **Simple**: $P(1)$ y $[P(k)\Rightarrow P(k+1)]$ ⇒ $P(n)$ para todo $n$ (en Análisis $\mathbb N$ empieza en 1).
- **Desde $n_0$**: lo mismo empezando en $n_0$.
- **Fuerte**: si $P(m)$ para todos los $n_0\le m\le k$ implica $P(k+1)$. Sirve cuando cada caso depende de **varios** anteriores."""),
    ("ej", "Ejemplos 1.1.17–1.1.19", r"""
- $1+\dots+n=\frac{n(n+1)}2$.
- $x_1=1$, $x_2=2$, $x_{n+2}=\frac{x_{n+1}+x_n}2$ ⇒ $1\le x_n\le2$ (inducción **fuerte**: usa los dos anteriores).
- **Bernoulli**: $(1+p)^n\ge1+np$ si $p>-1$. En probabilidad: $P(\text{alguno de } n \text{ sucesos})=1-(1-p)^n\le np$."""),
], "Inducción (tema 2 de Finita)"),

S("topologia", "1.3 Intervalos y topología de ℝ", "§1.2.1–1.2.3", [
    ("idea", "Interior, frontera, acumulación con una lupa", r"""
Coge una lupa (un intervalo pequeñito $(a-\delta,a+\delta)$) y ponla sobre el punto $a$:
- si **todo** lo que ves es del conjunto → $a$ es **interior**;
- si **nada** es del conjunto → **exterior**;
- si ves de las dos cosas por pequeña que sea la lupa → **frontera**;
- si siempre ves puntos del conjunto **distintos de $a$** → **acumulación**."""),
    ("def", "Definiciones 1.2.2", r"""
- **Abierto**: todos sus puntos son interiores. **Cerrado**: contiene todos sus puntos de acumulación.
- **Entorno reducido** $(a-\delta,a+\delta)^*$: el entorno sin el propio $a$ (aparece en la definición de límite).
- **Compacto** en ℝ ⇔ **cerrado y acotado** (Heine–Borel, 1.2.3) ⇔ toda sucesión tiene una subsucesión convergente dentro ⇔ todo
  subconjunto infinito tiene un punto de acumulación dentro."""),
    ("ej", r"$A=[0,1)\cup\{2\}$", r"""Interior $(0,1)$; frontera $\{0,1,2\}$; acumulación $[0,1]$; el 2 es **aislado** (está en $A$ pero no es de acumulación);
$A$ no es abierto ni cerrado; $\sup A=\max A=2$, $\inf A=\min A=0$."""),
    ("ojo", "Abierto y cerrado no son contrarios", r"""$[0,1)$ no es ninguna de las dos cosas; $\mathbb R$ y $\varnothing$ son las dos a la vez."""),
], "Supremo, ínfimo y topología"),

S("rn", "1.4 El espacio euclídeo ℝⁿ", "§1.2.4–1.2.11", [
    ("def", "Vectores, combinaciones y bases (1.2.5–1.2.9)", r"""
- Suma y producto por escalar componente a componente ⇒ $\mathbb R^n$ es **espacio vectorial**.
- **Linealmente independientes**: $\lambda_1v_1+\dots+\lambda_kv_k=0\Rightarrow$ todos los $\lambda_i=0$.
- **Sistema generador**: todo vector es combinación de ellos. **Base** = independientes + generadores (en $\mathbb R^n$, exactamente $n$).
- **Coordenadas** en una base: los únicos $\alpha_i$ con $v=\sum\alpha_iv_i$. Ej. 1.2.9: $(1,3)=2(1,1)-(1,-1)$ ⇒ $(2,-1)_B$."""),
    ("def", "Producto escalar, norma, distancia (1.2.10)", r"""
$x\cdot y=x_1y_1+\dots+x_ny_n$, $\quad\|x\|=\sqrt{x\cdot x}$, $\quad d(x,y)=\|x-y\|$. Bolas $B(a,\delta)=\{x: d(x,a)<\delta\}$ generalizan
los intervalos, y con ellas se definen interior, frontera, acumulación, abierto y cerrado igual que en ℝ."""),
    ("teo", "Cauchy–Schwarz", r"""$|x\cdot y|\le\|x\|\,\|y\|$ (por eso $\cos\theta=\frac{x\cdot y}{\|x\|\|y\|}$ está entre −1 y 1). Ortogonales ⇔ $x\cdot y=0$."""),
    ("ojo", "ℝⁿ no es un cuerpo ordenado", r"""Para $n\ge2$ no hay producto de vectores que sea operación interna ni un orden compatible: no tiene sentido decir que un vector «es menor» que otro."""),
    ("ia", None, r"""Un dato con $n$ variables es un vector de $\mathbb R^n$. La **distancia euclídea** es la de k-vecinos y k-medias, y el producto escalar
normalizado es la **similitud coseno** de los buscadores y los *embeddings* de los modelos de lenguaje."""),
], "Vectores de ℝⁿ"),

S("complejos", "1.5 El cuerpo de los números complejos", "§1.3 (Proposición 1.3.1 – Teorema 1.3.9)", [
    ("idea", "Un complejo es una flecha en el plano", r"""
$z=x+iy$ es el punto $(x,y)$. **Sumar** = sumar flechas. **Multiplicar** = multiplicar las longitudes y **sumar los ángulos**.
Multiplicar por $i$ es **girar 90°**: por eso $i\cdot i=-1$ (dos giros de 90° = media vuelta)."""),
    ("def", "Construcción (1.3.1–1.3.4)", r"""
En $\mathbb R^2$: $(a_1,b_1)+(a_2,b_2)=(a_1+a_2,b_1+b_2)$ y $(a_1,b_1)(a_2,b_2)=(a_1a_2-b_1b_2,\ a_1b_2+b_1a_2)$. Es un **cuerpo**;
el inverso de $(a,b)\neq0$ es $\left(\frac a{a^2+b^2},\frac{-b}{a^2+b^2}\right)$. Con $i=(0,1)$: $i^2=-1$ y $z=x+iy$ (forma binómica).
$\operatorname{Re}z=x$, $\operatorname{Im}z=y$, conjugado $\bar z=x-iy$, módulo $|z|=\sqrt{x^2+y^2}$."""),
    ("teo", "Propiedades (1.3.8)", r"""
$\overline{z+w}=\bar z+\bar w$, $\overline{zw}=\bar z\,\bar w$, $\ z\bar z=|z|^2$, $\ \frac1z=\frac{\bar z}{|z|^2}$, $\ |zw|=|z||w|$,
$\operatorname{Re}z=\frac{z+\bar z}2$, $\operatorname{Im}z=\frac{z-\bar z}{2i}$, $\ |z+w|\le|z|+|w|$."""),
    ("teo", "Teorema Fundamental del Álgebra (1.3.9)", r"""
Todo polinomio complejo de grado $n\ge1$ tiene **exactamente $n$ raíces** contando multiplicidades: $Q(z)=C(z-r_1)^{m_1}\cdots(z-r_k)^{m_k}$.
(Por eso en $\mathbb C$ los únicos irreducibles son los de grado 1, y de aquí sale la descomposición en fracciones simples.)"""),
    ("ojo", "ℂ no se puede ordenar (1.3.10 ii)", r"""Si hubiera un orden compatible, todo cuadrado no nulo sería positivo: $1=1^2\succ0$ ⇒ $-1\prec0$, pero $-1=i^2\succ0$. Contradicción."""),
], "Complejos"),

S("polar", "1.6 Forma polar, De Moivre y raíces", "§1.4 (1.4.1–1.4.10)", [
    ("def", "Argumento y forma polar", r"""
$\theta$ es un **argumento** de $z\neq0$ si $\frac{z}{|z|}=\cos\theta+i\operatorname{sen}\theta$. Hay infinitos: $\arg z=\theta_0+2\pi\mathbb Z$.
El **principal** $\operatorname{Arg}z\in(-\pi,\pi]$. **Forma polar**: $z=|z|e^{i\theta}=|z|(\cos\theta+i\operatorname{sen}\theta)$, con
$e^{i(\theta+\varphi)}=e^{i\theta}e^{i\varphi}$. Así $\arg(zw)=\arg z+\arg w$, $\arg\bar z=-\arg z$."""),
    ("teo", "De Moivre (1.4.8)", r"""$z=\rho e^{i\theta}\Rightarrow z^n=\rho^ne^{in\theta}$, es decir $(\cos\theta+i\operatorname{sen}\theta)^n=\cos n\theta+i\operatorname{sen}n\theta$.
Sirve para calcular potencias y para expresar $\operatorname{sen}5\theta$, $\cos5\theta$ en función de $\operatorname{sen}\theta$, $\cos\theta$ (problema 1.12)."""),
    ("teo", "Raíces n-ésimas (1.4.9)", r"""
Todo $z\neq0$ tiene exactamente $n$ raíces $n$-ésimas:"""),
    ("latex", None, r"w_k=\sqrt[n]{|z|}\;\exp\!\left(i\,\frac{\theta+2\pi(k-1)}{n}\right),\qquad k=1,\dots,n"),
    ("idea", "Geometría (1.4.10)", r"""Las $n$ raíces son los **vértices de un polígono regular** de $n$ lados inscrito en la circunferencia de radio $\sqrt[n]{|z|}$.
El conjugado es la reflexión en el eje OX y $|z-w|$ la distancia entre dos puntos."""),
    ("ej", "Problema 1.10", r"""Raíces cuartas de $-9i$: $|{-9i}|=9$, $\operatorname{Arg}=-\pi/2$ ⇒ $w_k=\sqrt3\,e^{i(-\pi/2+2\pi(k-1))/4}$, $k=1,\dots,4$."""),
], "Complejos"),

S("funciones", "1.7 Aplicaciones y funciones", "§1.5 (1.5.1–1.5.9)", [
    ("def", "Lo esencial", r"""
- **Grafo** $\{(x,f(x))\}$, **imagen** $f(X)$, **contraimagen** $f^{-1}(Y')$ (no exige inversa), **restricción** $f|_{X'}$.
- Cuando $f$ se da con una fórmula, su **dominio** $D(f)$ son los $x$ donde tiene sentido: $D(1/x)=\mathbb R\setminus\{0\}$.
- Composición $(g\circ f)(x)=g(f(x))$ (asociativa); inyectiva, sobreyectiva, biyectiva e inversa como en el tema 2 de Finita."""),
    ("def", "Operaciones y orden con funciones reales (1.5.7–1.5.9)", r"""
$f+g$, $fg$, $\lambda f$ en el mismo dominio y $f/g$ donde $g\neq0$. $f\le g$ si $f(x)\le g(x)$ en todo punto (orden **no total**).
Acotada, creciente ($x<x'\Rightarrow f(x)\le f(x')$), estrictamente creciente ($<$), decreciente…"""),
], "Funciones"),
])
