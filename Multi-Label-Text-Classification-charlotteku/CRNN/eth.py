# -*- coding:utf-8 -*-
import socket
import sys
import threading
import json
import numpy as np
import test_tx
from utils import param_parser as parser

import json

# nn=network.getNetWork()
# cnn = conv.main(False)
# 深度学习训练的神经网络,使用TensorFlow训练的神经网络模型，保存在文件中


def main():
    # 创建服务器套接字
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 获取本地主机名称
    host = socket.gethostname()
    # 设置一个端口
    port = 12345
    # 将套接字与本地主机和端口绑定
    serversocket.bind((host, port))
    # 设置监听最大连接数
    serversocket.listen(5)
    # 获取本地服务器的连接信息
    myaddr = serversocket.getsockname()
    print("服务器地址:%s" % str(myaddr))
    # 循环等待接受客户端信息
    while True:
        # 获取一个客户端连接
        clientsocket, addr = serversocket.accept()
        print("连接地址:%s" % str(addr))
        try:
            t = ServerThreading(clientsocket)  # 为每一个请求开启一个处理线程
            t.start()
            pass
        except Exception as identifier:
            print(identifier)
            pass
        pass
    serversocket.close()
    pass


class ServerThreading(threading.Thread):
    # words = text2vec.load_lexicon()
    def __init__(self, clientsocket, recvsize=1024 * 1024, encoding="utf-8"):
        threading.Thread.__init__(self)
        self._socket = clientsocket
        self._recvsize = recvsize
        self._encoding = encoding
        pass

    def run(self):
        print("开启线程.....")
        try:
            # 接受数据
            msg = ''
            while True:
                # 读取recvsize个字节
                rec = self._socket.recv(self._recvsize)
                # 解码
                msg += rec.decode(self._encoding)
                print(msg)
                # 文本接受是否完毕，因为python socket不能自己判断接收数据是否完毕，
                # 所以需要自定义协议标志数据接受完毕
                if msg.strip().endswith('over'):
                    msg = msg[:-4]
                    break
            # 解析json格式的数据
            print(msg)
            re = json.loads(msg)
            print(type(re['hash']))
            # 调用神经网络模型处理请求
            #res = test_tx.hand(re['content'])
            #sendmsg=test_tx.test_crnn("0x1ae5f96a8b446ddd51e96019472f7a31fcad3d2e774373ecfbb2ba94ff72fc04")
            sendmsg = test_tx.test_crnn(re['hash'])
            #sendmsg = json.dumps(res)
            # 发送数据
            print(sendmsg)

            self._socket.send(("%s" % sendmsg).encode(self._encoding))
            pass
        except Exception as identifier:
            print(identifier)
            self._socket.send("500".encode(self._encoding))

            pass
        finally:
            self._socket.close()
        print("任务结束.....")

        pass

    def __del__(self):

        pass


if __name__ == "__main__":
    main()