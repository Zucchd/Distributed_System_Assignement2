import socket
import threading
from sys import argv

connected_users = 0
lock = threading.Lock()

def handle_client(conn, addr):
    global connected_users
    with lock:
        connected_users += 1

    print(f"Connected by {addr}")
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break
            message = data.decode("utf-8")
            print(f"Received message from {addr}: {message}")
            conn.sendall(f"Echo: {message}".encode("utf-8"))
            if message.strip().lower() == "end":
                print(f"Ending connection with {addr}")
                break
        except ConnectionResetError:
            break

    conn.close()
    with lock:
        connected_users -= 1
    print(f"Connection closed with {addr}")

def operator_thread():
    global connected_users
    while True:
        command = input("Enter command: ")
        if command.strip().lower() == "num users":
            with lock:
                print(f"Number of connected users: {connected_users}")

def start_server():
    try:
        port = int(argv[1])
    except:
        port = 8080

    print(f"Server started on port {port}")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("0.0.0.0", port))
        s.listen(5)
        print("Waiting for clients...")

        threading.Thread(target=operator_thread, daemon=True).start()

        while True:
            conn, addr = s.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()

if __name__ == "__main__":
    start_server()
