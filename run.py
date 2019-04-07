# coding:utf-8

import sys
from flask import *
from form import *
from flask_bootstrap import Bootstrap 

import warnings
warnings.filterwarnings("ignore")
from config import *
import pprint

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'
bootstrap = Bootstrap(app)
app.config.from_object(__name__)


##
from model import * 
from database import * 

##1.
@app.route('/')
def index():
	return render_template('index.html')

# 2.用户登录
@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if request.method == 'POST':
		user_id = form.user_id.data 
		user = query_user(user_id)
		if user is not None and form.password.data == user['password']:
			session['current_user']= user_id
			print ('login current_user:',user_id)
			return redirect(url_for('user') )

		flash('Wrong username or password!')

	# GET 请求
	return render_template('login.html',form=form)

@app.route('/logout', methods=['GET'])
def logout():
	session.pop('current_user')
	return render_template('logout.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
	form = RegisterForm()
	if request.method == 'POST':
		user_id = form.user_id.data 
		user = query_user(user_id)
		if user is not None:
			flash('用户名已被注册!')
		else:
			if form.password.data != form.repassword.data:
				flash('密码前后不一致')
			else:

				#insert_user( )
				users = {
				'id':form.user_id.data, 
				'password':form.password.data,
				'Role':'user',
				'TotalCur':20,
				'company':form.company.data,
				'info':form.info.data
				}
				insert_user( users )
				inser_user_api(users)
				#print (user_info)

				session['current_user']= user_id
				print ('login current_user:',user_id)
				return redirect(url_for('user') )
	# GET 请求
	return render_template('register.html',form=form)

## 3. 用户
@app.route('/user', methods=['GET'])
def user():
	if 'current_user' in session:
		userapi = get_user_api_left(session['current_user'])
		userlog = get_user_api_log(session['current_user'] )
	else:
		userapi = {}
		userlog = []

	#print ('userapi',userapi)
	return render_template('user.html',userapi=userapi,userlog = userlog)

## 4. 标注语料管理；管理员权限;API 方式运作

@app.route('/resource', methods=['GET'])
def resource():
	# 验证操作用户是否为管理员
	if  'current_user' in session and query_user(session['current_user'])['Role']=='admin':

		return 'ok'
	else:
		return 'No Authority!'


def apiLog(line):
    #if not os.path.exists('apiLog.log'):
    line =[str(w) for w in line]
    flog  = open('apiLog.log','a')
    import datetime 
    now = datetime.datetime.now()
    time = str(now)

    row = [time]
    row.extend(line)
    flog.write('\t'.join(row)+'\n')
    flog.close()

####5. 
from werkzeug.utils import secure_filename
from flask import send_file, send_from_directory
import os
from flask import make_response
import sys
sys.path.append('..')
from pdfparser1207 import Parser

@app.route('/api',methods=['GET','POST'])
def api():

	if request.method == 'POST' and ('current_user' not in session):
		flash(u'你没有注册！')
		return u'未注册'

	if request.method == 'POST' and ('current_user' in session) :
		userapi = get_user_api_left(session['current_user'])

		left_api = userapi['ApiCurLeft']
		if left_api<=0:
			flash(u'API调用份额使用完了')
			return render_template('api.html')
		f = request.files['file']
		filename = secure_filename(f.filename)
		f.save('static/'+str(filename))
		print ('remote_addr:',request.remote_addr)
		print ('username:',session['current_user'])
		line = [ session['current_user'],'api',request.remote_addr,str(filename)]
		apiLog(line)
		directory ='static'
		result = Parser('static/'+str(filename )) 
		result.to_csv(directory)
		add_user_api(session['current_user'])

		filename  = filename[:-4]+'.csv'
		response = make_response(send_from_directory(directory, filename, as_attachment=True))
		response.headers["Content-Disposition"] = "attachment; filename={}".format(filename.encode().decode('latin-1'))
		return response
	else:
		return render_template('api.html')

if __name__ == '__main__':
	app.run(debug=True)
	#app.run(host='0.0.0.0',port=3000)