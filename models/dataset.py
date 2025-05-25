from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Estacion(Base):
    __tablename__ = 'datos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    año = Column(Integer)
    trimestre = Column(String)
    nombre = Column(String)
    abonados_servicio = Column(Integer)
    abonados_pospago = Column(Integer)
    lineas_activas = Column(Integer)
    lineas_retiradas = Column(Integer)
    abonados_prepago = Column(Integer)