from io import BytesIO
from PIL import Image
from tinydb import TinyDB


def product_data(**changes):
    data = {'name': 'Тестовий товар', 'content': 'Опис тестового товару',
            'price': '125.50', 'category': 'books', 'quantity': '3'}
    data.update(changes)
    return data


def create(client, **changes):
    return client.post('/product/add', data=product_data(**changes), follow_redirects=True)


def test_create_read(client, app):
    response = create(client)
    assert response.status_code == 200
    assert 'Тестовий товар'.encode() in response.data
    with TinyDB(app.config['DATA_PATH']) as db:
        product = db.table('products').all()[0]
    assert product['id'] == 1 and product['price'] == '125.50'
    assert product['created_at']
    assert client.get('/product/1').status_code == 200


def test_update_keeps_id_and_date(client, app):
    create(client)
    with TinyDB(app.config['DATA_PATH']) as db:
        old = db.table('products').all()[0]
    response = client.post('/product/1/edit', data=product_data(name='Оновлений товар'), follow_redirects=True)
    assert response.status_code == 200
    with TinyDB(app.config['DATA_PATH']) as db:
        new = db.table('products').all()[0]
    assert new['name'] == 'Оновлений товар'
    assert new['id'] == old['id'] and new['created_at'] == old['created_at']


def test_delete_and_missing(client):
    create(client)
    assert client.get('/product/999').status_code == 404
    assert client.get('/product/1/delete').status_code == 405
    response = client.post('/product/1/delete', follow_redirects=True)
    assert response.status_code == 200
    assert client.get('/product/1').status_code == 404


def test_validation(client):
    response = create(client, name='ab', price='-5', quantity='-1')
    assert 'Перевірте введені дані'.encode() in response.data
    assert client.get('/product/1').status_code == 404
    response = create(client, price='10.123')
    assert 'не більше 2 знаків'.encode() in response.data


def test_upload_and_keep_image(client, app):
    image = Image.new('RGB', (8, 8), 'red')
    buffer = BytesIO()
    image.save(buffer, format='PNG')
    buffer.seek(0)
    response = client.post('/product/add', data={**product_data(), 'image': (buffer, 'photo.png')}, content_type='multipart/form-data', follow_redirects=True)
    assert response.status_code == 200
    with TinyDB(app.config['DATA_PATH']) as db:
        old = db.table('products').all()[0]
    assert old['image'].startswith('uploads/')
    client.post('/product/1/edit', data=product_data(name='Інша назва'))
    with TinyDB(app.config['DATA_PATH']) as db:
        new = db.table('products').all()[0]
    assert new['image'] == old['image']


def test_missing_image(client):
    create(client)
    assert 'Без зображення'.encode() in client.get('/product').data


def test_bad_image(client):
    response = client.post('/product/add', data={**product_data(), 'image': (BytesIO(b'not an image'), 'bad.png')}, content_type='multipart/form-data')
    assert 'коректним зображенням'.encode() in response.data
    assert client.get('/product/1').status_code == 404
