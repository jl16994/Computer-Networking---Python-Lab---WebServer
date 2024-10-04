# import socket module
from socket import *
# In order to terminate the program
import sys


def webServer(port=13331):
    serverSocket = socket(AF_INET, SOCK_STREAM)

    # Prepare a server socket
    serverSocket.bind(("", port))

    # Fill in start
    serverSocket.listen(1)  # Enable the server to accept connections, backlog = 1
    # Fill in end

    while True:
        # Establish the connection
        print('Ready to serve...')
        # Fill in start
        connectionSocket, addr = serverSocket.accept()  # Accept connection from client
        # Fill in end

        try:
            # Fill in start
            message = connectionSocket.recv(1024).decode()  # Receive message from client
            filename = message.split()[1]  # Extract the requested file name
            # Fill in end

            # Open the requested file in binary read mode
            f = open(filename[1:], 'rb')  # Remove leading '/' and open the file

            # Initialize a variable to hold the file content
            file_content = b""

            # Use a for-loop to read the file and append content
            for i in f:
                file_content += i  # Collect all file content

            f.close()

            # Prepare the response headers
            response_header = "HTTP/1.1 200 OK\r\n"
            response_header += "Content-Type: text/html\r\n"
            response_header += "Connection: close\r\n"  # Add Connection header
            response_header += "Server: Simple-Python-Server\r\n"  # Add Server header
            response_header += f"Content-Length: {len(file_content)}\r\n"  # Content length
            response_header += "\r\n"  # End of headers

            # Combine headers and file content into a single variable
            response = response_header.encode() + file_content

            # Send the combined response (headers + file content) in one go
            connectionSocket.send(response)

            # Close the connection socket
            connectionSocket.close()

        except Exception as e:
            # Send response message for file not found (404)
            error_message = "<html><body><h1>404 Not Found</h1></body></html>".encode()
            response_header = "HTTP/1.1 404 Not Found\r\n"
            response_header += "Content-Type: text/html\r\n"
            response_header += "Connection: close\r\n"  # Add Connection header for 404 response
            response_header += "Server: Simple-Python-Server\r\n"  # Add Server header for 404 response
            response_header += f"Content-Length: {len(error_message)}\r\n"  # Content length
            response_header += "\r\n"

            # Combine headers and error message into a single variable
            response = response_header.encode() + error_message

            # Send the combined 404 response in one go
            connectionSocket.send(response)

            # Close the client connection socket
            connectionSocket.close()


if __name__ == "__main__":
    webServer(13331)
