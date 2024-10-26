from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'astro-hacks'

@app.route('/create_curve', methods=['POST'])
def create_curve():
    data = request.form
    # process the form
    return data


if __name__ == '__main__':  
   app.run() 