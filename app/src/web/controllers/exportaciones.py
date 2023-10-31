import uuid

from flask import Blueprint, render_template, request, flash, redirect, make_response, jsonify, abort, Response
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
from flask_jwt_extended import jwt_required, unset_jwt_cookies
from flask_jwt_extended import create_access_token, set_access_cookies, get_jwt_identity

from src.core import usuarios
from src.core import sedes
from src.web.controllers.validators import validator_usuario, validator_permission

exportacion_blueprint = Blueprint("exportaciones", __name__, url_prefix="/exportaciones")

@exportacion_blueprint.route("/tipo_exportacion/<id>")
def devolver_dato(id):
    """Esta funcion recibe el parametro de la lista que se quiere exportar en PDF"""

    sede = sedes.get_sede(id)

    return sede

@exportacion_blueprint.route("/exportar_pdf/<id>")
def generar_pdf(id):
    """Esta funcion genera el pdf, recibe por parametro el id de la sede"""

    # Obtener los datos
    sede = devolver_dato(id)

    # Crear un objeto PDF
    output = BytesIO()
    p = canvas.Canvas(output, pagesize=letter)

    # Agregar datos al PDF
    texto = f'Nombre: {sede.nombre}, Latitud: {sede.latitud}, Longitud: {sede.longitud}, Flujo de Personas: {sede.flujo_personas}, Personal: {sede.personal_estable}, Piso: {sede.pisos}, Estado: {sede.estado}'
    lineas = texto.split(', ')

    for i, linea in enumerate(lineas):
        p.drawString(100, 750 - i * 15, linea)
    
    # Finalizar el PDF
    p.showPage()
    p.save()

    pdf_out = output.getvalue()
    output.close()

    response = make_response(pdf_out)
    response.headers['Content-Disposition'] = f"attachment; filename={sede.nombre}.pdf"
    response.mimetype = 'application/pdf'

    return response