
users = [
    {'id':'Tom', 'username': 'Tom', 'password': '111111','Role':'user'},
    {'id':'Michael', 'username': 'Michael', 'password': '123456','Role':'user'},
    {'id':'admin', 'username': 'admin', 'password': 'admin','Role':'admin'}
]

def query_user(user_id):
    for user in users:
        if user_id == user['id']:
            return user
