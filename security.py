from werkzeug.security import safe_str_cmp
from models.user import UserModel

def authenticate(username, password):
    #user = username_mapping.get(username, None) # Another way to get data from dictionary (instead of []). None is the default value if username is not found
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password,password):
        return user

def identity(payload):
    user_id = payload['identity']
    #return userid_mapping.get(user_id, None)
    return UserModel.find_by_id(user_id) 
