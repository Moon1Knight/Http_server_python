import os.path
import socket
import sys
import threading
import gzip


def send_response(client_socket, body, content_encoding=""):
     
    encoding = ""
    content_encoding = content_encoding.strip()
    if content_encoding == "gzip":
        encoding = f"\r\nContent-Encoding: gzip"
    else:
        for encoding_type in content_encoding.split(","):
            encoding_type = encoding_type.strip()
            if encoding_type == "gzip":
                encoding = f"\r\nContent-Encoding: gzip"
    body = body.encode()
    if encoding == "\r\nContent-Encoding: gzip":
        body = gzip.compress(body)
    body_length = str(len(body))
    response_string = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain{encoding}\r\nContent-Length: {body_length}\r\n\r\n"
    response = response_string.encode() + body
    print(response)
    client_socket.sendall(response)


def send_file(client_socket, file, directory):
    if os.path.isfile(f"{directory}/{file}"):
        file = open(f"{directory}/{file}", "r")
        file_content = file.read()
        file.close()
        file_length = str(len(file_content))
        response_string = f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {file_length}\r\n\r\n{file_content}"
        response = response_string.encode()
        client_socket.sendall(response)
    else:
        client_socket.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")



def make_post(client_socket, file, body, directory):
    file = open(f"{directory}/{file}", "w")
    file.write(body)
    client_socket.sendall(b"HTTP/1.1 201 Created\r\n\r\n")



def start_server(client_socket, address, directory):
    data = client_socket.recv(1024).decode("utf-8")
    data = data.split("\r\n")
    request_line = data[0].split(" ")
    action = request_line[0]
    request_target = request_line[1]
    request_target_content = request_target.split("/")
    user_agent = ""
    content_encoding = ""
    for i in range(1, len(data) - 1):
        header = data[i]
        header_name = header.split(":")[0]
        if header_name.lower() == "user-agent":
            user_agent = header.split(" ")[1]
        elif header_name.lower() == "accept-encoding":
            content_encoding = header.split(":")[1]
    body = data[-1]
    
    if action == "POST" and request_target_content[1] == "files":
        make_post(client_socket, request_target_content[2], body, directory)
    elif request_target == "/":
        client_socket.sendall(b"HTTP/1.1 200 OK\r\n\r\n")
    elif request_target_content[1] == "files" and request_target_content[2]:
        send_file(client_socket, request_target_content[2], directory)
    elif request_target_content[1] == "echo" and request_target_content[2]:
        send_response(client_socket, request_target_content[2], content_encoding)
    elif request_target_content[1] == "user-agent":
        send_response(client_socket, user_agent)
    else:
        client_socket.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")



def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    directory = "~/Desktop/data"
    if len(sys.argv) >= 2 and sys.argv[1] == "--directory":
        directory = sys.argv[2]
    while True:
        client_socket, address = server_socket.accept()
        thread = threading.Thread(
            target=start_server, args=(client_socket, address, directory)
        )
        thread.start()




if __name__ == "__main__":
    main()