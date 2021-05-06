# from gevent import monkey
# monkey.patch_all()
import time

from flask import Flask, request, render_template
from flask_cors import CORS
from flask_restful import Resource, Api, reqparse
from io import BytesIO
import os


os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import numpy as np
from PIL import Image as PIL
from tensorflow.keras.models import load_model
from tensorflow.keras.applications import imagenet_utils
from werkzeug.datastructures import FileStorage
import base64
from flask_socketio import SocketIO, emit
import tensorflow as tf

tf.get_logger().setLevel('INFO')
tf.autograph.set_verbosity(1)

# tf.Session(tf.ConfigProto(device_count={'GPU': 0}))
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
# cors = CORS(app, resources={r"/foo": {"origins": "http://127.0.0.1:8080"}})
# app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy   dog'
app.config['CORS_HEADERS'] = 'Content-Type'

api = Api(app, '/api')
socketio = SocketIO(app, cors_allowed_origins="*")
model = None
model2 = None


@app.route('/test')
def index():
    return render_template('test.html')


def process_image(filestr, img_size, v):
    # get_model()
    image = PIL.open(BytesIO(filestr))
    if image.mode != "RGB" and v == 1:
        image = image.convert("RGB")
    if v == 2:
        image = image.convert("L")
    image = image.resize((img_size, img_size))
    image = np.array(image)
    image = np.expand_dims(image, axis=0)
    image = imagenet_utils.preprocess_input(image)
    image = image[0].reshape(1, 48, 48, 1)
    image = image / 255
    return image


# ========== Sending Messages
# The following examples bounce received events back to the client that sent them:


# When working with namespaces, send() and emit() use the namespace of the incoming message by default. A different
# namespace can be specified with the optional namespace argument:

# To send an event with multiple arguments, send a tuple:
# SocketIO supports acknowledgment callbacks that confirm that a message was received by the client:
def ack():
    print('message was received!')


record_result = [0, 0, 0, 0, 0, 0, 0]


@socketio.on('end_record')
def handle_my_custom_event_end():
    global record_result
    output = {
        'error': 'None',
        'response': {
            'Neutral': record_result[4],
            'Anger': record_result[0],
            'Disgust': record_result[1],
            'Fear': record_result[2],
            'Happiness': record_result[3],
            'Sadness': record_result[5],
            'Surprise': record_result[6]
        }
    }
    record_result = [0, 0, 0, 0, 0, 0, 0]
    emit('new_message_client', output)


@socketio.on('start_record')
def handle_my_custom_event(arg1):
    global record_result
    # emit('my response', ('foo', 'bar', json), namespace='/chat', callback=ack)
    # print('received args: ' + arg1)
    img = base64.decodebytes(arg1.split(',')[1].encode())
    temp_file_name = 'static/img/' + str(time.time()) + '.jpg'
    fh = open(temp_file_name, "wb")
    fh.write(img)
    fh.close()

    image = process_image(img, 48, 2)
    predictions = model2.predict(image)[0]
    print(predictions)
    print("Natural :" + str(predictions[4]))
    print("Max Val:" + str(max(predictions)))
    if predictions[4] != max(predictions):
        list3 = zip(record_result, predictions)
        record_result = [x + y for (x, y) in list3]
    #print(list3)
    #print(record_result.shape)
    print(record_result)


# socketio.on_event('my event', handle_my_custom_event)
@socketio.on('connect')
def test_connect():
    # if not authenticate(request.args):
    #     raise ConnectionRefusedError('unauthorized!')
    emit('client event', {'data': 'Connected', 'received_data': request.args}, callback=ack)
    # return 'test'


@socketio.on('disconnect')
def test_disconnect():
    emit('socket disconnected')


# Error Handling
# Flask-SocketIO can also deal with exceptions:
@socketio.on_error()  # Handles the default namespace
def error_handler(e):
    pass


@socketio.on_error_default  # handles all namespaces without an explicit error handler
def default_error_handler(e):
    pass


# The message and data arguments of the current request can also be inspected with the request.event variable
@socketio.on("my error event")
def on_my_event(data):
    raise RuntimeError()


@socketio.on_error_default
def default_error_handler(e):
    print(request.event["message"])  # "my error event"
    print(request.event["args"])  # (data,)


class Image2(Resource):
    def post(self):
        try:
            parse = reqparse.RequestParser()
            parse.add_argument(
                'file', type=FileStorage, location='files')
            args = parse.parse_args()
            filestr = args['file'].read()
            image = process_image(filestr, 48, 2)
            predictions = model2.predict(image)[0]
            return {
                'error': 'None',
                'response': {
                    'Neutral': str(predictions[4]),
                    'Anger': str(predictions[0]),
                    'Disgust': str(predictions[1]),
                    'Fear': str(predictions[2]),
                    'Happiness': str(predictions[3]),
                    'Sadness': str(predictions[5]),
                    'Surprise': str(predictions[6])
                }
            }
        except Exception as e:
            print(e)
            return {'error': e}


class Root(Resource):
    def post(self):
        return {'response': {'ho': 'ho'}}


api.add_resource(Image2, '/image')


def get_model():
    # import tensorflow as tf
    # print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))
    global model
    global model2
    if model == None:
        # export_path = os.path.join(os.getcwd(), 'saved_models', 'model_tl_1')
        export_path = "./saved_models/model_tl_2"
        # model = load_model(export_path)
    if model2 == None:
        # export_path = os.path.join(os.getcwd(), 'saved_models', 'model_tl_1')
        export_path2 = "./saved_models/model_v2"
        model2 = load_model(export_path2)
    return


get_model()
if __name__ == '__main__':
    socketio.run(app, debug=True, port=8090)
