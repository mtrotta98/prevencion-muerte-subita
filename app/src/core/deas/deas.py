from src.core.db import db
from src.core.responsables.responsables import Responsable


class DEA(db.Model):
    __tablename__ = "deas"
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    denominacion =db.Column(db.String(100))
    marca = db.Column(db.Integer, nullable=False)
    modelo = db.Column(db.String, nullable=False)
    nSerie = db.Column(db.String, nullable=False)
    ultimoMantenimiento = db.Column(db.Date)
    solidario = db.Column(db.Boolean)
    activo = db.Column(db.Boolean)
    sede_id = db.Column(db.Integer, db.ForeignKey("Sedes.id"))


def __init__(self, denominacion, modelo, marca, nSerie, solidario, activo, sede_id):
    self.denominacion = denominacion
    self.marca = marca
    self.modelo = modelo
    self.nSerie = nSerie
    self.solidario = solidario
    self.activo = activo
    self.sede_id = sede_id