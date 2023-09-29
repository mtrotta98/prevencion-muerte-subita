from src.core.db import db


class Visita(db.Model):
    __tablename__ = "Visitas"
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    fecha = db.Column(db.Date)
    resultado = db.Column(db.Boolean)
    observacion = db.Column(db.String(50))
    #id_sede = db.Column(db.Integer, db.ForeignKey("Sedes.id"))
    


def __init__(self, fecha, resultado, observacion):
    self.fecha = fecha
    self.resultado = resultado
    self.observacion = observacion