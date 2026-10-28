"""Exámenes reales de Matemática Finita I (curso 2025/26) con soluciones explicadas y comprobadas.

Cada pregunta: enunciado, pista, solución paso a paso y, si hace falta, una errata del enunciado o de la
solución oficial. Las soluciones oficiales (modelos G, H y J) se han revisado una a una.
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Pregunta:
    num: int
    puntos: int
    temas: list[str]                 # ids de tema: f1…f8
    enunciado: str
    pista: str
    solucion: str
    errata: str | None = None
    herramienta: tuple[str, str] | None = None   # (id de tema, nombre de la pestaña)


@dataclass
class Examen:
    id: str
    modelo: str
    tipo: str
    fecha: str
    tiempo: str
    total: int
    aprobado: int
    preguntas: list[Pregunta] = field(default_factory=list)
    oficial: bool = False            # ¿traía soluciones el PDF?


# ============================================================ soluciones compartidas
DIOF_572 = (r"""**1. ¿Tiene solución?** Euclides: $572=3\cdot156+104$, $\ 156=1\cdot104+52$, $\ 104=2\cdot52$ ⇒ $\operatorname{mcd}(572,156)=52$, y $52\mid104$ ✓.

**2. Simplifica** dividiendo entre 52: $11X+3Y=2$.

**3. Solución particular:** $11\cdot1+3\cdot(-3)=2$ ⇒ $(X_0,Y_0)=(1,-3)$.

**4. Homogénea** $11X+3Y=0$ con $\operatorname{mcd}(11,3)=1$: $X=3t$, $Y=-11t$.

**Solución general:** $\boxed{X=1+3t,\quad Y=-3-11t,\quad t\in\mathbb Z}$. Comprobación: $572(1+3t)+156(-3-11t)=572-468+(1716-1716)t=104$ ✓.""")

BASE6 = (r"""Mirar la última cifra en base 6 es mirar el **resto módulo 6**. Todo entero es $6k+r$ con $r\in\{0,\dots,5\}$, y si $p>3$ es primo no puede ser
$r=0,2,4$ (sería par) ni $r=3$ (múltiplo de 3). Luego $p=6k\pm1$ y
$$p^2=36k^2\pm12k+1=6(6k^2\pm2k)+1\equiv1\pmod6,$$
así que la última cifra de $p^2$ en base 6 es **1**. (Ej.: $5^2=25=41_{(6)}$, $7^2=49=121_{(6)}$.)""")

ISO_PRODUCTO = (r"""Define $\varphi:G_1\times G_2\times G_3\times G_4\to G_2\times G_4\times G_3\times G_1$, $\ \varphi(g_1,g_2,g_3,g_4)=(g_2,g_4,g_3,g_1)$.

- **Homomorfismo**: en un producto se opera componente a componente, así que
  $\varphi\big((g_i)(h_i)\big)=\varphi(g_1h_1,g_2h_2,g_3h_3,g_4h_4)=(g_2h_2,g_4h_4,g_3h_3,g_1h_1)=\varphi(g)\,\varphi(h)$.
- **Biyectiva**: $\psi(a,b,c,d)=(d,a,c,b)$ cumple $\psi\circ\varphi=\mathrm{id}$ y $\varphi\circ\psi=\mathrm{id}$.

Luego $\varphi$ es un isomorfismo y los grupos son isomorfos (reordenar factores no cambia el grupo).""")

Z64 = (r"""**(a)** $\overline2\cdot\overline{32}=\overline{64}=\overline0$ con $\overline2,\overline{32}\neq\overline0$ ⇒ hay divisores de cero ⇒ **no es dominio**.

**(b)** Sea $\overline a\neq\overline0$ que **no** es divisor de cero. Si $a$ fuese par, $a=2b$ y $\overline a\cdot\overline{32}=\overline{64b}=\overline0$, contradicción.
Luego $a$ es impar, $\operatorname{mcd}(a,64)=1$ y por Bézout existen $s,t$ con $sa+64t=1$ ⇒ $\overline s\,\overline a=\overline1$: **es unidad**.

**(c)** Por (a) y (b), los divisores de cero (con el $\overline0$) son exactamente los pares: $\mathfrak m=\{\overline0,\overline2,\dots,\overline{62}\}$.
Es ideal: $\overline{2a}-\overline{2b}=\overline{2(a-b)}\in\mathfrak m$ y, **para todo** $\overline r\in\mathbb Z_{64}$, $\overline r\cdot\overline{2a}=\overline{2ra}\in\mathfrak m$ (absorbe).

**(d)** $\mathbb Z_{64}/\mathfrak m$ tiene dos clases, $[0]$ (pares) y $[1]$ (impares), con $[1]+[1]=[0]$: es $\cong\mathbb Z_2$, que es un **cuerpo**.
Como el cociente es cuerpo, $\mathfrak m$ es **maximal**. (Directamente: un ideal que contenga a $\mathfrak m$ y a un impar contiene una unidad, luego es todo $\mathbb Z_{64}$.)""")

DIOF_23 = (r"""$\operatorname{mcd}(23,16)=1\mid7$ ⇒ tiene solución. **Particular**: $23-16=7$ ⇒ $(x_0,y_0)=(1,-1)$.
**Homogénea** $23X+16Y=0$ ⇒ $23X=-16Y$ y, como son coprimos, $X=-16t$, $Y=23t$.

**Solución general:** $\boxed{x=1-16t,\quad y=-1+23t,\quad t\in\mathbb Z}$ (comprobación: $23-16+(-368+368)t=7$ ✓).""")

BINARIOS = (r"""Interpretamos el superíndice como el número de bloques «10»: $m=(10\,10\cdots10)_{(2)}$ con 201 bloques y $n$ con 50.
Cada bloque «10» vale 2 en su posición, así que $m=2\,(1+4+\dots+4^{200})=\frac{2(4^{201}-1)}3$ y $n=\frac{2(4^{50}-1)}3$.

**Euclides**: como $201=4\cdot50+1$, al dividir $m$ entre $n$ se «quitan» cuatro copias de $n$ desplazadas y sobra el último bloque: $r=10_{(2)}=2$.
Entonces $\operatorname{mcd}(m,n)=\operatorname{mcd}(n,2)=2$, porque $n$ es par.

**Resultado:** $\operatorname{mcd}(m,n)=10_{(2)}=2$. (Otra forma: $\operatorname{mcd}(4^a-1,4^b-1)=4^{\operatorname{mcd}(a,b)}-1$ con $\operatorname{mcd}(201,50)=1$.)""")

TGL = (r"""**Es grupo.** Las matrices inversibles forman grupo con el producto, así que basta ver que $G$ es un **subgrupo**:
$\begin{pmatrix}a&b\\0&c\end{pmatrix}\begin{pmatrix}x&y\\0&z\end{pmatrix}=\begin{pmatrix}ax&ay+bz\\0&cz\end{pmatrix}$ es triangular superior (y producto de inversibles es inversible),
la identidad está en $G$ y $\begin{pmatrix}a&b\\0&c\end{pmatrix}^{-1}=\begin{pmatrix}a^{-1}&-a^{-1}bc^{-1}\\0&c^{-1}\end{pmatrix}$ también es triangular superior.

**No abeliano:** $\begin{pmatrix}1&-1\\0&-1\end{pmatrix}\begin{pmatrix}1&1\\0&1\end{pmatrix}=\begin{pmatrix}1&0\\0&-1\end{pmatrix}$ pero $\begin{pmatrix}1&1\\0&1\end{pmatrix}\begin{pmatrix}1&-1\\0&-1\end{pmatrix}=\begin{pmatrix}1&-2\\0&-1\end{pmatrix}=\begin{pmatrix}1&1\\0&-1\end{pmatrix}$.

**Orden:** inversible ⇔ $ac\neq0$: $a\in\{1,2\}$, $b\in\mathbb Z_3$, $c\in\{1,2\}$ ⇒ $|G|=2\cdot3\cdot2=12$.

**Subgrupos abelianos:**
- Orden 2: $\left\{I,\begin{pmatrix}-1&0\\0&1\end{pmatrix}\right\}$ (la matriz al cuadrado da $I$).
- Orden 3: $\left\{I,\begin{pmatrix}1&1\\0&1\end{pmatrix},\begin{pmatrix}1&-1\\0&1\end{pmatrix}\right\}$ (cíclico).
- Orden 4: las diagonales $\left\{I,\begin{pmatrix}-1&0\\0&1\end{pmatrix},\begin{pmatrix}1&0\\0&-1\end{pmatrix},\begin{pmatrix}-1&0\\0&-1\end{pmatrix}\right\}\cong\mathbb Z_2\times\mathbb Z_2$.
- Orden 5: **imposible** por Lagrange, $5\nmid12$.""")

Z2X_X2 = (r"""**Elementos.** Al dividir entre $x^2$ (grado 2) los restos tienen grado $\le1$: $a+bx$ con $a,b\in\mathbb Z_2$ ⇒ $\{[0],[1],[x],[1+x]\}$, **4 elementos**.

**No es $\cong\mathbb Z_4$.** Un isomorfismo de anillos lleva $1\mapsto1$, luego $1+1\mapsto1+1$. En $\mathbb Z_2[x]/(x^2)$ es $[1]+[1]=[0]$,
pero en $\mathbb Z_4$ es $1+1=2\neq0$: imposible (tienen distinta **característica**, 2 frente a 4).""")


# ============================================================ los exámenes
EXAMENES = [
Examen("A", "Modelo A", "Parcial I", "31 de octubre de 2025", "2 horas", 100, 50, [
    Pregunta(1, 20, ["f2"], r"""Se define el $n$-ésimo número armónico $H_n=1+\frac12+\dots+\frac1n$. Probar que para todo $k\ge0$:
