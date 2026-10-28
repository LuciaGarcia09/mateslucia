from ui.teoria import Tema, S

TEMA = Tema("f8", "Matemática Finita", 8, "Grupos, anillos y cuerpos",
            "Lo que cae en el Parcial II y en los finales: grupos (ℤₙ, Sₙ, matrices), orden y Lagrange, isomorfismos, "
            "anillos, ideales, cocientes y cuerpos finitos.", [

S("grupos", "8.1 Grupos", "Exámenes E, F, G, H, J (Parcial II y finales)", [
    ("idea", "Un grupo es un «juego de movimientos» que se puede deshacer", r"""Piensa en los giros de un cubo de Rubik: puedes **encadenar** dos giros (operación), hay un giro que **no hace nada**
(neutro), todo giro se puede **deshacer** (inverso) y da igual cómo agrupes una cadena de giros (asociativa). Lo que **no** se pide
es que el orden dé igual: girar la cara A y luego la B no es lo mismo que B y luego A (grupo **no abeliano**)."""),
    ("def", "Grupo y grupo abeliano", r"""$(G,\cdot,e)$ es **grupo** si la operación es **interna** y **asociativa**, existe **neutro** $e$ ($ae=ea=a$) y todo $a$ tiene
**inverso** $a^{-1}$ ($aa^{-1}=a^{-1}a=e$). Es **abeliano** si además $ab=ba$ para todos $a,b$. El **orden del grupo** es $|G|$."""),
    ("ej", "Los grupos que salen en los exámenes", r"""
- $(\mathbb Z_n,+)$: abeliano, orden $n$, **cíclico** (lo genera $\overline1$).
- $(\mathbb Z_n^\times,\cdot)$: las **unidades** de $\mathbb Z_n$, orden $\varphi(n)$.
- $S_n=\operatorname{Biy}(\{1,\dots,n\})$ con la composición: orden $n!$, **no abeliano** si $n\ge3$ (examen J).
- Matrices inversibles con el producto, por ejemplo $TGL(2,\mathbb Z_3)$ (triangulares superiores): orden $2\cdot3\cdot2=12$, no abeliano (examen G/H).
- $\mathbb Q/\mathbb Z$ con la suma: infinito, todo elemento tiene orden finito, **no cíclico** (examen H).
- Productos $G_1\times G_2$ con la operación componente a componente."""),
    ("def", "Subgrupo y orden de un elemento", r"""$H\subseteq G$ es **subgrupo** si es no vacío y $a,b\in H\Rightarrow ab^{-1}\in H$.
El **orden** de $g$ es el menor $k\ge1$ con $g^k=e$; coincide con el orden del subgrupo cíclico $\langle g\rangle=\{e,g,g^2,\dots\}$.
En $(\mathbb Z_n,+)$: $o(\overline a)=\dfrac{n}{\operatorname{mcd}(a,n)}$. En $\mathbb Q/\mathbb Z$: $o([p/q])=q$ (con la fracción **irreducible**)."""),
    ("teo", "Lagrange", r"""Si $G$ es finito y $H\le G$, entonces $|H|$ **divide** a $|G|$. En particular $o(g)\mid|G|$ y $g^{|G|}=e$.
Uso típico: «no hay subgrupos (ni elementos) de orden 5 en un grupo de orden 12 porque $5\nmid12$». Ojo: el **recíproco es falso**
(un divisor de $|G|$ no garantiza un subgrupo de ese orden)."""),
    ("teo", "Cíclico ⇒ abeliano", r"""Si $G=\langle g\rangle$, $g^ig^j=g^{i+j}=g^jg^i$. Por tanto **un grupo no abeliano nunca es cíclico** (así se resuelve el (d) del J)."""),
    ("teo", "Permutaciones: orden por ciclos", r"""Toda permutación es producto de **ciclos disjuntos**, y su orden es el **mcm de las longitudes** de los ciclos.
En $S_4$ los tipos son $\mathrm{id}$, $(a\,b)$, $(a\,b)(c\,d)$, $(a\,b\,c)$, $(a\,b\,c\,d)$ → órdenes $1,2,2,3,4$: **no hay elementos de orden 5 ni 6**.
Se compone **de derecha a izquierda**: $(f\circ g)(i)=f(g(i))$."""),
    ("truco", "Para dar dos grupos del mismo orden NO isomorfos", r"""Busca una propiedad que uno tenga y el otro no: ser **abeliano**, ser **cíclico**, tener un elemento de cierto orden…
Para orden 18 con un elemento de orden 3 (examen F): $G=\mathbb Z_{18}$ ($\overline6$ tiene orden 3) y $H=\mathbb Z_3\times\mathbb Z_6$ ($(\overline1,\overline0)$
tiene orden 3). $G$ es cíclico y $H$ no (el orden máximo en $H$ es $\operatorname{mcm}(3,6)=6<18$), así que $G\not\cong H$. Otra opción no abeliana: $S_3\times\mathbb Z_3$."""),
    ("ia", None, r"""La criptografía que protege tus contraseñas (Diffie–Hellman, curvas elípticas) se basa en grupos donde calcular $g^k$ es fácil
y recuperar $k$ es dificilísimo. Y las simetrías de las imágenes (giros, reflexiones) forman grupos que las redes convolucionales «respetan»."""),
], "Permutaciones"),

S("isomorfismos", "8.2 Homomorfismos e isomorfismos", "Exámenes E, F, G, H", [
    ("idea", "Isomorfo = el mismo juego con otras fichas", r"""Dos grupos son **isomorfos** si son el mismo grupo con los elementos renombrados: hay un diccionario biyectivo que respeta
la operación. Para ver que **no** lo son basta encontrar algo que uno tenga y el otro no."""),
    ("def", "Homomorfismo e isomorfismo", r"""$f:G\to H$ es **homomorfismo** si $f(ab)=f(a)f(b)$ (entonces $f(e)=e$ y $f(a^{-1})=f(a)^{-1}$). **Isomorfismo** = homomorfismo biyectivo.
En anillos se pide además $f(a+b)=f(a)+f(b)$ y $f(1)=1$."""),
    ("ej", "Reordenar factores (exámenes E y F)", r"""$\varphi:G_1\times G_2\times G_3\times G_4\to G_2\times G_4\times G_3\times G_1$, $\ \varphi(g_1,g_2,g_3,g_4)=(g_2,g_4,g_3,g_1)$.
Es homomorfismo porque se opera componente a componente: $\varphi(gh)=(g_2h_2,g_4h_4,g_3h_3,g_1h_1)=\varphi(g)\varphi(h)$. Es biyectiva porque
tiene inversa $(a,b,c,d)\mapsto(d,a,c,b)$. Luego son isomorfos."""),
    ("resumen", "Invariantes que conserva un isomorfismo", r"""
| Si $G\cong H$ entonces… | Ejemplo de uso |
|---|---|
| $\lvert G\rvert=\lvert H\rvert$ | $\mathbb Z_4\not\cong\mathbb Z_5$ |
| $G$ abeliano ⇔ $H$ abeliano | $\mathbb Z_6\not\cong S_3$ |
| $G$ cíclico ⇔ $H$ cíclico | $\mathbb Z_{18}\not\cong\mathbb Z_3\times\mathbb Z_6$ |
| mismo número de elementos de cada orden | $\mathbb Z_4\not\cong\mathbb Z_2\times\mathbb Z_2$ (sólo uno tiene orden 4) |
| (anillos) misma **característica**: $1+1+\dots+1=0$ | $\mathbb Z_4\not\cong\mathbb Z_2[x]/(x^2)$ |
| (anillos) ser cuerpo, tener nilpotentes ($a\neq0$, $a^k=0$) | $\mathbb Z_2[x]/(x^2)\not\cong\mathbb Z_2[x]/(x^2+x)$ |"""),
], "Cocientes de polinomios"),

S("anillos", "8.3 Anillos, unidades y divisores de cero", "Exámenes E, F, J", [
    ("def", "Anillo, dominio y cuerpo", r"""
- **Anillo** $(A,+,\cdot)$: $(A,+)$ grupo abeliano, producto asociativo y distributivo. Lo usamos **conmutativo y con 1**.
- **Unidad**: $a$ con inverso multiplicativo. **Divisor de cero**: $a\neq0$ con $ab=0$ para algún $b\neq0$.
- **Dominio de integridad**: sin divisores de cero ($ab=0\Rightarrow a=0$ o $b=0$).
- **Cuerpo**: todo elemento no nulo es unidad. Cuerpo ⇒ dominio; **dominio finito ⇒ cuerpo**."""),
    ("teo", "En $\mathbb Z_n$ todo es unidad o divisor de cero", r"""
$\overline a$ es **unidad** ⇔ $\operatorname{mcd}(a,n)=1$ (Bézout). Si $d=\operatorname{mcd}(a,n)>1$, entonces $\overline a\cdot\overline{n/d}=\overline0$ con $\overline{n/d}\neq\overline0$: **divisor de cero**.
Así: $\mathbb Z_n$ es dominio ⇔ es cuerpo ⇔ $n$ primo."""),
    ("ej", "$\mathbb Z_{64}$ (exámenes E y F)", r"""
(a) $\overline2\cdot\overline{32}=\overline{64}=\overline0$ ⇒ no es dominio.
(b) Si $\overline a$ no es divisor de cero, $a$ es impar (si fuera par, $\overline a\cdot\overline{32}=\overline0$), luego $\operatorname{mcd}(a,64)=1$ y es unidad.
(c) Los divisores de cero (junto con el $\overline0$) son los pares: $\mathfrak m=\{\overline0,\overline2,\dots,\overline{62}\}=\langle\overline2\rangle$, que es un ideal.
(d) $\mathbb Z_{64}/\mathfrak m=\{[0],[1]\}\cong\mathbb Z_2$, que es un cuerpo ⇒ $\mathfrak m$ es **maximal**."""),
    ("ej", "$\mathbb Z_{24}$ (examen J)", r"""$7\cdot7=49\equiv1$ ⇒ $\overline7^{-1}=\overline7$. Unidades: los coprimos con $24=2^3\cdot3$: $\{1,5,7,11,13,17,19,23\}$ ($\varphi(24)=8$)."""),
], "ℤₙ: anillo e ideales"),

S("ideales", "8.4 Ideales, cocientes y cuerpos finitos", "Exámenes F, G, H, J", [
    ("idea", "Un ideal es un «agujero negro» para la multiplicación", r"""Un ideal $I$ absorbe: multiplicas cualquier cosa del anillo por algo de $I$ y caes dentro de $I$. Hacer el cociente $A/I$
es decidir que todo lo de $I$ «vale 0» y trabajar con lo que sobra: es como $\mathbb Z_n=\mathbb Z/n\mathbb Z$, donde los múltiplos de $n$ valen 0."""),
    ("def", "Ideal, cociente y maximal", r"""
$I\subseteq A$ es **ideal** si $(I,+)$ es subgrupo ($a,b\in I\Rightarrow a-b\in I$) **y absorbe**: $r\in A,\ a\in I\Rightarrow ra\in I$.
$A/I=\{a+I\}$ con $[a]+[b]=[a+b]$, $[a][b]=[ab]$. $I$ es **maximal** si $I\neq A$ y no hay ideales intermedios.
**$A/I$ es cuerpo ⇔ $I$ maximal**, y $A/I$ es dominio ⇔ $I$ primo."""),
    ("teo", "Ideales de $\mathbb Z_n$", r"""Son exactamente $\langle\overline d\rangle$ con $d\mid n$, y $\mathbb Z_n/\langle\overline d\rangle\cong\mathbb Z_d$. Es maximal ⇔ $d$ primo.
Ej. (J): $I=3\mathbb Z_{24}$, $\ \mathbb Z_{24}/I=\{[0],[1],[2]\}\cong\mathbb Z_3$, cuerpo (y por tanto dominio)."""),
    ("teo", "Cocientes de polinomios $\mathbb K[x]/(f)$", r"""
Los elementos son los **restos** de dividir entre $f$: polinomios de grado $<\operatorname{gr}f$. Con $\mathbb K=\mathbb Z_p$ hay $p^{\operatorname{gr}f}$ elementos.
**$\mathbb Z_p[x]/(f)$ es cuerpo ⇔ $f$ es irreducible** en $\mathbb Z_p[x]$.
Ej. (H): en $\mathbb Z_2[x]$ los tres cocientes por $x^2$, $x^2+x$ y $x^2+x+1$ tienen $2^2=4$ elementos $\{0,1,x,x+1\}$. Sólo el tercero es cuerpo;
en el primero $x^2=0$ ($x$ es nilpotente) y en el segundo no hay nilpotentes ($x^2=x$, $(x+1)^2=x+1$) ⇒ no son isomorfos entre sí.
Ninguno es $\cong\mathbb Z_4$: en ellos $1+1=0$ y en $\mathbb Z_4$ no."""),
    ("ej", "$\mathbb Z_3(i)$ (examen F)", r"""$x^2+1$ no tiene raíces en $\mathbb Z_3$ ($0^2+1=1$, $1^2+1=2$, $2^2+1=2$), y al ser de grado 2 es irreducible. Por tanto
$\mathbb Z_3(i)=\mathbb Z_3[x]/(x^2+1)$ es un **cuerpo de 9 elementos**. Inverso explícito: $(a+bi)^{-1}=\dfrac{a-bi}{a^2+b^2}$, y $a^2+b^2\neq0$ si $(a,b)\neq(0,0)$
(los cuadrados de $\mathbb Z_3$ son 0 y 1)."""),
    ("teo", "Cuerpo de fracciones", r"""El **cuerpo de fracciones** de un dominio $D$ son los pares $\frac ab$ ($b\neq0$) con $\frac ab=\frac cd\iff ad=bc$. Es el menor cuerpo que contiene a $D$:
$\operatorname{Frac}(\mathbb Z)=\mathbb Q$. **Si $D$ ya es cuerpo, $\operatorname{Frac}(D)\cong D$** mediante $\frac ab\mapsto ab^{-1}$. Así $\operatorname{Frac}(\mathbb Z_5)\cong\mathbb Z_5$ (examen F)."""),
    ("ojo", "La absorción no es «cerrado para el producto»", r"""Para que $I$ sea ideal hay que comprobar $ra\in I$ para **todo** $r$ del anillo, no sólo $ab\in I$ con $a,b\in I$.
En $3\mathbb Z_{24}$: $r\cdot3n=3(rn)\in I$ para todo $r\in\mathbb Z_{24}$ ✓."""),
], "Cocientes de polinomios"),
])
