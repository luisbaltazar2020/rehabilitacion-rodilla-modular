from fastapi import FastAPI, HTTPException,Depends
from database import engine, Base
from models import Paciente, Ejercicio, Serie,Sesion,Movimiento,Fisioterapeuta
from sqlalchemy.orm import Session
from database import SessionLocal
import random
from fastapi.middleware.cors import CORSMiddleware
from schemas import PacienteCreate,EjercicioCreate,SerieCreate,SesionCreate,Fisioterapeutacreate,FisioterapeutaLogin,FisioterapeutaOut,MovimientoCreate
from auth import hashear_password,verificar_password,crear_token,obtener_fisioterapeuta_actual
from logica_simulacion import generar_angulo_realista
from ia_recomendacion import calcular_promedio_angulo, recomendar_angulo_objetivo, estimar_dias_recuperacion

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crear tablas
Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"mensaje": "Sistema de Rehabilitación funcionando"}

#ver:
# Ver pacientes
@app.get("/pacientes/{paciente_id}/sesiones")
def obtener_sesiones(paciente_id: int):
    db = SessionLocal()
    sesiones = db.query(Sesion).filter(Sesion.paciente_id == paciente_id).all()
    db.close()
    if not sesiones:
        raise HTTPException(status_code=404, detail="No existen sesiones para este paciente")
    return sesiones

#Ver ejercico
@app.get("/ejercicios/{ejercicio_id}")
def ver_ejercicio(ejercicio_id: int):
    db = SessionLocal()
    ejercicio = db.query(Ejercicio).filter(Ejercicio.id == ejercicio_id).first()
    db.close()
    if not ejercicio:
        raise  HTTPException(status_code=404, detail="Ejercicio no encontrado")
    return ejercicio
    
@app.get("/paciente/")
def ver_paciente(fisio_actual: str= Depends(obtener_fisioterapeuta_actual)):
    db = SessionLocal()
    pacientes = db.query(Paciente).all()
    db.close()
    if not pacientes:
        raise HTTPException(status_code=404, detail="Pacientes no encontrados")
    return pacientes

@app.get("/ejercicios/")
def ver_ejercicios(fisio_actual: str= Depends(obtener_fisioterapeuta_actual)):
    db = SessionLocal()
    ejercicios = db.query(Ejercicio).all()
    db.close()
    return ejercicios

@app.get("/sesiones/{sesion_id}/movimientos")
def obtener_movimientos(sesion_id: int):
    db = SessionLocal()
    movimientos = db.query(Movimiento).filter(Movimiento.sesion_id == sesion_id).all()
    db.close()
    if not movimientos:
        raise HTTPException(status_code=404,detail="no hay movimientos registrados en esa sesión")
    return movimientos

# Crear
#Paciente
@app.post("/pacientes/")
def crear_paciente(paciente: PacienteCreate,fisio_actual: str= Depends(obtener_fisioterapeuta_actual)):
    db = SessionLocal()
    nuevo_paciente = Paciente(
        nombre=paciente.nombre,
        edad=paciente.edad,
        diagnostico=paciente.diagnostico
    )
    db.add(nuevo_paciente)
    db.commit()
    db.refresh(nuevo_paciente)
    db.close()
    return nuevo_paciente

#Eercicio
@app.post("/ejercicios/")
def crear_ejercicio(ejercicio: EjercicioCreate,fisio_actual: str= Depends(obtener_fisioterapeuta_actual)):
    db = SessionLocal()
    nuevo_ejercicio = Ejercicio(nombre=ejercicio.nombre)

    db.add(nuevo_ejercicio)
    db.commit()
    db.refresh(nuevo_ejercicio)
    db.close()
    return nuevo_ejercicio

#Serie
@app.post("/ejercicios/{ejercicio_id}/series/")
def agregar_serie(ejercicio_id: int, serie: SerieCreate):
    db = SessionLocal()

    ejercicio = db.query(Ejercicio).filter(Ejercicio.id == ejercicio_id).first()
    if not ejercicio:
        db.close()
        raise HTTPException(status_code=404, detail="El ejercicio no existe")

    nueva_serie = Serie(
        repeticiones=serie.repeticiones,
        duracion=serie.duracion,
        ejercicio_id=ejercicio_id
    )

    db.add(nueva_serie)
    db.commit()
    db.refresh(nueva_serie)
    db.close()

    return nueva_serie



@app.post("/sesiones/")
def crear_sesion(sesion: SesionCreate,fisio_actual: str= Depends(obtener_fisioterapeuta_actual)):
    db = SessionLocal()

    paciente = db.query(Paciente).filter(Paciente.id == sesion.paciente_id).first()
    if not paciente:
        db.close()
        raise HTTPException(status_code=404, detail="El paciente especificado no existe")
    
    nueva_sesion = Sesion(
        paciente_id=sesion.paciente_id,
        fecha=sesion.fecha
    )
    db.add(nueva_sesion)
    db.commit()
    db.refresh(nueva_sesion)
    db.close()

    return nueva_sesion

