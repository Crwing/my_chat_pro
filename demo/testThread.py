import threading

import threading
import time


def show(arg):
    time.sleep(1)
    print("thread " + str(arg) + " running......")


for i in range(10):
    t = threading.Thread(target=show, args=(i,))  # 注意传入的参数一定是一个元组!
    print('This is the main program', i)
    t.start()

for i in range(10):
    time.sleep(1)

print('end')
