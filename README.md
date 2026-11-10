# Лабораторна №6 — Flask ORM / SQLAlchemy / CRUD

Продовження лабораторної №5. Python, Flask, SQLAlchemy 2.0, Flask-Migrate, Flask-WTF, Bootstrap 5, unittest.

## Запуск на macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
```

В `.env` замініть `SECRET_KEY` на власний випадковий ключ.

### Для звіту: міграції у два етапи

У фінальній моделі `app/posts/models.py` вже є `author` і `is_active`. Щоб показати **дві окремі міграції** відповідно до методички, перед першою міграцією тимчасово видаліть ці два поля з моделі (і відповідні імпорти за бажанням). Після `flask db init`, `flask db migrate -m "Initial migration"`, `flask db upgrade` поверніть обидва поля з цього файлу й виконайте `flask db migrate -m "add is_active, author"`, `flask db upgrade`. У SQLite Alembic може вимагати `batch_alter_table` для складніших змін, але додавання цих полів з `server_default` підтримується.

```bash
flask db --help
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
flask db migrate -m "add is_active, author"
flask db upgrade
flask db history
flask run
```

**Не виконуйте дві команди `migrate` без зміни моделі між ними.**

## Flask Shell — частина 2 (до міграцій, у тимчасовій базі)

```python
from app import db
from app.posts.models import Post
db.create_all()
p = Post(title='Test', content='Example post')
db.session.add(p)
db.session.commit()
db.session.scalars(db.select(Post).order_by(Post.title.asc())).all()
db.session.get(Post, p.id)
db.session.delete(p)
db.session.commit()
db.session.scalars(db.select(Post)).all()
db.drop_all()
```

Після цієї демонстрації закрийте shell, видаліть тимчасову базу `instance/data.sqlite`, і лише тоді робіть міграції.

## Тести

```bash
python -m unittest discover -s tests -v
```

## Git

У попередньому репозиторії створіть гілку `lab6` від `lab5` та перенесіть файли з цього архіву, зберігши історію Git. Не комітьте `.env` та `instance/`.
