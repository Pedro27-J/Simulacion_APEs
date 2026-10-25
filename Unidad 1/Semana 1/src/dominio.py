"""Modelo (MVC): entidades y reglas del problema meteorológico."""
from dataclasses import dataclass


@dataclass(frozen=True)
class RegistroMeteorologico:
    hora: str
    humedad: float          # porcentaje [0, 100]
    nubosidad: float        # porcentaje [0, 100]
    temperatura: float      # grados Celsius

    def __post_init__(self):
        if not (0 <= self.humedad <= 100 and 0 <= self.nubosidad <= 100):
            raise ValueError("Humedad y nubosidad deben estar entre 0 y 100")


@dataclass(frozen=True)
class ResultadoLluvia:
    hora: str
    humedad: float
    nubosidad: float
    temperatura: float
    h: float
    n: float
    tf: float
    indice: float
    estado: str
    escenario: str


def factor_temperatura(celsius: float) -> float:
    """Tabla de la guía; interpola los valores intermedios (p. ej. 15 y 17 °C)."""
    temperaturas = (10, 12, 14, 16, 18, 20, 22, 24, 26, 28)
    factores = (1.0, .9, .8, .7, .6, .5, .4, .3, .2, .1)
    if celsius <= 10:
        return 1.0
    if celsius >= 28:
        return .1
    for i in range(len(temperaturas) - 1):
        t0, t1 = temperaturas[i], temperaturas[i + 1]
        if t0 <= celsius <= t1:
            return factores[i] + (factores[i + 1] - factores[i]) * (celsius - t0) / (t1 - t0)
    raise AssertionError("Temperatura no alcanzable")


def clasificar(indice: float) -> str:
    if indice < .4:
        return "Sin lluvia"
    if indice < .6:
        return "Baja posibilidad"
    if indice < .75:
        return "Lluvia probable"
    return "Lluvia"
