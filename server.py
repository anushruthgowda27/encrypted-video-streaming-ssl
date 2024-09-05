import socket 
import cv2
import pickle
import struct
import ssl

# Server configuration
SERVER_HOST = "172.20.10.4"
SERVER_PORT = 5000

# Path to your certificate and private key files
CERTIFICATE_PATH = "domain.crt"
PRIVATE_KEY_PATH = "domain.key"

# Socket initialization
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(5)

# SSL context creation
ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
ssl_context.load_cert_chain(certfile=CERTIFICATE_PATH, keyfile=PRIVATE_KEY_PATH)

print("[INFO] Waiting for client connection...")
client_socket, client_address = server_socket.accept()
print(f"[INFO] Client connected: {client_address}")

# Wrap the client socket with SSL
ssl_client_socket = ssl_context.wrap_socket(client_socket, server_side=True)

# OpenCV camera setup
camera = cv2.VideoCapture(0)

try:
    while True:
        # Capture frame from camera
        success, frame = camera.read()
        if not success:
            break

        # Serialize frame
        data = pickle.dumps(frame)
        # Pack message length as 4 bytes integer
        message_size = struct.pack("L", len(data))

        # Send message length followed by the serialized frame
        ssl_client_socket.sendall(message_size + data)

except KeyboardInterrupt:
    print("\n[INFO] Interrupted. Closing connections...")
    camera.release()
    server_socket.close()
    ssl_client_socket.close()
