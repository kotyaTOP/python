from flask import Flask, render_template, request

from config import Config
from decodetools.main_decoder import Decoder

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/', methods=['POST', 'GET'])
@app.route('/index', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        result = request.form
        decode_result = Decoder.decode(result['textForDecode'])
        if decode_result.original_encoding == 'unknown':
            return render_template('index.html', o_data=decode_result.o_data,
                                   org_enc=decode_result.original_encoding)
        else:
            return render_template('index.html', o_data=decode_result.o_data, data=decode_result.data,
                                   org_enc=decode_result.original_encoding)
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
