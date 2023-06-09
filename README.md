<p align="center">
  <img src="https://raw.githubusercontent.com/Silence1017/EtherWatchdog_Dapp/main/images/card.png" align="middle"  width="500" />
</p>

------------------------------------------------------------------------------------------

<p align="center">
  <b>让🐶来帮助你解决最棘手的安全问题</b>😄😏😆
</p>

EtherWatchdog是一款通过**交易**的操作码序列**实时**检测智能合约漏洞的安全平台，我们全面的智能合约漏洞检测服务可以帮助从初创公司到企业的每个人维护他们的以太坊区块链应用程序。EtherWatchdog的**未来**绝不仅仅是一个普通的智能合约漏洞检测平台，它有能力成为像**Etherscan**一样优秀的**区块链搜索**、**API**和**分析平台**。

## 💡实现
客户端发出请求，Java服务端收到请求立刻进行socket通信向Python深度学习模型发出检测操作码序列的请求，Python监听到请求后调用模型将结果返回给Java服务端，Java服务端返回响应结果给客户端。
关于数据集，交易操作码序列通过EVM插桩技术获取存储到mongodb数据库，充当以太坊全节点。

## 🌎后端环境需求
1. Java
2. Python
3. [Bitquery](https://explorer.bitquery.io/)

## 📃Python Requirements

- Python 3.6
- Tensorflow 1.15.0
- Tensorboard 1.15.0
- Sklearn 0.19.1
- Numpy 1.16.2
- Gensim 3.8.3
- Tqdm 4.49.0

## 💻Python Project

The CNN-BiLSTM modle structure is below:

![](https://farm2.staticflickr.com/1915/43842346360_e4660c5921_o.png)

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
## 💻Java Project

SpringBoot+SpringMVC+MyBatisPlus+Maven+Mongodb

## 💿Bitquery

利用Bitquery中的API来获取交易中涉及到的所有合约地址

## 🔎展望

畅想一下未来，EtherWatchdog的未来绝不仅仅是一个普通的智能合约漏洞检测平台，它有能力成为像**Etherscan**一样优秀的**区块链搜索**、**API**和**分析平台**。未来🐶想做到：
```text
1、实时检测交易并像Etherscan一样展示最新区块中的含漏洞交易，并提供免费的API供开发者使用。
2、制作一个包含以太坊所有交易的漏洞数据集并提供相关API供开发者使用，有效地避免社区成员调用含有漏洞的合约。
3、🐶有能力做到像Etherscan一样获取以太坊相关信息，包括合约、交易、区块、账户等信息并提供相关API，因为🐶对EVM进行了修改。
```

![img](https://raw.githubusercontent.com/Silence1017/EtherWatchdog_Dapp/main/images/3.png)

## 🔔Citation

如果EtherWatchdog对您的研究有帮助，欢迎引用

```
@inproceedings{gu2023detecting,
  title={Detecting Unknown Vulnerabilities in Smart Contracts with Multi-Label Classification Model Using CNN-BiLSTM},
  author={Gu, Wanyi and Wang, Guojun and Li, Peiqiang and Li, Xubin and Zhai, Guangxin and Li, Xiangbin and Chen, Mingfei},
  booktitle={Ubiquitous Security: Second International Conference, UbiSec 2022, Zhangjiajie, China, December 28--31, 2022, Revised Selected Papers},
  pages={52--63},
  year={2023},
  organization={Springer}
}
```

## 👦👧About Us

**Lingnan Ethereum Darkness Agent**

✉️: cswygu@qq.com

✉️: 1257311626@qq.com

✉️: ouzhsh@126.com

✉️: 835837078@qq.com

✉️: 963544587@qq.com

最最感谢我们的博士师兄李培强以及**老王**❤️

## License

EtherWatchdog遵循[Apache-2.0开源协议](./LICENSE)。
