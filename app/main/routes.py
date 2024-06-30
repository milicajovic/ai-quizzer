from flask import render_template

from . import main


@main.route('/')
def home():
    return render_template('main/home.html')

@main.route('/about')
def about():
    return render_template('main/about.html')

@main.route('/contact')
def contact():
    return render_template('main/contact.html')