import json

USERS_FILE = 'data/users.json'

class User:
  def __init__(self, username = '', password = ''):
    self.username = username
    self.password = password
  
  def get_users(self):
    users = []
    try:
      with open(USERS_FILE) as json_file:
        users = json.load(json_file)
    except:
      with open(USERS_FILE, 'w') as outfile:
        json.dump([], outfile, indent=2)
    return users

  def find(self, username):
    users = self.get_users()
    for user in users:
      if user['username'] == username:
        return user
    return {"error": "OK!"}

  def to_dict(self):
    return {
      'username': self.username,
      'password': self.password,
    }
