import socket
# Define the server's IP address and port
SERVER_IP = '192.168.142.45' 
SERVER_PORT = 12345  
# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    # Connect to the server
    client_socket.connect((SERVER_IP, SERVER_PORT))
    print(f"Connected to server at {SERVER_IP}:{SERVER_PORT}")
    # Send data to the server
    while True:
        message = input("Enter message to send (or 'exit' to quit): ")
        if message.lower() == 'exit':
            break
        client_socket.sendall(message.encode())
finally:
    # Close the connection
    client_socket.close()
    print("Connection closed")
    
    
#import socket
#import time

#ADDRESS = '192.168.142.45' #localhost para conexion local 
#0.0.0.0 abrir soket a cualquiera en la red
#PORT = 3333

#sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) ##socket TCP this is the way to go

#sock.connect((ADDRESS, PORT))

#try:
#    while True:
#        to_send = input ("Do you want to send somenthing? -->")
#        sock.send(to_send.encode())
#        time.sleep(1)

#except KeyboardInterrupt:
 #   print("Shutting down server...")
#except Exception as e:
#    print(f"Something happened {e}")
#finally:
#    sock.close()






#import socket

# Dirección y puerto del servidor (Raspberry Pi)
#ADDRESS = '192.168.142.45'  # Reemplaza con la IP de tu Raspberry Pi
#PORT = 3333

#sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) ##socket TCP this is the way to go

#sock.connect((ADDRESS, PORT))

#@app.route('/')
#def index():
#    return render_template('index.html')

#@app.route('/control', methods=['POST'])
#def control():
#    action = request.form['action']
#    try:
#        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
#            sock.connect((ADDRESS, PORT))
#            if action == 'on':
#                sock.sendall('A'.encode())
#            elif action == 'off':
 #               sock.sendall('a'.encode())
 #   except socket.error as e:
 #       print(f"Error al conectar con el servidor de la Raspberry Pi: {e}")
  #  return 'Command sent'

#if __name__ == '__main__':
 #   app.run(host='0.0.0.0', port=5000, debug=True)
