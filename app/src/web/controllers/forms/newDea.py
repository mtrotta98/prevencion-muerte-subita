import datetime
from wtforms import Form, validators
from wtforms.fields import StringField, BooleanField, SelectField, DateField, IntegerField


class NewDEAForm(Form):
    denominacion = StringField(u'Denominacion', validators=[
                             validators.input_required(message='Se requiere una denominacion')])
    marca = SelectField(u'Marca', validate_choice=False, coerce=int,
                        validators=[validators.input_required(message='Marca es requerido')], choices=[('1', 'Otras')])
    modelo = SelectField(u'Modelo', validate_choice=False, 
                         validators=[validators.input_required(message='Modelo es requerido')], choices=[('1', 'Otras')])
    nSerie = StringField(u'Numero de Serie', validators=[
                             validators.input_required(message='Numero de serie es requerido')])
    activo = BooleanField('Activo', default=False)
    solidario = BooleanField('Solidario', default=False)
    ultimoMantenimiento = DateField(u'Ultimo Mantenimiento',  default=datetime.date.today(), 
                            validators=[validators.DataRequired()])
    sede_id = IntegerField(u'Sede')