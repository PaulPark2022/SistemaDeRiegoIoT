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
