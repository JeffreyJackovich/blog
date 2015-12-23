#from flask.ext.wtforms import Form

#rom wtforms import TextField, PasswordField, Required, Email


class ExistingUser(object):
    def __init__(self, message="Email doesn't exists"):
        self.message = message

    def __call__(self, form, field):
        if not User.query.filter_by(email=field.data).first():
            raise ValidationError(self.message)

reset_rules = [validators.Required(),
          validators.Email(),
          ExistingUser(message='Email address is not available')
         ]

class ResetPassword(Form):
    email = TextField('Email', validators=reset_rules)

class ResetPasswordSubmit(Form):
    password = PasswordField('Password', validators=custom_validators['edit_password'], )
    confirm = PasswordField('Confirm Password')