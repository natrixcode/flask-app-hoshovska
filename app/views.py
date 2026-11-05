import logging
from logging.handlers import RotatingFileHandler
from flask import Blueprint, current_app, flash, redirect, render_template, url_for
from app.forms import ContactForm

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        try:
            logger = logging.getLogger('contact_messages')
            log_path = current_app.config['CONTACT_LOG']
            # Avoid duplicated handlers when testing multiple app instances.
            handler = next((h for h in logger.handlers if getattr(h, 'baseFilename', None) == log_path), None)
            if handler is None:
                handler = RotatingFileHandler(log_path, maxBytes=1_000_000, backupCount=2, encoding='utf-8')
                handler.setFormatter(logging.Formatter('%(asctime)s | %(message)s'))
                logger.addHandler(handler)
            logger.setLevel(logging.INFO)
            logger.info('Name=%r | Email=%r | Phone=%r | Subject=%r | Message=%r',
                        form.name.data, form.email.data, form.phone.data, form.subject.data, form.message.data)
            flash('Повідомлення успішно збережено в журналі!', 'success')
        except OSError:
            current_app.logger.exception('Помилка запису контактного повідомлення')
            flash('Не вдалося зберегти повідомлення. Спробуйте пізніше.', 'danger')
        return redirect(url_for('main.contact'))
    if form.is_submitted() and not form.validate():
        flash('Перевірте правильність заповнення полів.', 'danger')
    return render_template('contact.html', form=form)