$$1+\frac k2\le H_{2^k}\le1+k.$$""",
             r"""Inducción en $k$. Compara $H_{2^{k+1}}$ con $H_{2^k}$: lo que se añade son $2^k$ sumandos. ¿Entre qué valores está cada uno?""",
             r"""**Caso base** $k=0$: $H_1=1$ y $1\le1\le1$ ✓.

**Paso inductivo.** Supongamos $1+\frac k2\le H_{2^k}\le1+k$. Entonces
$$H_{2^{k+1}}=H_{2^k}+\underbrace{\frac1{2^k+1}+\frac1{2^k+2}+\dots+\frac1{2^{k+1}}}_{2^k\ \text{sumandos}}.$$
Cada sumando está entre el más pequeño, $\frac1{2^{k+1}}$, y el más grande, $\frac1{2^k+1}<\frac1{2^k}$. Por tanto el bloque añadido cumple
$$2^k\cdot\frac1{2^{k+1}}=\frac12\ \le\ \text{bloque}\ \le\ 2^k\cdot\frac1{2^k}=1.$$
Sumando a la hipótesis: $1+\frac k2+\frac12\le H_{2^{k+1}}\le1+k+1$, es decir $1+\frac{k+1}2\le H_{2^{k+1}}\le1+(k+1)$ ✓.

💡 Consecuencia: $H_n\to\infty$ (la serie armónica diverge), pero tan despacio como $\log_2n$."""),
    Pregunta(2, 20, ["f1"], r"""Con $\lfloor x\rfloor=\max\{y\in\mathbb Z:y\le x\}$ y $\lceil x\rceil=\min\{y\in\mathbb Z:y\ge x\}$, encontrar el valor de verdad de:

a) $\forall n\in\mathbb N,\ \lfloor n\rfloor=\lfloor\sqrt{\lfloor n\rfloor}\rfloor$ $\quad$ b) $\forall n\in\mathbb N,\ \lceil n\rceil=\lceil\sqrt{\lfloor n\rfloor}\rceil$
$\quad$ c) $[\forall n\in\mathbb N,\ \lceil n\rceil=\lceil\sqrt{\lfloor n\rfloor}\rceil]\Rightarrow[\forall n\in\mathbb N,\ \lfloor n\rfloor=\lfloor\sqrt{\lfloor n\rfloor}\rfloor]$""",
             r"""Si $n$ es natural, $\lfloor n\rfloor=\lceil n\rceil=n$. Para tumbar un «para todo» basta **un** contraejemplo.""",
             r"""Como $n\in\mathbb N$ es entero, $\lfloor n\rfloor=\lceil n\rceil=n$.

**a) Falsa.** Diría $n=\lfloor\sqrt n\rfloor$ para todo $n$. Contraejemplo $n=2$: $\lfloor\sqrt2\rfloor=1\neq2$. (Sólo se cumple para $n=0,1$.)

**b) Falsa.** Diría $n=\lceil\sqrt n\rceil$. Contraejemplo $n=3$: $\lceil\sqrt3\rceil=2\neq3$. (Se cumple para $n=0,1,2$, no para todos.)

**c) Verdadera.** Es una implicación $F\Rightarrow F$, que vale **V** (una implicación sólo es falsa con antecedente V y consecuente F).""",
             errata=r"""Tal como está escrito, con $n\in\mathbb N$ los suelos y techos sobre $n$ no hacen nada. Probablemente se quería $x\in\mathbb R$ y
$\lfloor\sqrt x\rfloor=\lfloor\sqrt{\lfloor x\rfloor}\rfloor$ (que **sí** es cierto para $x\ge0$) y $\lceil\sqrt x\rceil=\lceil\sqrt{\lfloor x\rfloor}\rceil$ (falso: $x=1{,}5$ da $2\neq1$),
y entonces c) sería $F\Rightarrow V$, también verdadera. La solución de arriba responde al enunciado literal.""",
             herramienta=("f1", "Tabla de verdad")),
    Pregunta(3, 20, ["f2"], r"""Sea $A$ un conjunto. a) Dar un ejemplo de $f:A\to A$ con inversa a la derecha pero sin inversa a la izquierda.
b) Dar un ejemplo de $g:A\to A$ con $[\forall i,j\le10,\ i\neq j\Rightarrow g^i\neq g^j]\wedge[g^{10}=g^{11}=\dots=g^k,\ \forall k\ge10]$.""",
             r"""Inversa a la derecha ⇔ sobreyectiva; a la izquierda ⇔ inyectiva. ¿Puede pasar eso en un conjunto finito? Para b), piensa en una «escalera» que acaba en un punto fijo.""",
             r"""**a)** $f$ tiene inversa a la derecha ($f\circ h=\mathrm{id}$) ⇔ es **sobreyectiva**, y a la izquierda ($h\circ f=\mathrm{id}$) ⇔ es **inyectiva**.
Necesitamos una sobreyectiva no inyectiva de $A$ en sí mismo, lo cual **exige $A$ infinito** (en un finito, sobreyectiva ⇔ inyectiva). Ejemplo en $A=\mathbb N$:
$$f(0)=0,\qquad f(n)=n-1\ (n\ge1).$$
Es sobreyectiva ($f(n+1)=n$), con inversa a la derecha $h(n)=n+1$ ($f(h(n))=n$), pero no inyectiva ($f(0)=f(1)=0$), así que no hay inversa a la izquierda.

**b)** $A=\{0,1,\dots,10\}$ (o cualquier conjunto que lo contenga, dejando fijo el resto) y $g(k)=k+1$ si $k<10$, $g(10)=10$.
Entonces $g^j(0)=j$ para $j\le10$, así que $g^0,g^1,\dots,g^{10}$ son distintas (mandan el 0 a sitios distintos). Y $g^{10}$ manda **todo** al 10,
que es fijo: $g^{11}=g\circ g^{10}=g^{10}$, y por inducción $g^k=g^{10}$ para todo $k\ge10$ ✓.""",
             errata=r"""El apartado a) es **imposible si $A$ es finito** (y trivialmente imposible si $|A|\le1$): hay que tomar $A$ infinito, como $\mathbb N$."""),
    Pregunta(4, 20, ["f4"], r"""¿Cuántas soluciones enteras no negativas tiene la inecuación $x+y+z\le273$?""",
             r"""Añade una variable de «holgura» $h\ge0$ para convertirla en igualdad, y usa bolas y barras.""",
             r"""Con la holgura $h=273-(x+y+z)\ge0$, las soluciones son biyectivas con las de $x+y+z+h=273$, $x,y,z,h\ge0$.
Repartir 273 unidades **iguales** en 4 cajas **distintas**: combinaciones con repetición
$$\binom{273+4-1}{4-1}=\binom{276}{3}=\frac{276\cdot275\cdot274}{6}=\boxed{3\,466\,100}.$$
(Comprobado contando por ordenador las ternas una a una.)""",
             herramienta=("f4", "Repartos (las 12 formas)")),
    Pregunta(5, 20, ["f4"], r"""Probar: $\displaystyle\sum_{k=0}^n(-1)^k\binom nk=0$.""",
             r"""Binomio de Newton con $a=1$, $b=-1$. Mira qué pasa con $n=0$.""",
             r"""Por el binomio de Newton, $(a+b)^n=\sum_{k=0}^n\binom nk a^{n-k}b^k$. Con $a=1$, $b=-1$:
$$\sum_{k=0}^n(-1)^k\binom nk=(1-1)^n=0^n=0\qquad(n\ge1).$$
**Interpretación combinatoria:** en un conjunto de $n\ge1$ elementos hay tantos subconjuntos de cardinal par como impar (emparejar $X\leftrightarrow X\triangle\{a\}$).""",
             errata=r"""Para $n=0$ la suma vale $\binom00=1\neq0$. Como en Finita $\mathbb N$ incluye el 0, el enunciado necesita **$n\ge1$**.""",
             herramienta=("f4", "Binomio")),
]),

Examen("B", "Modelo B (pone «Modelo A»)", "Parcial I", "31 de octubre de 2025", "2 horas", 120, 50, [
    Pregunta(1, 20, ["f2", "f5"], r"""Probar que todo número mayor que 7 es suma de un múltiplo de 4 y un múltiplo de 3.""",
             r"""Inducción «de 4 en 4»: comprueba 8, 9, 10, 11 a mano y luego suma 4.""",
             r"""Buscamos $n=4a+3b$ con $a,b\ge0$ (múltiplos no negativos; si se permiten negativos es trivial por Bézout, $1=4-3$).

**Casos base:** $8=4\cdot2$, $\ 9=3\cdot3$, $\ 10=4\cdot1+3\cdot2$, $\ 11=4\cdot2+3\cdot1$.

**Paso (inducción fuerte):** si $n\ge12$, entonces $n-4\ge8$ y por hipótesis $n-4=4a+3b$, luego $n=4(a+1)+3b$ ✓.

(De hecho vale desde $n=6$: el mayor número que **no** se puede escribir así es $4\cdot3-4-3=5$, el número de Frobenius.)"""),
    Pregunta(2, 20, ["f1"], r"""Demostrar: a) $[(p\Rightarrow q)\Rightarrow r]\Rightarrow[p\Rightarrow(q\Rightarrow r)]$ $\quad$ b) $[[p\vee(q\wedge r)]\Rightarrow(r\wedge s)]\Rightarrow[\neg r\Rightarrow(r\Rightarrow s)]$""",
             r"""Método rápido: supón que la implicación es **falsa** (antecedente V, consecuente F) y llega a una contradicción.""",
             r"""**a)** Supongamos que es falsa: el consecuente $p\Rightarrow(q\Rightarrow r)$ es F, así que $p=V$, $q=V$, $r=F$. Entonces $p\Rightarrow q$ es V
