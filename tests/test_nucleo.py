"""Tests del núcleo matemático: todo se contrasta con SymPy o con fuerza bruta."""
import random
import sympy as sp
import pytest

import core  # noqa: F401
from core import polinomios as P, enteros as E, combinatoria as C, analisis as A
from core.parsing import leer, x
from core.ejercicios import GENERADORES, generar


def poly_rand(rnd, g, c=6):
    return sum(rnd.randint(-c, c) * x ** i for i in range(g + 1)) + x ** (g + 1) * rnd.choice([1, 2, -3])


# ------------------------------------------------------------- polinomios
def test_ejercicio_de_clase():
    K = P.Cuerpo()
    A_ = P.desde_expr(leer("x^10+11x^8+46x^6+90x^4+81x^2+27"), K)
    B_ = P.desde_expr(leer("x^10+9x^8+30x^6+46x^4+33x^2+9"), K)
    d = P.division(A_, B_, K)
    assert P.a_expr(d.cociente) == 1
    assert P.a_expr(d.resto) == sp.expand(2 * x ** 8 + 16 * x ** 6 + 44 * x ** 4 + 48 * x ** 2 + 18)
    g = P.mcd_extendido(A_, B_, K)
    assert sp.expand(P.a_expr(g.mcd) - (x ** 2 + 1) ** 2 * (x ** 2 + 3) ** 2) == 0


@pytest.mark.parametrize("p", [None, 2, 3, 5, 7, 11])
def test_division_y_mcd_aleatorios(p):
    rnd = random.Random(p or 0)
    K = P.Cuerpo(p)
    for _ in range(60):
        a = poly_rand(rnd, rnd.randint(0, 7))
        b = poly_rand(rnd, rnd.randint(0, 5))
        if rnd.random() < 0.4:   # forzar factor común
            comun = poly_rand(rnd, rnd.randint(1, 2), 3)
            a, b = sp.expand(a * comun), sp.expand(b * comun)
        A_, B_ = P.desde_expr(a, K), P.desde_expr(b, K)
        if P.es_cero(B_):
            continue
        d = P.division(A_, B_, K)
        assert P.verificar_division(d, K)
        if p is None:
            q_ref, r_ref = sp.div(sp.Poly(a, x), sp.Poly(b, x))
            assert sp.expand(P.a_expr(d.cociente) - q_ref.as_expr()) == 0
            assert sp.expand(P.a_expr(d.resto) - r_ref.as_expr()) == 0
        res = P.mcd_extendido(A_, B_, K)
        assert all(P.verificar_mcd(res, K).values())


def test_cuerpo_no_primo():
    with pytest.raises(ValueError):
        P.Cuerpo(6)


def test_ruffini():
    K = P.Cuerpo()
    rf = P.ruffini(P.desde_expr(leer("x^3-2x^2-x+2"), K), 1, K)
    assert rf.resto == 0 and P.a_expr(rf.cociente) == sp.expand(x ** 2 - x - 2)


# ------------------------------------------------------------- enteros
def test_enteros_aleatorios():
    rnd = random.Random(1)
    for _ in range(500):
        a, b = rnd.randint(-10 ** 6, 10 ** 6), rnd.randint(-10 ** 6, 10 ** 6)
        if a == b == 0:
            continue
        ee = E.euclides_extendido(a, b)
        assert ee.d == sp.gcd(a, b) and ee.s * a + ee.t * b == ee.d


def test_congruencias_fuerza_bruta():
    for m in range(1, 40):
        for a in range(0, m):
            for b in range(0, m):
                cg = E.congruencia_lineal(a, b, m)
                ref = [v for v in range(m) if (a * v - b) % m == 0]
                assert sorted(cg.soluciones) == ref, (a, b, m)


def test_diofantica():
    rnd = random.Random(2)
    for _ in range(300):
        a, b, c = rnd.randint(-60, 60), rnd.randint(-60, 60), rnd.randint(-200, 200)
        if a == b == 0:
            continue
        d = E.diofantica(a, b, c)
        if d.tiene_solucion:
            for l in range(-3, 4):
                assert a * (d.x0 + d.paso_x * l) + b * (d.y0 + d.paso_y * l) == c
        else:
            assert c % sp.gcd(a, b) != 0


def test_chino_fuerza_bruta():
    rnd = random.Random(3)
    for _ in range(300):
        mods = [rnd.randint(2, 15) for _ in range(rnd.randint(2, 3))]
        res = [rnd.randint(0, m - 1) for m in mods]
        t = E.chino_del_resto(res, mods)
        M = sp.ilcm(*mods)
        ref = [v for v in range(M) if all(v % m == r for r, m in zip(res, mods))]
        if t.tiene_solucion:
            assert ref == [t.x] and t.M == M
        else:
            assert ref == []


def test_potencias():
    for b in range(-5, 12):
        for e in range(0, 60, 7):
            for m in range(1, 30):
                assert E.potencia_modular(b, e, m)[0] == pow(b, e, m)


# ------------------------------------------------------------- combinatoria
def test_doce_formas_fuerza_bruta():
    for k in range(0, 7):
        for n in range(0, 6):
            for D in (True, False):
                for Cj in (True, False):
                    for cond in ("libre", "inyectiva", "sobreyectiva"):
                        assert C.doce_formas(k, n, D, Cj, cond).numero == C.doce_formas_fuerza_bruta(k, n, D, Cj, cond)


