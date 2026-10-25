"""Vista (MVC): CSV, métricas y gráficos de los cuatro modelos."""
import csv
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from .modelos import Resultado, Parametros


def _fig(ruta: Path, titulo: str, ylabel: str = "Población"):
    fig, ax = plt.subplots(figsize=(10, 5.6))
    ax.set(title=titulo, xlabel="Tiempo (períodos)", ylabel=ylabel)
    ax.grid(alpha=.27)
    return fig, ax


def graficar_comparacion(resultados: list[Resultado], datos: list[float], ruta: Path):
    fig, ax = _fig(ruta, "Comparación: modelos determinístico, discreto, estocástico y continuo")
    ax.scatter(range(len(datos)), datos, color="black", marker="x", s=60,
               label="Datos observados (guía)", zorder=5)
    for resultado in resultados:
        ax.plot(resultado.tiempo, resultado.poblacion, linewidth=2,
                marker="o" if len(resultado.tiempo) <= 8 else None, label=resultado.nombre)
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(ruta, dpi=150)
    plt.close(fig)


def graficar_serie(resultados: list[Resultado], titulos: list[str], titulo: str, ruta: Path):
    fig, ax = _fig(ruta, titulo)
    for r, label in zip(resultados, titulos):
        ax.plot(r.tiempo, r.poblacion, marker="o", label=label)
    ax.legend()
    fig.tight_layout()
    fig.savefig(ruta, dpi=150)
    plt.close(fig)


def guardar_tabla(resultados: list[Resultado], datos: list[float], ruta: Path):
    nombres = ("deterministico", "discreto", "estocastico", "continuo_euler")
    tiempos = np.arange(len(datos), dtype=float)
    with ruta.open("w", newline="", encoding="utf-8-sig") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["tiempo", "observado", *nombres])
        for i, t in enumerate(tiempos):
            fila = [i, round(float(datos[i]), 3)]
            fila += [round(float(np.interp(t, r.tiempo, r.poblacion)), 3) for r in resultados]
            escritor.writerow(fila)


def guardar_metricas(resultados: list[Resultado], datos: list[float], ruta: Path):
    obs = np.asarray(datos, dtype=float)
    with ruta.open("w", newline="", encoding="utf-8-sig") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["modelo", "rmse", "mape_porcentaje", "poblacion_final"])
        for res in resultados:
            sim = np.interp(np.arange(len(obs)), res.tiempo, res.poblacion)
            rmse = float(np.sqrt(np.mean((sim - obs) ** 2)))
            mape = float(np.mean(np.abs((sim - obs) / obs)) * 100)
            escritor.writerow([res.nombre, round(rmse, 3), round(mape, 3), round(float(sim[-1]), 3)])


def mostrar_resumen(p: Parametros, resultados: list[Resultado]):
    print(f"P0={p.p0:.2f}, r={p.r:.6f}, sigma={p.sigma:.3f}, "
          f"dt={p.dt:.3f}, períodos={p.periodos}, semilla={p.semilla}")
    print("Modelo                            Población final")
    for res in resultados:
        print(f"{res.nombre:33} {res.poblacion[-1]:12.2f}")
