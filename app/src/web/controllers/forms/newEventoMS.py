import datetime
from wtforms import Form, validators
from wtforms.fields import StringField, BooleanField, SelectField, IntegerField, DateTimeLocalField
from wtforms_components import DateRange



class NewEventoMSForm(Form):
    sede_id = IntegerField(u'Sede')
    fecha = DateTimeLocalField(u'Fecha estimada ', 
                            validators=[validators.DataRequired(), DateRange(max=datetime.datetime.today(),message='No puede ingresar una fecha futura')], format='%Y-%m-%dT%H:%M')
    edad = IntegerField(u'Edad estimada', validators=[
                             validators.input_required(message='Se requiere una edad estimada')])
    sexo = SelectField(u'Sexo aparente', validate_choice=False, coerce=int,
                         validators=[validators.input_required(message='Indique un sexo aparente')], choices=[('1', 'Masculino'),('2', 'Femenino'),('3', 'Otro')])
    sobrevive = BooleanField('Sobrevive', default=False)
    usoDea = BooleanField('Se utilizó DEA ', default=False)
    usosDEA = IntegerField(u'Cantidad de descargas DEA', default=0)
    usoRCP = BooleanField('Se aplicó RCP ', default=False)
    tiempoRCP = IntegerField(u'Cantidad de minutos RCP', default=0)
    marca = SelectField(u'Marca', validate_choice=False, coerce=int, choices=[('0', 'Negativo')])
    modelo = SelectField(u'Modelo', validate_choice=False, choices=[('0', 'Negativo')])
    descripcion = StringField(u'Descripcion del evento', validators=[
                             validators.input_required(message='Se requiere una descipción')])
 