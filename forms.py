# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 23:58:08 2020

@author: nki
"""

from flask_wtf import RecaptchaField, FlaskForm
from wtforms import Form, TextField, TextAreaField, SubmitField, StringField
from wtforms.validators import DataRequired, Email, Length

class ContactForm(FlaskForm):
    """Contact form."""
    name = StringField('Name', [
        DataRequired()])
    email = StringField('Email', [
        Email(message=('Not a valid email address.')),
        DataRequired()])
    body = TextField('Message', [
        DataRequired(),
        Length(min=4, message=('Your message is too short.'))])
    recaptcha = RecaptchaField()
    submit = SubmitField('Submit')