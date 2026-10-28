# 🌸 MatesLucía

Laboratorio de **Matemática Finita** y **Análisis** para 1º de Ingeniería de Datos e IA.
Resultados exactos (SymPy), paso a paso, y **cada resultado comprobado por un segundo método independiente**
(✅ si cuadra, ⚠️ si no).

## Arrancar

**Windows (lo más fácil):** doble clic en `iniciar.bat`. La primera vez instala todo (un par de minutos); después abre directamente.

**Desde VS Code / terminal:**
```bash
python -m venv .venv
.venv\Scripts\activate          # en Windows  (source .venv/bin/activate en Linux/WSL)
pip install -r requirements.txt
streamlit run app.py
```
Se abre en el navegador (http://localhost:8501). Requiere Python 3.10 o superior.

## Qué hay dentro (versión 2)

**14 temas** con la misma estructura: `📖 Teoría` · `🧪 calculadoras` · `✍️ Practica`.

| Matemática Finita | Análisis |
|---|---|
| 1. Conjuntos, lógica, cuantificadores y demostraciones | 1. ℝ, desigualdades, topología, ℝⁿ y ℂ |
| 2. Inducción, conjuntos, aplicaciones y cardinales | 2. Límites, equivalencias, continuidad (Bolzano, Weierstrass, uniforme) |
| 3. Relaciones de equivalencia y de orden (Hasse) | 3. Derivadas, Rolle, valor medio, L'Hôpital, Taylor, convexidad |
| 4. Combinatoria (12 formas, palomar, particiones) | 4. Integral de Riemann, TFC, técnicas, aplicaciones, impropias, Beta/Gamma |
| 5. Enteros: división, primos, bases, mcd/mcm | 5. Sucesiones: monotonía, Bolzano–Weierstrass, Cauchy, Stolz, lím sup |
| 6. Polinomios: división, Ruffini, mcd, irreducibles | 6. Series: criterios, absoluta/condicional, Leibniz, sumas, producto de Cauchy |
| 7. Aritmética modular: diofánticas, ℤₙ, Fermat/Euler/Wilson, chino | 7. Sucesiones y series de funciones, criterio M, series de potencias |

- **Teoría** de todo el temario de los apuntes y la guía, con cajas de colores (💡 idea con analogía, 📘 definición, ⭐ teorema,
  ✏️ ejemplo, 🪄 truco, ⚠️ cuidado, 🛠️ errata, 🤖 en Datos e IA) y botón «💗 ya la entiendo» que guarda tu progreso.
- **80 calculadoras** que enseñan el paso a paso y comprueban el resultado por un segundo método.
- **25 tipos de ejercicio** generados al revés (solución primero) y corregidos al instante, por tema o en Modo examen.
- **Buscador** en toda la teoría, **Erratas de los apuntes** (verificadas sobre el PDF original), **Chuleta**, **Mi progreso**
  y el **Rincón Datos e IA**.

## Cómo escribir
`x^2 + 3x`, `sen(x)`, `tg(x)`, `ln(x)`, `e^x`, `raiz(x)`, `|x-1|`, `pi`, `oo` (infinito), `arctg(x)`, `factorial(n)`, `I` (unidad imaginaria).

## Tests
```bash
pip install pytest
python -m pytest tests
```
231 tests: el núcleo matemático contra fuerza bruta y cálculo numérico, los 25 tipos de ejercicio (la respuesta buena se
acepta y la mala no), cada una de las 80 calculadoras, cada sección de teoría y cada página de la app. Además, todas las
fórmulas de la teoría (más de 2000) se han validado con KaTeX.

## Estructura
```
app.py            navegación
contenido/        la teoría de los 14 temas (como datos, fácil de ampliar)
core/             matemáticas puras (sin interfaz, testeables)
ui/               páginas de Streamlit (temas.py, herr_*.py, estilo.py…)
tests/            comprobaciones automáticas
```
