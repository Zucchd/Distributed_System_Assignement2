import socket
import message_es3_pb2 
import threading
from sys import argv

def handle_client(conn, addr, client_id):
    print(f"Connected by {addr}")
    
    handshake = message_es3_pb2.Handshake()
    handshake.id = client_id
    handshake.error = False 

    try:
        conn.sendall(handshake.SerializeToString())
    except Exception as e:
        print(f"Error during handshake: {e}")
        handshake.error = True
        conn.sendall(handshake.SerializeToString())
        conn.close()
        return

    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break
            chat_message = message_es3_pb2.ChatMessage()
            chat_message.ParseFromString(data)
            print(f"Received message from {chat_message.from_id}: {chat_message.msg}")
            
            conn.sendall(data)
            
            if chat_message.msg.strip().lower() == "end":
                print(f"Ending connection with {addr}")
                break
        except Exception as e:
            print(f"Error: {e}")
            break

    conn.close()
    print(f"Connection closed with {addr}")

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
        
        client_id = 1

        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr, client_id)).start()
            client_id += 1

if __name__ == "__main__":
    start_server()
