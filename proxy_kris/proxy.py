# ********* CONSTANT VARIABLES *********
import socket
import sys

import _thread

BACKLOG = 50  # how many pending connections queue will hold
MAX_DATA_RECV = 999999  # max number of bytes we receive at once
DEBUG = True  # set to True to see the debug msgs
BLOCKED = []  # just an example. Remove with [""] for no blocking at all.


class Proxy:

    def __init__(self, port: int = 5000) -> None:
        super().__init__()
        self.port = port
        self.host = 'localhost'  # localhost
        print("Прокси сервер выполняется по адресу: ", self.host, ":", port)

    def start(self):
        try:
            # создание сокета
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # связь сокетом хоста и порта
            s.bind((self.host, self.port))

            # слушание
            s.listen(BACKLOG)

        except RuntimeError as e:
            if s: s.close()
            print("Не удалось открыть соккет:", str(e))
            sys.exit(1)

        # получает соединение от клиента
        while True:
            conn, client_addr = s.accept()

            # создаёт поток обработки запроса
            _thread.start_new_thread(self.proxy_thread, (conn, client_addr))

        # s.close()

    def proxy_thread(self, conn, client_addr):
        # получает запрос из браузера
        request = conn.recv(MAX_DATA_RECV)

        reqStr = str(request)
        lines = reqStr.split(sep='\\n')
        # разбор первой строки
        first_line = str(request).split('\n')[0]

        # получение url
        url = first_line.split(' ')[1][1:]

        for i in range(0, len(BLOCKED)):
            if BLOCKED[i] in url:
                conn.close()
                sys.exit(1)

        # поиск веб-сервера и порта
        http_pos = url.find("://")  # поиск позиции ://
        if http_pos == -1:
            temp = url
        else:
            temp = url[(http_pos + 3):]  # поиск остальной части url

        port_pos = temp.find(":")  # поиск позиции порта (если есть)

        # поиск конца веб-сервера
        webserver_pos = temp.find("/")
        if webserver_pos == -1:
            webserver_pos = len(temp)

        if port_pos == -1 or webserver_pos < port_pos:  # стандартный порт
            port = 80
            webserver = temp[:webserver_pos]
        else:  # определенный порт
            port = int((temp[(port_pos + 1):])[:webserver_pos - port_pos - 1])
            webserver = temp[:port_pos]

        try:
            # создание соккета чтобы соединиться с веб-сервером
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((webserver, port))
            s.send(bytes(request))  # отправка запроса на веб-сервер

            while 1:
                # получение данных с веб-сервера
                data = s.recv(MAX_DATA_RECV)
                # тут мы получаем данные
                if len(data) > 0:
                    # отправка в браузер
                    conn.send(data)
                    # break  # может и не нужен fixme
                else:
                    break
            s.close()
            conn.close()
        except RuntimeError as e:
            if s:
                s.close()
            if conn:
                conn.close()
            sys.exit(1)


if __name__ == '__main__':
    p = Proxy(port=7654)
    p.start()