#simulador de angulos
@app.post("/simular/{sesion_id}")
def simular_movimiento(sesion_id: int, fisio_actual: str = Depends(obtener_fisioterapeuta_actual)):
    db = SessionLocal()

    sesion = db.query(Sesion).filter(Sesion.id == sesion_id).first()
    if not sesion:
        db.close()
        raise HTTPException(status_code=404, detail="La sesión no existe")

    numero_sesion = db.query(Sesion).filter(Sesion.paciente_id == sesion.paciente_id).count()

    movimientos = []
    for i in range(10):
        angulo = generar_angulo_realista(numero_sesion)
        movimiento = Movimiento(angulo=angulo, tiempo=f"{i}s", sesion_id=sesion_id)
        db.add(movimiento)
        movimientos.append({"angulo": angulo, "tiempo": f"{i}s"})

    db.commit()
    db.close()

    return {"mensaje": "Simulación completada", "movimientos": movimientos}

@app.get("/evaluar/{sesion_id}")
def evaluar_sesion(sesion_id: int):
    db = SessionLocal()
    sesion = db.query(Sesion).filter(Sesion.id == sesion_id).first()
    if not sesion:
        db.close()
        raise HTTPException(status_code=404, detail="La sesión no existe")

    paciente = db.query(Paciente).filter(Paciente.id == sesion.paciente_id).first()
    movimientos = db.query(Movimiento).filter(Movimiento.sesion_id == sesion_id).all()

    if not movimientos:
        db.close()
        return {"error": "No hay movimientos"}

    angulos = [m.angulo for m in movimientos]
    promedio = calcular_promedio_angulo(angulos)
    maximo = round(max(angulos), 2)

    angulo_objetivo = recomendar_angulo_objetivo(paciente.edad, promedio)
    dias_estimados = estimar_dias_recuperacion(paciente.edad, promedio)

    db.close()

    return {
        "promedio_actual": promedio,
        "maximo_alcanzado": maximo,
        "angulo_objetivo_recomendado": angulo_objetivo,
        "dias_estimados_recuperacion": dias_estimados
    }

    

@app.post("/fisioterapeutas/", response_model=FisioterapeutaOut)
def crear_fisioterapeuta(fisioterapeuta: Fisioterapeutacreate):
    db = SessionLocal()
    nuevo_fisioterapeuta = Fisioterapeuta(
        nombre=fisioterapeuta.nombre,
        email=fisioterapeuta.email,
        password_hash=hashear_password(fisioterapeuta.password)
    )
    db.add(nuevo_fisioterapeuta)
    db.commit()
    db.refresh(nuevo_fisioterapeuta)
    db.close()
    return nuevo_fisioterapeuta

@app.post("/fisioterapeutas/login")
def login_fisioterapeuta(datos: FisioterapeutaLogin):
    db = SessionLocal()
    fisioterapeuta = db.query(Fisioterapeuta).filter(Fisioterapeuta.email == datos.email).first()
    db.close()

    if not fisioterapeuta or not verificar_password(datos.password,fisioterapeuta.password_hash):
        raise HTTPException(status_code=401, detail="Email o contraseña incorrectos")
    
    token=crear_token(fisioterapeuta.email)
    return {"access_token": token, "token_type": "bearer"}

@app.post("/sesiones/{sesion_id}/movimientos/")
def recibir_movimiento(sesion_id: int,movimiento:MovimientoCreate):
    db=SessionLocal()
    sesion = db.query(Sesion).filter(Sesion.id == sesion_id).first()
    if not sesion:
        db.close()
        raise HTTPException(status_code=404, detail="La sesión no existe")
     # Paso 2: crear el objeto real con el modelo de base de datos
    nuevo_movimiento = Movimiento(
        angulo=movimiento.angulo,
        tiempo=movimiento.tiempo,
        sesion_id=sesion_id
    )
    # Paso 3: guardar
    db.add(nuevo_movimiento)
    db.commit()
    db.refresh(nuevo_movimiento)
    db.close()

    return nuevo_movimiento

@app.get("/pacientes/{paciente_id}/progreso")
def obtener_progreso(paciente_id: int):
    db = SessionLocal()

    paciente = db.query(Paciente).filter(Paciente.id == paciente_id).first()
    if not paciente:
        db.close()
        raise HTTPException(status_code=404, detail="El paciente no existe")

    sesiones = db.query(Sesion).filter(Sesion.paciente_id == paciente_id).all()

    progreso = []
    for sesion in sesiones:
        movimientos = db.query(Movimiento).filter(Movimiento.sesion_id == sesion.id).all()
        if movimientos:
            angulos = [m.angulo for m in movimientos]
            promedio = calcular_promedio_angulo(angulos)
            progreso.append({
                "fecha": sesion.fecha,
                "promedio": promedio
            })

    db.close()
    return progreso