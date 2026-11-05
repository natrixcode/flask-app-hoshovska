from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from uuid import uuid4

from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from PIL import Image, UnidentifiedImageError
from tinydb import Query
from werkzeug.exceptions import NotFound
from werkzeug.utils import secure_filename

from app.products.forms import ProductForm, DeleteForm
from app.products.storage import get_table, get_product

products = Blueprint('products', __name__, url_prefix='/product',
                     template_folder='templates', static_folder='static')
ALLOWED_FORMATS = {'PNG': '.png', 'JPEG': '.jpg'}


def save_image(file):
    if not file or not file.filename:
        return None
    if not secure_filename(file.filename).lower().endswith(('.png', '.jpg', '.jpeg')):
        raise ValueError('Дозволено лише PNG, JPG, JPEG.')
    try:
        file.stream.seek(0)
        with Image.open(file.stream) as image:
            image.verify()
        file.stream.seek(0)
        with Image.open(file.stream) as image:
            fmt = image.format
            if fmt not in ALLOWED_FORMATS:
                raise ValueError('Непідтримуваний формат зображення.')
            # Re-encode image to avoid retaining untrusted metadata.
            filename = f'{uuid4().hex}{ALLOWED_FORMATS[fmt]}'
            destination = Path(current_app.config['UPLOAD_FOLDER']) / filename
            image.convert('RGB').save(destination, format='JPEG') if fmt == 'JPEG' else image.save(destination, format='PNG')
        return f'uploads/{filename}'
    except (UnidentifiedImageError, OSError) as exc:
        raise ValueError('Файл не є коректним зображенням.') from exc


def delete_image(path):
    if path and path.startswith('uploads/'):
        filename = Path(path).name
        (Path(current_app.config['UPLOAD_FOLDER']) / filename).unlink(missing_ok=True)


def image_url(path):
    if path and path.startswith('uploads/') and (Path(current_app.config['UPLOAD_FOLDER']) / Path(path).name).is_file():
        return url_for('products.static', filename=path)
    return None

products.add_app_template_global(image_url, name='product_image_url')


@products.route('')
@products.route('/')
def list_products():
    db, table = get_table()
    try:
        items = sorted(table.all(), key=lambda x: x['id'], reverse=True)
    finally:
        db.close()
    return render_template('products/products.html', items=items)


@products.route('/add', methods=['GET', 'POST'])
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        try:
            image = save_image(form.image.data)
        except ValueError as exc:
            form.image.errors.append(str(exc))
        else:
            db, table = get_table()
            try:
                # Preserve monotonic IDs even when the last product was deleted.
                meta = db.table('meta')
                last_id = meta.get(Query().key == 'last_product_id')
                product_id = (last_id['value'] if last_id else 0) + 1
                meta.upsert({'key': 'last_product_id', 'value': product_id}, Query().key == 'last_product_id')
                table.insert({'id': product_id, 'name': form.name.data.strip(),
                              'content': form.content.data.strip(), 'price': str(form.price.data),
                              'category': form.category.data, 'quantity': form.quantity.data,
                              'image': image, 'created_at': datetime.now(timezone.utc).isoformat(timespec='seconds')})
            finally:
                db.close()
            flash('Товар успішно додано.', 'success')
            return redirect(url_for('products.list_products'))
    elif request.method == 'POST':
        flash('Перевірте введені дані.', 'danger')
    return render_template('products/form.html', form=form, heading='Додати товар', product=None)


@products.route('/<int:id>')
def product_detail(id):
    product = get_product(id)
    if product is None:
        raise NotFound()
    return render_template('products/detail_product.html', product=product, delete_form=DeleteForm())


@products.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit_product(id):
    product = get_product(id)
    if product is None:
        raise NotFound()
    form = ProductForm(data=product) if request.method == 'GET' else ProductForm()
    if form.validate_on_submit():
        try:
            new_image = save_image(form.image.data)
        except ValueError as exc:
            form.image.errors.append(str(exc))
        else:
            db, table = get_table()
            try:
                table.update({'name': form.name.data.strip(), 'content': form.content.data.strip(),
                              'price': str(form.price.data), 'category': form.category.data,
                              'quantity': form.quantity.data,
                              'image': new_image if new_image else product.get('image')}, Query().id == id)
            finally:
                db.close()
            if new_image:
                delete_image(product.get('image'))
            flash('Товар успішно оновлено.', 'success')
            return redirect(url_for('products.product_detail', id=id))
    elif request.method == 'POST':
        flash('Перевірте введені дані.', 'danger')
    return render_template('products/form.html', form=form, heading='Редагувати товар', product=product)


@products.route('/<int:id>/delete', methods=['POST'])
def delete_product(id):
    form = DeleteForm()
    if not form.validate_on_submit():
        flash('Не вдалося підтвердити видалення.', 'danger')
        return redirect(url_for('products.product_detail', id=id))
    db, table = get_table()
    try:
        product = table.get(Query().id == id)
        if product is None:
            raise NotFound()
        table.remove(Query().id == id)
    finally:
        db.close()
    delete_image(product.get('image'))
    flash('Товар видалено.', 'success')
    return redirect(url_for('products.list_products'))
