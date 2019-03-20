from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,FileField
from wtforms.validators import Required

class LoginForm(FlaskForm):
	user_id = StringField('userid', validators=[Required()])
	password = StringField('password', validators=[Required()])
	submit = SubmitField('Submit')

class apiForm(FlaskForm):

	file = FileField('file')
	submit = SubmitField('Submit')