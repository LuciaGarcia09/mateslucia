from ui.teoria import Tema, S

TEMA = Tema("f3", "Matemática Finita", 3, "Relaciones de equivalencia y de orden",
            "Relaciones, clases de equivalencia y conjunto cociente, órdenes, cotas, extremos y diagramas de Hasse.", [

S("relaciones", "3.1 Relaciones", "Apartados 78–79", [
    ("idea", "Una relación es una lista de parejas que «se llevan»", r"""
Una relación entre $A$ y $B$ es simplemente **qué pares están relacionados**: un subconjunto $R\subseteq A\times B$.
«Ser divisor de» en $\{1,2,3,4,6\}$ es la lista $(1,1),(1,2),(2,4),(2,6),(3,6),\dots$"""),
    ("def", "Relación, dominio, opuesta", r"""
- $R\subseteq A\times B$; una relación **en** $A$ es $R\subseteq A\times A$. Escribimos $aRb$ si $(a,b)\in R$.
- $\operatorname{dom}(R)=\{a:\exists b,\ (a,b)\in R\}$, $\ \operatorname{codom}(R)=\{b:\exists a,\ (a,b)\in R\}$.
- **Opuesta**: $(b,a)\in R^{op}\iff(a,b)\in R$ («dar la vuelta a las flechas»). $(R^{op})^{op}=R$."""),
    ("def", "Las propiedades importantes", r"""
| Propiedad | Definición | Se ve en la matriz… |
|---|---|---|
| Reflexiva | $aRa$ para todo $a$ | diagonal llena de 1 |
| Simétrica | $aRb\Rightarrow bRa$ | la matriz es simétrica |
| Antisimétrica | $aRb$ y $bRa\Rightarrow a=b$ | fuera de la diagonal nunca 1 en $(a,b)$ y $(b,a)$ |
| Transitiva | $aRb$ y $bRc\Rightarrow aRc$ | (hay que comprobar los caminos de 2 pasos) |"""),
    ("ojo", "Simétrica y antisimétrica no son opuestas", r"""La igualdad es simétrica **y** antisimétrica a la vez; $\{(1,2),(2,1),(1,3)\}$ no es ninguna de las dos.
Antisimétrica no significa «no simétrica»."""),
], "Analizar una relación"),

S("equivalencia", "3.2 Relaciones de equivalencia y conjunto cociente", "Apartados 80–89", [
    ("idea", "Equivalencia = «es lo mismo para lo que me importa»", r"""
Agrupas objetos que son «iguales» para tu propósito: personas con la **misma edad**, números con el **mismo resto**, fracciones
que valen **lo mismo**. Cada grupo es una **clase**, y el conjunto de grupos es el **cociente**. Es como clasificar calcetines por
color: cada cajón es una clase y los cajones no se mezclan."""),
    ("def", "Equivalencia, clase, cociente", r"""
- Equivalencia = **reflexiva + simétrica + transitiva**. Se escribe $a\sim b$.
- Clase de $a$: $[a]=\{b\in A: a\sim b\}$.
- **Dos clases o coinciden o son disjuntas** ⇒ las clases forman una **partición** de $A$.
- Cociente: $A/\!\sim\ =\{[a]: a\in A\}$; la proyección $\pi(a)=[a]$ es sobreyectiva."""),
    ("demo", "Por qué las clases o coinciden o no se tocan", r"""
Si $c\in[a]\cap[b]$, entonces $a\sim c$ y $b\sim c$, luego (simétrica + transitiva) $a\sim b$. Si $x\in[a]$, $b\sim a\sim x$, así que
$x\in[b]$: $[a]\subseteq[b]$, y por simetría $[b]\subseteq[a]$."""),
    ("teo", "Partición ⇔ equivalencia (ejercicio 82)", r"""
Toda partición $A=P_1\sqcup\dots\sqcup P_n$ define la equivalencia «estar en el mismo trozo», y toda equivalencia define la partición en
clases. Por eso el número de equivalencias con $k$ clases en un conjunto de $n$ elementos es el **Stirling** $S(n,k)$ y el total, el
número de **Bell** $B(n)$ (tema 4)."""),
    ("ej", "Ejemplos clásicos", r"""
- **Congruencia módulo m** (83): $a\equiv b\pmod m\iff m\mid(a-b)$. Hay $m$ clases: $\mathbb Z/(m)=\{[0],\dots,[m-1]\}$.
- **ℝ módulo ℤ** (84): $r\sim s\iff r-s\in\mathbb Z$. Cada clase tiene un representante en $[0,1)$; pegando 0 y 1 sale una circunferencia.
- **Fracciones** (85): $(a,b)\sim(c,d)\iff ad=bc$ en $\mathbb N^+\times\mathbb N^+$: el cociente es $\mathbb Q^+$.
- **Igual imagen** (86): $a\sim_f a'\iff f(a)=f(a')$. Entonces $\hat f([a])=f(a)$ es una biyección $A/\!\sim_f\ \to f(A)$: toda
  aplicación = «agrupar» + «biyección» (primer teorema de isomorfía).
- $x^2+y^2$ (87): las clases son circunferencias; $2x^2+3y^2$ (88): elipses; $xy$ (89): hipérbolas y los dos ejes."""),
    ("errata", "Apartados 80, 81, 85 y 89", r"""
- 80: la simétrica es «$(a,b)\in R\Rightarrow(b,a)\in R$» (el PDF escribe un ⇔ incompleto).
- 81: la clase es $\{b\in A: a\sim b\}$, no «$b\in a$».
- 85: con $0\in\mathbb N$ **no es transitiva**: $(1,2)\sim(0,0)\sim(2,1)$ pero $(1,2)\not\sim(2,1)$. Hay que usar $\mathbb N^+\times\mathbb N^+$.
- 89: la función se llama $h$, no $f$."""),
], "Equivalencia y clases"),

S("orden", "3.3 Relaciones de orden", "Apartados 90–100", [
    ("idea", "Un orden es una escalera (que puede tener ramas)", r"""
Un orden dice quién va «antes». Si cualquier par se puede comparar es **total** (una fila india, como $\le$ en $\mathbb R$).
Si hay pares que no se comparan es **parcial** (un árbol genealógico, o la divisibilidad: ni $2\mid3$ ni $3\mid2$)."""),
    ("def", "Orden y vocabulario", r"""
Orden = **reflexiva + antisimétrica + transitiva**. Para $B\subseteq A$:

| Concepto | Qué es | ¿Tiene que estar en B? |
|---|---|---|
| Cota superior | $c\succeq b$ para todo $b\in B$ | no |
| Supremo (extremo superior) | la **menor** de las cotas superiores | no |
| Máximo | cota superior que está en $B$ | **sí** (y es único) |
| Maximal | nadie de $B$ está estrictamente por encima | **sí** (puede haber varios) |

(y lo mismo por abajo: cota inferior, ínfimo, mínimo, minimal)."""),
    ("ojo", "Máximo ≠ maximal", r"""Máximo ⇒ maximal, pero no al revés. En $\{2,3\}$ con la divisibilidad, 2 y 3 son maximales y no hay máximo.
Si hay máximo, es único y coincide con el supremo."""),
    ("def", "Diagrama de Hasse", r"""
Se dibuja $a$ debajo de $b$ y se unen si $a\prec b$ **sin nada en medio** (cobertura). No se dibujan lazos ni lo que se deduce por
transitividad. Leer el diagrama: $a\preceq b$ ⇔ se puede subir de $a$ a $b$."""),
    ("ej", "Ejercicio 94: un ínfimo que no existe", r"""
En $(\mathbb Q^+,\le)$, $A=\{q: 2\le q^2\le16\}=\mathbb Q\cap[\sqrt2,4]$. Tiene **máximo 4** pero **no tiene mínimo**, y además
**no tiene ínfimo en $\mathbb Q^+$**: sería $\sqrt2$, que no es racional. (Esto es exactamente el «agujero» que rellena $\mathbb R$.)"""),
    ("teo", "Órdenes lexicográficos (96–97)", r"""
$(a_1,a_2)\preceq_L(b_1,b_2)\iff a_1\prec b_1$ **(estricto)** o $(a_1=b_1$ y $a_2\preceq b_2)$: el orden del diccionario. Es total ⇔ $\preceq$ es total.
En palabras: «casa» ≺ «casco» (4ª letra) y «casa» ≺ «casas» (prefijo). El **inverso** decide primero por la última coordenada; en
palabras compara antes la longitud (a, b, …, aa, ab, …)."""),
    ("def", "Preorden y buen orden", r"""
- **Preorden**: reflexiva + transitiva. Ej.: $|A|\le|B|$ en $\mathcal P(X)$; la divisibilidad en $\mathbb Z$ ($2\mid-2$ y $-2\mid2$ con $2\neq-2$).
- $(\mathbb N,\mid)$ sí es orden **parcial**: máximo 0 (todo divide a 0) y mínimo 1.
- **Buen orden**: orden total en el que todo subconjunto no vacío tiene mínimo. $(\mathbb N,\le)$ sí; $\mathbb Z,\mathbb Q,\mathbb R$ con $\le$ no.
  En un conjunto **finito**, buen orden ⇔ orden total."""),
    ("errata", "Apartados 94, 95, 96, 97, 98", r"""
- 94 (b): el ínfimo **no existe** en $\mathbb Q^+$ (el PDF dice que sí).
- 95: en $(\mathcal P(\mathbb N),\subseteq)$ el supremo de los finitos sí existe ($\mathbb N$), pero no es máximo.
- 96: falta el «≺» estricto en la primera condición (con «⪯» no sería antisimétrica). 97: el inverso se llama $\preceq_I$, no $\preceq_L$.
- 98 (iii): se repite la definición; se entiende $A^B=\{X\subseteq A: X\cap B=\varnothing\}=\mathcal P(A-B)$."""),
], "Orden y Hasse"),
])
