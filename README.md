# 上币监测、限价买入

[![Build Status](https://travis-ci.org/6r6/huobi-quick-in.svg?branch=master)](https://travis-ci.org/6r6/huobi-quick-in)

概括：Python3脚本持续监测huobi.pro的REST-API，在新币开放交易的时候快速买入

>SDK直接复制粘贴的官方推荐写法。

### 效果预览
```
任务说明>> 我想用 btc 来买 ela
钱包状况>> 我有 0.88 个 btc
当前进度>> 暂未上币...
当前进度>> 暂未上币...
当前进度>> 已下买单
订单追踪>> 未买到，取消订单...
当前进度>> 已下买单
订单追踪>> 已经买入，任务完成
```


### 参数说明
**例子：当ELA单价小于0.00153BTC，以卖1价购买10个ELA；**
```
# 等待买入的币种(小写)
COIN1 = 'ela'
# 你想买进的COIN1的数量
COIN1_AMOUNT = 10
# 当COIN1的价格小于这个价位，程序允许买入，单位为COIN2
COIN1_PRICE = 0.00153
# 用来支付的币种，在USDT/BTC/ETH中间选择
COIN2 = 'btc'
```

### 启动前的准备
在 火币PRO-我的资产-API管理 中添加一个新的API；

解压压缩包，修改 **huobi.pro-quick-in\plugins\huobi\Utils.py** 中的 **ACCESS_KEY** 和 **SECRET_KEY**；

修改 **huobi-quick-in\main.py** 中的 **COIN1** 和 **COIN2**。COIN2（例如BTC）代表用来支付COIN1（例如RUFF）的币种。

打开命令行，切换到文件夹目录；

运行 `pip install -r requirements.txt`；

运行 `python main.py` 。

### 风险自担

十分感谢V2EX的Elephant696童鞋以身试BUG...我感到十分抱歉！给他造成了大的损失！

本次提交后，买入方法改为从深度图获取价格、限价单买入。
