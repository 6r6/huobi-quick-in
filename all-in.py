#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import requests
from plugins.huobi.HuobiServices import get_balance, send_order


COIN1 = 'ruff'
COIN2 = 'eth'


def get_tote(coin):
    balance_dict = get_balance()
    token = {coin: 0}
    token_list = balance_dict['data']['list']
    for item in token_list:
        if item['currency'] == coin and item['type'] == 'trade':
            token[coin] = item['balance']
            break
    return token[coin]


def get_price(symbol):
    addr = 'https://api.huobi.pro/market/trade?symbol={symbol}'
    resp_json = requests.get(addr.format(symbol=symbol)).text
    if 'ok' in resp_json:
        resp_dict = json.loads(resp_json)
        sell_price = resp_dict['tick']['data'][0]['price']
        return '%f' % sell_price
    else:
        raise Exception


def cal_num(coin1, coin2='eth'):
    coin1_price = float(get_price(coin1 + coin2))
    print('{}的价格为{}'.format(coin1, coin1_price))
    coin2_balance = float(get_tote(coin2))
    print('{}我拥有的总量为{}'.format(coin1, coin2_balance))
    max_number = coin2_balance/coin1_price
    return '%.4f' % max_number


def all_in(coin1, coin2):
    amount = float(cal_num(coin1, coin2)) - 20
    resp_dict = send_order(amount=str(amount), source='', symbol=coin1 + coin2, _type='buy-market')
    print('火币接口返回字典为：')
    print(resp_dict)
    return resp_dict


def task():
    while all_in(COIN1, COIN2)['status'] != 'ok':
        print('正在用 {} 努力购买 {} ...'.format(COIN2, COIN1))


if __name__ == '__main__':
    task()


"""
huobi.pro all in 
telegram @soda36

计算账户里的USDT能买多少个ETH
print(cal_num('eth', 'usdt'))

用账户里全部未冻结的USDT购买BTC
print(all_in('btc', 'usdt'))
"""
