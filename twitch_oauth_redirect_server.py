import ssl
import logging
from http.server import HTTPServer,BaseHTTPRequestHandler

class TwitchOAuthRedirectRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        logging.info("GET")




if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s [%(levelname)s] twitch_oauth_redirect_server - %(message)s',
        level=logging.INFO
    )
    host = 'localhost'
    port = 8000
    server_address = (host, port)
    httpd = HTTPServer(server_address, TwitchOAuthRedirectRequestHandler)

    httpd.socket = ssl.wrap_socket(
        httpd.socket,
        keyfile="path/to/key.pem",
        certfile='path/to/cert.pem',
        server_side=True
    )

    logging.info(f'Listening on host [{host}] and port [{port}]')
    httpd.serve_forever()