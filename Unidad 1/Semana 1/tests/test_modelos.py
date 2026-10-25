import pytest
from src.dominio import RegistroMeteorologico, factor_temperatura, clasificar
from src.datos import REGISTROS
from src.modelos import ModeloOriginal, ModeloAjustado, SimuladorLluvia


def test_ejemplo_documento():
    caso = RegistroMeteorologico("prueba", 90, 80, 18)
    assert ModeloOriginal().calcular(caso).indice == pytest.approx(.81)


def test_interpolacion_temperaturas_no_tabulares():
    assert factor_temperatura(15) == pytest.approx(.75)
    assert factor_temperatura(17) == pytest.approx(.65)
    assert factor_temperatura(9) == 1.0
    assert factor_temperatura(29) == .1


def test_reglas_estado_en_umbral():
    assert [clasificar(i) for i in (.399, .4, .6, .75)] == [
        "Sin lluvia", "Baja posibilidad", "Lluvia probable", "Lluvia"
    ]


def test_registros_y_estrategias():
    original = SimuladorLluvia(ModeloOriginal()).ejecutar(REGISTROS)
    ajustado = SimuladorLluvia(ModeloAjustado()).ejecutar(REGISTROS)
    assert len(original) == len(ajustado) == 9
    assert any(abs(a.indice - b.indice) > .0001 for a, b in zip(original, ajustado))
    assert all(0 <= r.indice <= 1 for r in original + ajustado)


def test_validacion_porcentaje():
    with pytest.raises(ValueError):
        RegistroMeteorologico("prueba", 101, 30, 20)
