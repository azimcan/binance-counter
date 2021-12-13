from binance import Client
from binance.helpers import round_step_size
from binance.exceptions import BinanceAPIException

import pandas as pd
from numpy import average

import json

SYMBOLS_FILE = 'data/symbols.json'

api_json = pd.read_json("data/api.json", orient="index")

API_KEY = api_json[0]["api_key"]
API_SECRET = api_json[0]["api_secret"]

client = Client(API_KEY, API_SECRET)

class Symbol:
  def __init__(self, symbol = ''):
    self.symbol = {
      "symbol": symbol,
      "currency_pair": '',
      "average_buy": 0,
      "average_sell": 0,
      "executed_buy": 0,
      "executed_sell": 0,
      "net_executed": 0,
      "profit": 0,
      "global_average": 0,
      "commission": 0,
      "tick_size": 0,
      "step_size": 0
    }

  def get_symbols(self):
    data = []
    try:
      with open(SYMBOLS_FILE) as json_file:
        data = json.load(json_file)
    except:
      with open(SYMBOLS_FILE, 'w') as outfile:
        json.dump([], outfile, indent=2)
    return data

  def get_symbol(self, symbol_id = None):
    symbols = self.get_symbols()

    for symbol in symbols:
      if(symbol['symbol'] == symbol_id):
        return symbol
    return None

  def remove(self, symbol_id):
    data = self.get_symbols()
    for symbol in data:
      if symbol['symbol'] == symbol_id:
        data.remove(symbol)
        with open(SYMBOLS_FILE, 'w') as outfile:
          json.dump(data, outfile, indent=2)
        return True
    return False

  def save(self, symbol):
    try:
      self.symbol["symbol"] = symbol
      self.Calculate()
      data = self.get_symbols()
      data.append(self.symbol)
      with open(SYMBOLS_FILE, 'w') as outfile:
        json.dump(data, outfile, indent=2)
      return {
        'status': True
      }
    except BinanceAPIException as e:
      return {
        'status': False,
        'message': e.message
      }
    

  def all_update(self):
    data = self.get_symbols()
    for symbol in data:
      self.symbol["symbol"] = symbol["symbol"]
      data.remove(symbol)
      self.Calculate()
      data.append(self.symbol)
    with open(SYMBOLS_FILE, 'w') as outfile:
      json.dump(data, outfile, indent=2)

  def Calculate(self):
    self.symbol["currency_pair"] = self.symbol["symbol"] + 'USDT'

    trades_df = pd.DataFrame(client.get_my_trades(symbol=self.symbol["currency_pair"]))
    symbol_info = client.get_symbol_info(symbol=self.symbol["currency_pair"])

    self.symbol["tick_size"] = float(symbol_info['filters'][0]['tickSize'])
    self.symbol["step_size"] = float(symbol_info['filters'][2]['stepSize'])

    if(trades_df.size != 0):
      trades_df = trades_df[trades_df['time'] >= 1633972308381]

      trades_df['price'] = trades_df['price'].astype(float)
      trades_df['qty'] = trades_df['qty'].astype(float)
      trades_df['quoteQty'] = trades_df['quoteQty'].astype(float)
      trades_df['commission'] = trades_df['commission'].astype(float)


      try:
        self.symbol["average_buy"] = round_step_size(average(trades_df[trades_df['isBuyer'] == True]['price'], weights=trades_df[trades_df['isBuyer'] == True]['qty']), self.symbol["tick_size"])
      except:
        self.symbol["average_buy"] = 0.0
      self.symbol["executed_buy"] = round_step_size(trades_df[trades_df['isBuyer'] == True]['qty'].sum(), self.symbol["step_size"])


      try:
        self.symbol["average_sell"] = round_step_size(average(trades_df[trades_df['isBuyer'] == False]['price'], weights=trades_df[trades_df['isBuyer'] == False]['qty']), self.symbol["tick_size"])
      except:
        self.symbol["average_sell"] = 0.0
      self.symbol["executed_sell"] = round_step_size(trades_df[trades_df['isBuyer'] == False]['qty'].sum(), self.symbol["step_size"])


      self.symbol["profit"] = round_step_size(self.symbol["average_sell"]*self.symbol["executed_sell"] - self.symbol["average_buy"]*self.symbol["executed_buy"], self.symbol["tick_size"])

      self.symbol["net_executed"] = round_step_size(self.symbol["executed_buy"] - self.symbol["executed_sell"], self.symbol["step_size"])

      if(self.symbol["profit"] < 0 and self.symbol["net_executed"] > 0):
        self.symbol["global_average"] = round_step_size(abs(self.symbol["profit"]) / self.symbol["net_executed"], self.symbol["tick_size"])
      else:
        self.symbol["global_average"] = 0

      self.symbol["commission"] = round(trades_df['commission'].sum(), 8)



