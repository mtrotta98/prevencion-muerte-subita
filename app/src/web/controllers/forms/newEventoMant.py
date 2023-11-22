import datetime
from wtforms import Form, validators
from wtforms.fields import StringField, IntegerField, DateField
from wtforms_components import DateRange



class NewEventoMantForm(Form):
    dea_id = IntegerField(u'Sede')
    fecha = DateField(u'Ultimo Mantenimiento',  default=datetime.date.today(), 
                            validators=[validators.DataRequired(message='Se requiere una fecha'), DateRange(max=datetime.date.today(),message='No puede ingresar una fecha futura')])
    descripcion = StringField(u'Descripcion del evento', validators=[
                             validators.input_required(message='Se requiere una descripcion')])
 