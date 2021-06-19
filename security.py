from werkzeug.security import safe_str_cmp
from resources.user import User

"""
users = [
    {
        'id': 1,
        'username': 'bob',
        'password': 'asdf'
    }
]
"""

users = [
    User(1, 'bob', 'asdf')
]

"""
username_mapping = { 'bob': {
        'id': 1,
        'username': 'bob',
        'password': 'asdf'
}}
"""

username_mapping = {u.username: u for u in users}
"""
userid_mapping = {1: {
        'id': 1,
        'username': 'bob',
        'password': 'asdf'
}}
"""
userid_mapping = {u.id: u for u in users}



def authenticate(username, password):
    #user = username_mapping.get(username, None) # Another way to get data from dictionary (instead of []). None is the default value if username is not found
    user = User.find_by_username(username)
    if user and safe_str_cmp(user.password,password):
        return user

def identity(payload):
    user_id = payload['identity']
    #return userid_mapping.get(user_id, None)
    return User.find_by_id(user_id)
