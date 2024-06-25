import socketserver

class MyHandler(socketserver.BaseRequestHandler):
    # 접속 학생 관리
    users = {}

    def sendToAll(self, msg):
        for sock, addr in self.users.values():
            sock.send(msg.encode())
    
    def deleteUser(self, username):
        if username not in self.users:
            return
        del self.users[username]
        self.sendToAll("[{}] 님이 퇴장하셨습니다.".format(username))
        print("현재 참여 중 {} 명".format(len(self.users)))


    def addUser(self, username, c_sock, addr):
        # 이미 접속 중인 학생인 경우
        if username in self.users:
            c_sock.send("이미 등록된 학번 입니다.\n".encode())
            return None
        # 새로운 학생인 경우
        else:
            self.users[username] = (c_sock, addr)
            self.sendToAll("[{}]님이 접속했습니다.".format(username))
            print("현재 접속 인원 {}명".format(len(self.users)))
            return username

    def handle(self):
        print("[{}] 접속 연결됨".format(self.client_address[0]))

        while True:
            self.request.send("학번을 입력하세요.".encode())
            username = self.request.recv(1024).decode()
            if self.addUser(username, self.request, self.client_address):
                break
        
        while True:
            msg = self.request.recv(1024)
            print(msg)
            if msg.decode() == "/exit":
                self.request.close()
                break
            number = int(msg.decode())
            result_number = number * number
            self.sendToAll("[{}] {} X {} = {}".format(username, number, number, result_number))
        
        self.deleteUser(username)
        print("[{}] 접속종료".format(self.client_address[0]))


class ChatServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

chat = ChatServer(("", 9826), MyHandler)
chat.serve_forever()
chat.shutdown()
chat.server_close()