# Лабораторна робота №5 — Flask-WTF + TinyDB

## Встановлення на macOS

```bash
cd lab5_flask_wtf
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python run.py
```

Відкрийте http://127.0.0.1:5000

- `/contact` — контактна форма, записи в `logs/contacts.log`
- `/product` — список товарів
- `/product/add` — створення товару
- `/product/<id>` — деталі
- `/product/<id>/edit` — редагування
- `/product/<id>/delete` — POST видалення (через кнопку на сторінці деталей)

Дані зберігаються в `data/products.json`, зображення — в `app/products/static/uploads/`.

## Тести

```bash
python -m pytest -v
```

## Git-коміти за етапами

1. `git commit -m "feat: implement Flask-WTF contact form and validation"`
2. `git commit -m "feat: add TinyDB product CRUD and image uploads"`
3. `git commit -m "test: cover contact form and product CRUD"`

Коміти треба робити після реального виконання кожного етапу, а не всі наприкінці. Перед кожним комітом виконайте `git status`, `git add ...`.

**Безпека:** для публічного розгортання встановіть випадковий `SECRET_KEY` у змінних середовища та вимкніть debug.
