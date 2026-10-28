from ui.teoria import Tema, S

TEMA = Tema("f7", "Matemática Finita", 7, "Aritmética modular",
            "Ecuaciones diofánticas, congruencias y el anillo ℤₙ, inversos, Fermat, Wilson, Euler, sistemas lineales y el teorema chino de los restos.", [

S("diofanticas", "7.1 Ecuaciones diofánticas", "Apartados 195–200", [
    ("idea", "Ecuaciones donde sólo valen enteros", r"""
«¿Puedo pagar exactamente 30 € con billetes de 12 y de 42?» es $12x+42y=30$ con $x,y$ enteros. Como todo lo que puedes
formar con 12 y 42 es múltiplo de $\operatorname{mcd}(12,42)=6$, sólo puedes formar múltiplos de 6. ¡Ese es todo el truco!"""),
    ("teo", "Cuándo hay solución (197, 199)", r"""
$$a_1X_1+\dots+a_nX_n=b\ \text{ tiene solución en }\mathbb Z\iff\operatorname{mcd}(a_1,\dots,a_n)\mid b.$$
Para dos variables $aX+bY=c$, con $d=\operatorname{mcd}(a,b)=\lambda a+\mu b$:"""),
    ("latex", None, r"(x_0,y_0)=\left(\frac{c\lambda}{d},\ \frac{c\mu}{d}\right),\qquad (x,y)=\left(x_0+\frac{b}{d}t,\ \ y_0-\frac{a}{d}t\right),\ t\in\mathbb Z"),
    ("teo", "Estructura de las soluciones (198–199)", r"""
- La **homogénea** $aX+bY=0$ tiene soluciones $\left(\frac{bt}{d},-\frac{at}{d}\right)$.
- La **diferencia** de dos soluciones de $aX+bY=c$ es solución de la homogénea ⇒ solución general = **particular + homogénea**
  (como en las ecuaciones diferenciales y en los sistemas lineales)."""),
    ("ej", "Ejercicio 200: $63X+84Y=441$", r"""
$d=\operatorname{mcd}(63,84)=21$ y $21\mid441$ ✓. Dividiendo: $3X+4Y=21$. Bézout: $1=3\cdot(-1)+4\cdot1$ ⇒ $(x_0,y_0)=(-21,21)$.
General: $(-21+4t,\ 21-3t)$. Comprueba con $t=6$: $(3,3)$, $63\cdot3+84\cdot3=441$ ✓."""),
    ("errata", "Apartados 198 y 199", r"""
- 198: las soluciones son $\left(\frac{bt}{d},-\frac{at}{d}\right)$ (el PDF intercambia el orden) y en la prueba es $y_0=a't_2$, no $b't_2$.
- 199 (IV): la general es $\left(x_0+\frac{bt}{d},\ y_0-\frac{at}{d}\right)$; (V): la condición es $\operatorname{mcd}(a,b)\mid c$, no al revés."""),
], "Diofánticas"),

S("zn", "7.2 Congruencias y el anillo ℤₙ", "Apartados 201–208", [
    ("idea", "La aritmética del reloj", r"""
En un reloj de 12 horas, $10+5=3$. Dos números son **congruentes** módulo $n$ si dejan el mismo resto: $15\equiv3\pmod{12}$.
$\mathbb Z_n$ es el «reloj de $n$ horas»: sus elementos son las clases $[0],[1],\dots,[n-1]$."""),
    ("def", "Congruencia y ℤₙ (201–202)", r"""
$a\equiv b\pmod n\iff n\mid(a-b)$. Es de equivalencia y hay exactamente $n$ clases: $[r]=\{r+tn: t\in\mathbb Z\}$.
Representantes canónicos: $0,1,\dots,n-1$ (pero $[12]=[0]$ en $\mathbb Z_4$, $[-2]=[2]$…)."""),
    ("teo", "Operaciones bien definidas (203–207)", r"""
$[a]+[b]=[a+b]$ y $[a]\cdot[b]=[ab]$ **no dependen del representante**: si $a'=a+tn$, $b'=b+sn$, entonces
$a'b'=ab+(tb+as+tsn)n$. Con ellas $(\mathbb Z_n,+)$ es un **grupo abeliano** y $(\mathbb Z_n,+,\cdot)$ un **anillo conmutativo**."""),
    ("truco", "Reducir antes de operar", r"""Para calcular $123\cdot456 \bmod 7$ no hace falta multiplicar: $123\equiv4$, $456\equiv1$ ⇒ $4\cdot1=4$. Reduce en cada paso."""),
    ("ej", "Más anillos (208)", r"""$(\mathcal P(X),\triangle,\cap)$ es un anillo: el neutro de la «suma» $\triangle$ es $\varnothing$, el del «producto» $\cap$ es $X$, y el
opuesto de $A$ es él mismo ($A\triangle A=\varnothing$). Un anillo raro: $A\cdot A=A$ y $1+1=0$."""),
    ("errata", "Apartado 201", r"""Las clases son $\{1+tn: t\in\mathbb Z\}$ (el PDF escribe «$n\in\mathbb Z$» como índice, mezclando la $n$ del módulo)."""),
], "ℤₙ: tablas y unidades"),

S("inversos", "7.3 Inversos, Fermat, Wilson y Euler", "Apartados 209–222", [
    ("teo", "Cuándo hay inverso (210)", r"""
$$[m]\text{ tiene inverso en }\mathbb Z_n\iff\operatorname{mcd}(m,n)=1.$$
(⇐) Bézout: $\lambda m+\mu n=1$ ⇒ $[\lambda][m]=[1]$. (⇒) si $xm-tn=1$, el mcd divide a 1. **El inverso se calcula con Euclides extendido**:
$[7]^{-1}=[15]$ en $\mathbb Z_{26}$ porque $3\cdot26-11\cdot7=1$ y $-11\equiv15$."""),
    ("teo", "Cancelación (211)", r"""Si $\operatorname{mcd}(a,m)=1$: $ax\equiv ay\iff x\equiv y\pmod m$. Si no son coprimos falla: $3\cdot2\equiv3\cdot4\pmod6$ pero $2\not\equiv4$."""),
    ("teo", "Pequeño teorema de Fermat (212–213)", r"""
$p$ primo y $p\nmid a$ ⇒ $a^{p-1}\equiv1\pmod p$. Y para cualquier $a$: $a^p\equiv a\pmod p$.
**Idea de la prueba**: $a,2a,\dots,(p-1)a$ son los $p-1$ restos no nulos desordenados; multiplicándolos, $a^{p-1}(p-1)!\equiv(p-1)!$ y se cancela."""),
    ("teo", "Cuerpos ℤₚ (214–216)", r"""
Un **cuerpo** es un anillo donde todo $a\neq0$ tiene inverso ($\mathbb Q,\mathbb R,\mathbb C$). $\mathbb Z_m$ es cuerpo $\iff m$ **primo**.
Si $m=ab$ no es primo, $[a][b]=[0]$ con $[a],[b]\neq0$ (divisores de cero) y $[a]$ no puede tener inverso."""),
    ("teo", "Wilson (217)", r"""
$p$ es primo $\iff(p-1)!\equiv-1\pmod p$. Para $p\ge5$: en $2\cdot3\cdots(p-2)$ cada número se empareja con su inverso **distinto**
(los únicos con $x^2\equiv1$ son $\pm1$), así que ese producto vale 1, y queda $1\cdot1\cdot(p-1)\equiv-1$."""),
    ("def", "Función φ de Euler (218–219)", r"""
$\varphi(n)=|\{1\le m\le n:\operatorname{mcd}(m,n)=1\}|$ = número de **unidades** de $\mathbb Z_n$.
$\varphi(p)=p-1$, $\ \varphi(p^k)=p^k-p^{k-1}$, multiplicativa si son coprimos, y en general $\varphi(n)=n\prod_{p\mid n}\left(1-\frac1p\right)$.
Ejemplos: $\varphi(100)=40$, $\varphi(360)=96$; $\mathbb Z_8^\times=\{1,3,5,7\}$, $\mathbb Z_6^\times=\{1,5\}$."""),
    ("teo", "Teorema de Euler (220–222)", r"""
$\operatorname{mcd}(a,m)=1\Rightarrow a^{\varphi(m)}\equiv1\pmod m$ (generaliza Fermat). **Consecuencia**: los exponentes se pueden
reducir módulo $\varphi(m)$: si $a\equiv b\pmod{\varphi(m)}$, entonces $x^a\equiv x^b\pmod m$."""),
    ("ej", "Ejercicio 221: las 3 últimas cifras de $7^{103}$", r"""
Piden $7^{103}\bmod1000$. Módulo 8: $7^2\equiv1$ ⇒ $7^{103}\equiv7$. Módulo 125: $\varphi(125)=100$ ⇒ $7^{103}\equiv7^3=343\equiv93$.
Teorema chino: $x\equiv7\ (8)$, $x\equiv93\ (125)$ ⇒ $x=343$. **Las últimas cifras son 343.**"""),
    ("errata", "Apartado 217", r"""La prueba de Wilson del PDF no dice que cada $x\in\{2,\dots,p-2\}$ tiene inverso **distinto de sí mismo**; sin eso no
se pueden formar las parejas."""),
], "Fermat, Euler y Wilson"),

S("lineales", "7.4 Congruencias lineales y sistemas módulo p", "Apartados 223–225 y 230–233", [
    ("teo", r"Una incógnita: $aX\equiv b\pmod m$ (230)", r"""
Sea $d=\operatorname{mcd}(a,m)$. **Tiene solución ⇔ $d\mid b$**, y entonces hay exactamente $d$ soluciones módulo $m$.
Receta: divide todo entre $d$, multiplica por el inverso de $a/d$ módulo $m/d$, y suma múltiplos de $m/d$.
Ej.: $6X\equiv9\pmod{15}$: $d=3$ ⇒ $2X\equiv3\pmod5$ ⇒ $X\equiv4$ ⇒ $X\in\{4,9,14\}$."""),
    ("teo", "Varias incógnitas módulo p primo (224)", r"""
$a_1X_1+\dots+a_nX_n\equiv b\pmod p$: si algún $a_i\not\equiv0$, despejas $X_i$ y las demás son libres: **$p^{n-1}$ soluciones**.
Si todos los $a_i\equiv0$: hay $p^n$ soluciones si $b\equiv0$ y ninguna si no."""),
    ("teo", "Sistemas módulo p (225)", r"""
Como $\mathbb Z_p$ es un cuerpo, vale todo el álgebra lineal: **Gauss** y **Rouché–Frobenius**. Compatible ⇔ $\operatorname{rg}A=\operatorname{rg}(A|b)$, y
entonces hay $p^{\,n-\operatorname{rg}A}$ soluciones."""),
    ("teo", "Varias incógnitas módulo m cualquiera (232)", r"""
Con $g=\operatorname{mcd}(a_1,\dots,a_n,m)$: **solución ⇔ $g\mid b$**, y entonces hay $g\cdot m^{n-1}$ soluciones en $\mathbb Z_m^n$.
Ej. 231: $2X+3Y\equiv10\pmod{30}$: $g=1$ ⇒ 30 soluciones. Ej. 233: módulo $2310=2\cdot3\cdot5\cdot7\cdot11$ con $g=1$ ⇒ $2310^5$ soluciones."""),
    ("def", "Libre de cuadrados (228–229)", r"""$m$ es libre de cuadrados si ningún cuadrado $>1$ lo divide ⇔ en su factorización todos los exponentes son 1 ($30$ sí; $12$, $18$ no).
Entonces una congruencia módulo $m$ equivale a una congruencia módulo cada primo (teorema chino), y cada una es un problema en un cuerpo."""),
    ("errata", "Apartado 230", r"""El resultado ($d\mid b$ y $d$ soluciones) vale para **cualquier** $m$; no hace falta que sea libre de cuadrados."""),
], "Sistemas mód p"),

S("chino", "7.5 El teorema chino de los restos", "Apartados 226–227", [
    ("idea", "Construir un número que sea 1 en un sitio y 0 en los demás", r"""
Para $x\equiv2\ (8)$, $x\equiv3\ (15)$: con Bézout $1=2\cdot8-1\cdot15$. El número $-15$ es $\equiv1$ módulo 8 y $\equiv0$ módulo 15;
el $16$ es $\equiv0$ módulo 8 y $\equiv1$ módulo 15. Combinando: $x=2\cdot(-15)+3\cdot16=18$, y la solución es $x\equiv18\pmod{120}$."""),
    ("teo", "Teorema chino de los restos (227)", r"""
Si $n_1,\dots,n_s$ son **primos entre sí dos a dos**, el sistema $x\equiv b_i\pmod{n_i}$ tiene solución **única módulo $N=n_1\cdots n_s$**:"""),
    ("latex", None, r"x\equiv b_1e_1N_1+\dots+b_se_sN_s\pmod N,\qquad N_i=\frac{N}{n_i},\quad e_i\equiv N_i^{-1}\pmod{n_i}"),
    ("ej", "La adivinanza de Sun Zi", r"""
$x\equiv2\ (3)$, $x\equiv3\ (5)$, $x\equiv2\ (7)$: $N=105$; $N_i=35,21,15$; $e_i=2,1,1$. $x\equiv140+63+30=233\equiv23\pmod{105}$ ✓."""),
    ("truco", "Si los módulos NO son coprimos", r"""Se resuelve por sustitución: $x=b_1+n_1k$, se impone la segunda congruencia y se despeja $k$. Hay solución ⇔
$\operatorname{mcd}(n_1,n_2)\mid b_2-b_1$, y entonces es única módulo $\operatorname{mcm}(n_1,n_2)$. (La pestaña **Chino del resto** lo hace así.)"""),
    ("ia", None, r"""El teorema chino y la exponenciación modular rápida son la base de **RSA**: cifrar es $c=m^e\bmod n$ y descifrar $m=c^d\bmod n$ con
$d=e^{-1}\bmod\varphi(n)$ (Euclides extendido). Funciona por el teorema de Euler. Pruébalo en el **Rincón Datos e IA**."""),
], "Chino del resto"),
])