def test_selecciones_fuerza_bruta():
    for n in range(0, 7):
        for k in range(0, 6):
            for o in (True, False):
                for r in (True, False):
                    assert C.seleccion(n, k, o, r).numero == C.seleccion_fuerza_bruta(n, k, o, r)


def test_numeros_especiales():
    from sympy.functions.combinatorial.numbers import stirling, partition
    for n in range(10):
        for k in range(10):
            assert C.stirling2(n, k) == stirling(n, k)
            assert C.stirling1(n, k) == stirling(n, k, kind=1, signed=False)
    assert [C.bell(i) for i in range(8)] == [1, 1, 2, 5, 15, 52, 203, 877]
    assert [C.desarreglos(i) for i in range(8)] == [1, 0, 1, 2, 9, 44, 265, 1854]
    assert [C.particiones_hasta(i, i) for i in range(10)] == [int(partition(i)) for i in range(10)]


def test_recurrencias():
    for coefs, f, ini in [([1, 1], 0, [0, 1]), ([5, -6], 0, [1, 4]), ([4, -4], 0, [1, 4]), ([2], "n", [1]),
                          ([3], "2^n", [1]), ([0, 1], 0, [1, 2])]:
        cerrada, *_r, ok, nn = C.resolver_recurrencia(coefs, sp.sympify(f), ini)
        assert ok, (coefs, f, ini)


# ------------------------------------------------------------- análisis
@pytest.mark.parametrize("f,a,esperado", [("sen(x)/x", "0", "1"), ("(1+1/x)^x", "oo", "e"), ("(x^2-4)/(x-2)", "2", "4"),
                                          ("(1-cos(x))/x^2", "0", "1/2"), ("x*ln(x)", "0", "0")])
def test_limites(f, a, esperado):
    lado = "+" if f == "x*ln(x)" else "+-"
    Li = A.limite(leer(f), leer(a), lado)
    assert sp.simplify(Li.valor - leer(esperado)) == 0
    assert Li.coincide_numerico


def test_derivadas_numericas():
    for t in ["x^2*sen(x)", "ln(x^2+1)*e^(3x)", "arctg(2x)/(x^2+1)", "raiz(x^2+4)", "e^(sen(x))", "x^x"]:
        f = leer(t)
        assert A.comprobar_derivada(f, sp.diff(f, x)), t
        assert A.comprobar_derivada(f, sp.diff(f, x) + 0.001) is False, t


def test_integrales():
    for t, a, b in [("x*e^x", 0, 1), ("1/x^2", 1, sp.oo), ("x*cos(x)", 0, sp.pi), ("1/(x^2+1)", -sp.oo, sp.oo)]:
        I = A.integral(leer(t), a, b)
        assert I.comprobacion and I.coincide, t


def test_estudio_funciones():
    E_ = A.estudio_funcion(leer("x^3-3x"))
    assert [(c, y) for c, y, _ in E_.extremos] == [(-1, 2), (1, -2)]
    E_ = A.estudio_funcion(leer("ln(x)/x"))
    assert E_.asintota_h == {"+∞": 0} and [c for c, *_ in E_.asintotas_v] == [0]
    E_ = A.estudio_funcion(leer("(x^2-1)/(x-2)"))
    assert E_.asintota_o == {"+∞": x + 2, "−∞": x + 2}
    E_ = A.estudio_funcion(leer("|x|"))
    assert [(c, t) for c, _, t in E_.extremos] == [(0, "mínimo relativo")]


def test_series():
    assert A.estudiar_serie(leer("1/n^2")).suma == sp.pi ** 2 / 6
    assert A.estudiar_serie(leer("1/n")).convergente is False
    assert A.estudiar_serie(leer("(1/2)^n"), 0).suma == 2


def test_parsing_notacion_espanola():
    assert leer("2sen(x)cos(x)") == 2 * sp.sin(x) * sp.cos(x)
    assert leer("3ln(x)") == 3 * sp.log(x)
    assert leer("|x-1|") == sp.Abs(x - 1)


def test_son_iguales():
    assert A.son_iguales(leer("2sen(x)cos(x)"), leer("sen(2x)"))
    assert A.son_iguales(leer("(x-1)e^x"), leer("x e^x - e^x"))
    assert not A.son_iguales(leer("x+1"), leer("x+1.0001"))


# ------------------------------------------------------------- ejercicios
@pytest.mark.parametrize("asig,tema", [(a, t) for a in GENERADORES for t in GENERADORES[a]])
def test_ejercicios_se_corrigen_bien(asig, tema):
    for semilla in range(15):
        ej = generar(asig, tema, semilla)
        buenas = {k: sp.sstr(v) if not isinstance(v, str) else v for k, v in ej._correctas.items()}
        ok, msg = ej.corregir(buenas)
        assert ok, (tema, semilla, buenas, msg)
        if "oo" in buenas.values():
            continue
        malas = {k: (v + " + 1") if k != "x" or tema != "Congruencias lineales" else "999" for k, v in buenas.items()}
        ok, _ = ej.corregir(malas)
        assert not ok, (tema, semilla, malas)
