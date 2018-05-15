# -*- coding: utf-8 -*-
# 소켓 라이브러리 로딩

import socket
#접속 서버 정보
info = ("0.0.0.0",9999)

#TCP 소켓 생성
s = socket.socket()
#서버 접속
s.connect(info)
#데이터 전송
s.send("hello server")
#데이터 수집 및 출력
print s.recv(1024)
# 접속 종료
s.close()
