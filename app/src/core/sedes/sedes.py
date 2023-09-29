from src.core.db import db

class Sede(db.Model):
    __tablename__ = "Sedes"

    # Columnas
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    latitud = db.Column(db.Float, nullable=False)
    longitud = db.Column(db.Float, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    flujo_personas = db.Column(db.Integer, nullable=False)
    superficie = db.Column(db.Float, nullable=False)
    personal_estable = db.Column(db.Integer, nullable=False)
    pisos = db.Column(db.Integer, nullable=False)
    estado = db.Column(db.String(100), nullable=False)
    id_provincia = db.Column(db.Integer, db.ForeignKey("Provincias.id"))
    id_entidad = db.Column(db.Integer, db.ForeignKey("Sedes.id"))


def __init__(self, latitud, longitud, nombre, flujo_personas, superficie, personal_estable, pisos, estado):
    self.latitud = latitud
    self.longitud = longitud
    self.nombre = nombre
    self.flujo_personas = flujo_personas
    self.superficie = superficie
    self.personal_estable = personal_estable
    self.pisos = pisos
    self.estado = estado