from src.core.db import db


class Ddjj(db.Model):
    __tablename__ = "Ddjj"
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    personal_capacitado = db.Column(db.Boolean)
    dea_señalizado = db.Column(db.Boolean)
    responsable = db.Column(db.Boolean)
    protocolo_accion = db.Column(db.Boolean)
    sistema_emergencia = db.Column(db.Boolean)
    cantidad_dea = db.Column(db.Boolean)
    #id_sede = db.Column(db.Integer, db.ForeignKey("Sedes.id"))
    


def __init__(self, personal_capacitado, dea_señalizado, responsable, protocolo_accion, sistema_emergencia, cantidad_dea):
    self.personal_capacitado = personal_capacitado
    self.dea_señalizado = dea_señalizado
    self.responsable = responsable
    self.protocolo_accion = protocolo_accion
    self.sistema_emergencia = sistema_emergencia
    self.cantidad_dea = cantidad_dea