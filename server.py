
from tkinter import *
import tkinter.font as tkFont
import socket
import threading
import time, sys
import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.nlp.v20190408 import nlp_client, models

root = Tk()
root.title('我是一个服务器哦')
val = IntVar()
frame = [Frame(), Frame(), Frame(), Frame(), Frame()]
local = '127.0.0.1'
port = 5505
global serverSock
global connection
flag = False
cientMsg = ""
s = ""


# 关闭事件
def close():
    sys.exit()


# 转换事件
def switch():
    if val.get() == 1:
        frame[2].pack(expand=1, fill=BOTH)
        frame[4].pack(expand=1, fill=BOTH, side=RIGHT)
    else:
        frame[2].pack_forget()
        frame[4].pack_forget()


# GUI
def setgui():
    global Textbox, inputText
    ft = tkFont.Font(family='Fixes', size=11)
    chatTextS = Scrollbar(frame[0])
    chatTextS.pack(side=RIGHT, fill=Y)
    Textbox = Listbox(frame[0], yscrollcommand=chatTextS.set, width=60, height=18, font=ft)
    Textbox.pack(expand=1, fill=BOTH)
    frame[0].pack(expand=1, fill=BOTH)
    Radiobutton(frame[1], text='我自己来', value=1, variable=val).pack(side=BOTTOM)
    Radiobutton(frame[1], text='机器人来吧', value=0, variable=val).pack(side=BOTTOM)
    frame[1].pack(expand=1, fill=BOTH)
    inputTextS = Scrollbar(frame[2])
    inputTextS.pack(side=RIGHT, fill=Y)
    ft = tkFont.Font(family='Fixes', size=11)
    inputText = Text(frame[2], yscrollcommand=inputTextS.set, width=70, height=8, font=ft)
    inputText.pack(expand=1, fill=BOTH)
    sendButton = Button(frame[4], text=' 发 送 ', width=10, command=sendMessage)
    sendButton.pack(expand=1, side=BOTTOM and RIGHT, padx=25, pady=5)
    closeButton = Button(frame[3], text='关 闭 ', width=10, command=close)
    closeButton.pack(expand=1, side=RIGHT, padx=25, pady=5)
    switchButton = Button(frame[3], text=' 转 换 ', width=10, command=switch)
    switchButton.pack(expand=1, side=RIGHT, padx=25, pady=5)
    frame[3].pack(expand=1, fill=BOTH)


# 接收消息
def receiveMessage():
    global cientMsg
    # 建立Socket连接
    serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSock.bind((local, port))
    serverSock.listen(15)
    buffer = 1024
    Textbox.insert(END, '服务器已经就绪......')
    global connection
    global flag
    # 循环接受客户端的连接请求
    while True:
        connection, address = serverSock.accept()
        flag = True
        while True:
            # 接收客户端发送的消息
            cientMsg = connection.recv(buffer).decode('utf-8')
            if not cientMsg:
                continue
            elif cientMsg == 'Y':
                Textbox.insert(END, '服务器端已经与客户端建立连接......')
                connection.send(b'Y')
            elif cientMsg == 'N':
                Textbox.insert(END, '服务器端与客户端建立连接失败......')
                connection.send(b'N')
            else:
                theTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                Textbox.insert(END, '客户端 ' + theTime + ' 说：\n')
                Textbox.insert(END, '  ' + cientMsg)
                if val.get() == 0:
                    robot()


def sendMessage():
    global cientMsg
    theTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    Textbox.insert(END, '服务器 ' + theTime + ' 说：\n')
    message = inputText.get('1.0', END)
    Textbox.insert(END, '  ' + message + '\n')
    inputText.delete(0.0, message.__len__() - 1.0)
    if flag == True:
        # 将消息发送到客户端
        connection.send(message.encode())
    else:
        Textbox.insert(END, '您还未与客户端建立连接，客户端无法收到您的消息\n')


def startNewThread():
    # 启动一个新线程来接收客户端的消息
    thread = threading.Thread(target=receiveMessage, args=())
    thread.setDaemon(True)
    thread.start()


def robot():
    ifsend = True
    cred = credential.Credential("your_id", "your_key")
    httpProfile = HttpProfile()
    httpProfile.endpoint = "nlp.tencentcloudapi.com"
    clientProfile = ClientProfile()
    clientProfile.httpProfile = httpProfile
    client = nlp_client.NlpClient(cred, "ap-guangzhou", clientProfile)
    req = models.ChatBotRequest()
    print(cientMsg)
    params = {
        "Query": cientMsg
    }
    req.from_json_string(json.dumps(params))
    resp = client.ChatBot(req)
    s = resp.to_json_string().split("\"")[3]
    print(s)
    theTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    Textbox.insert(END, '服务器 ' + theTime + ' 说：\n')
    Textbox.insert(END, '  ' + s + '\n')
    if flag == True:
        # 将消息发送到客户端
        connection.send(s.encode())
    else:
        Textbox.insert(END, '您还未与客户端建立连接，客户端无法收到您的消息\n')


if __name__ == '__main__':
    setgui()
    startNewThread()
    mainloop()
