from src.core.db import db


class eventoMant(db.Model):
    __tablename__ = "eventosmant"
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    dea_id = db.Column(db.Integer, db.ForeignKey("deas.id"))
    fecha = db.Column(db.DateTime, nullable=False)
    descripcion =db.Column(db.String(250), nullable=False)


def __init__(self, dea_id, fecha, descripcion):
    self.fecha = fecha
    self.dea_id = dea_id
    self.descripcion = descripcion