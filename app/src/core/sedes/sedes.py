from src.core.db import db


Provincia_Sede = db.Table(
    "Provincia_Sede",
    db.Column(
        "id_provincia",
        db.Integer,
        db.ForeignKey("Provincias.id"),
        nullable=False,
        primary_key=True,
    ),
    db.Column(
        "id_sede",
        db.Integer,
        db.ForeignKey("Sedes.id"),
        nullable=False,
        primary_key=True,
    ),
)

Entidad_Sede = db.Table(
    "Entidad_Sede",
    db.Column(
        "id_entidad",
        db.Integer,
        db.ForeignKey("Entidades.id"),
        nullable=False,
        primary_key=True,
    ),
    db.Column(
        "id_sede",
        db.Integer,
        db.ForeignKey("Sedes.id"),
        nullable=False,
        primary_key=True,
    ),
)


class Sede(db.Model):
    __tablename__ = "Sedes"

    # Columnas
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    latitud = db.Column(db.Integer, nullable=False)
    longitud = db.Column(db.Integer, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    flujo_personas = db.Column(db.Integer, nullable=False)
    superficie = db.Column(db.Integer, nullable=False)
    personal_estable = db.Column(db.Integer, nullable=False)
    pisos = db.Column(db.Integer, nullable=False)
    estado = db.Column(db.String(100), nullable=False)

    provincias = db.relationship("Provincia", secondary=Provincia_Sede, backref="sedes")
    entidades = db.relationship("Entidad", secondary=Entidad_Sede, backref="sedes")


def __init__(self, latitud, longitud, nombre, flujo_personas, superficie, personal_estable, pisos, estado):
    self.latitud = latitud
    self.longitud = longitud
    self.nombre = nombre
    self.flujo_personas = flujo_personas
    self.superficie = superficie
    self.personal_estable = personal_estable
    self.pisos = pisos
    self.estado = estado