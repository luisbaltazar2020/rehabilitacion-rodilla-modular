# schemas.py
from pydantic import BaseModel,EmailStr,Field

class PacienteCreate(BaseModel):
    nombre: str
    edad: int
    diagnostico: str

class EjercicioCreate(BaseModel):
    nombre: str

class SerieCreate(BaseModel):
    repeticiones: int
    duracion: int

class SesionCreate(BaseModel):
    fecha: str
    paciente_id: int

class Fisioterapeutacreate(BaseModel):
    nombre: str
    email: EmailStr
    password:str =Field(min_length=6)

class FisioterapeutaLogin(BaseModel):
    email:EmailStr
    password:str

class FisioterapeutaOut(BaseModel):
    id: int
    nombre: str
    email: str

    class Config:
        from_attributes = True

class MovimientoCreate(BaseModel):
    angulo: float
    tiempo: str
