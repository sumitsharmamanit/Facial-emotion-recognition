# from gevent import monkey
# monkey.patch_all()
import random
import time

from flask import Flask, request, render_template
from flask_cors import CORS
from flask_restful import Resource, Api, reqparse
from io import BytesIO
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "nifty-foundry-292614-ef00096b72dd.json"
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
from google.cloud import storage


tf.get_logger().setLevel('INFO')
tf.autograph.set_verbosity(1)

# tf.Session(tf.ConfigProto(device_count={'GPU': 0}))
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)
# cors = CORS(app, resources={r"/foo": {"origins": "http://127.0.0.1:8080"}})
# app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy   dog'
# app.config['CORS_HEADERS'] = 'Content-Type'
# async_mode = None
api = Api(app, '/api')
# socketio = SocketIO(app,async_mode=async_mode, cors_allowed_origins="*")
socketio = SocketIO(app,cors_allowed_origins="http://127.0.0.1:8080")
model = None
model2 = None
# SocketIO(app,cors_allowed_origins="*")

# app = Flask(__name__)
#CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/service-worker.js')
def sw():
    return app.send_static_file('service-worker.js')


# @app.route('/index')
@app.route('/')
def index():
    images = ['1019', '1022', '1026', '1030', '1033', '1040', '1050', '1051', '1052', '1070', '1080', '1090', '1101',
              '1110', '1111', '1112', '1113', '1114', '1120', '1121', '1122', '1200', '1201', '1202', '1205', '1220',
              '1230', '1230', '1240', '1270', '1271', '1274', '1275', '1280', '1300', '1301', '1302', '1303', '1304',
              '1310', '1313', '1321', '1333', '1340', '1350', '1390', '1410', '1419', '1440', '1441', '1450', '1460',
              '1463', '1500', '1505', '1510', '1525', '1540', '1560', '1590', '1590', '1595', '1600', '1601', '1602',
              '1603', '1604', '1605', '1610', '1610', '1616', '1617', '1620', '1630', '1640', '1640', '1645', '1650',
              '1659', '1660', '1661', '1670', '1670', '1675', '1710', '1720', '1721', '1722', '1726', '1731', '1740',
              '1750', '1810', '1811', '1812', '1820', '1850', '1900', '1903', '1908', '1910', '1920', '1930', '1931',
              '1932', '1935', '1942', '1945', '1947', '1999', '2000', '2002', '2005', '2010', '2018', '2019', '2020',
              '2025', '2026', '2030', '2032', '2034', '2035', '2036', '2037', '2038', '2039', '2040', '2045', '2050',
              '2053', '2055.1', '2055.2', '2056', '2057', '2058', '2060', '2070', '2071', '2075', '2080', '2091',
              '2092', '2095', '2100', '2101', '2102', '2104', '2107', '2110', '2115', '2120', '2122', '2130', '2141',
              '2150', '2151', '2152', '2153', '2154', '2155', '2156', '2158', '2160', '2165', '2170', '2190', '2191',
              '2200', '2205', '2206', '2208', '2209', '2210', '2210', '2211', '2214', '2215', '2216', '2217', '2220',
              '2221', '2222', '2224', '2230', '2235', '2240', '2250', '2260', '2270', '2271', '2272', '2273', '2274',
              '2276', '2278', '2279', '2280', '2299', '2300', '2301', '2302', '2303', '2304', '2305', '2306', '2308',
              '2309', '2310', '2311', '2312', '2314', '2320', '2331', '2332', '2339', '2340', '2341', '2342', '2344',
              '2345.1', '2345', '2346', '2347', '2351', '2352', '2352.1', '2352.2', '2357', '2358', '2359', '2360',
              '2362', '2370', '2372', '2373', '2374', '2375.1', '2375.2', '2377', '2381', '2382', '2383', '2384',
              '2385', '2387', '2388', '2389', '2390', '2391', '2392', '2393', '2394', '2395', '2396', '2397', '2398',
              '2399', '2400', '2410', '2411', '2435', '2440', '2441', '2442', '2445', '2446', '2455', '2456', '2457',
              '2458', '2480', '2484', '2485', '2487', '2488', '2489', '2490', '2491', '2493', '2495', '2499', '2500',
              '2501', '2506', '2510', '2511', '2512', '2513', '2514', '2515', '2516', '2518', '2520', '2521', '2525',
              '2530', '2540', '2550', '2560', '2570', '2575', '2579', '2580', '2590', '2593', '2594', '2595', '2597',
              '2598', '2600', '2605', '2606', '2616', '2620', '2630', '2635', '2650', '2655', '2660', '2661', '2681',
              '2682', '2683', '2688', '2690', '2691', '2692', '2694', '2695', '2700', '2702', '2703', '2704', '2710',
              '2715', '2716', '2717', '2718', '2720', '2722', '2730', '2745.1', '2745.2', '2749', '2750', '2751',
              '2752', '2753', '2770', '2780', '2791', '2795', '2799', '2800', '2810', '2811', '2830', '2840', '2850',
              '2870', '2880', '2890', '2900', '2900.1', '2900.2', '2980', '2981', '3000', '3000', '3001', '3005.1',
              '3005.2', '3010', '3010', '3015', '3016', '3017', '3019', '3022', '3030', '3051', '3053', '3059', '3060',
              '3061', '3062', '3063', '3064', '3068', '3069', '3071', '3080', '3100', '3101', '3102', '3103', '3110',
              '3120', '3130', '3131', '3140', '3150', '3160', '3168', '3170', '3180', '3181', '3185', '3190', '3191',
              '3195', '3210', '3211', '3212', '3213', '3215', '3216', '3220', '3225', '3230', '3250', '3261', '3266',
              '3280', '3300', '3301', '3302', '3310', '3350', '3360', '3400', '3500', '3530', '3550', '3550.1',
              '3550.2', '4000', '4001', '4002', '4003', '4004', '4005', '4006', '4007', '4008', '4071', '4085', '4090',
              '4100', '4130', '4141', '4142', '4150', '4180', '4210', '4220', '4220', '4225', '4230', '4232', '4233',
              '4235', '4240', '4250', '4255', '4274', '4275', '4279', '4290', '4300', '4302', '4310', '4311', '4320',
              '4325', '4460', '4470', '4490', '4500', '4503', '4505', '4510', '4520', '4520', '4525', '4530', '4531',
              '4532', '4533', '4534', '4535', '4536', '4537', '4538', '4542', '4550', '4559', '4561', '4571', '4572',
              '4573', '4574', '4575', '4597', '4598', '4599', '4600', '4601', '4603', '4604', '4605', '4606', '4607',
              '4608', '4609', '4610', '4611', '4612', '4613', '4614', '4616', '4617', '4619', '4621', '4622', '4623',
              '4624', '4625', '4626', '4628', '4631', '4635', '4640', '4641', '4643', '4645', '4647', '4649', '4650',
              '4651', '4652', '4653', '4656', '4658', '4659', '4660', '4664', '4664.1', '4664.2', '4666', '4668',
              '4669', '4670', '4672', '4676', '4677', '4680', '4681', '4683', '4687', '4689', '4690', '4692', '4693',
              '4694', '4695', '4697', '4698', '4700', '4750', '4770', '4800', '4810', '5000', '5001', '5010', '5020',
              '5030', '5040', '5120', '5130', '5199', '5200', '5201', '5202', '5210', '5215', '5220', '5250', '5260',
              '5270', '5300', '5301', '5390', '5395', '5410', '5450', '5455', '5460', '5470', '5471', '5480', '5500',
              '5510', '5520', '5530', '5531', '5532', '5533', '5534', '5535', '5551', '5593', '5594', '5600', '5611',
              '5621', '5622', '5623', '5626', '5628', '5629', '5631', '5635', '5660', '5661', '5665', '5700', '5711',
              '5720', '5725', '5726', '5731', '5740', '5750', '5760', '5764', '5779', '5780', '5781', '5800', '5811',
              '5814', '5820', '5825', '5829', '5830', '5831', '5833', '5836', '5849', '5870', '5875', '5890', '5891',
              '5900', '5910', '5920', '5940', '5950', '5961', '5970', '5971', '5972', '5973', '5982', '5990', '5991',
              '5994', '6000', '6010', '6020', '6021', '6022', '6150', '6190', '6200', '6200', '6210', '6211', '6212',
              '6213', '6220', '6230', '6231', '6240', '6241', '6242', '6243', '6244', '6250', '6250.1', '6250.2',
              '6260', '6263', '6300', '6311', '6312', '6313', '6314', '6315', '6350', '6360', '6370', '6410', '6415',
              '6510', '6520', '6530', '6540', '6550', '6555', '6560', '6561', '6562', '6563', '6570', '6570.1',
              '6570.2', '6571', '6610', '6800', '6821', '6825', '6830', '6831', '6832', '6834', '6836', '6837', '6838',
              '6840', '6900', '6910', '6930', '6940', '7000', '7001', '7002', '7003', '7004', '7006', '7009', '7010',
              '7011', '7012', '7013', '7014', '7016', '7017', '7018', '7019', '7020', '7021', '7023', '7025', '7026',
              '7030', '7031', '7032', '7033', '7034', '7035', '7036', '7037', '7038', '7039', '7040', '7041', '7042',
              '7043', '7044', '7045', '7046', '7050', '7052', '7053', '7054', '7055', '7056', '7057', '7058', '7059',
              '7060', '7061', '7062', '7077', '7078', '7079', '7080', '7081', '7090', '7092', '7095', '7096', '7100',
              '7110', '7130', '7135', '7136', '7137', '7140', '7150', '7160', '7161', '7165', '7170', '7175', '7179',
              '7180', '7182', '7183', '7184', '7185', '7186', '7187', '7188', '7190', '7192', '7195', '7200', '7205',
              '7207', '7211', '7217', '7220', '7224', '7230', '7233', '7234', '7235', '7236', '7237', '7238', '7240',
              '7242', '7247', '7248', '7249', '7250', '7255', '7260', '7270', '7279', '7280', '7281', '7282', '7283',
              '7284', '7285', '7286', '7287', '7289', '7290', '7291', '7300', '7320', '7325', '7330', '7340', '7350',
              '7351', '7352', '7354', '7359', '7360', '7361', '7365', '7380', '7390', '7400', '7402', '7405', '7410',
              '7430', '7440', '7450', '7451', '7460', '7461', '7470', '7472', '7475', '7476', '7477', '7480', '7481',
              '7482', '7484', '7487', '7488', '7489', '7490', '7491', '7492', '7493', '7495', '7496', '7497', '7499',
              '7500', '7501', '7502', '7503', '7504', '7505', '7506', '7507', '7508', '7509', '7510', '7512', '7513',
              '7515', '7520', '7521', '7530', '7545', '7546', '7547', '7550', '7560', '7570', '7580', '7590', '7595',
              '7600', '7620', '7632', '7640', '7650', '7660', '7700', '7705', '7710', '7820', '7830', '7900', '7920',
              '7950', '8001', '8010', '8021', '8030', '8031', '8032', '8033', '8034', '8040', '8041', '8050', '8060',
              '8065', '8080', '8090', '8116', '8117', '8118', '8120', '8121', '8130', '8158', '8160', '8161', '8162',
              '8163', '8170', '8178', '8179', '8180', '8185', '8186', '8190', '8191', '8192', '8193', '8200', '8205',
              '8206', '8208', '8210', '8211', '8220', '8230', '8231', '8232', '8241', '8250', '8251', '8260', '8280',
              '8300', '8311', '8312', '8320', '8325', '8330', '8340', '8341', '8350', '8370', '8371', '8380', '8400',
              '8420', '8460', '8461', '8465', '8466', '8467', '8470', '8475', '8480', '8485', '8490', '8492', '8496',
              '8497', '8499', '8500', '8501', '8502', '8503', '8510', '8531', '8540', '8600', '8620', '9000', '9001',
              '9002', '9005', '9006', '9007', '9008', '9010', '9031', '9040', '9041', '9042', '9043', '9045', '9046',
              '9050', '9070', '9075', '9080', '9090', '9090', '9101', '9102', '9110', '9120', '9140', '9145', '9150',
              '9156', '9160', '9163', '9171', '9180', '9181', '9182', '9183', '9184', '9185', '9186', '9187', '9190',
              '9210', '9220', '9230', '9250', '9252', '9253', '9254', '9260', '9265', '9270', '9280', '9290', '9291',
              '9295', '9300', '9301', '9302', '9320', '9321', '9322', '9325', '9326', '9330', '9331', '9332', '9340',
              '9341', '9342', '9360', '9373', '9390', '9395', '9400', '9401', '9402', '9403', '9404', '9405', '9409',
              '9410', '9411', '9412', '9413', '9414', '9415', '9417', '9419', '9420', '9421', '9422', '9423', '9424',
              '9425', '9426', '9427', '9428', '9429', '9430', '9432', '9433', '9435', '9440', '9445', '9452', '9468',
              '9469', '9470', '9471', '9472', '9480', '9490', '9491', '9495', '9500', '9520', '9530', '9560', '9561',
              '9570', '9571', '9582', '9584', '9590', '9592', '9594', '9596', '9599', '9600', '9610', '9611', '9620',
              '9621', '9622', '9623', '9630', '9635.1', '9635.2', '9700', '9800', '9810', '9830', '9831', '9832',
              '9900', '9901', '9902', '9903', '9904', '9905', '9908', '9909', '9910', '9911', '9912', '9913', '9920',
              '9921', '9922', '9925', '9926', '9927', '9930', '9940', '9941']
    sampling = random.choices(images, k=3)
    # sampling = ['2055.2', '4233', '7179', '7508', '8116', '9300']
    # sampling = ['2055.2', '4233', '7179']

    storage_client = storage.Client()
    bucket_name = 'vibe_image'

    bucket = storage_client.get_bucket(bucket_name)
    for img in sampling:
        file_data = 'img/IAPS 1-20 Images/' + img + '.jpg'
        temp_file_name = 'static/img/' + img + '.jpg'
        blob = bucket.get_blob(file_data)
        blob.download_to_filename(temp_file_name)

    return render_template('index.html', sync_mode=socketio.async_mode, title='Welcome', sampling_images=sampling)


@app.route('/test')
def test():
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
    temp_file_name = 'static/img/test/' + str(time.time()) + '.jpg'
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
    socketio.run(app, debug=True, port=8080)
