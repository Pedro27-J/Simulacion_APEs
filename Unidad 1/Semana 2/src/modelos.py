"""Modelo + patrón Strategy para cuatro paradigmas de crecimiento poblacional."""
from abc import ABC, abstractmethod
from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class Parametros:
    p0: float
    r: float
    periodos: int
    sigma: float = 0.0
    dt: float = 0.1
    semilla: int = 42

    def __post_init__(self):
        if self.p0 < 0 or self.periodos < 1 or self.sigma < 0 or self.dt <= 0:
            raise ValueError("p0 >= 0, periodos >= 1, sigma >= 0 y dt > 0")


@dataclass(frozen=True)
class Resultado:
    nombre: str
    tiempo: np.ndarray
    poblacion: np.ndarray


class ModeloPoblacional(ABC):
    nombre: str

    @abstractmethod
    def simular(self, p: Parametros) -> Resultado: ...


class Deterministico(ModeloPoblacional):
    nombre = "Determinístico (exponencial)"

    def simular(self, p: Parametros) -> Resultado:
        t = np.arange(p.periodos + 1, dtype=float)
        return Resultado(self.nombre, t, p.p0 * np.exp(p.r * t))


class Discreto(ModeloPoblacional):
    nombre = "Discreto"

    def simular(self, p: Parametros) -> Resultado:
        t = np.arange(p.periodos + 1, dtype=float)
        valores = [float(p.p0)]
        for _ in range(p.periodos):
            valores.append(max(0.0, valores[-1] + p.r * valores[-1]))
        return Resultado(self.nombre, t, np.array(valores))


class Estocastico(ModeloPoblacional):
    nombre = "Estocástico"

    def simular(self, p: Parametros) -> Resultado:
        rng = np.random.default_rng(p.semilla)
        t = np.arange(p.periodos + 1, dtype=float)
        valores = [float(p.p0)]
        for _ in range(p.periodos):
            ruido = rng.normal(0.0, p.sigma)
            valores.append(max(0.0, valores[-1] + p.r * valores[-1] + ruido))
        return Resultado(self.nombre, t, np.array(valores))


class ContinuoEuler(ModeloPoblacional):
    nombre = "Continuo (Euler)"

    def simular(self, p: Parametros) -> Resultado:
        # dt es un máximo: el último paso se ajusta para terminar en t=periodos.
        pasos = int(np.ceil(p.periodos / p.dt))
        t = np.linspace(0.0, float(p.periodos), pasos + 1)
        valores = np.empty(len(t), dtype=float)
        valores[0] = p.p0
        for i in range(1, len(t)):
            h = t[i] - t[i - 1]
            valores[i] = max(0.0, valores[i - 1] + h * p.r * valores[i - 1])
        return Resultado(self.nombre, t, valores)


class FabricaModelos:
    """Factory Method simple: crea los cuatro algoritmos sin condicionales de simulación."""
    @staticmethod
    def crear_todos() -> list[ModeloPoblacional]:
        return [Deterministico(), Discreto(), Estocastico(), ContinuoEuler()]
