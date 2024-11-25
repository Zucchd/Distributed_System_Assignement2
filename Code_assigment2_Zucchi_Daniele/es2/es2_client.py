import socket
import message_pb2  

def start_client():
    host = "127.0.0.1"
    port = 8080

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((host, port))
        print("Connected to the server.")
        
        from_id = int(input("Enter your ID: "))
        to_id = int(input("Enter recipient ID: "))
        
        while True:
            msg = input("Enter message (type 'end' to quit): ")
            
            chat_message = message_pb2.ChatMessage()
            chat_message.from_id = from_id
            chat_message.to_id = to_id
            chat_message.msg = msg
            
            client.sendall(chat_message.SerializeToString())
            
            response = client.recv(1024)
            response_message = message_pb2.ChatMessage()
            response_message.ParseFromString(response)
            
            print(f"Echo from server - From: {response_message.from_id}, To: {response_message.to_id}, Message: {response_message.msg}")

            if msg.strip().lower() == "end":
                print("Ending connection with the server.")
                break

if __name__ == "__main__":
    start_client()
