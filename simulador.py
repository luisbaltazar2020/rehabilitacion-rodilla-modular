import requests
import random
import time
from logica_simulacion import  generar_angulo_realista

SERVIDOR_URL = "http://127.0.0.1:8000"

def generar_movimiento(numero_sesion: int):
    angulo = generar_angulo_realista(numero_sesion)
    return {
        "angulo": angulo,
        "tiempo": f"{time.time():.0f}s"
    }

def enviar_movimiento(sesion_id: int, numero_sesion: int):
    datos = generar_movimiento(numero_sesion)
    url = f"{SERVIDOR_URL}/sesiones/{sesion_id}/movimientos/"
    respuesta = requests.post(url, json=datos)

    if respuesta.status_code == 200:
        print(f"Movimiento enviado: {respuesta.json()}")
    else:
        print(f"Error {respuesta.status_code}: {respuesta.text}")

if __name__ == "__main__":
    sesion_id = int(input("Ingresa el id de la sesión a simular: "))
    numero_sesion = int(input("¿Qué número de sesión es para este paciente (1, 2, 3...)? "))
    for i in range(10):
        enviar_movimiento(sesion_id, numero_sesion)
        time.sleep(1)