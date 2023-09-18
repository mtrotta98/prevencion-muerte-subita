from src.core.db import db

Usuario_Provincia = db.Table(
    "Usuario_Provincia",
    db.Column(
        "id_usuario",
        db.Integer,
        db.ForeignKey("Usuarios.id"),
        nullable=False,
        primary_key=True,
    ),
    db.Column(
        "id_provincia",
        db.Integer,
        db.ForeignKey("Provincias.id"),
        nullable=False,
        primary_key=True,
    ),
)


class Provincia(db.Model):
    __tablename__ = "Provincias"
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    nombre = db.Column(db.String, nullable=False, unique=True)

    usuarios = db.relationship("Usuario", secondary=Usuario_Provincia, backref="provincias")


def __init__(self, nombre):
    self.nombre = nombre