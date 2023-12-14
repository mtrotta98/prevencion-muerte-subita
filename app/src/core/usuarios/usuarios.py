from src.core.db import db


class Usuario(db.Model):
    __tablename__ = "Usuarios"
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    id_publico = db.Column(db.String(50), unique = True)
    nombre = db.Column(db.String, nullable=False)
    apellido = db.Column(db.String, nullable=False)
    usuario = db.Column(db.String, nullable=False)
    contraseña = db.Column(db.String, nullable=False)
    dni = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    fecha_nacimiento = db.Column(db.Date)
    id_rol = db.Column(db.Integer, db.ForeignKey("Roles.id"))
    


def __init__(self, nombre, apellido, usuario, contraseña, dni):
    self.nombre = nombre
    self.apellido = apellido
    self.usuario = usuario
    self.contraseña = contraseña
    self.dni = dni


def __repr__(self):
    return (
        f"Usuario(id={self.id!r}, nombre={self.nombre!r}, apellido={self.apellido!r})"
    )