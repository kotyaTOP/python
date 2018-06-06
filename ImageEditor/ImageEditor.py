import os

from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from PIL import Image, ImageEnhance

UPLOAD_FOLD = os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static'))
UPLOAD_FOLDER = os.path.join(UPLOAD_FOLD, 'tmp_images')
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
filename = None
file_path = None


def image(img=None):
    global filename, file_path
    if img is not None:
        im = img
        parts = filename.split('.')
        filename = parts[len(parts) - 2] + '.png'
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
        img.save(file_path, 'PNG')
    else:
        im = Image.open(file_path)

    return render_template('index.html', fname=filename, image_width=im.size[0], image_height=im.size[1])


@app.route('/')
@app.route('/index')
@app.route('/transform')
def standard():
    return render_template('index.html')


def allowed_file(filename):
    return True


@app.route('/transform', methods=['POST', 'GET'])
def image_load():
    global filename, file_path
    if len(request.args) > 0:
        if request.args['type'] == 'contrast':
            return transform_contrast()
        elif request.args['type'] == 'brightness':
            return transform_brightness()
        else:
            return transform_sharpness()
    if request.method == 'POST':
        file = request.files['f']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            return image()
        else:
            return "file not allowed"
    return standard


def transform_contrast():
    img = Image.open(file_path)
    contrast = ImageEnhance.Contrast(img)
    img = contrast.enhance(2)

    return image(img=img)


def transform_brightness():
    img = Image.open(file_path)
    brightness = ImageEnhance.Brightness(img)
    img = brightness.enhance(1.5)

    return image(img=img)


def transform_sharpness():
    img = Image.open(file_path)
    sharpness = ImageEnhance.Sharpness(img)
    img = sharpness.enhance(2)

    return image(img=img)


if __name__ == '__main__':
    app.run()
