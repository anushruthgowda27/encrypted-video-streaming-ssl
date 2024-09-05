import socket
import cv2
import pickle
import struct
import ssl

# Server configuration
SERVER_HOST = "172.20.10.4"
SERVER_PORT = 5000

# Path to your certificate file
CERTIFICATE_PATH = "C:\\Users\\AnushruthGowda\\Desktop\\twmp\\rootCA.crt"

# Socket initialization
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# SSL context creation
ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
ssl_context.load_verify_locations(CERTIFICATE_PATH)

# Wrap the client socket with SSL
wrapped_socket = ssl_context.wrap_socket(client_socket, server_hostname=SERVER_HOST)

try:
    # Connect to the server
    wrapped_socket.connect((SERVER_HOST, SERVER_PORT))
    print("Connected to server")

    # OpenCV window setup
    cv2.namedWindow("Live Video")

    while True:
        # Receive message length
        message_size = wrapped_socket.recv(struct.calcsize("L"))
        if not message_size:
            break

        # Unpack message length as 4 bytes integer
        message_size = struct.unpack("L", message_size)[0]

        # Receive serialized frame
        data = b""
        while len(data) < message_size:
            packet = wrapped_socket.recv(message_size - len(data))
            if not packet:
                break
            data += packet

        # Deserialize frame
        frame = pickle.loads(data)

        # Display frame
        cv2.imshow("Live Video", frame)
        cv2.waitKey(1)

except KeyboardInterrupt:
    print("\n[INFO] Interrupted. Closing connection...")
    cv2.destroyAllWindows()
    wrapped_socket.close()
