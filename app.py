from flask import Flask, render_template, request, redirect, url_for
from wtforms import Form
from forms import ContactForm
import sys
app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')


@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/hello')
@app.route('/hello/<name>')
def hello_name(name=None):
    return render_template('index.html', name=name)

@app.route('/question')
def question():
    form = ContactForm()  # https://hackersandslackers.com/flask-wtforms-forms/
    if request.method == 'POST':
        if request.form['submit_button'] == 'Do Something':
            return render_template('index.html', name = 'hest')
        elif request.form['submit_button'] == 'Do Something Else':
            return url_for('127.0.0.1:5000/hello')   # render_template('index.html', name=None)
        else:
            print('unknown')
    elif request.method == 'GET':
        print(42, sys.stderr)
        return render_template('buttons.html', form=form)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm(request.form)
    if request.method == 'POST':#form.validate():#form.validate_on_submit():
        return 'POST'
        # return render_template('index.html')
    return render_template('contact.html', form=form)

@app.route('/success')
def success():
    return '42'

if __name__ == '__main__':
    app.run(debug=True, port=5001)