from src.core.db import db

class Rol(db.Model):
    __tablename__ = "Roles"

    # Columnas
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    nombre = db.Column(db.String(100), nullable=False)