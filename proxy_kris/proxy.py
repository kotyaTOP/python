# ********* CONSTANT VARIABLES *********
import socket
import sys
import requests as rq

import _thread

BACKLOG = 5000  # how many pending connections queue will hold
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

            # listening
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
        if DEBUG:
            print('Соединились')
        # получает запрос из браузера
        request = conn.recv(MAX_DATA_RECV)
        if len(request) < 3:
            return
        if DEBUG:
            print('полученный из браузера запрос: ' + str(request))

        # разбор первой строки
        first_line = str(request).split('\n')[0]

        # получение url
        url = first_line[2:-1]  # вырезаем url
        print('URL[1] = ' + url)
        if first_line.startswith('b\'GET'):  # альтернативный вариант
            url = first_line.split(' ')[1]
            print('URL[2] = ' + url)
            if url.startswith('/?site='):  # ещё один
                url = url[len('/?site='):]
                print('URL[3] = ' + url)
        # if url.startswith('/'):  # иногда начинается на / вместе http://
        #     url = 'http:/' + url
        if DEBUG:
            print('Сформирован url: ' + url)

        # вариант красивого, но неработающего запроса
        request = '''GET ''' + url + ''' HTTP/1.1
User-Agent: Mozilla/5.0 (Windows NT 6.1; rv:18.0) Gecko/20100101 Firefox/18.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Cookie: wp-settings
Connection: keep-alive'''

        # вариант плохого (bad request 404) ,но работающего запроса
        request2 = bytes(
            'GET ' + '' + url + ' \r\naccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8 \r\nAccept-Encoding: gzip, deflate, br \r\nAccept-Language: ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7 \r\nCache-Control: no-cache \r\nConnection: keep-alive \r\nContent-Type: application/x-www-form-urlencoded \r\nPragma: no-cache \r\nUpgrade-Insecure-Requests: 1 \r\nUser-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
            encoding='utf-8')


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
            data = rq.get(url)
            data_text = data.text
            if DEBUG:
                print('Данные получили, ожидаем обработку...')
            data_text = self.substitute_link(data_text, webserver='http://' + webserver + '/')
            content_type = 'text/html'
            if DEBUG:
                print('Данные обработаны, возвращаем...')
            data = '''HTTP/1.1 200 OK
            Date: Mon, 27 Jul 2009 12:28:53 GMT
            Server: Apache/2.2.14 (Win32)
            Last-Modified: Wed, 22 Jul 2009 19:15:56 GMT
            Content-Length: ''' + str(len(data_text)) + '''
            Content-Type: ''' + content_type + '''
            Connection: Closed\n\n''' + data_text

            data_send = data if url.endswith(('css', 'js')) else data_text
            conn.send(bytes(str(data), encoding='utf-8'))
            # conn.send(data.raw)
            conn.close()
        # except rq.exceptions.MissingSchema:
        #     pass
        except RuntimeError as e:
            if conn:
                conn.close()
            sys.exit(1)

    def substitute_link(self, html_data, webserver=''):
        '''
        Редактирование результата от сервера.
        :param html_data: результат
        :param webserver: веб-сервер (нужен для редактирования относительных ссылок)
        :return: измененные данные
        '''
        if DEBUG:
            print('webserver:' + webserver)
        # .replace('\\\\t', '').replace('\\\\n', '').replace('\\\\r', '').replace('\\t',
        #                                                                                                '').replace(
        #    '\\n', '').replace('\\r', '').replace('\t', '').replace('\n', '').replace('\r', '')
        s = str(html_data)
        a = s.find('<base href')
        b = s[a:].find('/>') + 2
        base_1 = s[a: a + b]
        # servername = base_1[base_1.find('"') + 1:base_1.find('"') + 1 + base_1[base_1.find('"') + 1:].find('"')]
        s = s.replace(base_1, '').replace('src="/', 'src="' + webserver).replace('href="/',
                                                                                 'href="' + webserver) \
            .replace('href="http', 'href="http://127.0.0.1:7654?site=http').replace('url(/', 'url(' + webserver)
        # .replace('src="http', 'src="http://127.0.0.1:7654?site=http')
        if DEBUG:
            print('Строка результата после обработки: ' + s)
        return s


if __name__ == '__main__':
    p = Proxy(port=7654)
    p.start()