y $(p\Rightarrow q)\Rightarrow r$ es $V\Rightarrow F=F$: el antecedente es falso, contradicción. **Es tautología.**

**b)** El consecuente $\neg r\Rightarrow(r\Rightarrow s)$ es **siempre V**: si $r=F$, $r\Rightarrow s$ es V; si $r=V$, $\neg r$ es F. Una implicación con
consecuente tautológico es tautología, sin mirar el antecedente. **Es tautología.**""",
             herramienta=("f1", "Tabla de verdad")),
    Pregunta(3, 20, ["f3"], r"""En $\mathbb R$, $x\sim y\iff\exists k\in\mathbb Z:\ x-y=2\pi k$. a) Probar que es de equivalencia y dar $\mathbb R/\!\sim$.
b) Probar que $f:\mathbb R/\!\sim\ \to\mathbb R^2$, $f([x])=(\cos x,\operatorname{sen}x)$, es aplicación y calcular $\operatorname{Im}f$.""",
             r"""Para b) «es aplicación» significa **bien definida**: no depende del representante elegido.""",
             r"""**a)** Reflexiva: $x-x=2\pi\cdot0$. Simétrica: $x-y=2\pi k\Rightarrow y-x=2\pi(-k)$. Transitiva: $x-y=2\pi k$, $y-z=2\pi l\Rightarrow x-z=2\pi(k+l)$.
Cada clase $[x]=\{x+2\pi k:k\in\mathbb Z\}$ tiene **un único representante en $[0,2\pi)$**, así que $\mathbb R/\!\sim\ =\{[x]:x\in[0,2\pi)\}$: los «ángulos» (la circunferencia).

**b)** Bien definida: si $[x]=[y]$, $y=x+2\pi k$ y por periodicidad $\cos y=\cos x$, $\operatorname{sen}y=\operatorname{sen}x$, luego $f([x])=f([y])$.
Imagen: $\cos^2x+\operatorname{sen}^2x=1$ da $\operatorname{Im}f\subseteq S^1=\{(a,b):a^2+b^2=1\}$, y todo punto de $S^1$ es $(\cos\theta,\operatorname{sen}\theta)$ para algún $\theta$.
**$\operatorname{Im}f=S^1$**, la circunferencia unidad (y $f$ es además inyectiva: biyección entre $\mathbb R/\!\sim$ y $S^1$).""",
             herramienta=("f3", "Equivalencia y clases")),
    Pregunta(4, 20, ["f4"], r"""$n$ bolas numeradas y $t$ tubos numerados; cada tubo contiene una cantidad **ordenada** de bolas (incluso ninguna).
a) $\mu_0(n,t)$: maneras de distribuirlas. b) $\mu_1(n,t)$: maneras con al menos una bola por tubo.""",
             r"""Coloca las $n$ bolas en fila y separa con $t-1$ barras. ¿Cuántas filas y cuántas posiciones de barras hay?""",
             r"""**a)** Una distribución es una ordenación de las $n$ bolas en fila más $t-1$ separadores entre tubos: permutaciones de $n$ objetos distintos y $t-1$ barras iguales,
$$\mu_0(n,t)=\frac{(n+t-1)!}{(t-1)!}=t(t+1)\cdots(t+n-1)\quad(\text{factorial creciente } t^{\overline n}).$$
(Otra forma: la bola 1 tiene $t$ sitios, la 2 tiene $t+1$ —antes o después de la 1 o en otro tubo—, …, la $n$ tiene $t+n-1$.)

**b)** Ordena las bolas ($n!$) y elige dónde cortar: $t-1$ cortes en los $n-1$ huecos, sin repetir para que ningún tubo quede vacío:
$$\mu_1(n,t)=n!\binom{n-1}{t-1}.$$
(Comprobado enumerando todos los casos con $n\le4$, $t\le3$. Son los números de **Lah** multiplicados por $t!$.)""",
             herramienta=("f4", "Repartos (las 12 formas)")),
    Pregunta(5, 20, ["f4"], r"""Probar: $\displaystyle{n+1\brace k}=\sum_{j=0}^{n-k+1}{n-j\brace k-1}\cdot k^{j-1}$ (números de Stirling de segunda especie).""",
             r"""Clasifica las particiones de $\{1,\dots,n+1\}$ en $k$ bloques según cuál es el **mayor elemento que no está en el bloque del $n+1$**… o, más fácil: según el último elemento que abre un bloque nuevo.""",
             r"""La identidad correcta es (ver errata)
$${n+1\brace k}=\sum_{j=0}^{n-k+1}{n-j\brace k-1}\,k^{\,j}.$$
**Prueba combinatoria.** En una partición de $\{1,\dots,n+1\}$ en $k$ bloques, ordena los bloques por su menor elemento y llama $m$ al menor elemento del **último** bloque.
Escribe $m=n+1-j$. Entonces:
- los $m-1=n-j$ elementos anteriores forman una partición en $k-1$ bloques: ${n-j\brace k-1}$ formas;
- $m$ abre el bloque $k$;
- cada uno de los $j$ elementos posteriores $m+1,\dots,n+1$ va a cualquiera de los $k$ bloques (ya existen todos): $k^j$ formas.

Como $m$ va de $k$ a $n+1$, $j=n+1-m$ va de $0$ a $n-k+1$, y sumando sale la fórmula.

**Por inducción** también sale de ${n+1\brace k}={n\brace k-1}+k{n\brace k}$, desarrollando ${n\brace k}$ una y otra vez.""",
             errata=r"""Con $k^{j-1}$ la igualdad es **falsa**: para $n=1$, $k=2$ el lado izquierdo es ${2\brace2}=1$ y el derecho ${1\brace1}\cdot2^{-1}=\frac12$.
El exponente correcto es $k^{\,j}$ (comprobado por ordenador para todos los $n\le6$).""",
             herramienta=("f4", "Números especiales")),
    Pregunta(6, 20, ["f2", "f4"], r"""Sea $A$ con $n\ge1$ elementos y $PECS(A)=\{(X,Y):X\subsetneq Y\subseteq A\}$. Probar: (i) $|PECS(A)|<2^{2n}$ $\quad$ (ii) $|PECS(A)|=3^n-2^n$.""",
             r"""Para cada elemento de $A$, ¿cuántas posibilidades hay respecto de $X$ e $Y$ si $X\subseteq Y$?""",
             r"""**(ii)** Contamos primero los pares con $X\subseteq Y\subseteq A$. Cada $a\in A$ está en una de **tres** situaciones: $a\in X$ (y por tanto en $Y$), $a\in Y\setminus X$,
o $a\notin Y$. Elegir independientemente para los $n$ elementos da $3^n$ pares. De ellos, los que tienen $X=Y$ son $2^n$ (uno por subconjunto).
Luego $|PECS(A)|=3^n-2^n$.

**(i)** $PECS(A)\subseteq\mathcal P(A)\times\mathcal P(A)$, que tiene $2^n\cdot2^n=2^{2n}$ elementos, y la inclusión es estricta (el par $(A,A)$ no está).
O con (ii): $3^n-2^n<3^n<4^n=2^{2n}$.""",
             herramienta=("f2", "Partes y producto")),
]),

Examen("C", "Modelo C", "Parcial I", "31 de octubre de 2025", "2 horas y media", 120, 50, [
    Pregunta(1, 10, ["f2"], r"""Probar que para todo $n\in\mathbb N$: $1\cdot1!+2\cdot2!+\dots+n\cdot n!=(n+1)!-1$.""",
             r"""Inducción. Truco: $k\cdot k!=(k+1)!-k!$ (¡telescópica!).""",
             r"""**Base** $n=0$: suma vacía $=0=1!-1$ ✓ (y $n=1$: $1=2!-1$ ✓).

**Paso:** si $\sum_{k=1}^nk\cdot k!=(n+1)!-1$, entonces
$$\sum_{k=1}^{n+1}k\cdot k!=(n+1)!-1+(n+1)(n+1)!=(n+1)!\,(1+n+1)-1=(n+2)!-1\ ✓.$$
**Sin inducción:** $k\cdot k!=(k+1)!-k!$, y la suma es telescópica: $(n+1)!-1!$.""",
             herramienta=("f2", "Inducción")),
    Pregunta(2, 10, ["f1"], r"""Demostrar el teorema $[p\Rightarrow q]\Rightarrow[\neg p\vee q\vee(p\Rightarrow r)\vee(r\Rightarrow s)]$.""",
             r"""Escribe las implicaciones del consecuente como disyunciones.""",
             r"""El consecuente es $\neg p\vee q\vee(\neg p\vee r)\vee(\neg r\vee s)$, que contiene $r\vee\neg r$: es **siempre verdadero**.
Una implicación con consecuente tautológico es tautología. (También: el antecedente $p\Rightarrow q\equiv\neg p\vee q$ aparece tal cual dentro del consecuente.)""",
             herramienta=("f1", "Tabla de verdad")),
    Pregunta(3, 25, ["f3", "f2"], r"""En $\mathcal P(\mathbb N)$ ($\mathbb N=\{1,2,\dots\}$) y $M=\{1,\dots,m\}$, sea $A\,R_M\,B\iff A\cap M=B\cap M$.
Probar que es de equivalencia, que $\mathcal P(\mathbb N)/R_M$ es finito, calcular su cardinal y dar un sistema de representantes.""",
             r"""$A\,R_M\,B$ significa que $A$ y $B$ «se ven igual a través de la ventana $M$». ¿Qué ves por la ventana?""",
             r"""**Equivalencia:** $R_M$ es «tener la misma imagen» por la aplicación $\pi(A)=A\cap M$, y toda relación $A\sim B\iff\pi(A)=\pi(B)$ es de equivalencia
(reflexiva, simétrica y transitiva porque lo es la igualdad).

