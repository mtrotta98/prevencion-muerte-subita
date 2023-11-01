from wtforms import Form, validators
from wtforms.fields import StringField, EmailField, IntegerField


class NewRespForm(Form):
    nombre = StringField(u'Nombre', validators=[
                             validators.input_required(message='Se requiere un nombre')])
    apellido = StringField(u'Apellido', validators=[
                             validators.input_required(message='Se requiere un apellido')])
    dni = StringField(u'DNI', validators=[
                             validators.input_required(message='Se requiere un DNI')])
    email = EmailField(u'Email', validators=[
                             validators.input_required(message='Se requiere un email')])
    teléfono = StringField(u'Teléfono', validators=[
                             validators.input_required(message='Se requiere un teléfono')])
    sede_id = IntegerField(u'Sede')