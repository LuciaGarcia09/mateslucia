from ui.teoria import Tema, S

TEMA = Tema("f5", "Matemática Finita", 5, "Aritmética de números enteros",
            "Orden y división en ℤ, primos y Teorema Fundamental, divisores, mcd y mcm, bases de numeración y algoritmo de Euclides.", [

S("orden_division", "5.1 El orden de ℤ y la división euclídea", "Apartados 148–150", [
    ("def", "Orden natural de ℤ (148)", r"""
$n\le m\iff$ existe $a\in\mathbb N$ con $m=n+a$ («$m$ está $a$ pasos a la derecha de $n$»). Es un orden **total** y compatible con las
operaciones: sumar conserva ($n\le m\Rightarrow n+x\le m+x$), multiplicar por $x>0$ conserva y por $x<0$ **invierte**.
Además $n^2\ge n$ y $n^2+m^2\ge2mn$ (porque $(n-m)^2\ge0$)."""),
    ("teo", "División euclídea (149)", r"""
Dados $n$ y $m\neq0$ existen **únicos** $C$ (cociente) y $R$ (resto) con
$$n=C\cdot m+R,\qquad 0\le R<|m|.$$
Idea de la prueba: $C$ es «cuántas veces cabe $m$»: el mayor con $Cm\le n$ (existe por el buen orden)."""),
    ("ojo", "El resto nunca es negativo", r"""$-17=(-4)\cdot5+3$ (resto 3), **no** $(-3)\cdot5-2$. Es el convenio de la asignatura (y el de Python con `//` y `%` si el divisor es positivo)."""),
    ("errata", "Apartados 148 (8) y 150", r"""
- 148 (8): «dados $n>m$, ∃! $k$ con $mk>n$» está mal: no es único (si $mk>n$, también $m(k+1)>n$) y hace falta $m>0$.
- 150: el pseudocódigo debe ser `while m[2] ≥ m` (con «>» y $n=10$, $m=5$ acabaría con resto 5)."""),
], "División entera"),

S("primos", "5.2 Primos y Teorema Fundamental de la Aritmética", "Apartados 151–157", [
    ("idea", "Los primos son los ladrillos", r"""Todo número se construye **multiplicando primos**, igual que una molécula con átomos, y de una sola manera
(salvo el orden). $360=2^3\cdot3^2\cdot5$."""),
    ("def", "Primo", r"""$p\ge2$ es primo si sus únicos divisores positivos son 1 y $p$."""),
    ("teo", "Teorema Fundamental de la Aritmética (153)", r"""
Todo $n\ge2$ se escribe como producto de primos $n=p_1\cdots p_r$, **de forma única** salvo el orden."""),
    ("demo", "Existencia y unicidad por el «mínimo contraejemplo»", r"""
**Existencia**: si algún $n\ge2$ no se factorizara, toma el menor, $n^*$. No es primo, así que $n^*=m_1m_2$ con ambos menores; esos sí
se factorizan y juntando las factorizaciones $n^*$ también: contradicción.
**Unicidad**: también se toma el menor $n$ con dos factorizaciones distintas y se llega a otro número menor con dos factorizaciones.
(O, más corto, con el Lema de Euclides.)"""),
    ("teo", "Euclides: infinitos primos (155)", r"""
Si sólo hubiera $p_1,\dots,p_N$, el número $q=p_1\cdots p_N+1$ no sería divisible por ninguno (dejaría resto 1), así que tendría un factor
primo nuevo. Contradicción."""),
    ("teo", "Lema de Euclides (156)", r"""$p$ es primo $\iff$ siempre que $p\mid ab$, se tiene $p\mid a$ o $p\mid b$. (Con 6: $6\mid 2\cdot3$ pero $6\nmid2$, $6\nmid3$.)"""),
    ("teo", "Criba de Eratóstenes (152)", r"""
Escribe $2,\dots,N$; deja el 2 y tacha sus múltiplos; el siguiente sin tachar es primo, tacha sus múltiplos… **Basta llegar a $k\le\sqrt N$**:
si $n=ab$ es compuesto, uno de los dos factores es $\le\sqrt n$, así que $n$ ya fue tachado. (Y se puede empezar a tachar en $k^2$.)"""),
    ("teo", "Divisores de un número (157)", r"""
Si $n=p_1^{r_1}\cdots p_s^{r_s}$:
- número de divisores: $d(n)=(r_1+1)\cdots(r_s+1)$ (cada exponente va de 0 a $r_i$);
- suma: $\sigma(n)=\prod\dfrac{p_i^{r_i+1}-1}{p_i-1}$ (desarrollar $\prod(1+p_i+\dots+p_i^{r_i})$);
- producto: $\prod_{d\mid n}d=\sqrt{n^{d(n)}}$ (emparejar cada $d$ con $n/d$)."""),
    ("teo", "La divisibilidad como orden (154)", r"""
$(\mathbb N,\mid)$ es orden parcial; los primos son los **minimales** de $\mathbb N\setminus\{0,1\}$. Si $n\ge2$ y $n\mid m$, entonces
$n\nmid m+k$ para $k=1,\dots,n-1$."""),
    ("errata", "Apartado 154 (ii)–(iii)", r"""
- (ii): los primos son minimales en $\mathbb N\setminus\{0,1\}$ (en $\mathbb N^+$ el minimal sería el 1).
- (iii): $(a\mathbb N,\mid)$ **no** es totalmente ordenado: $2a$ y $3a$ no son comparables."""),
], "Criba y primos"),

S("mcd_mcm", "5.3 Máximo común divisor y mínimo común múltiplo", "Apartados 158–162", [
    ("def", "mcd y mcm", r"""
$\operatorname{mcd}(m,n)$ = el mayor divisor común; $\operatorname{mcm}(m,n)$ = el menor múltiplo común positivo. Además: si $x\mid m$ y $x\mid n$,
entonces $x\mid\operatorname{mcd}$; si $m\mid x$ y $n\mid x$, entonces $\operatorname{mcm}\mid x$."""),
    ("teo", "Con factorizaciones (160)", r"""
$\operatorname{mcd}=\prod p_i^{\min(m_i,n_i)}$, $\quad\operatorname{mcm}=\prod p_i^{\max(m_i,n_i)}$, $\quad\operatorname{mcd}\cdot\operatorname{mcm}=m\cdot n$
(porque $\min+\max$ = suma de los dos exponentes)."""),
    ("teo", "Divisibilidad como retículo (161–162)", r"""
En $(\mathbb N^+,\mid)$: $\inf\{a,b\}=\operatorname{mcd}(a,b)$ y $\sup\{a,b\}=\operatorname{mcm}(a,b)$, y ambas operaciones son asociativas.
En los conjuntos del ejercicio 162 se piden diagramas de Hasse, cotas, extremos, maximales y minimales: hazlo en la pestaña **Orden y
Hasse** del tema 3 (están precargados)."""),
    ("errata", "Apartado 162 (v)", r"""Dice que ninguno está bien ordenado, pero $D=\operatorname{Div}(24)\cap\operatorname{Div}(160)=\{1,2,4,8\}$ **sí** lo está (es una cadena)."""),
], "Divisores y factorización"),

S("bases", "5.4 Sistemas de numeración", "Apartados 163–166", [
    ("idea", "Contar con otro número de dedos", r"""
En base 10 agrupas de 10 en 10; en base 2, de 2 en 2. $73=1\cdot64+0\cdot32+0\cdot16+1\cdot8+0\cdot4+0\cdot2+1=1001001_{(2)}$."""),
    ("teo", "Cambio de base por divisiones sucesivas (163)", r"""
Divide entre $b$, apunta el resto, divide el cociente entre $b$… hasta llegar a 0. **Los restos leídos de abajo arriba** son las cifras.
$73\div2$: restos 1, 0, 0, 1, 0, 0, 1 ⇒ $1001001$. $\ 73_{(10)}=2201_{(3)}$. Para volver: Horner, $((c_p b+c_{p-1})b+\dots)b+c_0$."""),
    ("teo", "Los algoritmos no dependen de la base (164–166)", r"""
Sumar, restar, multiplicar y dividir «en columna» funciona igual en cualquier base: sólo cambian las tablas ($b\times b$) y que cada
**llevada vale $b$**. Por eso se puede pasar $4664_{(7)}$ a base 3 dividiendo entre 3 **haciendo las cuentas en base 7**:
resultado $2100102_{(3)}$."""),
    ("errata", "Apartado 163", r"""El pseudocódigo del PDF tiene un bucle interior `while j ≤ i` que nunca incrementa $j$ (no termina). El algoritmo correcto
es el de las divisiones sucesivas (pestaña **Bases**)."""),
], "Bases"),

S("euclides", "5.5 Algoritmo de Euclides e identidad de Bézout", "Apartados 167–175", [
    ("idea", "La baldosa más grande", r"""
Quieres embaldosar un pasillo de $m\times n$ con baldosas cuadradas lo más grandes posible. Recortas el lado largo con el corto, luego
el corto con lo que sobró… hasta que un trozo encaja exacto. Ese lado es el **mcd**."""),
    ("teo", "Euclides (168)", r"""
Si $m=nc+r$ con $0\le r<n$, entonces $\operatorname{mcd}(m,n)=\operatorname{mcd}(n,r)$ (los divisores comunes de $m,n$ son exactamente los de $n,r$).
Repites hasta resto 0: **el último resto no nulo es el mcd**. Ejemplo: $\operatorname{mcd}(717933600, 6381632)=3190816$."""),
    ("teo", "Identidad de Bézout (167)", r"""
Existen $\lambda,\mu\in\mathbb Z$ con $\operatorname{mcd}(m,n)=\lambda m+\mu n$. Además el mcd es el **menor positivo** de la forma $am+bn$.
Los coeficientes **no son únicos**: $(\lambda+\frac{n}{d}t,\ \mu-\frac{m}{d}t)$ también valen."""),
    ("truco", "Euclides extendido en tabla (170–171)", r"""
Escribe cada resto como combinación de $m$ y $n$ y arrastra las combinaciones:
$r_{i}=r_{i-2}-q_i\,r_{i-1}$, $\ s_i=s_{i-2}-q_i\,s_{i-1}$, $\ t_i=t_{i-2}-q_i\,t_{i-1}$ empezando con $(r,s,t)=(m,1,0)$ y $(n,0,1)$.
La fila del último resto no nulo da $\operatorname{mcd}=s\,m+t\,n$. (O «sustitución regresiva» desde abajo, como en el PDF.)"""),
    ("teo", "En ℤ y con varios números (173–175)", r"""
- Con signos: si $\operatorname{mcd}=\lambda'|m|+\mu'|n|$, entonces $\lambda=\operatorname{signo}(m)\lambda'$, $\mu=\operatorname{signo}(n)\mu'$.
- Si $am+bn=c$ entonces $\operatorname{mcd}(m,n)\mid c$.
- $\operatorname{mcd}(m_1,\dots,m_s)=\lambda_1m_1+\dots+\lambda_sm_s$ (se hace encadenando: $\operatorname{mcd}(\operatorname{mcd}(m_1,m_2),m_3)\dots$)."""),
    ("ia", None, r"""El algoritmo de Euclides extendido es el que calcula los **inversos modulares** de RSA (mira el Rincón Datos e IA) y es de los
algoritmos más antiguos que se siguen usando: hace $O(\log n)$ divisiones."""),
], "mcd, mcm y Bézout"),
])
