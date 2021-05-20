#!/usr/bin/python3

"""Extend Python's built in HTTP server to save files

curl or wget can be used to send files with options similar to the following

  curl -X PUT --upload-file somefile.txt http://localhost:8000
  wget -O- --method=PUT --body-file=somefile.txt http://localhost:8000/somefile.txt

__Note__: curl automatically appends the filename onto the end of the URL so
the path can be omitted.

"""
import os
import http.server as server

def uid_generator():
    id = 0
    while True:
        yield id
        id = id + 1


class HTTPRequestHandler(server.SimpleHTTPRequestHandler):
    """Extend SimpleHTTPRequestHandler to handle PUT requests"""
    uid = 0

    def do_PUT(self):
        if os.path.basename(self.path) != "upload":
            self.send_response(404, 'Not found')
            self.end_headers()
            reply_body = ('No such page')
            self.wfile.write(reply_body.encode('utf-8'))
            return

        """Save a file following a HTTP PUT request"""
        filename = str(HTTPRequestHandler.uid)
        HTTPRequestHandler.uid += 1
        # filename = os.path.basename(self.path)

        # Don't overwrite files
        if os.path.exists(filename):
            self.send_response(409, 'Conflict')
            self.end_headers()
            reply_body = '"%s" already exists\n' % filename
            self.wfile.write(reply_body.encode('utf-8'))
            return

        file_length = int(self.headers['Content-Length'])
        with open(filename, 'wb') as output_file:
            output_file.write(self.rfile.read(file_length))
        self.send_response(201, 'Created')
        self.end_headers()
        reply_body = 'Saved "%s"\n' % filename
        self.wfile.write(reply_body.encode('utf-8'))
    
    def do_POST(self):
        file_length = int(self.headers['Content-Length'])
        uid = self.rfile.read(file_length)
        self.send_response(200, 'OK')
        self.end_headers()
        reply_body = str(uid.decode('utf-8'))
        print(reply_body)
        self.wfile.write(reply_body.encode('utf-8'))


if __name__ == '__main__':
    server.test(HandlerClass=HTTPRequestHandler, port=3000)
