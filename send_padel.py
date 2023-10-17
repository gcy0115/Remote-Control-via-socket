import pygame

# 局域网内的windows客户端
from socket import *        #导入socket里的所有东西
serverName = '10.16.108.118'    #换成局域网内服务器端IP即可实现局域网内通信
serverPort = 12001            #服务器端口，除了已知的被占用端口都可，一般建议10000-65535
clientSocket = socket(AF_INET,SOCK_DGRAM)    #UDP连接
#ipv4 udp

pygame.init()
pygame.joystick.init()
clock = pygame.time.Clock()
# 初始化
#  ['03007cb9efbe00006d04000000000000', '03003a84522600000257000000000000', '030093e2163400000103000000000000', '030069da163400002110000000000000', '030046e26f25000052c6000000000000']
#  ['3Dconnexion KMJ Emulator', '\x16\x16HE PRO GRS3', 'CAMMUS C5 Base', 'CAMMUS C5 Steering Wheel', '3Dconnexion Universal Receiver']
wheel_name = 'CAMMUS C5 Base'
pedal_name = '\x16\x16HE PRO GRS3'

def get_target(device_name):
    # 获取符合要求的手柄对象
    joynumber = pygame.joystick.get_count()
    print('%d joysticks detected.' %(joynumber))
    
    for i in range(joynumber):
        joy = pygame.joystick.Joystick(i) # 第i个手柄对象
        joy.init() # 初始化
        
        try:
            joy_guid = joy.get_name()
        except AttributeError:
            # get_guid() 是一个 SDL2 方法
            pass
        if joy_guid == device_name:
            print("Select joystick:", joy.get_name())
            targetjoy = joy
        else:
            pass
    return targetjoy

def get_data(joy_wheel, joy_pedal):
    # 获取方向盘和踏板的数据
    pygame.event.get() # 更新手柄数据
    # data = [0, 0, 0]
    wheel = joy_wheel.get_axis(0)
    throttle = joy_pedal.get_axis(2)
    throttle = (throttle + 1) / 1.2
    if throttle > 1:
        throttle = 1
    elif throttle < 0.04:
        throttle = 0
    else:
        throttle = throttle
    brake = joy_pedal.get_axis(0)
    brake = (- brake + 1) / 2
    if brake > 0.97:
        brake = 1
    elif brake < 0.03:
        brake = 0
    else:
        brake = brake
    joy_data = [wheel, throttle, brake]
    # clock.tick(500)
    # print('steering: %.4f, throttle: %.4f, brake: %.4f' % (wheel, throttle, brake))
    return joy_data

def sendMesssage(message:list):
    data = str(round(message[0], 5)), str(round(message[1], 5)), str(round(message[2], 5))
    data = ' '.join(data)
    # print(data, type(data))
    clientSocket.sendto(data.encode(),(serverName,serverPort))    #向服务器发送消息，使用socket时，只能以字节形式传送，故需要encode()
    reply,serverAddress = clientSocket.recvfrom(2048)                #接收服务器返回的消息和地址
    print (reply)
    # clientSocket.close()        #关闭连接   

joy_wheel = get_target(wheel_name)
joy_pedal = get_target(pedal_name)
wheel = 0.0
throttle = 0.0
breaks = 0.0

pygame.joystick.init()
joy_wheel.init() # 初始化
joy_pedal.init() # 初始化

while True:
    joy_data = get_data(joy_wheel, joy_pedal)
    sendMesssage(joy_data)
    # clock.tick(1)

clientSocket.close()