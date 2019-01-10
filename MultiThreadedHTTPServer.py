import sys
from http.server import HTTPServer
from threading import Thread, current_thread
from http.server import BaseHTTPRequestHandler


class MultiThreadedHTTPServer(HTTPServer):
    def process_request(self, request, client_address):
        Thread(target=self.__request, args=(self.RequestHandlerClass, request, client_address, self)).start()

    def __request(self, handler, request, address, server):
        handler(request, address, server)
        self.shutdown_request(request)


class RequestHandler(BaseHTTPRequestHandler):
    def _set_response_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_response_headers()
        self.wfile.write(('GET Request served on '+current_thread().getName()).encode())

    def do_POST(self):
        self._set_response_headers()
        self.wfile.write(('POST Request served on '+current_thread().getName()).encode())


if __name__ == '__main__':
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = 6789
    print('Starting server on port :' + str(port))
    server = MultiThreadedHTTPServer(('', port), RequestHandler)
    server.serve_forever()