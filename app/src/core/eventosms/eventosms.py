from src.core.db import db


class eventoMS(db.Model):
    __tablename__ = "eventosms"
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    sede_id = db.Column(db.Integer, db.ForeignKey("Sedes.id"))
    fecha = db.Column(db.DateTime, nullable=False)
    sexo =db.Column(db.Integer, nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    sobrevive = db.Column(db.Boolean)
    usoDea = db.Column(db.Boolean)
    usosDEA = db.Column(db.Integer)
    usoRCP = db.Column(db.Boolean)
    tiempoRCP = db.Column(db.Integer)
    modelo = db.Column(db.String)
    marca = db.Column(db.Integer)
    descripcion =db.Column(db.String(250), nullable=False)


def __init__(self, sede_id, fecha, sexo, edad, descripcion):
    self.fecha = fecha
    self.sede_id = sede_id
    self.sexo = sexo
    self.edad = edad
    self.usoRCP = descripcion