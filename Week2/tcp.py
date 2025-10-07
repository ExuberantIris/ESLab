import socket
import json
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation

HOST = '0.0.0.0'  # Listen on all available interfaces
PORT = 8002       # Port number (must match the STM32 client's port)

# Create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind
server_socket.bind((HOST, PORT))

# Listen for incoming connections (max 1 connection in the queue)
server_socket.listen(1)

print(f"TCP Server listening on {HOST}:{PORT}...")

fig, ax = plt.subplots()
x = []
y = []
z = []
line, = ax.plot(x, y)

def update_plot():
    ax.clear()
    ax.plot(x, label="X")
    ax.plot(y, label="Y")
    ax.plot(z, label="Z")
    ax.legend()
    plt.pause(0.001)

while True:
    # Wait for a connection
    print("Waiting for a connection...")
    client_socket, client_address = server_socket.accept()
    print(f"Connection established with {client_address}")

    try:
        while True:
            data = client_socket.recv(1024).decode('utf-8').strip()
            if not data:
                print("Client disconnected.")
                break  # Exit the inner loop if the client disconnects

            try:
                # Parse Json
                sensor_data = json.loads(data)
                print(f"Received sensor data: {sensor_data}")

                # Append new data
                x.append(sensor_data["x"])
                y.append(sensor_data["y"])
                z.append(sensor_data["z"])

                # Update
                update_plot()


                # Send confirmation message
                confirmation_message = "Data received and processed"
                client_socket.sendall(confirmation_message.encode('utf-8'))

            except json.JSONDecodeError:
                print("Invalid JSON data received")
                
                error_message = "Error: Invalid JSON format"
                client_socket.sendall(error_message.encode('utf-8'))
            except KeyError as e:  #Handle the case if x, y, or z keys do not exist in JSON
                print(f"KeyError: {e} not found in JSON data")
                error_message = f"Error: Key {e} missing in JSON"
                client_socket.sendall(error_message.encode('utf-8'))


    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close() #close connection
        print("Client socket closed.")
    
