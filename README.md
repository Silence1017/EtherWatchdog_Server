# EtherWatchdog
## 让我们来帮助你解决最棘手的安全问题
简介：EtherWatchdog是一款通过交易的操作码序列实时检测智能合约漏洞的安全平台，我们全面的智能合约漏洞检测服务可以帮助从初创公司到企业的每个人维护他们的以太坊区块链应用程序。

## 后端环境需求
1. Java
2. Python

## 具体实现方法
客户端发出请求，Java客户端收到请求立刻进行socket通信向Python深度学习模型发出请求检测操作码序列，Python监听到请求后进行检测将结果返回给Java，Java服务器返回响应结果给客户端。
关于数据集，交易操作码序列通过EVM插桩技术获取存储到mongodb数据库，充当以太坊全节点。

## Python Requirements

- Python 3.6
- Tensorflow 1.15.0
- Tensorboard 1.15.0
- Sklearn 0.19.1
- Numpy 1.16.2
- Gensim 3.8.3
- Tqdm 4.49.0

## Python Project

The CNN-BiLSTM modle structure is below:

```text
.
├── Model
│   ├── test_model.py
│   ├── text_model.py
│   ├── eth.py 
│   └── train_model.py
├── data
│   ├── Onehot
│   ├── Test_sample.json
│   ├── Train_sample.json
│   └── Validation_sample.json
└── utils
│   ├── checkmate.py
│   ├── data_helpers.py
│   └── param_parser.py
├── LICENSE
├── README.md
└── requirements.txt
```
## Java Project

SpringBoot+MyBatis Plus+Mongodb

## About Us

Lingnan Ethereum Darkness Agent


Email: cswygu@qq.com

