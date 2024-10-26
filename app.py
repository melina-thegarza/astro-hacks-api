from flask import Flask, request, send_file, jsonify
from flask_cors import CORS, cross_origin
import lightkurve as lk
import numpy as np
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('agg')
from PIL import Image
import io
from base64 import encodebytes
import logging, os

app = Flask(__name__)
app.logger.setLevel(logging.INFO)

@app.route('/')
def hello_world():
    return 'astro-hacks'


@app.route('/create_curve', methods=['POST'])
@cross_origin(origin='*')
def create_curve():
    
    data = request.form
    name = data['lightcurve'].split(',')[0]
    author = "Kepler"
    quarter = data['lightcurve'].split(',')[1]
   
    
    #processing the lightcurve
    lc = lk.search_lightcurve(name, author=author, quarter=int(quarter)).download()
    pg = lc.normalize(unit='ppm').to_periodogram()
    power = []
    for p in pg.power.flat:
        power.append(p.value)
    
    x = np.array(power)
    peaks, _ = find_peaks(x, distance=400)
    plt.clf() 
    plt.plot(x)
    plt.plot(peaks, x[peaks], "x")
    plt.plot(np.zeros_like(x), "--", color="gray")
    plt.savefig('lightcurve-frequency.png')

    pil_img = Image.open('lightcurve-frequency.png', mode='r') # reads the PIL image
    byte_arr = io.BytesIO()
    pil_img.save(byte_arr, format='PNG') # convert the PIL image to byte array
    encoded_img = encodebytes(byte_arr.getvalue()).decode('ascii') # encode as base64

    return jsonify( {'frequencies': list(x[peaks]), 'ImageBytes': encoded_img})

if __name__ == '__main__':  
   app.run(debug=True)