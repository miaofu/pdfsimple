import pandas as pd 
'''
users = [
    {'id':'Tom', 'username': 'Tom', 'password': '111111','Role':'user'},
    {'id':'Michael', 'username': 'Michael', 'password': '123456','Role':'user'},
    {'id':'admin', 'username': 'admin', 'password': 'admin','Role':'admin'}
]
'''

def load_user():
	users = pd.read_csv('user.csv')
	print (users)
	dd = []
	for i,r in users.iterrows():
		dd.append (dict(r))
	users = dd 
	return users 


def insert_user(user):
	#
	if not user['id']:
		return 0
	users = pd.read_csv('user.csv')

	dd = pd.Series(user)
	users = users.append(dd,ignore_index=True)
	print (users)
	users.to_csv('user.csv',index=False)

	# 
def inser_user_api(user):

	data = pd.read_csv('userAPI.csv')
	tmp = data['id']==user['id']
	g = data.loc[data['id']==user['id']]
	tmp = {'id':user['id'], 'TotalCur':user['TotalCur'], 'ApiCurUse':0,'ApiCurLeft':user['TotalCur']}
	#id,TotalCur,ApiCurUse,ApiCurLeft 
	if len(tmp)!=0:
		data = data.append( tmp, ignore_index = True)

		data.to_csv('userAPI.csv',index=False)



def query_user(user_id):
	users = load_user()
	for user in users:
		if user_id == user['id']:
			return user

def add_user_api(user_id):
	#
	data = pd.read_csv('userAPI.csv')
	tmp = data['id']==user_id
	g = data.loc[data['id']==user_id]
	if len(g):
		data.loc[tmp,'ApiCurUse']+=1
		data.loc[tmp,'ApiCurLeft']-=1 
	else:
		print ('wrong!')
	data.to_csv('userAPI.csv',index=None)

def get_user_api_left(user_id):
	#
	data = pd.read_csv('userAPI.csv')
	tmp = data['id']==user_id
	g = data.loc[data['id']==user_id]
	if len(g):
		return dict(g.iloc[0])
	else:
		print ('wrong!')
		return {}

def get_user_api_log(user_id):
	#
	if not os.path.exists('apiLog.log'):
		return []
	
	data = pd.read_csv('apiLog.log',sep='\t')
	data['id'] = data.index
	sdata = data.loc[data['user']==user_id]

	gg = []
	for i,r in sdata.iterrows():
		g = dict(r)
		  
		gg.append( g)
	return gg 

#add_user_api('admin')	
#print get_user_api_left('admin')
#get_user_api_log('admin')
user = {'id':'','username':'','password':'','Role':'','TotalCur':10}
insert_user(user)