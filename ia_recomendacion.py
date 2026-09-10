def calcular_promedio_angulo(angulos: list[float]) -> float:
    if not angulos:
        return 0.0
    return round(sum(angulos) / len(angulos), 2)

def recomendar_angulo_objetivo(edad: int, promedio_actual: float) -> float:
    if edad < 40:
        incremento = 15
    elif edad < 65:
        incremento = 10
    else:
        incremento = 6

    objetivo = promedio_actual + incremento
    return round(min(objetivo, 135), 2)

def estimar_dias_recuperacion(edad: int, promedio_actual: float) -> int:
    # Paso 1: días base según el rango de ángulo actual
    if promedio_actual < 40:
        dias_base = 30
    elif promedio_actual < 80:
        dias_base = 15
    else:
        dias_base = 7

    # Paso 2: factor de ajuste según edad
    if edad < 40:
        factor = 1.0
    elif edad < 65:
        factor = 1.3
    else:
        factor = 1.6

    return round(dias_base * factor)

# pendiente de validar con asesor:
# Explorar un modelo de Machine Learning real (scikit-learn, regresión) que
# reemplace o complemente este sistema de reglas. La idea sería generar un
# dataset sintético (edad, angulo_inicial, angulo_final, dias_reales) basado
# en literatura médica, entrenar un modelo de regresión con esos datos, y
# usarlo para predecir dias_estimados_recuperacion en vez de (o junto con)
# las reglas actuales. Pendiente de decidir alcance con el asesor, dado el
# tiempo disponible antes de la fecha de titulación.