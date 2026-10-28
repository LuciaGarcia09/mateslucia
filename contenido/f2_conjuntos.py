from ui.teoria import Tema, S

TEMA = Tema("f2", "Matemática Finita", 2, "Conjuntos y aplicaciones",
            "Naturales e inducción, operaciones con conjuntos, aplicaciones (inyectivas, sobreyectivas, biyectivas) y cardinales.", [

S("induccion", "2.1 Números naturales e inducción", "Apartados 37–43", [
    ("idea", "Fichas de dominó", r"""
Para que caigan **todas** las fichas basta con dos cosas: **(1)** que caiga la primera y **(2)** que, si cae una, tire a la
siguiente. Eso es la inducción: caso base + paso inductivo ⇒ cierto para todos los $n$."""),
    ("def", "Principio de inducción (axioma 38) y Buen Orden (axioma 39)", r"""
- **Inducción**: si $J\subseteq\mathbb N$ cumple (i) $0\in J$ y (ii) $n\in J\Rightarrow n+1\in J$, entonces $J=\mathbb N$.
- **Buen orden**: todo $S\subseteq\mathbb N$ no vacío tiene **mínimo**.
- En esta asignatura $\mathbb N=\{0,1,2,\dots\}$ y $\mathbb N^+=\{1,2,\dots\}$ (en Análisis se empieza en 1)."""),
    ("truco", "Plantilla para cualquier inducción", r"""
1. **Caso base**: compruebo $P(n_0)$ (el primer $n$ que pida el enunciado).
2. **Hipótesis de inducción**: «supongo que $P(n)$ es cierto».
3. **Paso**: escribo $P(n+1)$, busco dentro de él a $P(n)$, uso la hipótesis y llego a la fórmula con $n+1$.
4. **Conclusión**: «por el principio de inducción, $P(n)$ es cierto para todo $n\ge n_0$»."""),
    ("ej", "Suma de Gauss", r"""
$1+2+\dots+n=\frac{n(n+1)}2$. Base: $1=\frac{1\cdot2}{2}$ ✓. Paso: $\frac{n(n+1)}2+(n+1)=(n+1)\left(\frac n2+1\right)=\frac{(n+1)(n+2)}2$ ✓."""),
    ("ej", "Divisibilidad: $n^3-n$ es múltiplo de 3", r"""
$(n+1)^3-(n+1)=(n^3-n)+3(n^2+n)$: el primer sumando es múltiplo de 3 por hipótesis y el segundo lo es claramente."""),
    ("teo", "Desigualdad de Bernoulli (ejercicio 41)", r"""
Si $h>-1$: $\ (1+h)^n\ge 1+nh$ para todo $n$. Paso: como $1+h>0$, multiplicar conserva el orden:
$(1+h)^{n+1}\ge(1+nh)(1+h)=1+(n+1)h+nh^2\ge1+(n+1)h$. Sirve para acotar potencias (si $h>0$, $(1+h)^n\to\infty$)."""),
    ("teo", "Inducción ⇔ Buen Orden (ejercicio 42)", r"""
Los dos axiomas son equivalentes. (⇐) Si el conjunto $J^c$ de los $n$ donde falla fuera no vacío, tendría mínimo $m\neq0$; entonces $m-1\in J$
y por (ii) $m\in J$: contradicción. (⇒) se prueba con inducción «fuerte» aplicada al complementario de un $S$ sin mínimo."""),
    ("def", "Sistemas de numeración (ejercicio 43)", r"""
Si $b\ge2$, todo $n\in\mathbb N$ se escribe de forma **única** como $n=c_pb^p+\dots+c_1b+c_0$ con $0\le c_i<b$.
Ejemplo: $73=64+8+1=1001001_{(2)}$. (Se practica en el tema 5.)"""),
    ("errata", "Apartado 40 (ii)", r"""El PDF escribe $1+3+5+\dots+(2n+1)=n^2$, **falso** ($n=1$: $1+3=4\neq1$). Hay $n+1$ sumandos y la suma es $(n+1)^2$;
la fórmula con $n^2$ es la de $1+3+\dots+(2n-1)$. **Compruébalo** en la pestaña de inducción: el caso base falla."""),
    ("errata", "Apartado 40 (viii) y 43", r"""$n!<n^n$ falla para $n=1$ ($1<1$): vale para $n\ge2$. En el 43 pone «$0\ge c_i<b$»: es $0\le c_i<b$."""),
], "Inducción"),

S("operaciones", "2.2 Operaciones con conjuntos", "Apartados 44–53", [
    ("idea", "Cada operación de conjuntos es un conectivo lógico", r"""
$\cup\leftrightarrow\vee$, $\ \cap\leftrightarrow\wedge$, complementario $\leftrightarrow\neg$, $\ \subseteq\leftrightarrow\Rightarrow$.
Por eso todas las propiedades de conjuntos se «heredan» de las equivalencias lógicas del tema 1:
$x\in A\cup B\iff (x\in A)\vee(x\in B)$."""),
    ("def", "Operaciones", r"""
- $A\cup B=\{x: x\in A\vee x\in B\}$, $\quad A\cap B=\{x: x\in A\wedge x\in B\}$, $\quad A-B=\{x\in A: x\notin B\}$.
- $A^c=\Omega-A$ (respecto de un universo $\Omega$). $\quad A\,\triangle\,B=(A\cup B)-(A\cap B)$ (el «o exclusivo»).
- $\mathcal P(A)=\{X : X\subseteq A\}$ (partes). $\quad A\times B=\{(a,b): a\in A,\ b\in B\}$ (pares **ordenados**)."""),
    ("teo", "Propiedades", r"""
- Conmutativas, asociativas, idempotencia, $A\cup\varnothing=A$, $A\cap\varnothing=\varnothing$.
- Distributivas: $A\cup(B\cap C)=(A\cup B)\cap(A\cup C)$, $A\cap(B\cup C)=(A\cap B)\cup(A\cap C)$.
- **De Morgan**: $(A\cup B)^c=A^c\cap B^c$, $(A\cap B)^c=A^c\cup B^c$. $\ (A^c)^c=A$.
- $A-(A-B)=A\cap B$ (y $=B$ si $B\subseteq A$).
- $\triangle$ es asociativa, conmutativa, $A\triangle\varnothing=A$, $A\triangle A=\varnothing$ y $A\cap(B\triangle C)=(A\cap B)\triangle(A\cap C)$."""),
    ("truco", "La función característica (ejercicio 49)", r"""
Escribe $\chi_A(x)=1$ si $x\in A$ y $0$ si no. Entonces $\chi_{A\cap B}=\chi_A\chi_B$ y $\chi_{A\triangle B}=\chi_A+\chi_B\pmod 2$.
Las propiedades de $\triangle$ se vuelven propiedades de sumar con $1+1=0$: $A\triangle B\triangle C$ = «los que están en un
número **impar** de los tres»."""),
    ("ej", "Partes y producto (ejercicios 50–51)", r"""
$\mathcal P(\{a,b\})=\{\varnothing,\{a\},\{b\},\{a,b\}\}$ (4 = $2^2$ elementos) y $\mathcal P(\mathcal P(\{a,b\}))$ tiene $2^4=16$.
$\{1,3,4\}\times\{2\}=\{(1,2),(3,2),(4,2)\}$. $[-3,2]\times(1,3]$ es un rectángulo sin el lado de abajo."""),
    ("teo", "Producto cartesiano (ejercicio 52)", r"""
$A\times(B\cup C)=(A\times B)\cup(A\times C)$, $\ A\times(B\cap C)=(A\times B)\cap(A\times C)$, $\ A\times\varnothing=\varnothing$.
$(A\times B)\times C\neq A\times(B\times C)$ como conjuntos (sus elementos son $((a,b),c)$ y $(a,(b,c))$), aunque hay una biyección natural."""),
    ("errata", "Apartado 52 (i)", r"""$(A\neq B)\iff(A\times B\neq B\times A)$ necesita **A y B no vacíos**: si $A=\varnothing\neq B$, $A\neq B$ pero $A\times B=\varnothing=B\times A$."""),
    ("def", "Axioma de elección (53)", r"""El producto cartesiano de una familia de conjuntos no vacíos es no vacío (se puede «elegir» un elemento de cada uno, aunque sean infinitos)."""),
], "Conjuntos y Venn"),

S("aplicaciones", "2.3 Aplicaciones", "Apartados 54–70", [
    ("idea", "Una aplicación es un reparto de flechas", r"""
De **cada** elemento de $A$ sale **exactamente una** flecha hacia $B$. Nadie se queda sin flecha y nadie tiene dos.
- **Inyectiva**: a ningún elemento de $B$ le llegan dos flechas.
- **Sobreyectiva**: a todo elemento de $B$ le llega al menos una.
- **Biyectiva**: a cada elemento de $B$ le llega exactamente una (se puede «dar la vuelta» a las flechas)."""),
    ("def", "Imagen y contraimagen", r"""
$f(A)=\{f(a): a\in A\}$, $\quad f^{-1}(B')=\{a\in A: f(a)\in B'\}$. **Ojo**: $f^{-1}(B')$ es sólo notación; existe aunque $f$ no
tenga inversa."""),
    ("teo", "Imágenes y contraimágenes (ejercicio 57)", r"""
- $f(f^{-1}(B))\subseteq B$, con igualdad si $f$ es **sobreyectiva**.
- $A\subseteq f^{-1}(f(A))$, con igualdad si $f$ es **inyectiva**.
- La contraimagen respeta todo: $f^{-1}(\cup B_j)=\cup f^{-1}(B_j)$, $f^{-1}(\cap B_j)=\cap f^{-1}(B_j)$, $f^{-1}(B^c)=f^{-1}(B)^c$.
- La imagen respeta uniones, pero sólo $f(\cap A_i)\subseteq\cap f(A_i)$ (igualdad si $f$ inyectiva). Contraejemplo: $x^2$, $A_1=\{-1\}$, $A_2=\{1\}$."""),
    ("def", "Composición e inversa", r"""
$(g\circ f)(a)=g(f(a))$: **primero $f$, luego $g$**. Es asociativa y la identidad es su «1».
Si $f$ es biyectiva existe $f^{-1}$ con $f^{-1}\circ f=\mathrm{Id}_A$ y $f\circ f^{-1}=\mathrm{Id}_B$."""),
    ("teo", "Inversas por un lado (ejercicio 68) y composición (69)", r"""
- $f$ **inyectiva** ⇔ tiene inversa por la **izquierda** ($g\circ f=\mathrm{Id}$), si $A\neq\varnothing$.
- $f$ **sobreyectiva** ⇔ tiene inversa por la **derecha** ($f\circ g=\mathrm{Id}$) (usa el axioma de elección).
- Composición de inyectivas es inyectiva; de sobreyectivas, sobreyectiva; $(g\circ f)^{-1}=f^{-1}\circ g^{-1}$ (zapatos y calcetines:
  lo último que te pones es lo primero que te quitas).
- $g\circ f$ biyectiva NO obliga a que $f$ y $g$ lo sean: $f:\{a\}\to\{0,1\}$, $g:\{0,1\}\to\{a\}$."""),
    ("ej", r"Aplicaciones entre $A=\{a,b,c\}$ y $X=\{0,1\}$ (ejercicio 62)", r"""
- $X^A$: $2^3=8$ aplicaciones; 0 inyectivas; 6 sobreyectivas (todas menos las 2 constantes).
- $A^X$: $3^2=9$; 6 inyectivas; 0 sobreyectivas.
- $A^A$: 27; inyectiva ⇔ sobreyectiva ⇔ biyectiva (conjunto finito con el mismo tamaño): las $3!=6$ permutaciones."""),
    ("ej", "Función característica (ejercicio 70)", r"""
$\mathcal P(\Omega)\to\{0,1\}^\Omega$, $A\mapsto\chi_A$, es **biyectiva**: un subconjunto «es» lo mismo que una función a $\{0,1\}$.
Por eso $|\mathcal P(A)|=2^{|A|}$."""),
    ("ojo", "Raíz y cuadrado", r"""$(\sqrt x)^2=x$ para $x\ge0$, pero $\sqrt{x^2}=|x|$ para todo $x$. Por eso $x^2$ sólo se invierte en $[0,\infty)$."""),
], "Aplicaciones"),

S("cardinales", "2.4 Cardinales", "Apartados 71–77", [
    ("idea", "Contar es emparejar", r"""
Dos conjuntos tienen el mismo tamaño si puedes emparejar sus elementos uno a uno (una **biyección**), como sillas y
personas en una sala: si todos se sientan y no sobran sillas, hay tantas personas como sillas, sin contar."""),
    ("def", "Equipotencia y finito", r"""
$A\approx B$ si existe una biyección $A\to B$ (es una relación de equivalencia). $A$ es **finito** con $|A|=n$ si $A\approx\{1,\dots,n\}$."""),
    ("teo", "Cardinales finitos (ejercicio 73)", r"""
$|A\cup B|=|A|+|B|$ si son disjuntos; $\ |A\times B|=|A|\cdot|B|$; $\ |B^A|=|B|^{|A|}$; $\ |\mathcal P(A)|=2^{|A|}$."""),
    ("teo", "Teorema de Cantor (74)", r"""
**No existe una biyección $A\to\mathcal P(A)$.** Si $f$ fuera sobreyectiva, el conjunto «diagonal» $K=\{a: a\notin f(a)\}$ sería
$f(a_0)$ para algún $a_0$, y entonces $a_0\in K\iff a_0\notin K$: imposible. **Hay infinitos más grandes que otros**."""),
    ("teo", "Cantor–Bernstein–Schröder (75)", r"""
Si hay una inyección $A\hookrightarrow B$ y otra $B\hookrightarrow A$, entonces $A\approx B$. Así se prueba sin construir la biyección:
- $\mathbb N\times\mathbb N\approx\mathbb N$: $(m,n)\mapsto 2^m3^n$ es inyectiva (factorización única).
- $\mathcal P_f(\mathbb N)$ (subconjuntos finitos) $\approx\mathbb N$: $X\mapsto\sum_{x\in X}2^x$ (expresión binaria única).
- $A^+$ (palabras con alfabeto finito) $\approx\mathbb N$."""),
    ("errata", "Ejercicio 77 (v)", r"""La longitud $|\cdot|:A^+\to\mathbb N$ es sobreyectiva sobre $\mathbb N^+$, no sobre $\mathbb N$: $A^+$ no contiene la palabra vacía."""),
], "Contar aplicaciones"),
])