**Cociente:** la clase de $A$ queda determinada por $A\cap M\in\mathcal P(M)$, y todo $S\subseteq M$ aparece ($S\cap M=S$). Así
$\mathcal P(\mathbb N)/R_M\ \leftrightarrow\ \mathcal P(M)$, $[A]\mapsto A\cap M$, biyección. **Es finito con $2^m$ clases.**

**Representantes:** los subconjuntos de $M$, $\{S:S\subseteq\{1,\dots,m\}\}$ (cada $A$ es equivalente a $A\cap M$).""",
             herramienta=("f3", "Equivalencia y clases")),
    Pregunta(4, 25, ["f2"], r"""$f:A\to B$ y $f^*:\mathcal P(B)\to\mathcal P(A)$, $f^*(X)=\{a:f(a)\in X\}$ (imagen inversa). Demostrar:
a) $f^*(X\cap Y)=f^*(X)\cap f^*(Y)$ $\ $ b) $f^*(X\cup Y)=f^*(X)\cup f^*(Y)$ $\ $ c) si $f$ es biyectiva, $f^*$ es biyectiva y $(f^{-1})^*=(f^*)^{-1}$.""",
             r"""Cadena de «si y sólo si» elemento a elemento. Para c), calcula $f^*\circ(f^{-1})^*$ y al revés.""",
             r"""**a)** $a\in f^*(X\cap Y)\iff f(a)\in X\cap Y\iff f(a)\in X\wedge f(a)\in Y\iff a\in f^*(X)\cap f^*(Y)$.

**b)** Igual con $\vee$: $f(a)\in X\cup Y\iff f(a)\in X\vee f(a)\in Y$.

**c)** Si $f$ es biyectiva existe $f^{-1}:B\to A$ y $(f^{-1})^*:\mathcal P(A)\to\mathcal P(B)$, $(f^{-1})^*(Z)=\{b:f^{-1}(b)\in Z\}=f(Z)$.
- $f^*\big((f^{-1})^*(Z)\big)=f^*(f(Z))=\{a:f(a)\in f(Z)\}=Z$ (por ser $f$ inyectiva).
- $(f^{-1})^*\big(f^*(X)\big)=f(f^{-1}(X))=X$ (por ser $f$ sobreyectiva).

Luego $(f^{-1})^*$ es inversa de $f^*$ por los dos lados: $f^*$ es biyectiva y $(f^*)^{-1}=(f^{-1})^*$.

💡 Las imágenes **inversas** respetan ∩ y ∪ siempre; las imágenes directas sólo respetan ∪ ($f(X\cap Y)\subseteq f(X)\cap f(Y)$, con igualdad si $f$ es inyectiva).""",
             herramienta=("f2", "Aplicaciones")),
    Pregunta(5, 25, ["f4"], r"""En una muestra de gatos hay más gatos que gatas, más gatas crías que gatos naranjas, y más gatas naranjas que no son crías que gatos que ni son crías ni son naranjas.
Probar que hay menos gatas que no son crías ni son naranjas que gatos que son crías y no son naranjas.""",
             r"""Haz un «Venn» de 8 casillas: sexo × cría × naranja. Escribe las tres hipótesis como desigualdades y súmalas.""",
             r"""Notación: $m_{ab}$ = machos, $h_{ab}$ = hembras, con $a\in\{c,\bar c\}$ (cría o no) y $b\in\{n,\bar n\}$ (naranja o no).

Hipótesis:
1. $m_{cn}+m_{c\bar n}+m_{\bar cn}+m_{\bar c\bar n}>h_{cn}+h_{c\bar n}+h_{\bar cn}+h_{\bar c\bar n}$ (más gatos que gatas).
2. $h_{cn}+h_{c\bar n}>m_{cn}+m_{\bar cn}$ (gatas crías > gatos naranjas).
3. $h_{\bar cn}>m_{\bar c\bar n}$ (gatas naranjas no crías > gatos ni crías ni naranjas).

Sumando 2 y 3: $h_{cn}+h_{c\bar n}+h_{\bar cn}>m_{cn}+m_{\bar cn}+m_{\bar c\bar n}$. Sumando esto con 1, se cancelan esas seis casillas y queda
$$m_{c\bar n}>h_{\bar c\bar n},$$
es decir, **hay más gatos crías no naranjas que gatas ni crías ni naranjas**, que es lo pedido. ∎""",
             herramienta=("f4", "Inclusión–exclusión")),
    Pregunta(6, 25, ["f2", "f4"], r"""Sea $A$ con $n\ge1$ elementos y $\mathrm{Pecs}(A)=\{(X,Y):X\subsetneq Y\subseteq A\}$. a) $|\mathrm{Pecs}(A)|<2^{2n}$. b) $|\mathrm{Pecs}(A)|=3^n-2^n$.""",
             r"""Es la misma pregunta que la 6 del modelo B: tres situaciones posibles para cada elemento.""",
             r"""Igual que en el modelo B, pregunta 6: cada elemento está en $X$, en $Y\setminus X$ o fuera de $Y$ ⇒ $3^n$ pares con $X\subseteq Y$; quitando
los $2^n$ con $X=Y$ queda $3^n-2^n$. Y $3^n-2^n<4^n=2^{2n}$.""",
             herramienta=("f2", "Partes y producto")),
]),

Examen("D", "Modelo D", "Parcial I", "21 de noviembre de 2025", "2 horas y media", 120, 50, [
    Pregunta(1, 10, ["f2", "f7"], r"""Probar que si $n\ge1$ es impar, $7^n+1$ es divisible por 8.""",
             r"""Módulo 8, ¿a qué es congruente 7?""",
             r"""$7\equiv-1\pmod8$, luego $7^n+1\equiv(-1)^n+1=-1+1=0\pmod8$ para $n$ impar ✓.

**Por inducción** (de 2 en 2): $n=1$: $8$ ✓. Si $8\mid7^n+1$, entonces $7^{n+2}+1=49(7^n+1)-48$, y $8\mid48$ ✓.""",
             herramienta=("f2", "Inducción")),
    Pregunta(2, 10, ["f1"], r"""Demostrar el teorema $[\forall x,\ p(x)\wedge q(x)]\Rightarrow[\exists x,\ p(x)\Rightarrow q(x)]$.""",
             r"""Supón el antecedente y toma un elemento cualquiera del universo (que suponemos no vacío).""",
             r"""Supongamos $\forall x\,(p(x)\wedge q(x))$ y sea $x_0$ un elemento del universo (no vacío, como siempre en lógica de primer orden).
Entonces $q(x_0)$ es verdadero, luego $p(x_0)\Rightarrow q(x_0)$ es verdadero (consecuente V). Así $\exists x\,(p(x)\Rightarrow q(x))$ ✓.

(De hecho basta con $\forall x\,q(x)$: el $p$ no hace falta.)""",
             herramienta=("f1", "Negar cuantificadores")),
    Pregunta(3, 25, ["f3", "f2"], r"""En $\mathcal P(\mathbb N)$ y $M=\{m,m+1,m+2,\dots\}$ (infinito), $A\,R_M\,B\iff A\cup M=B\cup M$.
Probar que es de equivalencia, que el cociente es finito, su cardinal y un sistema de representantes.""",
             r"""Al unir con $M$ se «pierde» la información de los elementos $\ge m$. ¿Qué parte de $A$ sobrevive?""",
             r"""Es «tener la misma imagen» por $A\mapsto A\cup M$, luego es de equivalencia (como en el modelo C).

$A\cup M$ queda determinado por los elementos de $A$ **menores que $m$**: $A\cup M=(A\cap\{1,\dots,m-1\})\cup M$. Por tanto
$$A\,R_M\,B\iff A\cap\{1,\dots,m-1\}=B\cap\{1,\dots,m-1\}.$$
El cociente está en biyección con $\mathcal P(\{1,\dots,m-1\})$: **$2^{m-1}$ clases** (finito). **Representantes:** los subconjuntos de $\{1,\dots,m-1\}$.
(Si $m=1$, $M=\mathbb N$ y hay una sola clase.)""",
             herramienta=("f3", "Equivalencia y clases")),
    Pregunta(4, 25, ["f3", "f2"], r"""$f:A\to A$ y en $\mathcal P^+(A)=\{X\neq\varnothing,X\subseteq A\}$ la relación $X\preceq_fY\iff f(X)\subseteq f(Y)$.
Probar que $\preceq_f$ es de orden si y sólo si $f$ es una biyección.""",
             r"""Reflexiva y transitiva salen siempre. Todo depende de la antisimétrica: ¿cuándo $f(X)=f(Y)$ obliga a $X=Y$?""",
             r"""**Reflexiva** ($f(X)\subseteq f(X)$) y **transitiva** (la inclusión lo es) se cumplen **siempre**.

**Antisimétrica** ⇔ $[f(X)=f(Y)\Rightarrow X=Y]$ ⇔ $f$ **inyectiva**:
- Si $f$ no es inyectiva, $f(a)=f(b)$ con $a\neq b$: $X=\{a\}$, $Y=\{b\}$ cumplen $X\preceq_fY$ e $Y\preceq_fX$ con $X\neq Y$.
- Si $f$ es inyectiva y $f(X)=f(Y)$: para $x\in X$, $f(x)=f(y)$ para algún $y\in Y$, luego $x=y\in Y$; así $X\subseteq Y$ y, por simetría, $X=Y$.

Por tanto **$\preceq_f$ es de orden ⇔ $f$ es inyectiva**, y si $A$ es **finito** esto equivale a biyectiva.""",
             errata=r"""Para $A$ **infinito** el «si y sólo si biyección» es falso: $f:\mathbb N\to\mathbb N$, $f(n)=n+1$ es inyectiva y no sobreyectiva,
