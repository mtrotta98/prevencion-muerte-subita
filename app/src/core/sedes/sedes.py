from src.core.db import db

Usuario_Sede = db.Table(
    "Usuario_Sede",
    db.Column(
        "id_usuario",
        db.Integer,
        db.ForeignKey("Usuarios.id"),
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
    latitud = db.Column(db.Float, nullable=False)
    longitud = db.Column(db.Float, nullable=False)
    localidad = db.Column(db.String(100), nullable=True)
    nombre = db.Column(db.String(100), nullable=False)
    flujo_personas = db.Column(db.Integer, nullable=False)
    superficie = db.Column(db.Float, nullable=False)
    personal_estable = db.Column(db.Integer, nullable=False)
    pisos = db.Column(db.Integer, nullable=False)
    estado = db.Column(db.String(100), nullable=False)
    id_provincia = db.Column(db.Integer, db.ForeignKey("Provincias.id"))
    id_entidad = db.Column(db.Integer, db.ForeignKey("Entidades.id"))
    cantidad_DEA = db.Column(db.Integer, nullable=True)
    fecha_creacion = db.Column(db.Date)

    usuarios = db.relationship("Usuario", secondary=Usuario_Sede, backref="sedes")


def __init__(self, latitud, longitud, localidad, nombre, flujo_personas, superficie, personal_estable, pisos, estado, fecha_creacion):
    self.latitud = latitud
    self.longitud = longitud
    self.localidad = localidad
    self.nombre = nombre
    self.flujo_personas = flujo_personas
    self.superficie = superficie
    self.personal_estable = personal_estable
    self.pisos = pisos
    self.estado = estado
    self.fecha_creacion = fecha_creacion