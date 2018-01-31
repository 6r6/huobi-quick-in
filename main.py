#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import json
import requests
from plugins.huobi.HuobiServices import get_balance, send_order


COIN1 = 'zla'.lower()
COIN2 = 'btc'.lower()
COIN1_PRICE = 6.78e-5
COIN2_AMOUNT = 0.01


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
    if 'data' in resp_json:
        resp_dict = json.loads(resp_json)
        sell_price = resp_dict['tick']['data'][0]['price']
        return '%f' % sell_price
    else:
        return '0'


def buy_market(coin1, coin2, coin1_max_price, coin2_amount):
    coin1_price = float(get_price(coin1 + coin2))
    if 0 < coin1_price < coin1_max_price:
        resp_dict = send_order(amount=str(coin2_amount), source='', symbol=coin1 + coin2, _type='buy-market')
        return resp_dict
    else:
        return {'status': 'err'}


def task():
    print('任务说明>> 我想用 {} 个 {} 来买 {} '.format(COIN2_AMOUNT, COIN2, COIN1))
    print('钱包状况>> 我有 {} 个 {} '.format(get_tote(COIN2), COIN2))
    while buy_market(COIN1, COIN2, COIN1_PRICE, COIN2_AMOUNT)['status'] != 'ok':
        print('当前进度>> 未买到 ...')
    print('成功提醒>> 已经买到，程序退出... ')
    return


if __name__ == '__main__':
    if len(sys.argv) < 2:
        task()