y $\preceq_f$ sí es de orden. La condición exacta es «$f$ inyectiva» (que en conjuntos finitos es lo mismo que biyectiva).""",
             herramienta=("f3", "Orden y Hasse")),
    Pregunta(5, 25, ["f4", "f3"], r"""En $A=\{1,\dots,1000\}$, $S\subset A$ es **sólido** si $\forall x<y<z\in A,\ [x,z\in S\Rightarrow y\in S]$.
Dar ejemplos y calcular cuántos subconjuntos sólidos tiene $A$.""",
             r"""«Sólido» = sin agujeros. ¿Qué forma tienen?""",
             r"""Sólido significa que si contiene dos números contiene **todos los de en medio**: los sólidos no vacíos son los **intervalos** $\{a,a+1,\dots,b\}$ con $1\le a\le b\le1000$
(si $S\neq\varnothing$, toma $a=\min S$, $b=\max S$ y todo lo intermedio está). Ejemplos: $\varnothing$, $\{7\}$, $\{10,\dots,20\}$, $A$; **no** sólido: $\{1,3\}$.

**Cuenta:** un intervalo lo determinan $a\le b$: $\binom{1000}2$ con $a<b$ más $1000$ con $a=b$, total $\frac{1000\cdot1001}2=500\,500$.
Con el vacío (que es sólido por vacuidad): $\boxed{500\,501}$.

(Si «$S\subset A$» se lee como subconjunto **propio**, se quita $A$ y quedan $500\,500$.)""",
             herramienta=("f4", "Asistente: ¿qué fórmula uso?")),
    Pregunta(6, 25, ["f3", "f5"], r"""Con la divisibilidad en $\mathbb N$, $C=\{2k:2\le k\le50\}$. Encontrar los minimales; probar que existen $\inf C$ y $\sup C$ y calcularlos; calcular $\min C$ y $\max C$ si existen.""",
             r"""$2j\mid2k\iff j\mid k$. En $(\mathbb N,\mid)$ el ínfimo es el mcd y el supremo el mcm.""",
             r"""$C=\{4,6,8,\dots,100\}$. Como $2j\mid2k\iff j\mid k$, el elemento $2k$ es **minimal** si ningún $j$ con $2\le j<k$ divide a $k$, es decir, si **$k$ es primo**:
$$\text{minimales}=\{4,6,10,14,22,26,34,38,46,58,62,74,82,86,94\}\quad(2p,\ p\text{ primo}\le50:\ 15\text{ elementos}).$$
**Ínfimo:** en $(\mathbb N,\mid)$ el ínfimo de un conjunto es su mcd: $\operatorname{mcd}(C)=2$ (ya $\operatorname{mcd}(4,6)=2$, y 2 divide a todos).
**Supremo:** el mcm: $\sup C=\operatorname{mcm}(4,6,\dots,100)=2\operatorname{mcm}(1,\dots,50)=6\,198\,089\,008\,491\,993\,412\,800$.
**Mínimo y máximo no existen:** $\inf C=2\notin C$ y $\sup C\notin C$ (hay 15 minimales distintos; y es mayor que 100).""",
             herramienta=("f3", "Orden y Hasse")),
]),

Examen("E", "Modelo E", "Final", "9 de enero de 2026", "2 horas y media", 100, 50, [
    Pregunta(1, 10, ["f1"], r"""Demostrar el teorema $[\exists x,\ P(x)\Rightarrow\forall x,\ P(x)]\Rightarrow[a\wedge b]$.""",
             r"""Lee el antecedente como $\exists x\,[P(x)\Rightarrow\forall y\,P(y)]$: es la famosa «paradoja del bebedor».""",
             r"""**La parte verdadera: $\exists x\,[P(x)\Rightarrow\forall y\,P(y)]$ es un teorema** (universo no vacío). Dos casos:
- Si $\forall y\,P(y)$ es V, cualquier $x$ sirve (consecuente V).
- Si no, existe $x_0$ con $P(x_0)$ falso, y para ese $x_0$ la implicación $P(x_0)\Rightarrow\dots$ es V (antecedente F).

En ambos casos existe el $x$. («En todo bar hay alguien tal que, si él bebe, beben todos.»)""",
             errata=r"""Con el «$\Rightarrow[a\wedge b]$» final el enunciado **no es un teorema**: el antecedente es siempre verdadero, así que todo equivale a $a\wedge b$,
que es falso cuando $a$ es falsa. Lo más probable es que «$a\wedge b$» sobre (o se refiera a los apartados), y lo que se pide demostrar es la paradoja del bebedor.""",
             herramienta=("f1", "Negar cuantificadores")),
    Pregunta(2, 20, ["f2"], r"""Probar que si $n$ es entero positivo: $\displaystyle\frac{2\cdot4\cdots(2n)(2n+2)}{3\cdot5\cdots(2n+1)(2n+3)}<\frac{2\sqrt2}{3\sqrt{n+2}}$.""",
             r"""Inducción. Al pasar de $n$ a $n+1$ multiplicas por $\frac{2n+4}{2n+5}$; basta ver que eso es $\le\sqrt{\frac{n+2}{n+3}}$.""",
             r"""Llama $P_n$ al lado izquierdo y $c=\frac{2\sqrt2}3$.

**Base** $n=1$: $P_1=\frac{2\cdot4}{3\cdot5}=\frac8{15}\approx0{,}533$ y $\frac c{\sqrt3}\approx0{,}544$ ✓.

**Paso:** $P_{n+1}=P_n\cdot\frac{2n+4}{2n+5}<\frac c{\sqrt{n+2}}\cdot\frac{2n+4}{2n+5}$, y queremos $\le\frac c{\sqrt{n+3}}$, o sea
$$\frac{2n+4}{2n+5}\le\sqrt{\frac{n+2}{n+3}}\iff(2n+4)^2(n+3)\le(2n+5)^2(n+2).$$
Con $m=n+1$: izquierda $4m^3+16m^2+20m+8$, derecha $4m^3+16m^2+21m+9$: la diferencia es $m+1>0$ ✓.

(Comprobado numéricamente para $n\le30$. Con $n=0$ habría **igualdad**: $\frac23=\frac c{\sqrt2}$; por eso se pide $n\ge1$.)""",
             herramienta=("f2", "Inducción")),
    Pregunta(3, 20, ["f4"], r"""25 sospechosos: 10 con móvil, 10 con oportunidad, 20 sin coartada; 5 con móvil y oportunidad, 5 con móvil y sin coartada, 5 con oportunidad y sin coartada.
Pepe Carvalho dice que el criminal está entre los 25 y tiene móvil, oportunidad y no tiene coartada. Benoit Blanc dice que no está entre los sospechosos. ¿Quién tiene razón?""",
             r"""Inclusión–exclusión con $M$, $O$, $\bar C$ y la cota $|M\cup O\cup\bar C|\le25$.""",
             r"""Sea $x=|M\cap O\cap\bar C|$. Por inclusión–exclusión
$$|M\cup O\cup\bar C|=10+10+20-5-5-5+x=25+x.$$
Pero la unión está dentro de los 25 sospechosos: $25+x\le25$ ⇒ $x=0$. **Ningún sospechoso tiene a la vez móvil, oportunidad y falta de coartada.**

Así que si el asesino tiene esas tres cosas (como dice el propio Carvalho), **no puede estar entre los 25**: tiene razón **Benoit Blanc**, aunque Carvalho no haya bebido.""",
             herramienta=("f4", "Inclusión–exclusión")),
    Pregunta(4, 10, ["f5", "f7"], r"""Encontrar todas las soluciones enteras de $572X+156Y=104$.""",
             r"""mcd por Euclides, divide la ecuación entre él y busca una solución a ojo.""", DIOF_572,
             herramienta=("f7", "Diofánticas")),
    Pregunta(5, 10, ["f5", "f7"], r"""Probar que si $p$ es primo, la última cifra en base 6 de $p^2$ es 1.""",
             r"""Última cifra en base 6 = resto módulo 6. ¿Qué restos puede dar un primo grande?""", BASE6,
             errata=r"""Es **falso para $p=2$ y $p=3$**: $2^2=4=4_{(6)}$ y $3^2=9=13_{(6)}$. Hace falta $p>3$ (el modelo F lo corrige poniendo $p>6$; basta $p\ge5$).""",
             herramienta=("f5", "Bases")),
    Pregunta(6, 10, ["f8"], r"""Sean $(G_i,\cdot,e_i)$ grupos, $1\le i\le4$. Probar que $G_1\times G_2\times G_3\times G_4\cong G_2\times G_4\times G_3\times G_1$.""",
             r"""El isomorfismo obvio: reordenar las coordenadas.""", ISO_PRODUCTO),
    Pregunta(7, 20, ["f8", "f7"], r"""En el anillo $\mathbb Z_{64}$: (a) no es dominio; (b) todo no divisor de cero es unidad; (c) los divisores de cero forman un ideal $\mathfrak m$;
(d) $\mathfrak m$ es maximal; hallar el cuerpo $\mathbb Z_{64}/\mathfrak m$.""",
             r"""$64=2^6$: todo se decide por la paridad.""", Z64, herramienta=("f8", "ℤₙ: anillo e ideales")),
]),

Examen("F", "Modelo F", "Parcial II", "9 de enero de 2026", "2 horas y media", 100, 50, [
    Pregunta(1, 10, ["f5", "f7"], r"""Encontrar todas las soluciones enteras de $572X+156Y=104$.""",
             r"""mcd por Euclides, divide y busca una particular.""", DIOF_572, herramienta=("f7", "Diofánticas")),
    Pregunta(2, 10, ["f5", "f7"], r"""Probar que si $p>6$ es primo, la última cifra en base 6 de $p^2$ es 1.""",
             r"""Resto módulo 6 de un primo $>3$.""", BASE6 + "\n\n(Vale para todo primo $p\\ge5$; la condición $p>6$ del enunciado es más de lo necesario.)",
             herramienta=("f5", "Bases")),
    Pregunta(3, 10, ["f8"], r"""Probar que $G_1\times G_2\times G_3\times G_4\cong G_2\times G_4\times G_3\times G_1$.""",
             r"""Reordena coordenadas.""", ISO_PRODUCTO),
    Pregunta(4, 20, ["f8"], r"""Dar un grupo $G$ de orden 18 con un elemento de orden exactamente 3, y otro $H$ de orden 18 con un elemento de orden 3 que **no** sea isomorfo a $G$.""",
             r"""Uno cíclico y otro que no lo sea.""",
             r"""**$G=(\mathbb Z_{18},+)$**: $o(\overline6)=\frac{18}{\operatorname{mcd}(6,18)}=3$.

