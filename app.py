from flask import Flask, render_template, request, send_file
from PIL import Image
import os
import uuid
import numpy as np
import cv2

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
RESULT_FOLDER = 'static/results'

# Path to load the model 
PROTOTXT = "model/colorization_deploy_v2.prototxt"
POINTS = "model/pts_in_hull.npy"
MODEL = "model/colorization_release_v2.caffemodel"

# loadung the colorization model from Caffe using the prototxt and model weight files
net = cv2.dnn.readNetFromCaffe(PROTOTXT, MODEL)
points = np.load(POINTS)
points = points.transpose().reshape(2, 313, 1, 1)
net.getLayer(net.getLayerId("class8_ab")).blobs = [points.astype(np.float32)]
net.getLayer(net.getLayerId("conv8_313_rh")).blobs = [np.full([1, 313], 2.606, dtype="float32")]

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/About.html')
def about():
    return render_template('About.html')

@app.route('/colorize', methods=['POST'])
def colorize():
    file = request.files['image']
    if file:
        #Save uploaded image
        filename = str(uuid.uuid4()) + '.png'
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        
        bw_image = cv2.imread(filepath) #loading the image
        normalized = bw_image.astype("float32") / 255.0 #normalization
        lab = cv2.cvtColor(normalized, cv2.COLOR_BGR2LAB) #convert bgr-->lab
        resized = cv2.resize(lab, (224, 224)) #rsize 244*244 reqyired by the model
        L = cv2.split(resized)[0]  #extact l chanel (gray part)
        L -= 50

        

      #feeding the image to the network

        net.setInput(cv2.dnn.blobFromImage(L))
        #predecting the colores
        ab = net.forward()[0, :, :, :].transpose((1, 2, 0))
        ab = cv2.resize(ab, (bw_image.shape[1], bw_image.shape[0]))
        L = cv2.split(lab)[0]
        colorized = np.concatenate((L[:, :, np.newaxis], ab), axis=2)
        colorized = cv2.cvtColor(colorized, cv2.COLOR_LAB2BGR)
        colorized = (255.0 * colorized).astype("uint8")

        #displayin the image
        max_dim = 800
        result_path = os.path.join(RESULT_FOLDER, 'colorized_' + filename)
        cv2.imwrite(result_path, colorized)

     # Generate output 
        return send_file(result_path, mimetype='image/png')
    
    return 'No file uploaded', 400

if __name__ == '__main__':
    app.run(debug=True)
