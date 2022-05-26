import re
import os
from http import server
from socketserver import ThreadingMixIn
from html_helpers import *
from flickr_api_helper import *


# Making a threading server class
class HTTPThreadingServer(ThreadingMixIn, server.HTTPServer):
    pass


# Defining GET and POST methods to handle client's requests
class RequestHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            try:
                with open('pages/index.html') as file:
                    response = file.read()
            except FileNotFoundError:
                self.send_response(404)
                self.send_header('Content-type', 'text/plain; charset=utf-8')
                self.end_headers()
                self.wfile.write(b"Page not Found\n<index.html>")
            else:
                print(f"{self.client_address[0]} connected on {self.client_address[1]}")
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                html_body = f"{make_html_table(extract_recepies(read_csv('data/cookbook.csv')))}</body>"
                newdata = re.split('</body>', response)
                data = newdata[0] + html_body + newdata[1]
                self.wfile.write(data.encode())

        elif self.path.startswith('/img'):
            try:
                with open('.' + self.path, 'rb') as file:
                    response = file.read()
            except FileNotFoundError:
                self.send_response(404)
                self.send_header('Content-type', 'text/plain; charset=utf-8')
                self.end_headers()
                message = f"Page not Found\n<{self.path[1:]}>"
                self.wfile.write(message.encode())
            else:
                self.send_response(200)
                self.send_header('Content-type', 'image/jpeg')
                self.end_headers()
                self.wfile.write(response)

        elif self.path == '/recepies.html':
            try:
                with open('pages/recepies.html') as file:
                    response = file.read()
            except FileNotFoundError:
                self.send_response(404)
                self.send_header('Content-type', 'text/plain; charset=utf-8')
                self.end_headers()
                message = f"Page not Found\n<{self.path[1:]}>"
                self.wfile.write(message.encode())
            else:
                print(f"{self.client_address[0]} connected on {self.client_address[1]}")
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                html_body = f"{return_recepies_html(extract_recepies(read_csv('data/cookbook.csv')))}</body>"
                newdata = re.split('</body>', response)
                data = newdata[0] + html_body + newdata[1]
                self.wfile.write(data.encode())

        elif self.path == '/ingridients.html':
            try:
                with open('pages/ingridients.html') as file:
                    response = file.read()
            except FileNotFoundError:
                self.send_response(404)
                self.send_header('Content-type', 'text/plain; charset=utf-8')
                self.end_headers()
                message = f"Page not Found\n<{self.path[1:]}>"
                self.wfile.write(message.encode())
            else:
                print(f"{self.client_address[0]} connected on {self.client_address[1]}")
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                html_body = f"{return_ingridients_html(extract_recepies(read_csv('data/cookbook.csv')))}</body>"
                newdata = re.split('</body>', response)
                data = newdata[0] + html_body + newdata[1]
                self.wfile.write(data.encode())

        elif self.path == '/gallery.html':
            try:
                with open('pages/gallery.html') as file:
                    response = file.read()
            except FileNotFoundError:
                self.send_response(404)
                self.send_header('Content-type', 'text/plain; charset=utf-8')
                self.end_headers()
                message = f"Page not Found\n<{self.path[1:]}>"
                self.wfile.write(message.encode())
            else:
                print(f"{self.client_address[0]} connected on {self.client_address[1]}")
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                html_body = f"{gallery_loader()}</body>"
                newdata = re.split('</body>', response)
                data = newdata[0] + html_body + newdata[1]
                self.wfile.write(data.encode())

        elif self.path == '/feedback.html':
            try:
                with open('pages/feedback.html') as file:
                    response = file.read()
            except FileNotFoundError:
                self.send_response(404)
                self.send_header('Content-type', 'text/plain; charset=utf-8')
                self.end_headers()
                message = f"Page not Found\n<{self.path[1:]}>"
                self.wfile.write(message.encode())
            else:
                print(f"{self.client_address[0]} connected on {self.client_address[1]}")
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                html_body = f"{feedback_loader()}</body>"
                newdata = re.split('</body>', response)
                data = newdata[0] + html_body + newdata[1]
                self.wfile.write(data.encode('utf-8'))

        else:
            try:
                with open('pages' + self.path) as file:
                    response = file.read()
            except FileNotFoundError:
                self.send_response(404)
                self.send_header('Content-type', 'text/plain; charset=utf-8')
                self.end_headers()
                message = f"Page not Found\n<{self.path[1:]}>"
                self.wfile.write(message.encode())
            else:
                print(f"{self.client_address[0]} connected on {self.client_address[1]}")
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(response.encode())

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length).decode()

        if len(body) > 0 and body.startswith('recipe='):
            try:
                with open('pages' + self.path) as file:
                    response = file.read()
            except FileNotFoundError:
                self.send_response(404)
                self.send_header('Content-type', 'text/plain; charset=utf-8')
                self.end_headers()
                message = f"Page not Found\n<{self.path[1:]}>"
                self.wfile.write(message.encode())
            else:
                posted_data = re.findall('recipe=(\S+)', body)
                lookup_word = posted_data[0]
                lookup_word = lookup_word.replace('+', ' ')
                html_body = f'<h1>{lookup_word}</h1>' + f'<div><img src="{check_for_image(lookup_word)}" ' \
                            f'alt="{lookup_word}"/></div>' + f'<div>{load_recipe_from_file(lookup_word)}</div>' + "</body>"
                print(f"{self.client_address[0]} connected on {self.client_address[1]}")
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                newdata = re.split('</body>', response)
                data = newdata[0] + html_body + newdata[1]
                self.wfile.write(data.encode())

        if len(body) > 0 and body.startswith('search='):
            try:
                with open('pages' + self.path) as file:
                    response = file.read()
            except FileNotFoundError:
                self.send_response(404)
                self.send_header('Content-type', 'text/plain; charset=utf-8')
                self.end_headers()
                message = f"Page not Found\n<{self.path[1:]}>"
                self.wfile.write(message.encode())
            else:
                posted_data = re.findall('search=(\S+)', body)
                lookup_word = posted_data[0]
                html_body = f"{make_html_table(make_search(lookup_word))}</body>"
                print(f"{self.client_address[0]} connected on {self.client_address[1]}")
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                newdata = re.split('</body>', response)
                data = newdata[0] + html_body + newdata[1]
                self.wfile.write(data.encode())

        elif len(body) > 0 and body.startswith('fname='):
            try:
                with open('pages' + self.path) as file:
                    response = file.read()
            except FileNotFoundError:
                self.send_response(404)
                self.send_header('Content-type', 'text/plain; charset=utf-8')
                self.end_headers()
                message = f"Page not Found\n<{self.path[1:]}>"
                self.wfile.write(message.encode())
            else:
                posted_data = re.findall('fname=\S+', body)
                posted_data = posted_data[0].split('&')
                saved = feedback_saver(posted_data, self.client_address[0])
                html_body = f'<h2>{saved}</h2>'
                print(f"{self.client_address[0]} connected on {self.client_address[1]}")
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                head = re.split('<h2>', response)
                tail = re.split('</form>', response)
                data = head[0] + html_body + tail[1]
                self.wfile.write(data.encode())


if __name__ == '__main__':
    server_address = ('localhost', 8888)
    # server_address = ('', int(os.environ.get('PORT', '8000')))
    print('http://localhost:8888')
    httpd = HTTPThreadingServer(server_address, RequestHandler)
    httpd.serve_forever()
