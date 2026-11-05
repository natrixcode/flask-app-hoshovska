import pytest
from app import create_app

@pytest.fixture
def app(tmp_path):
    app = create_app({'TESTING': True, 'WTF_CSRF_ENABLED': False,
                      'DATA_PATH': str(tmp_path / 'products.json'),
                      'CONTACT_LOG': str(tmp_path / 'contacts.log'),
                      'UPLOAD_FOLDER': str(tmp_path / 'uploads')})
    return app

@pytest.fixture
def client(app):
    return app.test_client()
