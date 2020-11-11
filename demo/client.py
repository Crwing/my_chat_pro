import socket
import threading


def receive_message(client_socket):
    while True:
        recv_messsage = client_socket.recv(1024)
        if recv_messsage:
            print('Message Recieved: ')
            print(recv_messsage.decode('UTF-8'))


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 9001))
userName = input('Please input your user name:')
targetUserName = input("Please input your friend's name:")
messDict = {'userName': userName, 'targetUserName': targetUserName, 'content': ''}

thread = threading.Thread(target=receive_message, args=(client_socket,))
thread.start()
while True:
    message = ''
    message = input('Please input message: ')
    message = targetUserName + '/' + userName + '/' + message
    client_socket.send(message.encode('UTF-8'))