**$H=\mathbb Z_3\times\mathbb Z_6$** con la suma componente a componente: $|H|=18$ y $o\big((\overline1,\overline0)\big)=3$.

**No son isomorfos:** $G$ es **cíclico** (lo genera $\overline1$, de orden 18), mientras que en $H$ todo elemento cumple $6\cdot(a,b)=(\overline0,\overline0)$,
así que ningún elemento tiene orden 18 y $H$ no es cíclico. Un isomorfismo conserva ser cíclico ⇒ $G\not\cong H$.

(Otra opción no abeliana: $H=S_3\times\mathbb Z_3$ o el diedral $D_9$; ninguno es isomorfo a $\mathbb Z_{18}$ porque no son abelianos.)""",
             herramienta=("f8", "ℤₙ: anillo e ideales")),
    Pregunta(5, 20, ["f8", "f7"], r"""En $\mathbb Z_{64}$: (a) no es dominio; (b) no divisor de cero ⇒ unidad; (c) los divisores de cero forman un ideal $\mathfrak m$; (d) $\mathfrak m$ maximal y $\mathbb Z_{64}/\mathfrak m$.""",
             r"""Todo depende de la paridad.""", Z64, herramienta=("f8", "ℤₙ: anillo e ideales")),
    Pregunta(6, 10, ["f8"], r"""Construir el cuerpo de fracciones $\operatorname{Frac}(\mathbb Z_5)$ del dominio $\mathbb Z_5$.""",
             r"""$\mathbb Z_5$ ya es un cuerpo: ¿qué fracciones nuevas puede haber?""",
             r"""$\operatorname{Frac}(\mathbb Z_5)=\{\frac ab:a,b\in\mathbb Z_5,\ b\neq0\}$ con $\frac ab=\frac cd\iff ad=bc$, suma $\frac ab+\frac cd=\frac{ad+bc}{bd}$ y producto $\frac{ac}{bd}$.

Como $\mathbb Z_5$ es un **cuerpo** ($5$ primo), todo $b\neq0$ tiene inverso y $\frac ab=\frac{ab^{-1}}1$. La aplicación $\frac ab\mapsto ab^{-1}$ está bien definida
($ad=bc\Rightarrow ab^{-1}=cd^{-1}$), respeta suma y producto y es biyectiva con inversa $a\mapsto\frac a1$. Por tanto
$$\operatorname{Frac}(\mathbb Z_5)\cong\mathbb Z_5$$
(el cuerpo de fracciones de un cuerpo es él mismo: hay 5 clases, $\frac01,\frac11,\dots,\frac41$)."""),
    Pregunta(7, 20, ["f8", "f6"], r"""En $\mathbb Z_3$, probar que $\mathbb Z_3(i)=\{a+bi:a,b\in\mathbb Z_3,\ i^2=-1\}$ es un cuerpo con la suma y el producto inducidos. ¿Cuántos elementos tiene?""",
             r"""Es $\mathbb Z_3[x]/(x^2+1)$. ¿Es $x^2+1$ irreducible en $\mathbb Z_3$? También puedes dar el inverso explícitamente.""",
             r"""**Anillo:** con $(a+bi)+(c+di)=(a+c)+(b+d)i$ y $(a+bi)(c+di)=(ac-bd)+(ad+bc)i$ es un anillo conmutativo con 1 (es $\mathbb Z_3[x]/(x^2+1)$).

**Cuerpo:** si $a+bi\neq0$, entonces $a^2+b^2\neq0$, porque los cuadrados en $\mathbb Z_3$ son $0^2=0$, $1^2=1$, $2^2=1$, y $a^2+b^2=0$ sólo con $a=b=0$. Así
$$(a+bi)^{-1}=\frac{a-bi}{a^2+b^2},\quad\text{ya que }(a+bi)(a-bi)=a^2+b^2.$$
Equivalentemente: $x^2+1$ no tiene raíces en $\mathbb Z_3$ ($0\mapsto1$, $1\mapsto2$, $2\mapsto2$) y, al ser de grado 2, es irreducible.

**Cardinal:** $a,b\in\mathbb Z_3$ ⇒ $|\mathbb Z_3(i)|=3^2=9$ (es el cuerpo $\mathbb F_9$).""",
             herramienta=("f8", "Cocientes de polinomios")),
]),

Examen("G", "Modelo G", "Recuperación Parcial I + Parcial II", "9 de enero de 2026", "3 horas", 120, 50, [
    Pregunta(1, 10, ["f2"], r"""Probar que $\displaystyle\frac{0!}{2!}+\frac{1!}{3!}+\frac{2!}{4!}+\dots+\frac{k!}{(k+2)!}=\frac{k+1}{k+2}$.""",
             r"""Inducción. $\frac{(k+1)!}{(k+3)!}=\frac1{(k+2)(k+3)}$.""",
             r"""**Base** $k=0$: $\frac{0!}{2!}=\frac12=\frac{0+1}{0+2}$ ✓.

**Paso:** $\frac{k+1}{k+2}+\frac{(k+1)!}{(k+3)!}=\frac{k+1}{k+2}+\frac1{(k+2)(k+3)}=\frac{(k+1)(k+3)+1}{(k+2)(k+3)}=\frac{(k+2)^2}{(k+2)(k+3)}=\frac{k+2}{k+3}$ ✓.

**Sin inducción:** $\frac{j!}{(j+2)!}=\frac1{(j+1)(j+2)}=\frac1{j+1}-\frac1{j+2}$ (telescópica) ⇒ suma $=1-\frac1{k+2}$.""",
             herramienta=("f2", "Inducción")),
    Pregunta(2, 10, ["f1"], r"""Probar el teorema $[p\Rightarrow(q\Rightarrow r)]\Rightarrow[(p\Rightarrow q)\Rightarrow(p\Rightarrow r)]$.""",
             r"""Supón el consecuente falso: $p\Rightarrow q$ V y $p\Rightarrow r$ F.""",
             r"""**Por reducción al absurdo:** si fuese falso, el consecuente sería F, luego $p\Rightarrow q$ es V y $p\Rightarrow r$ es F, es decir $p=V$, $r=F$ y (por $p\Rightarrow q$) $q=V$.
Pero entonces el antecedente $p\Rightarrow(q\Rightarrow r)=V\Rightarrow(V\Rightarrow F)=F$: contradicción. **Es tautología** (es el axioma de distribución de la implicación).""",
             errata=r"""En la solución oficial, al final se pasa de $[p\wedge q\wedge\neg r]\vee(p\wedge\neg q)\vee\neg p\vee r$ a «$p\vee p\vee\neg p\vee r$» usando «$(a\wedge b)\Rightarrow a$».
Ese paso **no es válido como equivalencia** (debilita los disyuntandos). La conclusión es correcta, pero la forma limpia es: $(p\wedge\neg q)\vee\neg p\equiv\neg q\vee\neg p$,
y $(p\wedge q\wedge\neg r)\vee\neg p\vee\neg q\vee r\equiv\neg(p\wedge q\wedge\neg r)\vee(p\wedge q\wedge\neg r)$, que es tautología.""",
             herramienta=("f1", "Tabla de verdad")),
    Pregunta(3, 20, ["f3", "f4"], r"""¿Cuántas relaciones de equivalencia distintas hay en $X=\{1,2,3,4,5\}$?""",
             r"""Relación de equivalencia ↔ partición del conjunto. Cuenta particiones: número de Bell.""",
             r"""Cada relación de equivalencia corresponde a **una partición** de $X$ (sus clases). Las particiones en $k$ bloques son ${5\brace k}$ (Stirling de 2ª especie).
Con el triángulo ${n\brace k}={n-1\brace k-1}+k{n-1\brace k}$: ${5\brace1}=1$, ${5\brace2}=15$, ${5\brace3}=25$, ${5\brace4}=10$, ${5\brace5}=1$.
$$B_5=1+15+25+10+1=\boxed{52}.$$""",
             herramienta=("f4", "Números especiales")),
    Pregunta(4, 20, ["f5", "f3"], r"""$\operatorname{div}(1296)$. a) ¿Cuántos elementos tiene $A=\{a\in\operatorname{div}(1296):10\le a\le220\}$? b) Probar que $(A,\mid)$ es ordenado y hallar maximales y minimales.""",
             r"""$1296=2^4\cdot3^4$. Haz la tabla $2^m3^n$.""",
             r"""$1296=2^4\cdot3^4$, así que los divisores son $2^m3^n$ con $0\le m,n\le4$ (25 en total). Los que están entre 10 y 220:
$27,81\ (m=0)$; $18,54,162\ (m=1)$; $12,36,108\ (m=2)$; $24,72,216\ (m=3)$; $16,48,144\ (m=4)$ ⇒ **$|A|=14$**.

**Ordenado:** la divisibilidad es de orden en $\mathbb N$ (reflexiva, antisimétrica, transitiva) y lo sigue siendo restringida a $A$.

