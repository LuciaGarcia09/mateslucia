from ui.teoria import Tema, S

TEMA = Tema("f1", "Matemática Finita", 1, "Nociones comunes: conjuntos, lógica y demostraciones",
            "El idioma de las matemáticas: qué es un conjunto, cómo se razona y cómo se escribe una demostración.", [

S("conjuntos", "1.1 Conjuntos y elementos", "Apartados 1–5", [
    ("idea", "Un conjunto es una bolsa", r"""
Imagina una **bolsa** en la que metes cosas. Sólo importa **qué hay dentro**, no en qué orden lo metiste ni si
lo repetiste: la bolsa $\{1,2,2\}$ es la misma que $\{2,1\}$. Algo está dentro ($a\in A$) o no lo está ($a\notin A$);
no hay término medio."""),
    ("def", "Conjunto", r"""
Un **conjunto** es una colección de objetos llamados **elementos**. Se puede dar de tres formas:
- **Por extensión** (lista): $A=\{a,\,0,\,\text{rojo},\,\sqrt2\}$.
- **Por comprensión** (propiedad): $\{x : x^2-1=0\}=\{-1,1\}$ — se lee «los $x$ tales que…».
- **Parametrizado** (fórmula que los recorre): los impares son $\{2n-1 : n\in\mathbb N^+\}$."""),
    ("ej", "Ejercicio 2", r"""
- Pares: $P=\{2n : n\in\mathbb N\}=\{0,2,4,\dots\}$.
- Soluciones de $2x-3y=0$: como $2x=3y$ y 2, 3 son primos entre sí, $x=3t,\ y=2t$. Así $S=\{(3t,2t) : t\in\mathbb Z\}$
  (comprueba: $2\cdot 3t-3\cdot 2t=0$ ✓)."""),
    ("def", "Subconjunto e igualdad", r"""
- $A\subseteq B$ si **todo** elemento de $A$ está en $B$. Siempre $\varnothing\subseteq A$ y $A\subseteq A$.
- $A=B \iff A\subseteq B$ **y** $B\subseteq A$ (**doble contención**)."""),
    ("truco", "Cómo demostrar que dos conjuntos son iguales", r"""
Casi siempre por **doble contención**: «tomo $x\in A$ y demuestro que $x\in B$» y luego al revés.
¿Por qué $\varnothing\subseteq A$? Para que fallara tendría que haber un elemento de $\varnothing$ fuera de $A$, y $\varnothing$ no
tiene elementos: no hay contraejemplo posible."""),
    ("ej", "Ejercicio 5", r"""
1. $\{n\in\mathbb N : 3n-7\le 8\}=\{0,1,2,3,4,5\}$ porque $3n-7\le 8\iff n\le 5$ (y $0\in\mathbb N$ en esta asignatura).
2. $33\mathbb N\subsetneq 11\mathbb N$: $33n=11(3n)$, pero $11\in 11\mathbb N$ y $11\notin 33\mathbb N$.
3. Si $a\mathbb N=b\mathbb N$ entonces $a=b$; en cambio $a\mathbb Z=b\mathbb Z\Rightarrow a=\pm b$ (en $\mathbb Z$ el $-1$ tiene inverso: $5\mathbb Z=(-5)\mathbb Z$)."""),
], "Conjuntos y Venn (tema 2)"),

S("metodo", "1.2 El método axiomático y las demostraciones", "Apartados 6–17", [
    ("idea", "Una demostración es una cadena de fichas de dominó", r"""
Partes de cosas que aceptas (**axiomas**) o que ya están probadas, y cada paso empuja al siguiente con una regla
lógica válida hasta llegar a lo que quieres. Una demostración **no se memoriza: se entiende**.
Antes de empezar pregúntate: ¿qué **tengo** (hipótesis)? ¿qué **quiero** (tesis)? ¿qué **definiciones** aparecen?"""),
    ("def", "Proposición, axioma, demostración", r"""
- **Proposición**: afirmación que es verdadera o falsa (aunque no sepamos cuál). «¿Qué hora es?» no lo es.
- **Axioma**: proposición que se acepta sin demostrar (axiomas de conjuntos, de los naturales, Buen Orden, Elección…).
- **Demostración**: cadena de deducciones lógicas desde axiomas o resultados ya probados."""),
    ("teo", "Reglas de inferencia (apartado 10)", r"""
| Regla | Esquema | En cristiano |
|---|---|---|
| Modus ponens | $\{p,\ p\Rightarrow q\}\vdash q$ | «llueve» y «si llueve me mojo» ⇒ me mojo |
| Modus tollens | $\{p\Rightarrow q,\ \neg q\}\vdash\neg p$ | «si llueve me mojo» y «no me mojo» ⇒ no llueve |
| Silogismo | $\{p\Rightarrow q,\ q\Rightarrow r\}\vdash p\Rightarrow r$ | encadenar |
| Contraposición | $(\neg q\Rightarrow\neg p)\vdash(p\Rightarrow q)$ | probar «si no Q, no P» |
| Reducción al absurdo | $(\neg p\Rightarrow F)\vdash p$ | suponer lo contrario y llegar a algo imposible |"""),
    ("truco", "Los cuatro tipos de demostración", r"""
1. **Directa**: de la hipótesis a la tesis.
2. **Contrarrecíproco**: para $P\Rightarrow Q$ pruebo $\neg Q\Rightarrow\neg P$ (son equivalentes).
3. **Reducción al absurdo**: supongo lo contrario de lo que quiero y llego a una contradicción ($\sqrt2\notin\mathbb Q$).
4. **Contraejemplo**: para tumbar un «para todo» basta UN caso que falle."""),
    ("ej", "Contraejemplo famoso (ejercicio 11)", r"""
«Para todo $n\in\mathbb N$, $n^2+n+41$ es primo» es **falso**: para $n=0,\dots,39$ sale primo (¡por eso engaña!), pero
$n=40$ da $1600+40+41=1681=41^2$."""),
    ("ej", "Completar el cuadrado (ejercicio 12)", r"""
$ax^2+bx+c=0\ (a\neq0)\iff x^2+\tfrac bax=-\tfrac ca\iff\left(x+\tfrac{b}{2a}\right)^2=\tfrac{b^2-4ac}{4a^2}
\iff x=\dfrac{-b\pm\sqrt{b^2-4ac}}{2a}$. Cada paso es un $\iff$ (se puede deshacer)."""),
    ("ej", "√ de un entero (ejercicio 15)", r"""
Si $\sqrt[n]{m}=p/q$ con $\operatorname{mcd}(p,q)=1$, entonces $m q^n=p^n$. Un primo $r\mid q$ dividiría a $p^n$ y, por el Lema de
Euclides, a $p$: contradicción. Luego $q=1$ y la raíz es entera. **Moraleja**: $\sqrt[n]{m}$ es entero o es irracional (así se
ve que $\sqrt2,\sqrt3\notin\mathbb Q$)."""),
    ("errata", "Apartado 9 (b)", r"""En el PDF pone «$x\in\mathbb Q\Rightarrow 2x>0$», que es **falso** ($x=-1$). Se perdió el exponente: es $2^x>0$,
cierto porque $2^{p/q}=\sqrt[q]{2^p}$ es la raíz de un positivo."""),
    ("errata", "Apartado 17", r"""«Si $r\in\mathbb Q^+$ y $L=\log_{10}r$ entonces $L\in\mathbb N$ o $L\notin\mathbb Q$» es falso: $r=1/10$ da $L=-1\in\mathbb Z$.
Lo correcto: **$L\in\mathbb Z$ o $L\notin\mathbb Q$** (y si $r\ge1$, $L\in\mathbb N$)."""),
]),

S("proposicional", "1.3 Lógica proposicional: conectivos y tablas de verdad", "Apartados 18–28", [
    ("idea", "Los conectivos son interruptores", r"""
Cada proposición es una bombilla encendida (V) o apagada (F). Los conectivos combinan bombillas:
**¬** invierte, **∧** («y») exige las dos encendidas, **∨** («o», inclusivo) basta una, **⇒** sólo «miente» en un caso."""),
    ("def", "Tablas de los conectivos", r"""
| $p$ | $q$ | $\neg p$ | $p\wedge q$ | $p\vee q$ | $p\Rightarrow q$ | $p\Leftrightarrow q$ |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| V | V | F | V | V | **V** | V |
| V | F | F | F | V | **F** | F |
| F | V | V | F | V | **V** | F |
| F | F | V | F | F | **V** | V |"""),
    ("idea", "¿Por qué «F ⇒ lo que sea» es verdadero?", r"""
«Si estudias, apruebas» es una **promesa**. Sólo la rompes si **estudias y suspendes** (V ⇒ F). Si no estudias, pase lo que pase
no has mentido. Por eso $p\Rightarrow q$ es falsa sólo en la fila V, F."""),
    ("def", "Tautología, contradicción, equivalencia", r"""
- **Tautología** ($\top$): verdadera en todas las filas. **Contradicción** ($\bot$): falsa en todas. Si no, **contingencia**.
- $p\equiv q$ (**equivalentes**) si tienen la misma columna en la tabla de verdad.
- No contradicción: $p\wedge\neg p\equiv\bot$. Tercio excluso: $p\vee\neg p\equiv\top$."""),
    ("teo", "Equivalencias que hay que saber (apartados 23 y 27)", r"""
- Conmutativas, asociativas, idempotencia ($p\wedge p\equiv p$, $p\vee p\equiv p$).
- **Distributivas**: $p\wedge(q\vee r)\equiv(p\wedge q)\vee(p\wedge r)$ y $p\vee(q\wedge r)\equiv(p\vee q)\wedge(p\vee r)$.
- **De Morgan**: $\neg(p\vee q)\equiv\neg p\wedge\neg q$, $\ \neg(p\wedge q)\equiv\neg p\vee\neg q$.
- **Implicación**: $p\Rightarrow q\equiv\neg p\vee q$, y su negación $\neg(p\Rightarrow q)\equiv p\wedge\neg q$.
- **Contrarrecíproco**: $p\Rightarrow q\equiv\neg q\Rightarrow\neg p$.
- **Bicondicional**: $p\Leftrightarrow q\equiv(p\Rightarrow q)\wedge(q\Rightarrow p)$ — por eso un «si y sólo si» se prueba en dos sentidos.
- Tautologías: silogismo $[(p\Rightarrow q)\wedge(q\Rightarrow r)]\Rightarrow(p\Rightarrow r)$, modus ponens y modus tollens."""),
    ("ojo", "El error más típico", r"""
$p\Rightarrow q$ **NO** es equivalente a $q\Rightarrow p$ (el recíproco) ni a $\neg p\Rightarrow\neg q$ (el contrario).
Sólo al **contrarrecíproco** $\neg q\Rightarrow\neg p$. «Si es un perro, es un mamífero» no implica «si es un mamífero, es un perro»."""),
    ("errata", "Apartado 27", r"""Los apartados (iii) y (iv) del PDF son la misma equivalencia repetida: $\neg(p\Rightarrow q)\equiv p\wedge\neg q$."""),
], "Tabla de verdad"),

S("cuantificadores", "1.4 Predicados y cuantificadores", "Apartados 29–33", [
    ("def", "Predicado y cuantificadores", r"""
- Un **predicado** $p(x)$ es una frase con variable que se vuelve proposición al dar valor a $x$: $p(n)=$«$n$ es par».
- $\forall x,\ p(x)$: «para todo $x$». Verdadero sólo si se cumple **siempre**.
- $\exists x,\ p(x)$: «existe algún $x$». Verdadero si hay **al menos uno**."""),
    ("teo", "Negación de cuantificadores (apartado 32)", r"""
$$\neg(\forall x\ p(x))\equiv\exists x\ \neg p(x)\qquad\qquad \neg(\exists x\ p(x))\equiv\forall x\ \neg p(x)$$
«No es verdad que todos aprueben» = «alguien suspende». **Regla práctica: cambia ∀↔∃ y niega lo de dentro.**"""),
    ("ej", "Negar la definición de límite", r"""
$\lim a_n=L$: $\ \forall\varepsilon>0\ \exists n_0\ \forall n\ge n_0,\ |a_n-L|<\varepsilon$.

$L$ **no** es el límite: $\ \exists\varepsilon>0\ \forall n_0\ \exists n\ge n_0,\ |a_n-L|\ge\varepsilon$
(«hay una distancia ε a la que la sucesión se sale infinitas veces»). El «$\varepsilon>0$» y el «$n\ge n_0$» NO se niegan: indican dónde vive la variable."""),
    ("teo", "Cuantificadores con conectivos (apartado 33)", r"""
- $\forall x\,(P\wedge Q)\equiv(\forall x\,P)\wedge(\forall x\,Q)$ ✓ y $\exists x\,(P\vee Q)\equiv(\exists x\,P)\vee(\exists x\,Q)$ ✓.
- $\forall x\,(P\vee Q)\not\equiv(\forall x\,P)\vee(\forall x\,Q)$: todo número es par o impar, pero no «todos son pares» ni «todos son impares».
- $\exists x\,(P\wedge Q)\not\equiv(\exists x\,P)\wedge(\exists x\,Q)$: hay un par y hay un impar, pero ninguno es las dos cosas.
- $\forall x\,(P\Rightarrow Q)\not\equiv(\forall x P)\Rightarrow(\forall x Q)$ (contraejemplo $P$: «$x=1$», $Q$: «$x=2$»); sólo vale «⇒»."""),
    ("ojo", "El orden de los cuantificadores importa", r"""
$\forall x\ \exists y,\ y>x$ («para cada número hay uno mayor») es verdadero en $\mathbb N$.
$\exists y\ \forall x,\ y>x$ («hay un número mayor que todos») es falso. ¡Mismas piezas, distinto orden!"""),
], "Negar cuantificadores"),

S("sucesiones_cuant", "1.5 Límites y valores adherentes con cuantificadores", "Apartados 34–35", [
    ("idea", "Límite = «tan cerca como quieras, a partir de un momento»", r"""
$L$ es límite de $(a_n)$ si, por muy estrecha que sea la franja $(L-\varepsilon,L+\varepsilon)$, a partir de cierto $n_0$
**todos** los términos caen dentro. **Adherente** es más flojo: la sucesión vuelve a acercarse a $\alpha$ **infinitas veces**,
aunque no se quede allí."""),
    ("ej", "Ejercicio 34", r"""
$a_n=\dfrac{3n+275444}{n+17158}\to3$: $\ a_n-3=\dfrac{223970}{n+17158}<\dfrac{223970}{n}<\varepsilon$ si $n>\dfrac{223970}{\varepsilon}$.
Además el límite, si existe, es **único**: si hubiera dos, $L\neq L'$, con $\varepsilon=|L-L'|/2$ los términos tendrían que
estar a la vez cerca de los dos: $|L-L'|<|L-L'|$, absurdo."""),
    ("ej", "Ejercicio 35", r"""
$a_n=(-1)^n\dfrac{n}{n+1}$ tiene dos adherentes, $\{-1,1\}$ (pares $\to1$, impares $\to-1$), y **no tiene límite**.
Todo límite es adherente, pero no al revés."""),
], "Negar cuantificadores"),
])
