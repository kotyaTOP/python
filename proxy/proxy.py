import socket

from flask import Flask, render_template, request

app = Flask(__name__)

MAX_DATA_RECV = 999999


@app.route('/', methods=['POST', 'GET'])
@app.route('/index', methods=['POST', 'GET'])
def proxy():
    if request.method == 'POST':
        result = request.form
        proxy_adrs = result['proxy']
        url = result['url']
        try:
            # создание соккета чтобы соединиться с веб-сервером
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            proxy_adr_url = proxy_adrs.split(sep=':')[0]
            proxy_adr_port = proxy_adrs.split(sep=':')[1]
            s.connect((proxy_adr_url, int(proxy_adr_port)))
            request2 = bytes(
                'GET ' + '' + url + ' \r\naccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8 \r\nAccept-Encoding: gzip, deflate, br \r\nAccept-Language: ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7 \r\nCache-Control: no-cache \r\nConnection: keep-alive \r\nContent-Type: application/x-www-form-urlencoded \r\nPragma: no-cache \r\nUpgrade-Insecure-Requests: 1 \r\nUser-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
                encoding='utf-8')
            s.send(bytes(request2))  # отправка запроса на веб-сервер

            while 1:
                # получение данных с веб-сервера
                data = s.recv(MAX_DATA_RECV)
                # тут мы получаем данные
                if len(data) > 0:
                    # отправка в браузер
                    return data
                else:
                    break
            s.close()
        except:
            pass

    return render_template('base.html')


app.run()
