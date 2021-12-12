from flask import Flask, request, jsonify
from flask_cors import CORS

from app.models import Symbol
from app.models import User

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

@app.route('/symbols', methods=['GET', 'POST'])
def all_symbols():
  sym = Symbol()
  response_object = {'status': 'success'}
  if request.method == 'POST':
    post_data = request.get_json()
    sym.symbol = post_data.get("symbol")
    sym.save()

    response_object['message'] = 'Symbol added!'
  else:
    response_object['symbols'] = sym.get_symbols()

  return jsonify(response_object)

@app.route('/symbols/<symbol_id>', methods=['GET', 'DELETE'])
def single_symbol(symbol_id):
  sym = Symbol()
  response_object = {'status': 'success'}
  if request.method == 'DELETE':
    sym.remove(symbol_id)
    response_object['message'] = 'Symbol removed!'
  else:
    SYMBOLS = sym.get_symbols()
    for symbol in SYMBOLS:
      if symbol['symbol'] == symbol_id:
        response_object['symbol'] = symbol

  return jsonify(response_object)

@app.route('/symbols/update', methods=['GET'])
def all_symbol_update():
  sym = Symbol()
  response_object = {'status': 'success'}
  if request.method == 'GET':
    sym.all_update()
    response_object['message'] = 'Symbols updated!'

  return jsonify(response_object)

@app.route('/users/<username>', methods=['GET'])
def user(username):
  user = User()
  response_object = {'status': 'success'}
  if request.method == 'GET':
    response_object['user'] = user.find(username)

  return jsonify(response_object)