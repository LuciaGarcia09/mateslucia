from ui.teoria import Tema, S

TEMA = Tema("f4", "Matemática Finita", 4, "Combinatoria",
            "Reglas de contar, palomar, variaciones, combinaciones (con y sin repetición), Stirling y particiones de enteros.", [

S("contar", "4.1 Contar: regla del producto, de la suma e inclusión–exclusión", "Apartados 101–105", [
    ("idea", "«y» multiplica, «o» suma", r"""
Vestirse con 3 camisetas **y** 2 pantalones: $3\cdot2=6$ conjuntos (cada camiseta con cada pantalón). Ir al cine **o** al teatro
(excluyentes) con 4 y 5 opciones: $4+5=9$. Antes de cualquier fórmula, piensa en **qué decisiones tomas y en qué orden**."""),
    ("teo", "Reglas básicas (ejercicio 102)", r"""
- **Producto**: si una tarea son $s$ decisiones seguidas con $n_1,\dots,n_s$ opciones, hay $n_1n_2\cdots n_s$ formas ($=|T_1\times\dots\times T_s|$).
- **Suma**: si se hace de una de $s$ maneras excluyentes con $n_1,\dots,n_s$ opciones, hay $n_1+\dots+n_s$."""),
    ("ej", "Ejercicio 103", r"""
- Aplicaciones $A\to B$ ($|A|=m$, $|B|=n$): todas $n^m$; inyectivas $n(n-1)\cdots(n-m+1)$; biyectivas $n!$ si $m=n$.
- Matrículas 0000-BBB con 20 consonantes: $10^4\cdot20^3=80\,000\,000$.
- Cadenas de longitud $<n$ con $k$ letras: $k+k^2+\dots+k^{n-1}=\frac{k^n-k}{k-1}$.
- Contraseñas con al menos una mayúscula, minúscula, cifra y especial: **inclusión–exclusión** sobre las clases que faltan."""),
    ("teo", "Inclusión–exclusión (104–105)", r"""
$$|A\cup B|=|A|+|B|-|A\cap B|,\qquad |A\cup B\cup C|=|A|+|B|+|C|-|A\cap B|-|A\cap C|-|B\cap C|+|A\cap B\cap C|.$$
En general: suma de los de 1 en 1, **menos** los de 2 en 2, **más** los de 3 en 3… ($\binom{n}{r}$ términos de cada tipo).
Idea: al sumar $|A|+|B|$ los de $A\cap B$ se cuentan dos veces; al restar te pasas con los triples y hay que devolverlos."""),
    ("ej", "Múltiplos de 2, 3 o 5 entre 1 y 100", r"""$50+33+20-16-10-6+3=74$ (los $\lfloor100/m\rfloor$ con $m$ = 2, 3, 5, 6, 10, 15, 30)."""),
], "Palomar"),

S("palomar", "4.2 El principio del palomar", "Apartados 106–110", [
    ("idea", "Más palomas que nidos", r"""Si metes 13 palomas en 12 nidos, algún nido tiene al menos 2. Lo difícil no es la fórmula, sino decidir
**qué son las palomas y qué son los nidos** (meses, restos, parejas que suman 100, número de amigos…)."""),
    ("teo", "Principio de Dirichlet", r"""
- Si $|A|>|B|$ no hay aplicación inyectiva $A\to B$.
- **General**: $N$ objetos en $k$ cajas ⇒ alguna caja tiene al menos $\lceil N/k\rceil$. (Si todas tuvieran $\le\lceil N/k\rceil-1$, habría $<N$.)"""),
    ("ej", "Ejercicios 108 y 110", r"""
- 15 personas ⇒ dos cumplen años el mismo mes ($\lceil15/12\rceil=2$).
- En una fiesta de $n\ge2$ personas, dos tienen el mismo número de amigos: los valores posibles son $0,\dots,n-1$, pero 0 y $n-1$ no
  pueden darse a la vez (el que conoce a todos conocería al que no conoce a nadie) ⇒ $n$ personas y $n-1$ valores."""),
    ("errata", "Ejercicio 109", r"""
«26 enteros distintos entre 1 y 100 siempre incluyen dos que suman 100» es **falso** (1, 2, …, 26 suman como mucho 51).
Versiones correctas: **26 impares** (25 parejas $\{1,99\},\{3,97\},\dots,\{49,51\}$) o **52 enteros cualesquiera** (49 parejas más
$\{50\}$ y $\{100\}$: 51 cajas)."""),
], "Palomar"),

S("vcp", "4.3 Variaciones, permutaciones y combinaciones", "Apartados 111–121", [
    ("idea", "¿Importa el orden? ¿Se puede repetir?", r"""
Es como pedir **helado**: en cucurucho importa qué bola va abajo (orden), en tarrina no. Y puedes o no repetir sabor.
Las cuatro respuestas dan las cuatro fórmulas básicas:

| | importa el orden | no importa el orden |
|---|---|---|
| **sin repetir** | $V_{m,n}=\dfrac{m!}{(m-n)!}$ | $\dbinom mn=\dfrac{m!}{n!(m-n)!}$ |
| **repitiendo** | $VR_{m,n}=m^n$ | $CR_{m,n}=\dbinom{m+n-1}{n}$ |"""),
    ("def", "Variaciones, permutaciones, combinaciones", r"""
- **Variación** de orden $n$ de $m$ elementos: $n$-upla de elementos **distintos**: $V_{m,n}=m(m-1)\cdots(m-n+1)$.
- **Permutación**: variación de orden $m$: $P_m=m!$ ($0!=1$).
- **Combinación**: subconjunto de $n$ elementos: $\binom mn$. Cada combinación da $n!$ variaciones ⇒ $V_{m,n}=\binom mn n!$."""),
    ("teo", "Identidades", r"""
- $\binom mn=\binom{m}{m-n}$ (elegir los que entran = elegir los que se quedan fuera).
- **Pascal**: $\binom{m+1}{n}=\binom mn+\binom{m}{n-1}$ (el elemento nuevo está o no está).
- **Binomio**: $(x+y)^n=\sum_{i=0}^n\binom ni x^iy^{n-i}$; con $x=y=1$: $\sum_i\binom ni=2^n$.
- $\binom{2n}{n}=\sum_{i=0}^n\binom ni^2$ y **Vandermonde** $\binom{m+n}{r}=\sum_{i=0}^r\binom{m}{r-i}\binom ni$ (contar subconjuntos de $A\cup B$ de dos formas).
- Recursivas: $V_{m,n+1}=(m-n)V_{m,n}$, $\ V_{m+1,n}=(m+1)V_{m,n-1}$, $\ P_{m+1}=(m+1)P_m$ (insertar el nuevo en uno de los $m+1$ huecos)."""),
    ("ej", "Ejercicio 117: alineaciones", r"""26 jugadores, 3 porteros: $3\cdot\binom{23}{10}=3\,432\,198>2^{17}$. Sin calculadora: el mayor de los 24 números
$\binom{23}{k}$ es al menos su media $2^{23}/24$, y $\binom{23}{10}=\frac{11}{13}\binom{23}{11}$."""),
    ("errata", "Apartados 112 (b), 118, 120, 121", r"""
- 112 (b): es $V_{m+1,n}=(m+1)V_{m,n-1}$ (el PDF pone $V_{m,n+1}$, que no cumple la igualdad).
- 118 y 120: las sumas empiezan en $i=0$ (falta el término $y^n$ / $\binom n0^2$).
- 121: Vandermonde cuenta subconjuntos de $A\cup B$, no de $A\cap B$."""),
], "Asistente: ¿qué fórmula uso?"),

S("repeticion", "4.4 Con repetición: permutaciones, multinomial y estrellas y barras", "Apartados 122–132", [
    ("teo", "Permutaciones con repetición y multinomial (124–127)", r"""
$m$ objetos con $i_1,\dots,i_p$ iguales entre sí: $\dfrac{m!}{i_1!\cdots i_p!}$ ordenaciones. MISSISSIPPI: $\frac{11!}{1!\,4!\,4!\,2!}=34\,650$.
Multinomial: $(x_1+\dots+x_p)^n=\sum\frac{n!}{k_1!\cdots k_p!}x_1^{k_1}\cdots x_p^{k_p}$. **Mesa redonda**: $m$ personas, $(m-1)!$ (fijas a una y ordenas al resto)."""),
    ("idea", "Estrellas y barras", r"""
Cestas de 5 frutas con 7 tipos: escribe 5 estrellas (frutas) y 6 barras (separan los 7 compartimentos):
★★ | | ★★ | ★ | | | = 2 manzanas, 2 naranjas, 1 limón. Elegir una cesta = elegir dónde van las 5 estrellas entre 11 huecos: $\binom{11}{5}=462$."""),
    ("teo", "Combinaciones con repetición (130)", r"""
Elegir $m$ elementos (con repetición, sin orden) de $p$ tipos $=$ número de soluciones de $x_1+\dots+x_p=m$, $x_i\ge0$:
$$CR_{m,p}=\binom{m+p-1}{m}=\binom{m+p-1}{p-1}.$$
Si cada tipo tiene que aparecer al menos una vez ($x_i\ge1$): $\binom{m-1}{p-1}$."""),
    ("ej", "Ejercicio 131", r"""Repartir 1000 € entre **cuatro** personas: $x+y+z+w=1000$ ⇒ $\binom{1003}{3}=167\,668\,501$."""),
    ("errata", "Apartados 130, 131, 132", r"""
- 130: es $\binom{m+p-1}{m}$ (el PDF da $\binom{m-1+p}{p}$, que con el ejercicio 129 daría 330 en vez de 462).
- 131: con 4 personas son 4 incógnitas, $x+y+z+w=1000$.
- 132: la identidad correcta es $((m+1,p))=((m,p))+((m+1,p-1))$ (se usa o no el último tipo)."""),
], "Repartos (las 12 formas)"),

S("particiones_conj", "4.5 Repartos, sobreyecciones y números de Stirling", "Apartados 133–138 y 143", [
    ("idea", "Tres preguntas antes de contar un reparto", r"""
Repartir $n$ objetos en $k$ cajas. Pregúntate: **¿se distinguen los objetos? ¿se distinguen las cajas? ¿puede quedar alguna vacía?**
Bolas numeradas en cajas con nombre: cada bola elige caja ($k^n$). Caramelos iguales: sólo importa cuántos hay en cada caja.
Cajas iguales: sólo importa quién va con quién (grupos de trabajo sin nombre)."""),
    ("teo", "Sobreyecciones por inclusión–exclusión (133)", r"""
$$|\mathrm{Sob}(n,k)|=\sum_{i=0}^k(-1)^i\binom ki(k-i)^n$$
(de las $k^n$ aplicaciones quito las que no llegan a algún elemento; las que no llegan a $i$ fijos son $(k-i)^n$)."""),
    ("def", "Stirling de 2ª especie y Bell", r"""
$S(n,k)=\left\{{n\atop k}\right\}$: formas de partir un conjunto de $n$ elementos en $k$ bloques no vacíos (= objetos distintos en cajas
**iguales** sin vacías). $\ \mathrm{Sob}(n,k)=k!\,S(n,k)$. Recurrencia: $S(n,k)=S(n-1,k-1)+k\,S(n-1,k)$ (el elemento $n$ va solo o se une a
uno de los $k$ bloques). **Bell** $B(n)=\sum_k S(n,k)$ = número de relaciones de equivalencia en $n$ elementos: 1, 2, 5, 15, 52, 203, 877."""),
    ("ojo", "Stirling de 1ª vs 2ª especie", r"""**2ª especie = bloques** (grupos sin orden interno). **1ª especie** $s(n,k)$ = permutaciones de $n$ elementos con $k$ **ciclos**
(importa el orden circular dentro de cada grupo): $s(n,k)=(n-1)s(n-1,k)+s(n-1,k-1)$. Siempre $s(n,k)\ge S(n,k)$."""),
    ("resumen", "Las situaciones de objetos en cajas (ejercicio 143)", r"""
| Objetos | Cajas | ¿Vacías? | Número |
|---|---|---|---|
| distintos | distintas | sí | $k^n$ |
| distintos | distintas | no | $k!\,S(n,k)$ |
| iguales | distintas | sí | $\binom{n+k-1}{n}$ |
| iguales | distintas | no | $\binom{n-1}{k-1}$ |
| distintos | iguales | sí | $\sum_{i=1}^k S(n,i)$ |
| distintos | iguales | no | $S(n,k)$ |
| iguales | iguales | sí | $P(n,\le k)$ |
| iguales | iguales | no | $P(n,k)$ |

Con $n=4$, $k=2$: 16, 14, 5, 3, 8, 7, 3, 2. (Y si cada caja admite como mucho 1: $V_{k,n}$, $\binom kn$, 1.)"""),
    ("errata", "Apartado 133", r"""El signo es $(-1)^i$ (dentro de la suma), no $(-1)^k$."""),
], "Números especiales"),

S("particiones_num", "4.6 Particiones de números enteros", "Apartados 139–147", [
    ("def", "Partición de un entero", r"""
Una partición de $n$ es una lista **no creciente** de positivos con suma $n$: $3+2+2$ es una partición de 7 (y $2+3+2$ es la misma).
$p(n)$ = número de particiones: 1, 2, 3, 5, 7, 11, 15 para $n=1,\dots,7$. $\ P(n,k)$ = con exactamente $k$ sumandos."""),
    ("teo", "Ferrers y recurrencia (141–142)", r"""
- **Diagrama de Ferrers**: filas de puntos. Trasponer (filas ↔ columnas) da la **conjugada** y cambia «número de sumandos» por
  «sumando mayor» ⇒ $P(n,k)=P'_k(n)$.
- $P(n,k)=P(n-1,k-1)+P(n-k,k)$: o hay un sumando 1 (lo quito) o todos son $\ge2$ (quito 1 a cada uno).
- $P(n,\le k)=P(n+k,k)$ (sumar 1 a cada una de las $k$ partes, rellenando con ceros)."""),
    ("def", "ν(n; J) (144–147)", r"""
$\nu(n;J)$ = particiones de $n$ con sumandos en $J$ en las que aparecen **todos** los de $J$. Se calcula clasificando por cuántas
veces aparece el último: $\nu(n,\{m_1,\dots,m_{j+1}\})=\sum_{k\ge1}\nu(n-k\,m_{j+1},\{m_1,\dots,m_j\})$. Ejemplos: $\nu(40,\{2,5\})=3$,
$\nu(100,\{2,3,7\})=105$."""),
    ("errata", "Apartado 145", r"""Hay que tomar $\nu(0,\{m_1\})=0$: si al quitar los $m_2$ no queda nada, no hay ningún $m_1$ y esa partición no cuenta
(la fórmula «1 si $m\mid n$» la contaría mal porque $m\mid0$)."""),
], "Particiones"),
])
