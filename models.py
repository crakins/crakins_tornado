from wtforms import Form, BooleanField, StringField, validators

class Email(Form):
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
