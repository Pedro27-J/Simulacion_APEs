"""Patrón Strategy: elección intercambiable de los pesos del índice de lluvia."""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from .dominio import RegistroMeteorologico, ResultadoLluvia, factor_temperatura, clasificar


class EstrategiaIndice(ABC):
    @property
    @abstractmethod
    def nombre(self) -> str: ...

    @property
    @abstractmethod
    def pesos(self) -> tuple[float, float, float]: ...

    def __init__(self):
        if abs(sum(self.pesos) - 1.0) > 1e-10:
            raise ValueError("Los pesos deben sumar 1")

    def calcular(self, registro: RegistroMeteorologico) -> ResultadoLluvia:
        h = registro.humedad / 100.0
        n = registro.nubosidad / 100.0
        tf = factor_temperatura(registro.temperatura)
        ph, pn, pt = self.pesos
        indice = ph * h + pn * n + pt * tf
        return ResultadoLluvia(registro.hora, registro.humedad, registro.nubosidad,
                              registro.temperatura, h, n, tf, indice,
                              clasificar(indice), self.nombre)


class ModeloOriginal(EstrategiaIndice):
    nombre = "Original"
    pesos = (.5, .3, .2)  # fórmula textual de la guía


class ModeloAjustado(EstrategiaIndice):
    nombre = "Ajustado"
    pesos = (.6, .3, .1)  # propuesta explícita: más peso a la humedad


@dataclass
class SimuladorLluvia:
    """Controlador (MVC): aplica la estrategia a todos los registros."""
    estrategia: EstrategiaIndice

    def ejecutar(self, registros: list[RegistroMeteorologico]) -> list[ResultadoLluvia]:
        return [self.estrategia.calcular(registro) for registro in registros]
