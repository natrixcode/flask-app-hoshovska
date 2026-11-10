from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, DateTimeLocalField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length

class PostForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired(), Length(max=150)])
    content = TextAreaField('Текст публікації', validators=[DataRequired()])
    enabled = BooleanField('Опублікувати', default=True)
    publish_date = DateTimeLocalField('Дата й час публікації', format='%Y-%m-%dT%H:%M', default=datetime.now, validators=[DataRequired()])
    category = SelectField('Категорія', choices=[('news', 'Новини'), ('publication', 'Публікації'), ('tech', 'Технології'), ('other', 'Інше')])
    submit = SubmitField('Зберегти')
