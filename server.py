import socketserver
import sys
from util.request import Request
# encode into byte array before sending
class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        received_data = self.request.recv(2048)
        print(self.client_address)
        print("--- received data ---")
        print(received_data)
        print("--- end of data ---\n\n")
        request = Request(received_data)
       # print("Request headers are: ", request.headers)
        rHeader = request.headers
        host = rHeader["Request"]
        if (host[0].strip() == "GET"):
            print("Trying to access: ", rHeader["Request"][1].strip(), "\n\n")
            pathHTML = './public/index.html'
            pathIMG = './public/image'
            pathPublic = './public/'
            print("Headers: ", rHeader, "\n\n")
            try: 
                if host[1][13::] == "" or host[1][13::] == "/":
                    print("Host: ", host)
                    with open(pathHTML, "rb") as file: # rb = read as bytes
                        htmlContent = file.read().decode().strip()
                    # manually write response header
                    response_headers = """HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\nContent-Length: {}\r\nX-Content-Type-Options: nosniff\r\n\r\n""".format(len(htmlContent))
                    # add response header with html to send
                    response_headers = response_headers.encode() + htmlContent.encode()
                    self.request.sendall(response_headers)
                elif "public/image" in host[1]:
                    pathIMG = pathIMG + "/" + host[1][13::]
                    print("Trying to access an image:", pathIMG)
                    with open(pathIMG, "rb") as img: # concatenates image name from url to path and read it
                        image = img.read()
                    response_headers = """HTTP/1.1 200 OK\r\nContent-Type: {}\r\nContent-Length: {}\r\nX-Content-Type-Options: nosniff\r\n\r\n""".format("image/jpeg", len(image))
                    response_headers = response_headers.encode() + image
                    self.request.sendall(response_headers)
                elif ".css" in host[1] or ".js" in host[1]:
                    print("Trying to access CSS or JS file")
                    if ".css" in host[1]:
                        mime = 'text/css'
                    else:
                        mime = 'text/js'
                    pathPublic += host[1][7::]
                    with open(pathPublic, "rb") as file:
                        readFile = file.read()
                    response_headers = """HTTP/1.1 200 OK\r\nContent-Type: {}\r\nContent-Length: {}\r\nX-Content-Type-Options: nosniff\r\n\r\n""".format(mime, len(readFile))
                    response_headers = response_headers.encode() + readFile
                    self.request.sendall(response_headers)
                else:
                    err = 'ERROR 404 :('
                    errorMsg = """HTTP/1.1 404 Not Found\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: {}\r\nX-Content-Type-Options: nosniff\r\n\r\n""".format(len(err))
                    errorMsg += err
                    self.request.sendall(errorMsg.encode())
            except IndexError:
                    err = '400 Bad Request'
                    errorMsg = """HTTP/1.1 404 Not Found\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: {}\r\nX-Content-Type-Options: nosniff\r\n\r\n""".format(len(err))
                    errorMsg += err
                    self.request.sendall(errorMsg.encode())                    
        # TODO: Parse the HTTP request and use self.request.sendall(response) to send your response


def main():
    host = "0.0.0.0"
    port = 8000

    socketserver.TCPServer.allow_reuse_address = True

    server = socketserver.TCPServer((host, port), MyTCPHandler)

    print("Listening on port " + str(port))
    sys.stdout.flush()
    sys.stderr.flush()

    server.serve_forever()


if __name__ == "__main__":
    main()
