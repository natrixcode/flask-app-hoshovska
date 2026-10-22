from flask import render_template
from app import app

@app.route('/')
def resume():
    page_title = "Nataliia Hoshovska | Portfolio"
    return render_template('resume.html', title=page_title)

@app.route('/contacts')
def contacts():
    page_title = "Contacts | Nataliia Hoshovska"
    return render_template('contacts.html', title=page_title)

@app.route('/homepage')
def homepage():
    return render_template('homepage.html', title="Homepage")