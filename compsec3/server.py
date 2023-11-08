import socket
import ssl
import hashlib
import sys

HASH_ALGORITHM = 'SHA-256'
FILE_NAME = 'hashpasswd.txt'

def hash_password(password):
    digest = hashlib.sha256()
    digest.update(password.encode())
    return digest.hexdigest()

def id_and_password_exists(user_id, hashed_password):
    try:
        with open(FILE_NAME, 'r') as file:
            for line in file:
                stored_id, stored_password, _ = line.strip().split(' ', 2)
                if user_id == stored_id and hashed_password == stored_password:
                    return True
    except FileNotFoundError:
        pass
    return False

def main(port):
    # Set SSL context
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile='keystore.p12', password='rushabh')

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        with context.wrap_socket(sock, server_side=True) as ssock:
            ssock.bind(('', port))
            ssock.listen(5)
            print(f'SSL Server started on port {port}')

            while True:
                client_socket, _ = ssock.accept()
                with client_socket:
                    print('Client connected.')
                    try:
                        while True:
                            data = client_socket.recv(1024).decode()
                            if data == 'Over' or not data:
                                break

                            user_id, password = data.split(' ', 1)
                            hashed_password = hash_password(password)

                            if id_and_password_exists(user_id, hashed_password):
                                response = 'correct ID/Password'
                            else:
                                response = 'Incorrect ID/Password'

                            client_socket.sendall(response.encode())
                            if response == 'correct ID/Password':
                                break

                    finally:
                        print('Closing connection')
                        client_socket.close()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python server.py <port number>')
        sys.exit(1)

    main_port = int(sys.argv[1])
    main(main_port)
