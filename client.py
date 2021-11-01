from tkinter import *
import tkinter.font as tkFont
import socket
import threading
import time, sys

root = Tk()
root.title('我是一个无聊的客户端')
val = IntVar()
frame = [Frame(), Frame(), Frame(), Frame(), Frame()]
local = '127.0.0.1'
port = 5505
global clientSock
flag = False
flag2 = False


def setcon():
    global flag, flag2
    global clientSock, chatText
    if not flag2:
        try:
            # 建立Socket连接
            clientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            clientSock.connect((local, port))
            flag = True
        except:
            flag = False
            chatText.insert(END, '您还未与服务器端建立连接，请检查服务器端是否已经启动')
            return
        chatText.insert(END, '连接成功')
        startNewThread()
        flag2 = True
    else:
        chatText.insert(END, '请勿重复连接')


# 接收消息
def receiveMessage():
    global flag
    global clientSock
    buffer = 1024
    clientSock.send('Y'.encode())
    while True:
        if flag:
            # 连接建立，接收服务器端消息
            serverMsg = clientSock.recv(buffer).decode('utf-8')
            if serverMsg == 'Y':
                chatText.insert(END, '客户端已经与服务器端建立连接......')
            elif serverMsg == 'N':
                chatText.insert(END, '客户端与服务器端建立连接失败......')
            elif not serverMsg:
                continue
            else:
                theTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                chatText.insert(END, '服务器端 ' + theTime + ' 说：\n')
                chatText.insert(END, '  ' + serverMsg)
        else:
            break


# 发送消息
def sendMessage():
    # 得到用户在Text中输入的消息
    message = inputText.get('1.0', END)
    # 格式化当前的时间
    t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    chatText.insert(END, '客户端' + t + ':\n')
    chatText.insert(END, '  ' + message + '\n')
    if flag:
        # 将消息发送到服务器端
        clientSock.send(message.encode())
    else:
        chatText.insert(END, '未与服务器端建立连接\n')
    inputText.delete(0.0, message.__len__() - 1.0)


# 关闭消息窗口并退出
def close():
    sys.exit()


# 启动线程接收服务器端的消息
def startNewThread():
    # 启动一个新线程来接收服务器端的消息
    thread = threading.Thread(target=receiveMessage, args=())
    thread.setDaemon(True);
    thread.start()


def gui():
    global chatText, inputText
    # 显示消息Text右边的滚动条
    chatTextScrollBar = Scrollbar(frame[0])
    chatTextScrollBar.pack(side=RIGHT, fill=Y)

    # 显示消息Text，并绑定上面的滚动条
    ft = tkFont.Font(family='Fixes', size=11)
    chatText = Listbox(frame[0], width=70, height=18, font=ft, yscrollcommand=chatTextScrollBar.set)
    chatText.pack(expand=1, fill=BOTH)
    frame[0].pack(expand=1, fill=BOTH)
    label = Label(frame[1], height=2)
    label.pack(fill=BOTH)
    frame[1].pack(expand=1, fill=BOTH)

    # 输入消息Text的滚动条
    inputTextScrollBar = Scrollbar(frame[2])
    inputTextScrollBar.pack(side=RIGHT, fill=Y)

    # 输入消息Text，并与滚动条绑定
    ft = tkFont.Font(family='Fixes', size=11)
    inputText = Text(frame[2], width=70, height=8, font=ft, yscrollcommand=inputTextScrollBar.set)
    inputText.pack(expand=1, fill=BOTH)
    frame[2].pack(expand=1, fill=BOTH)

    # 按钮
    sendButton = Button(frame[3], text=' 发 送 ', width=10, command=sendMessage)
    sendButton.pack(expand=1, side=BOTTOM and RIGHT, padx=15, pady=8)
    reconButton = Button(frame[3], text=' 重 试 ', width=10, command=setcon)
    reconButton.pack(expand=1, side=BOTTOM and LEFT, padx=15, pady=8)
    closeButton = Button(frame[3], text=' 关 闭 ', width=10, command=close)
    closeButton.pack(expand=1, side=RIGHT, padx=15, pady=8)
    frame[3].pack(expand=1, fill=BOTH)


if __name__ == '__main__':
    gui()
    setcon()
    root.mainloop()
