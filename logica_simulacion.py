import random

def generar_angulo_realista(numero_sesion: int, angulo_inicial: float = 20.0) -> float:
    mejora_base = numero_sesion * 5
    variacion = random.uniform(-8, 8)
    angulo = angulo_inicial + mejora_base + variacion
    return round(min(max(angulo, 5), 130), 2)