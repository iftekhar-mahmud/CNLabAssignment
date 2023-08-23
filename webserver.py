import socket

def handle_request(client_socket):
    request_data = client_socket.recv(1024).decode()


    requested_file = request_data.split(" ")[1]
    if requested_file == "/":
        requested_file = "/index.html"

    try:
        with open("." + requested_file, "rb") as file:
            response_data = file.read()
        status_line = "HTTP/1.1 200 OK\r\n"
        content_type_line = "Content-Type: text/html\r\n"
    except FileNotFoundError:
        response_data = b"<h1>404 Not Found</h1>"
        status_line = "HTTP/1.1 404 Not Found\r\n"
        content_type_line = "Content-Type: text/html\r\n"

    response = status_line + content_type_line + "\r\n" + response_data.decode()
    client_socket.sendall(response.encode())
    client_socket.close()

def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ("127.0.0.1", 8080)
    server_socket.bind(server_address)
    server_socket.listen(1)

    print("Ready to Serve...")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            handle_request(client_socket)
    except KeyboardInterrupt:
        print("Server is shutting down...")
    finally:
        server_socket.close()

if __name__ == "__main__":
    run_server()
