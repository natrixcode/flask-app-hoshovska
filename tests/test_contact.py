def test_contact_valid(client, app):
    response = client.post('/contact', data={'name': 'Олена', 'email': 'test@example.com',
        'phone': '+380991234567', 'subject': 'question', 'message': 'Тестове повідомлення'}, follow_redirects=True)
    assert response.status_code == 200
    assert 'успішно збережено'.encode() in response.data
    assert 'test@example.com' in open(app.config['CONTACT_LOG'], encoding='utf-8').read()


def test_contact_invalid(client):
    response = client.post('/contact', data={'name': 'A', 'email': 'bad', 'phone': '123', 'subject': '', 'message': ''})
    assert response.status_code == 200
    assert 'Перевірте правильність'.encode() in response.data
