import uuid

from flask import Blueprint, render_template, request, flash, redirect, make_response, jsonify, abort, Response
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
from flask_jwt_extended import jwt_required, unset_jwt_cookies
from flask_jwt_extended import create_access_token, set_access_cookies, get_jwt_identity

from src.core import sedes
from src.core import deas

from src.web.controllers.validators import validator_usuario, validator_permission

exportacion_blueprint = Blueprint("exportaciones", __name__, url_prefix="/exportaciones")

@exportacion_blueprint.route("/exportar_pdf/<id>")
def generar_pdf(id):
    """Esta funcion genera el pdf, recibe por parametro el id de la sede"""

    # Obtener los datos
    sede = sedes.get_sede(id)
    deas_sede = deas.get_by_sede(id)
    direccion = sedes.get_direccion(sede)

    # Crear un objeto PDF
    output = BytesIO()
    p = canvas.Canvas(output, pagesize=letter)

    # Agregar datos al PDF
    texto = f'Nombre: {sede.nombre}, Calle: {direccion[0]}, Numero: {direccion[1]}, Flujo de Personas: {sede.flujo_personas}, Personal: {sede.personal_estable}, Piso: {sede.pisos}, Estado: {sede.estado}, DEAS de la Sede: '
    
    for dea in deas_sede:
        if dea.solidario:
            solidario = "Si"
        else:
            solidario = "No"
        if dea.activo:
            activo = "Si"
        else:
            activo = "No"
        texto += f', , Denominacion: {dea.denominacion}, Marca: {dea.marca}, Modelo: {dea.modelo}, Nro. de Serie: {dea.nserie}, Ultimo Mantenimiento: {dea.ultimomantenimiento}, Solidario: {solidario}, Activo: {activo}'
    
    lineas = texto.split(', ')

    # Determinar la longitud máxima de la clave
    max_key_length = max(len(linea.split(': ')[0]) for linea in lineas if ': ' in linea)
                         
    for i, linea in enumerate(lineas):
        if i == lineas.index('DEAS de la Sede: '):
            p.drawString(100, 750 - i * 15, '')
            i += 1
        if ':' in linea:
            if ': ' in linea:
                key, value = linea.split(': ', 1)
            else:
                key, value = linea, ''
            p.setFont("Helvetica-Bold", 12)
            p.drawString(100, 750 - i * 15, key + ': ')
            p.setFont("Helvetica", 12)
            p.drawString(100 + max_key_length * 7, 750 - i * 15, value)
        else:
            p.setFont("Helvetica", 12)
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