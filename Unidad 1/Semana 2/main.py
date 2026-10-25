"""APE 2. Ejecutar desde Semana 2: python main.py"""
import argparse
from pathlib import Path
from src.datos import DATOS
from src.experimentos import calibrar, ejecutar, estudiar_ruido, estudiar_tasa
from src.reportes import (
    graficar_comparacion, graficar_serie, guardar_tabla,
    guardar_metricas, mostrar_resumen,
)


def main():
    parser = argparse.ArgumentParser(description="Comparación de cuatro modelos poblacionales")
    parser.add_argument("--salida", default="resultados", help="Carpeta de tablas y gráficas")
    parser.add_argument("--dt", type=float, default=0.1, help="Tamaño máximo del paso de Euler")
    parser.add_argument("--semilla", type=int, default=42, help="Semilla del modelo estocástico")
    args = parser.parse_args()
    salida = Path(args.salida)
    salida.mkdir(parents=True, exist_ok=True)

    parametros = calibrar(DATOS, dt=args.dt, semilla=args.semilla)
    resultados = ejecutar(parametros)
    mostrar_resumen(parametros, resultados)
    guardar_tabla(resultados, DATOS, salida / "tabla_comparativa.csv")
    guardar_metricas(resultados, DATOS, salida / "metricas.csv")
    graficar_comparacion(resultados, DATOS, salida / "comparacion_cuatro_modelos.png")
    graficar_serie(estudiar_tasa(parametros), ["r negativo", "r = 0", "r positivo"],
                  "Efecto de la tasa r: crecimiento y decrecimiento", salida / "influencia_tasa_r.png")
    graficar_serie(estudiar_ruido(parametros), ["σ = 0", "σ estimada", "σ × 2"],
                  "Efecto del ruido sobre el modelo estocástico", salida / "influencia_ruido.png")
    print(f"Archivos guardados en: {salida.resolve()}")


if __name__ == "__main__":
    main()
