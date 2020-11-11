import socket
import threading
import queue
import time
import sys


def split_message(message):
    splited_messages = message.split('/')
    targetContact = splited_messages[0]
    sourceContact = splited_messages[1]
    messageContent = splited_messages[2]
    return targetContact, sourceContact, messageContent


def add_message2queue(targetContact, sourceContact, meesageContent, contactDict):
    message = targetContact + '/' + sourceContact + '/' + meesageContent
    try:
        q = contactDict[targetContact]
    except KeyError as e:
        q = queue.Queue()
        print(message)
        q.put(message)
        contactDict[targetContact] = q
    else:
        q.put(message)


def find_address_by_user(target_user, user_address_dict):
    return user_address_dict[target_user]


def log_user_address(souceContact, addr, user_address_dict):
    try:
        address = user_address_dict[souceContact]
    except KeyError as e:
        user_address_dict[souceContact] = addr


def send_queue_message(sock, contactsDict, user_address_dict, my_addr):
    while True:
        time.sleep(1)
        if not contactsDict:
            print('currently no message in queue')
        send_contactsDict = dict(contactsDict)
        for target_user, message_queue in send_contactsDict.items():
            try:
                addr = find_address_by_user(target_user, user_address_dict)
            except KeyError as e:
                continue
            if my_addr != addr:
                continue
            while not message_queue.empty():
                mix_message = message_queue.get().split('/')
                sourceContact = mix_message[0]
                messageContent = mix_message[2]
                message = 'You friend ' + sourceContact + ' send a message to you:' + messageContent + '\n'
                sock.sendto(message.encode('UTF-8'), addr)
            if message_queue.empty():
                try:
                    contactsDict.pop(target_user)
                except KeyError as e:
                    continue


def receive_message(sock, addr, contactsDict, user_address_dict):
    print(addr)
    sock.setblocking(0)
    thread = threading.Thread(target=send_queue_message, args=(sock, contactsDict, user_address_dict, addr))
    thread.start()
    while True:
        try:
            message = sock.recv(1024)
        except BlockingIOError as e:
            time.sleep(2)
            message = None
            continue
        if message:
            messageDecoded = message.decode('UTF-8')
            if messageDecoded:
                targetContact, sourceContact, messageContent = split_message(messageDecoded)
                add_message2queue(targetContact, sourceContact, messageContent, contactsDict)
                log_user_address(sourceContact, addr, user_address_dict)
                print(messageDecoded)
            # return_message = get_recvd_message(sourceContact, contactsDict)
            # sock.sendto(return_message.encode('UTF-8'), addr)
        else:
            print('Click')
            sys.exit()
            break


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('45.32.130.93', 9001))
server_socket.listen(5)
threads = []
user_address_dict = {}
contactsDict = {}

print('Waiting for connection...')

for i in range(10):
    sock, addr = server_socket.accept()
    print(sock, addr)
    thread = threading.Thread(target=receive_message, args=(sock, addr, contactsDict, user_address_dict))
    thread.start()
    threads.append(thread)

print('all thread are started')

for j in threads:
    j.join()