**Minimales** (ningún otro de $A$ los divide): $\{12,16,18,27\}$. **Maximales** (no dividen a ningún otro de $A$): $\{144,162,216\}$.
Por ejemplo 81 no es maximal porque $81\mid162$, y 24 no es minimal porque $12\mid24$.""",
             herramienta=("f3", "Orden y Hasse")),
    Pregunta(5, 10, ["f5", "f7"], r"""Encontrar todas las soluciones enteras de $23X+16Y=7$.""", r"""$23-16=7$.""", DIOF_23,
             herramienta=("f7", "Diofánticas")),
    Pregunta(6, 10, ["f5"], r"""Dar el mcd de los binarios $m=1010\cdots10_{(2)}$ (201) y $n=1010\cdots10_{(2)}$ (50).""",
             r"""Cada bloque «10» vale 2 por una potencia de 4. Euclides en binario.""", BINARIOS, herramienta=("f5", "Bases")),
    Pregunta(7, 20, ["f8"], r"""Probar que $G=TGL(2,\mathbb Z_3)=\left\{\begin{pmatrix}a&b\\0&c\end{pmatrix}\text{ inversibles},\ a,b,c\in\mathbb Z_3\right\}$ es un grupo no abeliano con el producto.
Calcular su orden y hallar, si es posible, subgrupos abelianos de órdenes 2, 3, 4 y 5.""",
             r"""Subgrupo de $GL(2,\mathbb Z_3)$. Inversible ⇔ $ac\neq0$. Lagrange para el orden 5.""", TGL),
    Pregunta(8, 20, ["f8", "f6"], r"""En $\mathbb Z_2[x]$ con $I=(x^2)$: a) $\mathbb Z_2[x]/I$ tiene 4 elementos. b) No es isomorfo a $\mathbb Z_4$.""",
             r"""Restos de grado $\le1$. Compara $1+1$ en los dos anillos.""", Z2X_X2, herramienta=("f8", "Cocientes de polinomios")),
], oficial=True),

Examen("H", "Modelo H", "Parcial II", "9 de enero de 2026", "3 horas", 120, 50, [
    Pregunta(1, 10, ["f5", "f7"], r"""Encontrar todas las soluciones enteras de $23X+16Y=7$.""", r"""$23-16=7$.""", DIOF_23,
             herramienta=("f7", "Diofánticas")),
    Pregunta(2, 10, ["f5"], r"""Dar el mcd de los binarios $m=1010\cdots10_{(2)}$ (201) y $n=1010\cdots10_{(2)}$ (50).""",
             r"""Euclides con los bloques «10».""", BINARIOS, herramienta=("f5", "Bases")),
    Pregunta(3, 20, ["f8"], r"""$TGL(2,\mathbb Z_3)$: grupo no abeliano, orden y subgrupos abelianos de órdenes 2, 3, 4 y 5.""",
             r"""Igual que el modelo G, pregunta 7.""", TGL),
    Pregunta(4, 30, ["f3", "f8"], r"""En $\mathbb Q$, $r\sim s\iff r-s\in\mathbb Z$. a) Es de equivalencia y $\mathbb Q/\!\sim$ es infinito. b) El cociente es grupo con la suma ($\mathbb Q/\mathbb Z$).
c) Orden de $1/5$, $-2/7$, $0.333$ en $\mathbb Q/\mathbb Z$. ¿Es $\mathbb Q/\mathbb Z$ cíclico?""",
             r"""El orden de $[p/q]$ (irreducible) es $q$. Para «cíclico»: ¿puede un solo elemento generar elementos de todos los órdenes?""",
             r"""**a)** Reflexiva ($0\in\mathbb Z$), simétrica ($s-r=-(r-s)$), transitiva ($r-t=(r-s)+(s-t)$). **Infinito:** $[1/n]\neq[1/m]$ si $2\le n<m$, porque
$0<\frac1n-\frac1m<1$ no es entero.

**b)** $[r]+[s]=[r+s]$ está **bien definida**: si $r'=r+a$, $s'=s+b$ con $a,b\in\mathbb Z$, entonces $r'+s'=(r+s)+(a+b)$. Asociativa y conmutativa (heredadas de $\mathbb Q$), neutro $[0]$, opuesto $[-r]$.

**c)** El orden de $[p/q]$ con $\operatorname{mcd}(p,q)=1$ es $q$: $k\frac pq\in\mathbb Z\iff q\mid kp\iff q\mid k$.
- $o(1/5)=5$, $\ o(-2/7)=7$, $\ o(0.333)=o\!\left(\frac{333}{1000}\right)=1000$ ($\operatorname{mcd}(333,1000)=1$).

**No es cíclico:** si fuese $\langle[p/q]\rangle$, todos sus elementos tendrían orden divisor de $q$; pero $[1/(q+1)]$ tiene orden $q+1\nmid q$. (Todos sus elementos tienen orden finito y el grupo es infinito.)""",
             errata=r"""La solución oficial calcula los órdenes pero **no responde** si $\mathbb Q/\mathbb Z$ es cíclico: la respuesta es **no** (ver arriba).""",
             herramienta=("f8", "ℤₙ: anillo e ideales")),
    Pregunta(5, 20, ["f6"], r"""Encontrar el mcd en $\mathbb Z_3[x]$ de $m(x)=x^8+x^6+x^4-x^2$ y $n(x)=x^6+x^4-x^3+x^2+x+1$.""",
             r"""Algoritmo de Euclides con coeficientes módulo 3 ($-1=2$, $2^{-1}=2$). ¡Termina cada división hasta que el grado del resto sea menor!""",
             r"""En $\mathbb Z_3$: $m=x^8+x^6+x^4+2x^2$, $\ n=x^6+x^4+2x^3+x^2+x+1$.

1. $m=x^2\cdot n+r_1$, $\ r_1=x^5+2x^3+x^2$.
2. $n=x\cdot r_1+r_2$, $\ r_2=2x^4+x^3+x^2+x+1$.
3. $r_1=(2x+2)\cdot r_2+r_3$, $\ r_3=x^3+2x+1$. (El cociente tiene **dos** términos: $2x$ y luego $+2$.)
4. $r_2=(2x+1)\cdot r_3+0$: en efecto $(2x+1)(x^3+2x+1)=2x^4+x^3+4x^2+4x+1=2x^4+x^3+x^2+x+1$ ✓.

El último resto no nulo, ya mónico, es el mcd:
$$\boxed{\operatorname{mcd}(m,n)=x^3+2x+1=x^3-x+1}\quad(\text{irreducible en }\mathbb Z_3:\ \text{no tiene raíces}).$$
(Comprobado con SymPy en $\mathbb Z_3[x]$.)""",
             errata=r"""En la solución oficial, el paso 3 se detiene en $x^4+2x^2+x$, que **tiene grado 4, igual que el divisor**: la división no había terminado (falta restar $2r_2$).
Su «$r_4=x^3+2x+1$» es en realidad el resto de esa división, y el mcd buscado. Además la solución oficial se corta **sin dar la conclusión**.""",
             herramienta=("f6", "Calculadora de polinomios")),
    Pregunta(6, 30, ["f8", "f6"], r"""En $\mathbb Z_2[x]$: a) $\mathbb Z_2[x]/(x^2)$, $\mathbb Z_2[x]/(x^2+x)$ y $\mathbb Z_2[x]/(x^2+x+1)$ tienen 4 elementos. b) Ninguno es $\cong\mathbb Z_4$. c) No son isomorfos entre sí.""",
             r"""Busca invariantes: característica, ser cuerpo, tener nilpotentes.""",
             r"""**a)** En los tres casos se divide por un polinomio de grado 2, así que los restos son $a+bx$, $a,b\in\mathbb Z_2$: $\{[0],[1],[x],[1+x]\}$.

**b)** En los tres $[1]+[1]=[0]$ (característica 2) y en $\mathbb Z_4$ $1+1=2\neq0$ (característica 4) ⇒ ninguno es $\cong\mathbb Z_4$.

**c)**
- $x^2+x+1$ es **irreducible** en $\mathbb Z_2$ (no tiene raíces: $0\mapsto1$, $1\mapsto1$) ⇒ $\mathbb Z_2[x]/(x^2+x+1)$ es un **cuerpo** ($\mathbb F_4$).
  $x^2=x\cdot x$ y $x^2+x=x(x+1)$ son reducibles ⇒ esos cocientes tienen divisores de cero y **no** son cuerpos.
- $\mathbb Z_2[x]/(x^2)$ tiene un **nilpotente** no nulo: $[x]^2=[0]$. En $\mathbb Z_2[x]/(x^2+x)$ no hay ninguno: $1^2=1$, $x^2=x$, $(x+1)^2=x^2+1=x+1$.

Ser cuerpo y tener nilpotentes se conservan por isomorfismo ⇒ los tres son **distintos dos a dos**.
(De hecho $\mathbb Z_2[x]/(x^2+x)\cong\mathbb Z_2\times\mathbb Z_2$ por el chino del resto.)""",
             herramienta=("f8", "Cocientes de polinomios")),
], oficial=True),

Examen("J", "Modelo J", "Final 2ª convocatoria", "27 de enero de 2026", "3 horas", 120, 50, [
    Pregunta(1, 10, ["f1", "f2"], r"""Probar: $\forall n\ge2,\ \neg(p_1\wedge\dots\wedge p_n)\iff(\neg p_1\vee\dots\vee\neg p_n)$.""",
             r"""Inducción en $n$. El caso $n=2$ es De Morgan (tabla de verdad).""",
             r"""**Base** $n=2$: De Morgan, $\neg(p\wedge q)\iff\neg p\vee\neg q$ (tabla: los dos lados sólo son F cuando $p=q=V$).

