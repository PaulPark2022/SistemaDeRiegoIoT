from flask import Flask, render_template, request
import socket

app = Flask(__name__)

# Dirección y puerto del servidor (Raspberry Pi)
ADDRESS = '192.168.142.45'  # Reemplaza con la IP de tu Raspberry Pi
PORT = 12345

def send_command(action):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((ADDRESS, PORT))
            if action == 'on':
                sock.sendall('A'.encode())
            elif action == 'off':
                sock.sendall('a'.encode())
            else:
                return 'Invalid action'
            return 'Command sent successfully'
    except Exception as e:
        return f'Error: {str(e)}'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/control', methods=['POST'])
def control():
    action = request.form['action']
    result = send_command(action)
    return result

if __name__ == '__main__':
    app.run(debug=True)
