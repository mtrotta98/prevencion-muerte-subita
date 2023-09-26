from src.core.db import db

class Entidad(db.Model):
    __tablename__ = "Entidades"

    # Columnas
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    cuit = db.Column(db.String, unique=True, nullable=False)
    razon_social = db.Column(db.String(100), nullable=False)
    tipo_institucion = db.Column(db.String(100), nullable=False)
    sector = db.Column(db.String(100), nullable=False)



def __init__(self, cuit, razon_social, tipo_institucion, sector):
    self.cuit = cuit
    self.razon_social = razon_social
    self.tipo_institucion = tipo_institucion
    self.sector = sector

