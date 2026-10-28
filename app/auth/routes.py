from flask import Blueprint, render_template, request, redirect, url_for, session, flash, make_response

auth_bp = Blueprint('auth', __name__, template_folder='templates')

# Заглушки для автентифікації (Логін: admin, Пароль: password123)
USER_CREDENTIALS = {"admin": "password123"}

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if USER_CREDENTIALS.get(username) == password:
            session['username'] = username
            flash(f'Успішний вхід! Вітаємо, {username}.', 'success')
            return redirect(url_for('auth.profile'))
        else:
            flash('Неправильні дані! Спробуйте ще раз.', 'danger')
            return redirect(url_for('auth.login'))
            
    return render_template('auth/login.html')

@auth_bp.route('/profile')
def profile():
    if 'username' not in session:
        flash('Будь ласка, увійдіть у систему.', 'warning')
        return redirect(url_for('auth.login'))
    
    # Отримуємо тему з кукі (за замовчуванням світла)
    theme = request.cookies.get('theme', 'light')
    # Отримуємо всі кукі для таблиці
    cookies_list = request.cookies
    
    return render_template('auth/profile.html', username=session['username'], theme=theme, cookies=cookies_list)

@auth_bp.route('/logout')
def logout():
    session.pop('username', None)
    flash('Ви вийшли з системи.', 'info')
    return redirect(url_for('auth.login'))

# --- Робота з кукі ---

@auth_bp.route('/add_cookie', methods=['POST'])
def add_cookie():
    if 'username' not in session:
        return redirect(url_for('auth.login'))
    
    key = request.form.get('cookie_key')
    value = request.form.get('cookie_value')
    days = int(request.form.get('cookie_days', 1))
    
    if key and value:
        resp = make_response(redirect(url_for('auth.profile')))
        resp.set_cookie(key, value, max_age=days*24*60*60)
        flash(f'Кукі "{key}" успішно додано!', 'success')
        return resp
    return redirect(url_for('auth.profile'))

@auth_bp.route('/delete_cookie', methods=['POST'])
def delete_cookie():
    if 'username' not in session:
        return redirect(url_for('auth.login'))
    
    key = request.form.get('cookie_key')
    if key:
        resp = make_response(redirect(url_for('auth.profile')))
        resp.delete_cookie(key)
        flash(f'Кукі "{key}" видалено.', 'success')
        return resp
    return redirect(url_for('auth.profile'))

@auth_bp.route('/delete_all_cookies', methods=['POST'])
def delete_all_cookies():
    if 'username' not in session:
        return redirect(url_for('auth.login'))
    
    resp = make_response(redirect(url_for('auth.profile')))
    for key in request.cookies:
        resp.delete_cookie(key)
    flash('Всі кукі видалено.', 'success')
    return resp

# --- Зміна кольорової схеми (Тема) ---

@auth_bp.route('/set_theme/<theme_name>')
def set_theme(theme_name):
    if 'username' not in session:
        return redirect(url_for('auth.login'))
    
    if theme_name in ['light', 'dark']:
        resp = make_response(redirect(url_for('auth.profile')))
        resp.set_cookie('theme', theme_name, max_age=30*24*60*60)
        flash(f'Тему змінено на {theme_name}.', 'success')
        return resp
    return redirect(url_for('auth.profile'))