from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()

class NumeroExtraido(Base):
    __tablename__ = 'numeros_extraidos'
    id = Column(Integer, primary_key=True)
    numero = Column(Integer, nullable=False)
    fecha_extraccion = Column(DateTime, default=datetime.utcnow)
    nombre_sorteo = Column(String(100))
    hora_sorteo = Column(String(20))
    fuente = Column(String(255))
    metadata_extra = Column(String(500))

class Prediccion(Base):
    __tablename__ = 'predicciones'
    id = Column(Integer, primary_key=True)
    numero_predicho = Column(Integer, nullable=False)
    confianza = Column(Float)
    fecha_prediccion = Column(DateTime, default=datetime.utcnow)
    modelo_usado = Column(String(100))
    acertado = Column(Boolean, default=None)
    numero_real = Column(Integer, default=None)

class ConfiguracionScraper(Base):
    __tablename__ = 'configuracion_scraper'
    id = Column(Integer, primary_key=True)
    url_objetivo = Column(String(500), nullable=False)
    selector_css = Column(String(255))
    selector_xpath = Column(String(255))
    intervalo_minutos = Column(Integer, default=60)
    activo = Column(Boolean, default=True)
    ultima_ejecucion = Column(DateTime)

DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///prediccion.db')

# Corrección para compatibilidad con SQLAlchemy 2.0 y Render (postgres:// -> postgresql://)
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(engine)
    print("[OK] Base de datos inicializada")

def get_session():
    return Session()
