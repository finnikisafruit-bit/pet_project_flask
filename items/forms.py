from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField
from wtforms.validators import DataRequired, Length


class ProductForm(FlaskForm):
    name = StringField("Название", validators=[DataRequired(), Length(max=120)])
    price = IntegerField("Цена", validators=[DataRequired()])
    size = StringField("Размер", validators=[DataRequired(), Length(max=4)])
    submit = SubmitField("Добавить")
