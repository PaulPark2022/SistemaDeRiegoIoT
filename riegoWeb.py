import socket
import threading
import serial

from fastapi import FastAPI
from fastapi import File
from fastapi import UploadFile
from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse

app = FastAPI()

# Detalles del socket
SOCKET_ADDRESS = '192.168.142.45'
SOCKET_PORT = 12345

# Variable para simular la humedad (puedes reemplazarla con la lectura real del sensor)
current_humidity = 0.0

@app.get('/', response_class=HTMLResponse)
async def main():
    content = f"""
<!DOCTYPE html>
<html>
    <head>
        <title>Riego TEC</title>
    </head>
    <body>
        <h1>Bienvenido a Riego TEC</h1>
        <p>Humedad actual: {current_humidity} %</p>
        <form action="/startpump/" method="post">
            <input type="submit" value="Encender Bomba de Agua">
        </form>
        <form action="/stoppump/" method="post">
            <input type="submit" value="Apagar Bomba de Agua">
        </form>
    </body>
</html>
    """
    return content

@app.post('/startpump/')
def start_pump():
    return send_command_to_socket("start")

@app.post('/stoppump/')
def stop_pump():
    return send_command_to_socket("stop")

def send_command_to_socket(command):
    try:
        # Create a socket connection to the server
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((SOCKET_ADDRESS, SOCKET_PORT))
        
        # Send command
        sock.send(command.encode())
        sock.close()
        return f"Bomba de agua {command == 'start' and 'encendida' or 'apagada'}"
    except Exception as e:
        return f"Failed to {command == 'start' and 'encender' or 'apagar'} bomba: {e}"
    
def socket_server():
    global current_humidity
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((SOCKET_ADDRESS, SOCKET_PORT))
    server_socket.listen(5)
    print("Socket server listening on", SOCKET_ADDRESS, SOCKET_PORT)

    while True:
        client_socket, addr = server_socket.accept()
        print('Connection from:', addr)
        data = client_socket.recv(1024).decode()
        if data.startswith("humidity:"):
            current_humidity = data.split(":")[1]
        client_socket.close()

# Iniciar el servidor de sockets en un hilo separado
threading.Thread(target=socket_server, daemon=True).start()

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app=app, host="0.0.0.0", port=8000)