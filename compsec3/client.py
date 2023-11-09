import ssl
import socket
import sys

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def start(self):
        # Set up the SSL context
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        context.load_verify_locations(cafile="server.crt")
        context.verify_mode = ssl.CERT_REQUIRED
        context.check_hostname = False

        # Create SSL socket
        with context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=self.host) as ssl_sock:
            try:
                # Connect to server
                ssl_sock.connect((self.host, self.port))
                print("Connected to SSL Server")

                while True:
                    # Prompt user for ID
                    user_id = input("Enter ID (or type 'exit' to quit): ")
                    if user_id.lower() == 'exit':
                        break

                    # Prompt user for Password
                    password = input("Enter Password: ")

                    # Send data
                    ssl_sock.sendall((user_id + " " + password).encode())

                    # Receive response
                    response = ssl_sock.recv(1024).decode()
                    print(response)

                    if response == "correct ID/Password":
                        break

                print("Closing connection")

            except ssl.SSLError as e:
                print(f"SSL error: {e}")
            except Exception as e:
                print(f"I/O error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python client.py <host> <port number>")
    else:
        host = sys.argv[1]
        port = int(sys.argv[2])
        client = Client(host, port)
        client.start()
