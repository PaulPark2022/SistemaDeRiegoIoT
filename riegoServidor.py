import socket
import serial
import time
import threading

# Configuración del socket
ADDRESS = '0.0.0.0'  # Escuchar en todas las interfaces
PORT = 12345

# Configuración del puerto serial
SERIAL_PORT = '/dev/ttyACM0'  # Cambia esto según el puerto donde esté conectado tu ATmega328P
BAUD_RATE = 9600

# Inicializar comunicación serial
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE)
except serial.SerialException as e:
    print(f"Error al abrir el puerto serial: {e}")
    exit(1)

# Función para manejar conexiones individuales
def handle_connection(connection, client_address):
    try:
        while True:
            data = connection.recv(1024)
            if not data:
                break
            command = data.decode()
            if command == 'A' or command == 'a':
                print(f"Enviando comando: {command}")
                if command == 'a':
                    time.sleep(2)
                    ser.write(b'a')
                elif command == 'A':
                    time.sleep(2)
                    ser.write(b'A')
                # Enviar confirmación al cliente
                connection.sendall(b'Command executed successfully')
    except Exception as e:
        print(f"Error en la conexión con {client_address}: {e}")
    finally:
        connection.close()

# Inicializar socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((ADDRESS, PORT))
sock.listen()

try:
    while True:
        print("Esperando conexión...")
        connection, client_address = sock.accept()
        print(f"Conexión recibida desde: {client_address}")
        # Manejar la conexión en un hilo separado
        threading.Thread(target=handle_connection, args=(connection, client_address)).start()
except KeyboardInterrupt:
    print("Shutting down server...")
except Exception as e:
    print(f"Something happened: {e}")
finally:
    ser.close()
    sock.close()
