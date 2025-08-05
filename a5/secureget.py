import socket
import ssl

# target server and port
host = "www.google.com"
port = 443

# create a TCP connection
try:
    context = ssl.create_default_context()
    with socket.create_connection((host, port)) as sock:
        with context.wrap_socket(sock, server_hostname=host) as ssock:
            # send an HTTP GET request
            http_request = (
                f"GET / HTTP/1.1\r\n"
                f"Host: {host}\r\n"
                f"Connection: close\r\n"
                f"User-Agent: PythonSSLClient\r\n"
                f"\r\n"
            )
            ssock.sendall(http_request.encode("utf-8"))

            # read the response
            response = b""
            while True:
                data = ssock.recv(4096)
                if not data:
                    break
                response += data
except Exception as e:
    print(f"Error occurred: {e}")
    exit(1)

# save the response to a file
try:
    with open("response.html", "wb") as file:
        file.write(response)
    print("Saved response to response.html")
except Exception as e:
    print(f"Failed to write response: {e}")
    exit(1)
