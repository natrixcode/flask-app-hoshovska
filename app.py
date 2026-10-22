from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def resume():
    page_title = "Моє Резюме - Головна"
    return render_template('resume.html', title=page_title)

@app.route('/contacts')
def contacts():
    page_title = "Контакти - Зв'яжіться зі мною"
    return render_template('contacts.html', title=page_title)

if __name__ == '__main__':
    app.run(debug=True)