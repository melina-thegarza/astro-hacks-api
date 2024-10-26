from flask import Flask, request, send_file, jsonify, g
from flask_cors import CORS, cross_origin
import lightkurve as lk
import numpy as np
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
import logging

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
   
    
    #processing the lighcurve
    lc = lk.search_lightcurve(name, author=author, quarter=int(quarter)).download()
    pg = lc.normalize(unit='ppm').to_periodogram()
    power = []
    for p in pg.power.flat:
        power.append(p.value)
    
    x = np.array(power)
    peaks, _ = find_peaks(x, distance=400)

    return jsonify( {'frequencies': list(x[peaks])})

if __name__ == '__main__':  
   app.run(debug=True)