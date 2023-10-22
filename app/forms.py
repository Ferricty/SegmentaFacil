from flask_wtf import FlaskForm
from wtforms import IntegerField,SubmitField,FloatField
from wtforms.validators import DataRequired, ValidationError

# Estableciendo Validaciones
def campo_positivo(form,field):
    error_to_show ={
    "recency":  "El valor de Recency tiene que ser positivo (mayor que 0)",
    "frequency":  "El valor de Frequency tiene que ser positivo (mayor que 0)",
    "monetary_value":  "El valor del campo Monetary Value tiene que ser positivo (mayor que 0)"}
    if field.data <=0:
        raise ValidationError(error_to_show[field.name])

def campo_menor_365(form,field):
    if field.data >=365:
        raise ValidationError('El valor de recency tiene que ser menor que 365 días. Si el cliente compró hace más de un año ya ha abandonado la compañía')

class CustomerForm(FlaskForm):

    recency = IntegerField('Recency',
                           validators=[
                               DataRequired(message = "El valor recency es un campo numérico positivo (mayor que 0) necesario para segmentar los clientes"),
                               campo_menor_365,
                               campo_positivo
                               ])


    frequency = IntegerField('Frequency',validators=[
        DataRequired(message = "El valor frequency es un campo numérico positivo (mayor que 0) necesario para segmentar los clientes"),
        campo_positivo
        ])


    monetary_value = FloatField('Monetary Value',validators=[
        DataRequired(message = "El valor monetario es un campo numérico positivo (mayor que 0) necesario para segmentar los clientes"),
        campo_positivo
    ])
    submit = SubmitField('Submit')


