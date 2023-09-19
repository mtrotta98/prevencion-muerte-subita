from src.core.db import db

class Entidad(db.Model):
    __tablename__ = "Entidades"

    # Columnas
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    razon_social = db.Column(db.String(100), nullable=False)
    tipo_institucion = db.Column(db.String(100), nullable=False)
    sector = db.column(db.String(100), nullable=False)


def __init__(self, razon_social, tipo_institucion, sector):
    self.razon_social = razon_social
    self.tipo_institucion = tipo_institucion
    self.sector = sector

