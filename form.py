from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,FileField
from wtforms.validators import Required

class LoginForm(FlaskForm):
	user_id = StringField('用户名', validators=[Required()])
	password = StringField('密码', validators=[Required()])
	submit = SubmitField('登陆')

class RegisterForm(FlaskForm):
	user_id = StringField('用户名', validators=[Required()])
	password = StringField('密码', validators=[Required()])
	repassword = StringField('验证密码', validators=[Required()])
	company =  StringField('公司', validators=[Required()])
	info =  StringField('个人简介', validators=[Required()])
	submit = SubmitField('注册')

class apiForm(FlaskForm):

	file = FileField('file')
	submit = SubmitField('Submit')