from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from celery_app import app as celery_app

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # replace with your secret key
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.form.get('message')
    celery_app.send_task('process_incoming_message', kwargs={'message': message})
    return jsonify({})

@app.route('/receive_bot_message', methods=['POST'])
def receive_bot_message():
    message = request.form.get('message')
    socketio.emit('message', {'text': message, 'type': 'robot'})
    return jsonify({})

if __name__ == '__main__':
    socketio.run(app, debug=True)