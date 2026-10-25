"""APE 1. Ejecutar desde la carpeta Semana 1 con: python main.py"""
import argparse
from pathlib import Path
from src.datos import REGISTROS
from src.modelos import ModeloOriginal, ModeloAjustado, SimuladorLluvia
from src.reportes import guardar_csv, grafica_individual, grafica_comparativa, mostrar_tabla


def main():
    parser = argparse.ArgumentParser(description="Simulación de probabilidad de lluvia durante 24 h")
    parser.add_argument("--salida", default="resultados", help="Directorio de gráficos y tablas")
    args = parser.parse_args()
    salida = Path(args.salida)
    salida.mkdir(parents=True, exist_ok=True)
    original = SimuladorLluvia(ModeloOriginal()).ejecutar(REGISTROS)
    ajustado = SimuladorLluvia(ModeloAjustado()).ejecutar(REGISTROS)
    for nombre, datos in (("original", original), ("ajustado", ajustado)):
        mostrar_tabla(datos)
        guardar_csv(datos, salida / f"tabla_{nombre}.csv")
        grafica_individual(datos, salida / f"lluvia_{nombre}.png")
    grafica_comparativa(original, ajustado, salida / "comparacion_modelos.png")
    print(f"\nArchivos guardados en: {salida.resolve()}")


if __name__ == "__main__":
    main()
