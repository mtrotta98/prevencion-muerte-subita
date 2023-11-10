import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def enviar_email_alta_admin_prov(data_usuario):
    sender = "nicolastrotta88@gmail.com"
    receiver = data_usuario["email"]
    nombre = data_usuario["nombre"]
    apellido = data_usuario["apellido"]
    usuario = data_usuario["usuario"]
    contrasenia = data_usuario["contraseña"]

    message = MIMEMultipart("alternative")
    message["Subject"] = "multipart test"
    message["From"] = sender
    message["To"] = receiver

    text = f"""\
    Bienvenido {nombre} {apellido} para ingresar al sistema debera usar las siguientes credenciales 
    Usuario {usuario} 
    Contrasenia {contrasenia}."""

    part = MIMEText(text, "plain")
    message.attach(part)

    with smtplib.SMTP("sandbox.smtp.mailtrap.io", 2525) as server:
        server.login("eff9de5c2d2573", "4b08ba2521c0a7")
        server.sendmail(sender, receiver, message.as_string())

def enviar_email_vencimiento_certificacion(receiver, nombre, apellido, nombre_sede):
    sender = "nicolastrotta88@gmail.com"
    message = MIMEMultipart("alternative")
    message["Subject"] = "multipart test"
    message["From"] = sender
    message["To"] = receiver

    text = f"""\
    Buenos dias {nombre} {apellido} este email es para informarle que la certificacion de la sede {nombre_sede} a vencido el dia de hoy, debera renovarla."""

    part = MIMEText(text, "plain")
    message.attach(part)

    with smtplib.SMTP("sandbox.smtp.mailtrap.io", 2525) as server:
        server.login("eff9de5c2d2573", "4b08ba2521c0a7")
        server.sendmail(sender, receiver, message.as_string())

def enviar_mail_alerta_asistencia(receiver, nombre, apellido, direccion):
    sender = "nicolastrotta88@gmail.com"
    message = MIMEMultipart("alternative")
    message["Subject"] = "multipart test"
    message["From"] = sender
    message["To"] = receiver

    text = f"""\
    Buenos dias {nombre} {apellido} se solicita asistencia medica en la siguiente direccion: {direccion}"""

    part = MIMEText(text, "plain")
    message.attach(part)

    with smtplib.SMTP("sandbox.smtp.mailtrap.io", 2525) as server:
        server.login("eff9de5c2d2573", "4b08ba2521c0a7")
        server.sendmail(sender, receiver, message.as_string())
