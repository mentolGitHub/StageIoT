from queue import Queue
from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)
Q_out : Queue

@app.route('/')
def accueil():
    return 0

@app.route('/post_data', methods=['POST'])
def post_data():
    print("post_data")
    if request.method == 'POST':
        data = request.get_data()
        print(data)
        Q_out.put(data)    
    return "200"
    
@app.route('/get_data', methods=['GET', 'POST'])
def get_data():
    pass

def IPnode(Q_output : Queue):
    global Q_out
    Q_out = Q_output
    socketio.run(app, host='0.0.0.0', port=5000)

    while True:
        print("IPnode")
        # get_data()

    

if __name__ == '__main__':
    q = Queue()
    IPnode(q)