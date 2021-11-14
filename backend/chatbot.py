# start

from flask import Flask, request, Response
from fu_lib import *
from gan import *


app = Flask(__name__)


@app.route('/faceai', methods=['POST'])
def faceai():
    """
    For dealing with the POST request.
    :return:
    """

    data = request.files
    image1 = data.get('my_animal').read()
    with open('my_animal.jpg', "wb") as f:
        f.write(image1)
    image2 = data.get('target').read()
    with open('target.jpg', "wb") as f:
        f.write(image2)

    reply()
    with open("target.jpg", "rb") as f:
        return_data = f.read()

    return Response(return_data,  content_type="image/jpeg")


@app.route('/faceaigan1', methods=['POST'])
def faceaigan1():
    """
    For dealing with the POST request.
    :return:
    """

    data = request.files
    image1 = data.get('my_animal').read()
    with open('a.jpg', "wb") as f:
        f.write(image1)
    image2 = data.get('target').read()
    with open('b.jpg', "wb") as f:
        f.write(image2)

    ganVersion()
    with open("ab.jpg", "rb") as f:
        return_data = f.read()

    return Response(return_data,  content_type="image/jpeg")


@app.route('/faceaigan2', methods=['POST'])
def faceaigan2():
    """
    For dealing with the POST request.
    :return:
    """

    # data = request.files
    # image1 = data.get('my_animal').read()
    # with open('my_animal.jpg', "wb") as f:
    #     f.write(image1)
    # image2 = data.get('target').read()
    # with open('target.jpg', "wb") as f:
    #     f.write(image2)

    # reply()
    with open("ba.jpg", "rb") as f:
        return_data = f.read()

    return Response(return_data,  content_type="image/jpeg")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
