from wtforms import Form, validators
from wtforms.fields import StringField, BooleanField, IntegerField, SelectField


class NewDEAForm(Form):
    denominacion = StringField(u'Denominacion', validators=[
                             validators.input_required(message='Se requiere una denominacion')])
    marca = SelectField(u'Marca', validate_choice=False, coerce=int,
                        validators=[validators.input_required(message='Marca es requerido')])
    modelo = SelectField(u'Modelo', validate_choice=False, coerce=int,
                         validators=[validators.input_required(message='Modelo es requerido')])
    nSerie = StringField(u'Numero de Serie', validators=[
                             validators.input_required(message='Numero de serie es requerido')])
    activo = BooleanField('Activo', default=False)
    solidario = BooleanField('Solidario', default=False)
    sede = SelectField(u'Sede',  validate_choice=False,coerce=int,
                       validators=[validators.input_required(message='Debe asignarse una sede')])
    responsable = SelectField(u'Responsable', validate_choice=False, coerce=int,
                       validators=[validators.input_required(message='Debe asignarse un responsable')])