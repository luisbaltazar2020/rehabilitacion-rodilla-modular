from sqlalchemy import Column, Integer, String, ForeignKey,Float
from sqlalchemy.orm import relationship
from database import Base

class Paciente(Base):
    __tablename__ = "pacientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    edad = Column(Integer)
    diagnostico = Column(String)

    sesiones = relationship("Sesion")

class Fisioterapeuta(Base):
    __tablename__ = "fisioterapeutas"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    email = Column(String, unique=True)
    password_hash = Column(String)

class Ejercicio(Base):
    __tablename__= "ejercicios"

    id=Column(Integer, primary_key=True, index=True)
    nombre = Column(String,index=True)

    series = relationship(
    "Serie",
    back_populates="ejercicio",
    cascade="all, delete"
)


class Sesion(Base):
    __tablename__ = "sesiones"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(String)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"))


class Serie(Base):
    __tablename__= "series"

    id = Column(Integer, primary_key=True, index=True)
    repeticiones = Column(Integer)
    duracion = Column(Integer)  # segundos
    ejercicio_id = Column(
    Integer,
    ForeignKey("ejercicios.id", ondelete="CASCADE")
)

    ejercicio = relationship("Ejercicio", back_populates="series")

class Movimiento(Base):
    __tablename__ = "movimientos"

    id = Column(Integer, primary_key=True, index=True)
    angulo = Column(Float)
    tiempo = Column(String)
    sesion_id = Column(Integer, ForeignKey("sesiones.id"))