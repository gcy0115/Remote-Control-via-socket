# 如果是局域网内的linux作为服务器端执行该代码，注意先关闭防火墙
from socket import *
serverPort = 12001
serverSocket = socket(AF_INET,SOCK_DGRAM)
serverSocket.bind(('',serverPort))    #注意bind方法括号内为一个元组，引号默认表示为127.0.0.1，即监听本地端口
print('ready')

def str2float(str):
    data = str.split()
    for i in range(len(data)):
        data[i] = float(data[i])
    return data


while True:
    message,clientAddress = serverSocket.recvfrom(2048)        #接收客户端发来的消息
    message = str2float(message)
    print(message, type(message[0]))
    serverSocket.sendto('have received'.encode(),clientAddress)        #使用socket时，只能以字节形式传送，故需要encode()