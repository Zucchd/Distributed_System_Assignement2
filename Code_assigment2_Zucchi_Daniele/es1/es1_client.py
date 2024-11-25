import socket

def start_client():
    host = "127.0.0.1"  
    port = 8080         

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((host, port))
        print("Connected to the server.")

        while True:
            message = input("Enter message (type 'end' to quit): ")

            client.sendall(message.encode("utf-8"))

            response = client.recv(1024).decode("utf-8")
            print("Server replied:", response)

            if message.lower() == "end":
                print("Ending connection with the server.")
                break

        print("Connection closed.")

if __name__ == "__main__":
    start_client()