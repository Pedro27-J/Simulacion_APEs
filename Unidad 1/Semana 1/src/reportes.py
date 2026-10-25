"""Vista (MVC): tablas CSV y visualizaciones para los escenarios."""
import csv
from dataclasses import asdict
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from .dominio import ResultadoLluvia


def guardar_csv(resultados: list[ResultadoLluvia], archivo: Path) -> None:
    archivo.parent.mkdir(parents=True, exist_ok=True)
    with archivo.open("w", newline="", encoding="utf-8-sig") as f:
        escritor = csv.DictWriter(f, fieldnames=list(asdict(resultados[0])))
        escritor.writeheader()
        for r in resultados:
            fila = asdict(r)
            fila.update({k: round(fila[k], 4) for k in ("h", "n", "tf", "indice")})
            escritor.writerow(fila)


def grafica_individual(resultados: list[ResultadoLluvia], ruta: Path):
    horas = [r.hora for r in resultados]
    valores = [r.indice for r in resultados]
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(horas, valores, marker="o", linewidth=2.3, label=resultados[0].escenario)
    for y, label in ((.4, "Baja posibilidad"), (.6, "Lluvia probable"), (.75, "Lluvia")):
        ax.axhline(y, linestyle="--", alpha=.7, label=f"Umbral {label}: {y}")
    ax.set(title=f"Índice de lluvia: modelo {resultados[0].escenario.lower()}",
           xlabel="Hora", ylabel="Índice de lluvia", ylim=(0, 1.02))
    ax.legend(loc="upper left", fontsize=8)
    ax.grid(alpha=.25)
    fig.tight_layout()
    fig.savefig(ruta, dpi=150)
    plt.close(fig)


def grafica_comparativa(original: list[ResultadoLluvia], ajustado: list[ResultadoLluvia], ruta: Path):
    horas = [r.hora for r in original]
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(horas, [r.indice for r in original], marker="o", label="Original: 0.5H + 0.3N + 0.2Tf")
    ax.plot(horas, [r.indice for r in ajustado], marker="s", label="Ajustado: 0.6H + 0.3N + 0.1Tf")
    ax.axhline(.75, linestyle="--", label="Umbral lluvia (0.75)")
    ax.set(title="Comparación del índice de lluvia", xlabel="Hora", ylabel="Índice", ylim=(0, 1.02))
    ax.grid(alpha=.25)
    ax.legend(fontsize=9)
    fig.tight_layout()
    fig.savefig(ruta, dpi=150)
    plt.close(fig)


def mostrar_tabla(resultados: list[ResultadoLluvia]):
    print(f"\nMODELO {resultados[0].escenario.upper()}")
    print(f"{'Hora':6s} {'Hum.%':>6s} {'Nub.%':>6s} {'Temp':>5s} {'H':>5s} {'N':>5s} {'Tf':>5s} {'Índice':>7s}  Estado")
    for r in resultados:
        print(f"{r.hora:6s} {r.humedad:6.0f} {r.nubosidad:6.0f} {r.temperatura:5.0f} "
              f"{r.h:5.2f} {r.n:5.2f} {r.tf:5.2f} {r.indice:7.3f}  {r.estado}")
