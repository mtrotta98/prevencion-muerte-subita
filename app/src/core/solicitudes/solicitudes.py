from src.core.db import db


class Solicitud(db.Model):
    __tablename__ = "Solicitudes"
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey("Usuarios.id"))
    #id_sede = db.Column(db.Integer, db.ForeignKey("Sede.id"))
    estado = db.Column(db.String, nullable=False)
    razon = db.Column(db.String)
    


def __init__(self, id_usuario, id_sede, estado, razon):
    self.id_usuario = id_usuario
    #self.id_sede = id_sede
    self.estado = estado
    self.razon = razon