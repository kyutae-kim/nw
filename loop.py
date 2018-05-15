# -*- coding: utf-8 -*-
import time
import threading
import multiprocessing

def yes(no):
    while True:
        print "yes - %d" % no
        time.sleep(0.5)
    
def no(no):
    while True:
        print "yes - %d" % no
        time.sleep(0.5)

#쓰레드 생성(메모리에 정보가 올라감, 실행은 아님)
#t1 = threading.Thread(target=yes, args=(1,))
#t2 = threading.Thread(target=yes, args=(2,))

#쓰레드 실행
#t1.start()
#t2.start()

if __name__== '__main__':
    p1 = multiprocessing.Process(target = yes, args=(1,))
    p2 = multiprocessing.Process(target = yes, args=(2,))
    p1.start()
    p2.start()

