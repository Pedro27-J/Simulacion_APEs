"""Controlador: estimación transparente de parámetros y experimentos."""
from dataclasses import replace
import numpy as np
from .datos import DATOS
from .modelos import Parametros, Resultado, FabricaModelos, Estocastico, Deterministico


def calibrar(datos: list[float] = DATOS, dt: float = 0.1, semilla: int = 42) -> Parametros:
    """r = ln(P_final/P_inicial)/N; sigma = desv. de residuos discretos.

    Estas son decisiones analíticas para los datos de la guía, no fórmulas
    de calibración establecidas por el docente.
    """
    valores = np.asarray(datos, dtype=float)
    if len(valores) < 3 or np.any(valores <= 0):
        raise ValueError("Se requieren >=3 valores de población positivos")
    periodos = len(valores) - 1
    r = float(np.log(valores[-1] / valores[0]) / periodos)
    residuos = np.diff(valores) - r * valores[:-1]
    sigma = float(np.std(residuos, ddof=1))
    return Parametros(p0=float(valores[0]), r=r, periodos=periodos,
                      sigma=sigma, dt=dt, semilla=semilla)


def ejecutar(p: Parametros) -> list[Resultado]:
    return [m.simular(p) for m in FabricaModelos.crear_todos()]


def estudiar_ruido(p: Parametros) -> list[Resultado]:
    modelo = Estocastico()
    return [modelo.simular(replace(p, sigma=s)) for s in (0, p.sigma, 2 * p.sigma)]


def estudiar_tasa(p: Parametros) -> list[Resultado]:
    modelo = Deterministico()
    return [modelo.simular(replace(p, r=r)) for r in (-abs(p.r), 0., abs(p.r))]
