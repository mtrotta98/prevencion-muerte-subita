from src.core.db import db

class Responsable(db.Model):
    __tablename__ = "Responsables"
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    nombre = db.Column(db.String, nullable=False)
    apellido = db.Column(db.String, nullable=False)
    dni = db.Column(db.String, nullable=False)
    email = db.Column(db.String)
    teléfono = db.Column(db.String, nullable=False)
    sede_id = db.Column(db.Integer, db.ForeignKey("Sedes.id"))

def __init__(self, nombre, apellido, dni, telefono):
    self.nombre = nombre
    self.apellido = apellido
    self.telefono = telefono
    self.dni = dni