**Paso:** suponiéndolo para $n-1$,
$$\neg(p_1\wedge\dots\wedge p_n)\overset{\text{asoc.}}\iff\neg\big((p_1\wedge\dots\wedge p_{n-1})\wedge p_n\big)\overset{n=2}\iff\neg(p_1\wedge\dots\wedge p_{n-1})\vee\neg p_n\overset{\text{H.I.}}\iff(\neg p_1\vee\dots\vee\neg p_{n-1})\vee\neg p_n.$$
Por la asociatividad de $\vee$ es $\neg p_1\vee\dots\vee\neg p_n$ ✓.""",
             herramienta=("f1", "Equivalencias")),
    Pregunta(2, 20, ["f3"], r"""(a) Todo subconjunto finito no vacío de $(\mathbb R,\le)$ tiene máximo y mínimo. (b) Todo subconjunto finito no vacío de $(\mathbb R^n,\le_{lex})$ tiene máximo y mínimo.""",
             r"""Los dos órdenes son **totales**. Prueba el resultado general para órdenes totales por inducción en $|F|$.""",
             r"""Ambos órdenes son **totales** (dos elementos siempre se comparan; en el lexicográfico, se miran las coordenadas hasta la primera distinta).
Basta probar: en un conjunto totalmente ordenado, todo $F$ finito no vacío tiene máximo y mínimo.

**Inducción en $|F|$.** Si $|F|=1$, su único elemento es máximo y mínimo. Si $|F|=n$, quita un elemento $f_n$: $F'=F\setminus\{f_n\}$ tiene máximo $M'$ y mínimo $m'$
(hipótesis de inducción). Como el orden es total, $f_n$ y $M'$ se comparan: $\max F=\max\{M',f_n\}$; igual $\min F=\min\{m',f_n\}$ ✓.

💡 La totalidad es clave: en $(\mathcal P(A),\subseteq)$ el conjunto $\{\{1\},\{2\}\}$ es finito y no tiene máximo.""",
             herramienta=("f3", "Lexicográfico")),
    Pregunta(3, 20, ["f3"], r"""$\mathrm{Conv}(\mathbb Q)$ = sucesiones racionales convergentes (en $\mathbb R$). (a) $x\sim y\iff\lim x(n)=\lim y(n)$ es de equivalencia. (b) ¿Cuál es el cociente?""",
             r"""Es «tener la misma imagen» por $x\mapsto\lim x(n)$. ¿Qué números reales son límite de racionales?""",
             r"""**(a)** $\sim$ es la relación «misma imagen» por $L(x)=\lim x(n)$, y por tanto reflexiva, simétrica y transitiva (lo hereda de la igualdad).

**(b)** $L:\mathrm{Conv}(\mathbb Q)\to\mathbb R$ es **sobreyectiva**: todo real es límite de racionales (sus truncamientos decimales, por ejemplo).
La aplicación inducida $\hat L([x])=\lim x(n)$ está bien definida y es inyectiva por definición de $\sim$, luego es biyectiva:
$$\mathrm{Conv}(\mathbb Q)/\!\sim\ \cong\ \mathbb R.$$
(¡Así se **construyen** los números reales a partir de los racionales!)"""),
    Pregunta(4, 10, ["f5"], r"""Probar que $n=abcabc_{(10)}$ es divisible por 7, 11 y 13 para cualesquiera cifras $a,b,c$.""",
             r"""Escribe $abcabc=abc\cdot1000+abc$.""",
             r"""$n=a\cdot10^5+b\cdot10^4+c\cdot10^3+a\cdot10^2+b\cdot10+c=(100a+10b+c)(1000+1)=1001\cdot\overline{abc}$, y $1001=7\cdot11\cdot13$ ✓.""",
             herramienta=("f5", "Divisores y factorización")),
    Pregunta(5, 20, ["f7"], r"""Encontrar todas las soluciones enteras del sistema $x\equiv2\pmod{18}$, $x\equiv6\pmod{20}$.""",
             r"""Los módulos no son coprimos: primero comprueba la compatibilidad ($\operatorname{mcd}(18,20)=2$ divide a $6-2$) y luego sustituye.""",
             r"""$\operatorname{mcd}(18,20)=2$ y $2\mid6-2$ ⇒ el sistema es **compatible** y la solución es única módulo $\operatorname{mcm}(18,20)=180$.

$x=2+18t$ ⇒ $2+18t\equiv6\pmod{20}$ ⇒ $18t\equiv4\pmod{20}$ ⇒ (dividiendo entre 2) $9t\equiv2\pmod{10}$.
$9^{-1}\equiv9\pmod{10}$ ($81\equiv1$) ⇒ $t\equiv18\equiv8\pmod{10}$, $t=8+10s$.

$$x=2+18(8+10s)=\boxed{146+180s,\ s\in\mathbb Z}.$$
Comprobación: $146=8\cdot18+2$ ✓ y $146=7\cdot20+6$ ✓.""",
             errata=r"""La solución oficial empieza diciendo «18, **12** no son primos entre sí»: es una errata, los módulos son **18 y 20**.""",
             herramienta=("f7", "Chino del resto")),
    Pregunta(6, 20, ["f8", "f2"], r"""$A=\{1,2,3,4\}$. (a) $\operatorname{Biy}(A)$ es grupo con la composición. (b) Orden. (c) ¿Abeliano? (d) ¿Cíclico? (e) Elementos de orden 1, 2, 3, 4, 5, 6 si existen.""",
             r"""Es $S_4$. El orden de una permutación es el mcm de las longitudes de sus ciclos disjuntos.""",
             r"""**(a)** La composición de biyecciones es biyección (operación interna), es asociativa, el neutro es $\mathrm{id}_A$ y cada $f$ tiene inversa $f^{-1}$ biyectiva.

**(b)** $|\operatorname{Biy}(A)|=4!=24$.

**(c)** No abeliano: con $f=\begin{pmatrix}1&2&3&4\\2&3&1&4\end{pmatrix}$, $g=\begin{pmatrix}1&2&3&4\\3&2&1&4\end{pmatrix}$ es $f\circ g=1324\neq g\circ f=2134$.

**(d)** No cíclico, porque todo grupo cíclico es abeliano.

**(e)** Por ciclos disjuntos, los tipos en $S_4$ son: $\mathrm{id}$ (orden 1), $(a\,b)$ (2), $(a\,b)(c\,d)$ (2), $(a\,b\,c)$ (3), $(a\,b\,c\,d)$ (4).
- Orden 1: $\mathrm{id}$. Orden 2: $2134=(1\,2)$. Orden 3: $2314=(1\,2\,3)$. Orden 4: $2341=(1\,2\,3\,4)$.
- **Orden 5: no hay** (Lagrange: $5\nmid24$; o porque ningún mcm de longitudes con suma $\le4$ da 5).
- **Orden 6: no hay**: haría falta un 3-ciclo y una transposición disjuntos, que necesitan $3+2=5$ elementos. (Que $6\mid24$ no basta: Lagrange no tiene recíproco.)

Recuento: 1 de orden 1, 9 de orden 2, 8 de orden 3, 6 de orden 4 (total 24).""",
             errata=r"""En el apartado (e) la solución oficial dice que el orden del grupo «es **12**»; es **24**. La conclusión (no hay elementos de orden 5) no cambia porque $5\nmid24$.""",
             herramienta=("f8", "Permutaciones")),
    Pregunta(7, 20, ["f8", "f7"], r"""En $\mathbb Z_{24}$: (a) inverso de 7. (b) Unidades. (c) $I=\{3n:n\in\mathbb Z_{24}\}$ es ideal. (d) $\mathbb Z_{24}/I$ es dominio de integridad. (e) $\mathbb Z_{24}/I$ es cuerpo.""",
             r"""Unidades: coprimos con 24. Ideal: subgrupo + absorción. El cociente tiene 3 clases.""",
             r"""**(a)** $\operatorname{mcd}(7,24)=1$ ⇒ existe. $7\cdot7=49=2\cdot24+1$ ⇒ $\overline7^{-1}=\overline7$.

**(b)** Unidades = coprimos con $24=2^3\cdot3$: $\mathbb Z_{24}^\times=\{1,5,7,11,13,17,19,23\}$ ($\varphi(24)=8$).

**(c)** $I=\{0,3,6,\dots,21\}$. **Subgrupo:** $3a-3b=3(a-b)\in I$. **Absorbe:** para **todo** $r\in\mathbb Z_{24}$, $r\cdot3a=3(ra)\in I$ ⇒ es ideal.

**(d) y (e)** $\mathbb Z_{24}/I$ tiene tres clases según el resto módulo 3:
$[0]=\{0,3,\dots,21\}$, $[1]=\{1,4,\dots,22\}$, $[2]=\{2,5,8,11,14,17,20,23\}$, y $\mathbb Z_{24}/I\cong\mathbb Z_3$.
Como 3 es primo, $\mathbb Z_3$ es un **cuerpo** (todo no nulo tiene inverso: $[1]^{-1}=[1]$, $[2]^{-1}=[2]$) y por tanto **dominio de integridad**.""",
             errata=r"""Dos detalles de la solución oficial: (c) para ser ideal hay que comprobar la **absorción** $r\cdot a\in I$ para todo $r$ del anillo, no sólo $ab\in I$ con $a,b\in I$;
y en (d) la clase $[2]$ aparece con el 22 en lugar del **23**: $[2]=\{2,5,8,11,14,17,20,23\}$.""",
             herramienta=("f8", "ℤₙ: anillo e ideales")),
], oficial=True),
]


def frecuencia_temas() -> dict[str, int]:
    """Puntos totales que ha valido cada tema en los exámenes (una pregunta con varios temas reparte sus puntos)."""
    out: dict[str, float] = {}
    for e in EXAMENES:
        for p in e.preguntas:
            for t in p.temas:
                out[t] = out.get(t, 0) + p.puntos / len(p.temas)
    return dict(sorted(out.items(), key=lambda kv: -kv[1]))
