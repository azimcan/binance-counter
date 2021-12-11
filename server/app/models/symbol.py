from binance import Client
from binance.helpers import round_step_size

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
    self.symbol = symbol
    self.currency_pair = ''
    self.average_buy = 0
    self.average_sell = 0
    self.executed_buy = 0
    self.executed_sell = 0
    self.net_executed = 0
    self.profit = 0
    self.global_average = 0
    self.commission = 0
    self.tick_size = 0
    self.step_size = 0

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
        self.symbol = symbol['symbol']
        self.currency_pair = symbol['currency_pair']
        self.average_buy = symbol['average_buy']
        self.average_sell = symbol['average_sell']
        self.executed_buy = symbol['executed_buy']
        self.executed_sell = symbol['executed_sell']
        self.net_executed = symbol['net_executed']
        self.profit = symbol['profit']
        self.global_average = symbol['global_average']
        self.commission = symbol['commission']
        self.tick_size = symbol['tick_size']
        self.step_size = symbol['step_size']
        break
    return self.to_dict()

  def remove(self, symbol_id):
    data = self.get_symbols()
    for symbol in data:
      if symbol['symbol'] == symbol_id:
        data.remove(symbol)
        with open(SYMBOLS_FILE, 'w') as outfile:
          json.dump(data, outfile, indent=2)
        return True
    return False

  def save(self):
    self.Calculate()
    data = self.get_symbols()
    data.append(self.to_dict())
    with open(SYMBOLS_FILE, 'w') as outfile:
      json.dump(data, outfile, indent=2)

  def to_dict(self):
    return {
      'symbol': self.symbol,
      'currency_pair': self.currency_pair,
      'average_buy': self.average_buy,
      'average_sell': self.average_sell,
      'executed_buy': self.executed_buy,
      'executed_sell': self.executed_sell,
      'net_executed': self.net_executed,
      'profit': self.profit,
      'global_average': self.global_average,
      'commission': self.commission,
      'tick_size': self.tick_size,
      'step_size': self.step_size
    }

  def all_update(self):
    data = self.get_symbols()
    for symbol in data:
      self.symbol = symbol.symbol
      data.remove(symbol)
      self.Calculate()
      data.append(self.to_dict())
    with open(SYMBOLS_FILE, 'w') as outfile:
      json.dump(data, outfile, indent=2)
      
  def Calculate(self):
    self.currency_pair = self.symbol + 'USDT'

    trades_df = pd.DataFrame(client.get_my_trades(symbol=self.currency_pair))
    symbol_info = client.get_symbol_info(symbol=self.currency_pair)

    self.tick_size = float(symbol_info['filters'][0]['tickSize'])
    self.step_size = float(symbol_info['filters'][2]['stepSize'])

    if(trades_df.size != 0):
      trades_df = trades_df[trades_df['time'] >= 1633972308381]

      trades_df['price'] = trades_df['price'].astype(float)
      trades_df['qty'] = trades_df['qty'].astype(float)
      trades_df['quoteQty'] = trades_df['quoteQty'].astype(float)
      trades_df['commission'] = trades_df['commission'].astype(float)


      try:
        self.average_buy = round_step_size(average(trades_df[trades_df['isBuyer'] == True]['price'], weights=trades_df[trades_df['isBuyer'] == True]['qty']), self.tick_size)
      except:
        self.average_buy = 0.0
      self.executed_buy = round_step_size(trades_df[trades_df['isBuyer'] == True]['qty'].sum(), self.step_size)


      try:
        self.average_sell = round_step_size(average(trades_df[trades_df['isBuyer'] == False]['price'], weights=trades_df[trades_df['isBuyer'] == False]['qty']), self.tick_size)
      except:
        self.average_sell = 0.0
      self.executed_sell = round_step_size(trades_df[trades_df['isBuyer'] == False]['qty'].sum(), self.step_size)


      self.profit = round_step_size(self.average_sell*self.executed_sell - self.average_buy*self.executed_buy, self.tick_size)

      self.net_executed = round_step_size(self.executed_buy - self.executed_sell, self.step_size)

      if(self.profit < 0 and self.net_executed > 0):
        self.global_average = round_step_size(abs(self.profit) / self.net_executed, self.tick_size)
      else:
        self.global_average = 0

      self.commission = round(trades_df['commission'].sum(), 8)

    return self.to_dict()


