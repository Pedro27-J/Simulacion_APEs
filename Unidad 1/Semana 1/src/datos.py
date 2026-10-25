"""Registros proporcionados en la guía de la práctica 001."""
from .dominio import RegistroMeteorologico

REGISTROS = [
    RegistroMeteorologico("06:00", 65, 40, 14),
    RegistroMeteorologico("08:00", 70, 50, 16),
    RegistroMeteorologico("10:00", 68, 45, 18),
    RegistroMeteorologico("12:00", 60, 30, 22),
    RegistroMeteorologico("14:00", 75, 70, 20),
    RegistroMeteorologico("16:00", 85, 85, 18),
    RegistroMeteorologico("18:00", 92, 95, 16),
    RegistroMeteorologico("20:00", 88, 90, 17),
    RegistroMeteorologico("22:00", 80, 75, 15),
]
