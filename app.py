from flask import Flask, request, send
import matplotlib
import lightkurve as lk
import scipy
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'astro-hacks'

@app.route('/create_curve', methods=['POST'])
def create_curve():
    data = request.form
    
    #processing the lighcurve
    search_result = lk.search_lightcurve("V1357 Cyg")
    lc = search_result[0].download()
    pg = lc.normalize(unit='ppm').to_periodogram()
    
    #returning plot
    pg. plot() 
    plt.savefig('my_plot.png')
    
    
    #returning the array of peaks
    pow=pg.power
    power_array= np.zeros(12000)
    k=0
    for i in pow:
        power_array[k]=i.value
        k=k+1
    peaks=scipy.signal.find_peaks(power_array, height=0, distance=350)
    return jsonify(peaks), send_file('my_plot.png', mimetype='image/gif')

if __name__ == '__main__':  
   app.run()