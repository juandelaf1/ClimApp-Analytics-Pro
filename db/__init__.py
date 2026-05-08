"""
Database Schema - ClimApp-Analytics-Pro
====================================
SQLite schema for production.

Usage:
  python -m db.init_db  # Create tables
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

Base = declarative_base()

class RegistroClimatico(Base):
    __tablename__ = 'registros_climaticos'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    municipio = Column(String(100), nullable=False, index=True)
    estacion_id = Column(String(50))
    fecha = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Datos meteorológicos
    temperatura = Column(Float)
    humedad = Column(Float)
    viento = Column(Float)
    lluvia = Column(Float)
    presion = Column(Float)
    
    # Metadatos
    fuente = Column(String(20), default='AEMET')  # AEMET, MANUAL, FALLBACK
    lat = Column(Float)
    lon = Column(Float)
    alertas = Column(String(200))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        Index('idx_municipio_fecha', 'municipio', 'fecha'),
        Index('idx_fecha', 'fecha'),
    )


class Zona(Base):
    __tablename__ = 'zonas'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), unique=True, nullable=False)
    cod_ine = Column(String(10), unique=True)
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)
    provincia = Column(String(50))
    activa = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class Usuario(Base):
    __tablename__ = 'usuarios'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(200), nullable=False)
    nombre = Column(String(100))
    rol = Column(String(20), default='user')  # admin, user
    api_key = Column(String(50), unique=True)
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


# Database connection
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///data/climapp.db')


def get_engine():
    return create_engine(DATABASE_URL, echo=False)


def get_session():
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    return Session()


def init_db():
    """Inicia la base de datos."""
    engine = get_engine()
    Base.metadata.create_all(engine)
    print("Base de datos inicializada!")


def migrate_from_json():
    """Migra datos desde JSON a SQLite."""
    import json
    
    session = get_session()
    json_file = 'data/registros_climaticos.json'
    
    if not os.path.exists(json_file):
        print("No hay archivo JSON para migrar")
        return
    
    with open(json_file, 'r', encoding='utf-8') as f:
        registros = json.load(f)
    
    for reg in registros:
        nuevo = RegistroClimatico(
            municipio=reg.get('municipio'),
            estacion_id=reg.get('estacion_id'),
            temperatura=reg.get('temperatura'),
            humedad=reg.get('humedad'),
            viento=reg.get('viento'),
            lluvia=reg.get('lluvia'),
            presion=reg.get('presion'),
            fuente=reg.get('fuente'),
            alertas=str(reg.get('alertas', []))
        )
        session.add(nuevo)
    
    session.commit()
    print(f"Migrados {len(registros)} registros!")


if __name__ == '__main__':
    init_db()