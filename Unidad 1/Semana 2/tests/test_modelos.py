from dataclasses import replace
import numpy as np
import pytest
from src.datos import DATOS
from src.modelos import Deterministico, Discreto, Estocastico, ContinuoEuler, Parametros, FabricaModelos
from src.experimentos import calibrar, ejecutar


def test_calibracion_datos_guia():
    p = calibrar()
    assert p.p0 == 1000
    assert p.periodos == 6
    assert p.r == pytest.approx(np.log(2.1) / 6)
    assert p.sigma > 0


def test_deterministico_vs_exponencial():
    p = Parametros(p0=100, r=.1, periodos=3)
    r = Deterministico().simular(p)
    assert r.poblacion[-1] == pytest.approx(100 * np.exp(.3))


def test_discreto_primera_iteracion():
    p = Parametros(p0=100, r=.1, periodos=3)
    assert Discreto().simular(p).poblacion[1] == pytest.approx(110)


def test_estocastico_reproducible_y_sin_negativos():
    p = Parametros(p0=2, r=-.8, sigma=3, periodos=20, semilla=42)
    a, b = Estocastico().simular(p), Estocastico().simular(p)
    assert np.array_equal(a.poblacion, b.poblacion)
    assert np.all(a.poblacion >= 0)


def test_sin_ruido_coincide_discreto():
    p = Parametros(p0=100, r=.1, periodos=5, sigma=0)
    assert np.allclose(Estocastico().simular(p).poblacion,
                       Discreto().simular(p).poblacion)


def test_euler_aproxima_exponencial():
    p = Parametros(p0=100, r=.12, periodos=6, dt=.01)
    euler = ContinuoEuler().simular(p)
    exacto = Deterministico().simular(p)
    assert euler.tiempo[-1] == pytest.approx(6)
    assert euler.poblacion[-1] == pytest.approx(exacto.poblacion[-1], rel=.005)


def test_cuatro_resultados_con_semilla_fija():
    resultados = ejecutar(calibrar(DATOS))
    assert len(resultados) == len(FabricaModelos.crear_todos()) == 4
    assert all(r.poblacion[0] == 1000 for r in resultados)


def test_r_negativo_produce_descenso_deterministico():
    p = Parametros(p0=100, r=-.1, periodos=3)
    valores = Deterministico().simular(p).poblacion
    assert all(np.diff(valores) < 0)


def test_parametros_invalidos():
    with pytest.raises(ValueError):
        replace(calibrar(), dt=0)
