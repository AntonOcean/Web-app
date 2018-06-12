import socket

from views import index, blog

URLS = {
    '/': index,
    '/blog': blog,
}


def parse_request(request):
    parsed = request.split()
    method = parsed[0]
    url = parsed[1]
    return method, url


def generate_headers(method, url):
    if not method == 'GET':
        return 'HTTP/1.1 405 method not allowed\n\n', 405
    if url not in URLS:
        return 'HTTP/1.1 404 not found\n\n', 404
    return 'HTTP/1.1 200 OK\n\n', 200


def generate_content(status_code, url):
    if status_code == 404:
        return '<h1>404</h1><p>page not found</p>'
    if status_code == 405:
        return '<h1>405</h1><p>method not allowed</p>'
    return URLS[url]()


def generate_response(request):
    method, url = parse_request(request)
    headers, status_code = generate_headers(method, url)
    body = generate_content(status_code, url)
    return (headers + body).encode()


def run():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # AF_INET - IPv4 protocol
    # SOCK_STREAM - TCP protocol
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 5001))  # сокет ждет обращение на адрес по порту
    server_socket.listen()  # прослушка порта на наличие входящих пакетов

    while True:
        client_socket, addr = server_socket.accept()  # получил от клиента
        request = client_socket.recv(1024)
        print(request)
        print(addr)

        response = generate_response(request.decode('utf-8'))

        client_socket.sendall(response)
        client_socket.close()


if __name__ == '__main__':
    run()
