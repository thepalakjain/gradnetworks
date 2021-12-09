import socket
#from do import do
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer
import webbrowser
import sys

hostName = socket.gethostname()
serverPort = 8085

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path.strip("/").split("/")
        if path[0] == "":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            with open("index.html", "r") as f:
                self.wfile.write(bytes(f.read(), "utf-8"))

        elif path[0] == "break":
            md5hash = urllib.parse.unquote(path[1])
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            crack_the_password(md5hash)
#            print(md5hash)
            
def crack_the_password(md5hash):
    #connect to manager
    HOST = socket.gethostname()
    PORT = 8080 

    man = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    man.connect((HOST, PORT))

    #send hashval to manager
    man.sendall(md5hash.encode())
    print("connected to manager, sending hash...")

    #listen for password
    while True:
        response = man.recv(1024).decode("utf-8")
        if response:
            print("received cracked password!")
            password,start_time,stop_time = response.split()
            print(md5hash + " " + response)
            man.close()
            return


if __name__ == "__main__":

    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))
    url = 'http://' + hostName + ":" + str(serverPort)
    webbrowser.open_new(url)
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
