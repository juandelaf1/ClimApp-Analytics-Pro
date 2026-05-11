from app.db.base import Base
from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Municipio(Base):
    __tablename__ = "municipios"

    id = Column(Integer, primary_key=True, index=True)
    cod_ine = Column(String(10), unique=True, index=True)
    nombre = Column(String(100), nullable=False)
    lat = Column(Numeric(10, 6))
    lon = Column(Numeric(10, 6))
    zona_id = Column(Integer, ForeignKey("zonas.id", ondelete="SET NULL"))
    created_at = Column(TIMESTAMP, server_default=func.now())

    zona = relationship("Zona", backref="municipios")
    estaciones = relationship("Estacion", back_populates="municipio")