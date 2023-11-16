import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

port = 587
smtp_server = "smtp-mail.outlook.com"
sender = "nicolastrotta88@outlook.com.ar"

def enviar_email_alta_admin_prov(data_usuario):
    receiver = data_usuario["email"]
    nombre = data_usuario["nombre"]
    apellido = data_usuario["apellido"]
    usuario = data_usuario["usuario"]
    contrasenia = data_usuario["contraseña"]

    message = MIMEMultipart("alternative")
    message["Subject"] = "Registro admin provincial"
    message["From"] = sender
    message["To"] = receiver

    text = f"""\
    Bienvenido {nombre} {apellido} para ingresar al sistema debera usar las siguientes credenciales 
    Usuario {usuario} 
    Contrasenia {contrasenia}."""

    part = MIMEText(text, "plain")
    message.attach(part)

    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls()
        server.login(sender, "Sym280615")
        server.sendmail(sender, receiver, message.as_string())

def enviar_email_vencimiento_certificacion(receiver, nombre, apellido, nombre_sede):
    message = MIMEMultipart("alternative")
    message["Subject"] = "Vencimiento certificacion"
    message["From"] = sender
    message["To"] = receiver

    text = f"""\
    Buenos dias {nombre} {apellido} este email es para informarle que la certificacion de la sede {nombre_sede} a vencido el dia de hoy, debera renovarla."""

    part = MIMEText(text, "plain")
    message.attach(part)

    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls()
        server.login(sender, "Sym280615")
        server.sendmail(sender, receiver, message.as_string())

def enviar_mail_alerta_asistencia(receiver, nombre, apellido, direccion):
    message = MIMEMultipart("alternative")
    message["Subject"] = "Alerta Asistencia"
    message["From"] = sender
    message["To"] = receiver

    text = f"""\
    Buenos dias {nombre} {apellido} se solicita asistencia medica en la siguiente direccion: {direccion}"""

    part = MIMEText(text, "plain")
    message.attach(part)

    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls()
        server.login(sender, "Sym280615")
        server.sendmail(sender, receiver, message.as_string())
