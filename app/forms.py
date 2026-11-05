import re
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Regexp


class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=4, max=10)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired(), Regexp(r'^\+380\d{9}$', message='Формат: +380XXXXXXXXX')])
    subject = SelectField('Subject', choices=[('', 'Оберіть тему'), ('question', 'Запитання'), ('order', 'Замовлення'), ('support', 'Підтримка')], validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired(), Length(max=500)])
    submit = SubmitField('Send Message')
