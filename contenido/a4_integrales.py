from ui.teoria import Tema, S

TEMA = Tema("a4", "Análisis", 4, "Integral de Riemann",
            "Sumas de Riemann y Darboux, propiedades, Teoremas Fundamentales, técnicas de integración, aplicaciones e integrales impropias.", [

S("riemann", "4.1 La integral de Riemann", "§4.1 (Definiciones 4.1.1–4.1.10)", [
    ("idea", "Medir un terreno con tiras", r"""Para el área bajo una curva, corta el terreno en tiras finas y suma rectángulos. Si usas en cada tira la altura **máxima** te pasas
(suma superior); con la **mínima** te quedas corto (suma inferior). La función es integrable si, afinando las tiras, las dos se juntan."""),
    ("def", "Partición, sumas superior e inferior (4.1.1–4.1.3)", r"""
Partición $P=\{a=x_0<x_1<\dots<x_n=b\}$, diámetro $\Delta_P=\max\Delta x_i$. Con $M_i=\sup$ y $m_i=\inf$ de $f$ en $[x_{i-1},x_i]$:
$$U(P,f)=\sum M_i\Delta x_i,\qquad L(P,f)=\sum m_i\Delta x_i.$$
Si $Q$ es **más fina** que $P$: $L(P,f)\le L(Q,f)\le U(Q,f)\le U(P,f)$."""),
    ("def", "Integrable (4.1.5–4.1.8)", r"""
$f$ acotada es **integrable Riemann** si $\sup_P L(P,f)=\inf_P U(P,f)$; ese número es $\int_a^bf$. Equivale a: $\forall\varepsilon\ \exists\delta$,
$\Delta_P<\delta\Rightarrow U-L<\varepsilon$; y a que las **sumas de Riemann** $\sum f(c_i)\Delta x_i$ tengan límite cuando $\Delta_P\to0$
(sea cual sea la elección de $c_i$)."""),
    ("teo", "Propiedades (4.1.9)", r"""
- **Lineal**, **monótona** ($f\le g\Rightarrow\int f\le\int g$), **aditiva** en el intervalo ($\int_a^b=\int_a^c+\int_c^b$).
- Son integrables: las **monótonas** acotadas, las **continuas salvo en un número finito de puntos** (y acotadas), $g\circ f$ con $g$ continua.
- $|f|$ integrable y $\left|\int f\right|\le\int|f|$ (el recíproco falla). Producto integrable.
- **Cauchy–Schwarz** $\left(\int fg\right)^2\le\int f^2\int g^2$; Hölder y Minkowski (generalizaciones con $p$)."""),
    ("def", "Valor medio integral (4.1.10)", r"""$\mu=\frac1{b-a}\int_a^bf$; si $f$ es continua existe $c$ con $\int_a^bf=f(c)(b-a)$ (el rectángulo de altura media tiene la misma área)."""),
], "Riemann y Darboux"),

S("tfc", "4.2 Teoremas Fundamentales y regla de Barrow", "§4.1 (Teoremas 4.1.11–4.1.15)", [
    ("idea", "Integrar y derivar son operaciones inversas", r"""Si $F(x)$ es «el área acumulada desde $a$ hasta $x$», al mover $x$ un poquito el área crece en un rectángulo de altura $f(x)$:
por eso $F'(x)=f(x)$."""),
    ("teo", "Primer Teorema Fundamental (4.1.11)", r"""$F(x)=\int_a^xf(t)\,dt$ es **continua** (de hecho Lipschitz: $|F(x)-F(x_0)|\le M|x-x_0|$), y si $f$ es continua en $x$, $F'(x)=f(x)$."""),
    ("teo", "Límites variables (Corolario 4.1.12)", r"""$$\frac{d}{dx}\int_{h(x)}^{g(x)}f(t)\,dt=f(g(x))\,g'(x)-f(h(x))\,h'(x).$$
Ej. (problema 4.3): $\frac{d}{dx}\int_{x^2}^{x^3}\operatorname{sen}^3t\,dt=3x^2\operatorname{sen}^3(x^3)-2x\operatorname{sen}^3(x^2)$."""),
    ("teo", "Barrow (4.1.14–4.1.15)", r"""$f$ continua en $[a,b]$ y $G$ una **primitiva** ($G'=f$) ⇒ $\int_a^bf=G(b)-G(a)$. (Dos primitivas se diferencian en una constante.)"""),
    ("resumen", "Integrales inmediatas", r"""
$\int(x-a)^mdx=\frac{(x-a)^{m+1}}{m+1}$ ($m\neq-1$), $\ \int\frac{dx}{x-a}=\ln|x-a|$, $\ \int e^{ax}dx=\frac{e^{ax}}a$, $\ \int a^{bx}dx=\frac{a^{bx}}{b\ln a}$,
$\int\cos(ax)dx=\frac{\operatorname{sen}(ax)}a$, $\ \int\operatorname{sen}(ax)dx=-\frac{\cos(ax)}a$, $\ \int\operatorname{tg}(ax)dx=-\frac{\ln|\cos ax|}a$,
$\int\frac{dx}{\cos^2ax}=\frac{\operatorname{tg}ax}a$, $\ \int\frac{dx}{x^2-a^2}=\frac1{2a}\ln\left|\frac{x-a}{x+a}\right|$, $\ \int\frac{dx}{\sqrt{x^2\pm a}}=\ln\left|x+\sqrt{x^2\pm a}\right|$,
$\int\frac{dx}{\sqrt{a^2-x^2}}=\arcsin\frac x{|a|}$, $\ \int\frac{dx}{a^2+x^2}=\frac1{|a|}\operatorname{arctg}\frac x{|a|}$, $\ \int\frac{f'}{f}=\ln|f|$."""),
], "TFC"),

S("tecnicas", "4.3 Técnicas de integración", "§4.2 (4.2.1–4.2.6)", [
    ("teo", "Cambio de variable (4.2.1) y partes (4.2.2)", r"""
- **Cambio** $x=\varphi(t)$, $dx=\varphi'(t)dt$: $\int f(x)dx=\int f(\varphi(t))\varphi'(t)dt$, y al final se deshace el cambio.
- **Partes**: $\int u\,dv=uv-\int v\,du$."""),
    ("truco", "¿Quién es u en partes? (4.2.3)", r"""
- $P(x)e^{ax}$, $P(x)\operatorname{sen}(ax)$, $P(x)\cos(ax)$: $u=P(x)$ (el polinomio baja de grado al derivar).
- $P(x)\ln(ax)$, $P(x)\arcsin(ax)$, $P(x)\operatorname{arctg}(ax)$: $u=$ el logaritmo/arco, $dv=P(x)dx$.
- $e^{ax}\operatorname{sen}(bx)$: dos veces por partes y **se despeja** la integral (vuelve a aparecer).
- Regla mnemotécnica **ALPES**: Arcos, Logaritmos, Polinomios, Exponenciales, Senos: el que aparezca antes es $u$."""),
    ("teo", "Trigonométricas (4.2.4)", r"""
- $\int\operatorname{sen}^m\cos^n$: si una potencia es **impar**, separa un factor y cambia $t=\cos x$ (o $t=\operatorname{sen}x$) usando $\operatorname{sen}^2+\cos^2=1$;
  si las dos son **pares**, $\operatorname{sen}^2x=\frac{1-\cos2x}2$, $\cos^2x=\frac{1+\cos2x}2$.
- $\int\sec^m\operatorname{tg}^n$: secante par → $t=\operatorname{tg}x$; tangente impar → $t=\sec x$.
- **Racional en sen y cos**: $t=\operatorname{tg}\frac x2$, $\ \operatorname{sen}x=\frac{2t}{1+t^2}$, $\cos x=\frac{1-t^2}{1+t^2}$, $dx=\frac{2dt}{1+t^2}$."""),
    ("teo", "Sustituciones trigonométricas (4.2.5)", r"""$\sqrt{a^2-x^2}$: $x=a\operatorname{sen}z$. $\ \sqrt{a^2+x^2}$: $x=a\operatorname{tg}z$. $\ \sqrt{x^2-a^2}$: $x=a\sec z$."""),
    ("teo", "Racionales (4.2.6)", r"""
1. Si $\operatorname{gr}N\ge\operatorname{gr}D$, **divide**: $\frac ND=C+\frac RD$.
2. Factoriza $D$ en lineales y cuadráticos irreducibles (tema 6 de Finita).
3. Fracciones simples: $\frac{A}{x-a}$ (→ ln), $\frac{Bx+C}{x^2+px+q}$ (→ ln + arctg); con raíces múltiples, **Hermite**.
También $\int\frac{P(x)}{\sqrt{ax^2+bx+c}}dx=Q(x)\sqrt{ax^2+bx+c}+k\int\frac{dx}{\sqrt{ax^2+bx+c}}$ con $\operatorname{gr}Q<\operatorname{gr}P$."""),
], "Primitivas paso a paso"),

S("aplicaciones", "4.4 Aplicaciones de la integral", "§4.3 (4.3.1–4.3.8)", [
    ("idea", "Trocear, aproximar y sumar", r"""Todas las fórmulas salen igual: divide el objeto en trocitos, aproxima cada uno (un rectángulo, un segmento, un disco) y suma.
En el límite la suma es una integral."""),
    ("resumen", "Fórmulas", r"""
| Qué | Fórmula |
|---|---|
| Área entre curvas | $\int_a^b\lvert g-f\rvert\,dx$ (parte en los cortes) |
| Longitud de $y=f(x)$ | $\int_a^b\sqrt{1+f'(x)^2}\,dx$ |
| Longitud paramétrica | $\int_a^b\sqrt{x'(t)^2+y'(t)^2}\,dt$ |
| Área de curva cerrada paramétrica | $\frac12\left\lvert\int_a^b(xy'-yx')\,dt\right\rvert$ |
| Área en polares | $\frac12\int\rho(\theta)^2d\theta$ |
| Volumen al girar en torno a OX | $\pi\int_a^bf^2\,dx$ (paramétrica: $\pi\int y^2x'\,dt$) |
| Área lateral (OX) | $2\pi\int_a^bf\sqrt{1+f'^2}\,dx$ |
| Volumen por secciones | $\int_a^bA(x)\,dx$ |
| Cantidad con densidad $f$ | $\int_a^bf$ |"""),
    ("ojo", "Área ≠ integral", r"""La integral es área **con signo**: lo que queda bajo el eje cuenta negativo. Para el área de verdad hay que integrar $|f-g|$, partiendo
en los puntos de corte."""),
    ("ia", None, r"""Una **densidad de probabilidad** es una $f\ge0$ con $\int f=1$, y $P(a\le X\le b)=\int_a^bf$ (Observación 4.3.8). La curva ROC y su
**AUC** (área bajo la curva), que mide lo bueno que es un clasificador, es una integral."""),
], "Áreas"),

S("impropias", "4.5 Integrales impropias", "§4.4 (4.4.1–4.4.22)", [
    ("idea", "Áreas infinitas que suman algo finito", r"""Un tejado infinitamente largo puede tener área finita si se estrecha lo bastante rápido: $\int_1^\infty\frac{dx}{x^2}=1$, pero
$\int_1^\infty\frac{dx}x=\infty$. La impropia se define como **límite** de integrales normales."""),
    ("def", "Primera y segunda especie (4.4.2 y 4.4.15)", r"""
- **1ª especie** (intervalo no acotado): $\int_a^\infty f=\lim_{b\to\infty}\int_a^bf$. Si el límite es finito **converge**, si es $\pm\infty$ **diverge**, si no existe **oscila**.
- **2ª especie** (función no acotada en un extremo): $\int_a^bf=\lim_{t\to b^-}\int_a^tf$.
- $\int_{-\infty}^\infty$ (o con varios problemas) se parte en trozos y **cada uno** tiene que converger."""),
    ("ojo", "Ejemplo 4.4.3", r"""$\lim_{a\to\infty}\int_{-a}^a2x\,dx=0$, pero $\int_{-\infty}^\infty2x\,dx$ **no existe**: hay que tomar los dos límites por separado."""),
    ("teo", "Las integrales de referencia (4.4.4 y 4.4.17)", r"""
$$\int_a^\infty\frac{dx}{x^s}\ \text{converge}\iff s>1,\qquad\int_a^b\frac{dx}{(b-x)^s}\ \text{converge}\iff s<1.$$
(¡Al revés una de otra!) Truco: en ∞ hace falta que $f$ baje rápido (exponente grande); cerca de un punto hace falta que no suba demasiado (exponente pequeño)."""),
    ("teo", "Criterios (4.4.5–4.4.12, 4.4.18–4.4.21)", r"""
- **Necesaria**: si $\int_a^\infty f$ converge y existe $\lim_{x\to\infty}f$, ese límite es 0 (pero $f$ puede no tener límite: Ej. 4.4.6).
- $f\ge0$: converge ⇔ $\int_a^xf$ está acotada.
- **Comparación**: $0\le f\le g$ y $\int g$ converge ⇒ $\int f$ converge.
- **Paso al límite**: $\alpha=\lim f/g$. Si $\alpha\in(0,\infty)$, **mismo carácter**; si $\alpha=0$ y $\int g$ converge, converge; si $\alpha=\infty$ y $\int g$ diverge, diverge.
- **Práctico**: $\alpha=\lim_{x\to\infty}x^sf(x)$ finito con $s>1$ ⇒ converge; no nulo con $s\le1$ ⇒ diverge. En un punto $b$: $\lim(b-x)^sf(x)$ con $s<1$ / $s\ge1$."""),
    ("ej", "Ejemplo 4.4.13", r"""$\int_1^\infty\frac{x^2}{(1+x^2)^2}dx$: $x^2\cdot\frac{x^2}{(1+x^2)^2}\to1$ con $s=2>1$ ⇒ **converge**. $\ \int_1^\infty\frac{x^3-1}{x^4}$: con $s=1$ el límite es 1 ⇒ **diverge**."""),
    ("def", "Integrales eulerianas (4.4.23–4.4.29)", r"""
$\beta(p,q)=\int_0^1x^{p-1}(1-x)^{q-1}dx$ (converge si $p,q>0$) y $\Gamma(p)=\int_0^\infty x^{p-1}e^{-x}dx$ (converge si $p>0$).
$\Gamma(1)=1$, $\Gamma(p)=(p-1)\Gamma(p-1)$, $\Gamma(n)=(n-1)!$, $\beta(p,q)=\beta(q,p)=\frac{\Gamma(p)\Gamma(q)}{\Gamma(p+q)}$,
$\beta(p,q)=2\int_0^{\pi/2}\cos^{2p-1}t\operatorname{sen}^{2q-1}t\,dt$. Problema 4.19: $\beta(\frac12,\frac12)=\pi$ ⇒ $\Gamma(\frac12)=\sqrt\pi$."""),
    ("errata", "Ejemplo 4.4.17", r"""Se titula «integral impropia de **primera** especie en $(a,b)$», pero $\int_a^b\frac{dx}{(b-x)^s}$ es de **segunda** especie (intervalo acotado,
función no acotada en $b$)."""),
], "Impropias"),
])
