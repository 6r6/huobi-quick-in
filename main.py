#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import json
import requests
from plugins.huobi.HuobiServices import get_balance, send_order, cancel_order, order_matchresults


# 等待买入的币种(小写)
COIN1 = 'ela'
# 你想买进的COIN1的数量
COIN1_AMOUNT = 10
# 当COIN1的价格小于这个价位，程序允许买入，单位为COIN2
COIN1_PRICE = 0.00153
# 用来支付的币种，在USDT/BTC/ETH中间选择
COIN2 = 'btc'


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
    addr = 'https://api.huobi.pro/market/depth?symbol={symbol}&type=step0'
    resp_json = requests.get(addr.format(symbol=symbol)).text
    if '[]' not in resp_json:
        resp_dict = json.loads(resp_json)
        sell_price = resp_dict['tick']['asks'][0][0]
        return '%f' % sell_price
    else:
        return '0'


def buy_limit(coin1, coin2, coin1_max_price, coin1_amount):
    coin1_price = get_price(coin1 + coin2)
    if 0 < float(coin1_price) < coin1_max_price:
        resp_dict = send_order(amount=str(coin1_amount),
                               source='',
                               symbol=coin1 + coin2,
                               _type='buy-limit',
                               price=coin1_price)
        return resp_dict
    else:
        return {'status': 'err'}


def task():
    print('任务说明>> 我想用 {} 来买 {} '.format(COIN2, COIN1))
    print('钱包状况>> 我有 {} 个 {} '.format(get_tote(COIN2), COIN2))
    while True:
        resp_dict = buy_limit(COIN1, COIN2, COIN1_PRICE, COIN1_AMOUNT)
        if 'data' in resp_dict:
            order_id = resp_dict['data']
            print('当前进度>> 已下买单,订单ID为 {}'.format(order_id))
            if order_matchresults(order_id)['status'] != 'ok':
                print('订单追踪>> 未买到，取消订单...')
                cancel_order(order_id)
            else:
                print('订单追踪>> 已经买入，任务完成')
                break
        else:
            print('当前进度>> 暂未上币...')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        task()
