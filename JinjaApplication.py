from wsgiref.simple_server import make_server
from jinja2 import Environment,FileSystemLoader,Template

def app(environ, start_response):
    status = "404 Not Found"
    template=['File not found.']
    environment=Environment(loader=FileSystemLoader('HTML'))
    response_headers = [('Content-type', 'text/html; charset=utf-8')]

    if environ["PATH_INFO"] == "/" or environ["PATH_INFO"] == "/index.html":
        status="200 OK"
        template=environment.get_template('/index.html').render(link='<a href="/about/aboutme.html">About me</a>',
                                                         head='<h1>Index</h1>')
    elif environ["PATH_INFO"] == "/about/aboutme.html":
        status="200 OK"
        template = environment.get_template('/about/aboutme.html').render(link='<a href="/index.html">About me</a>',
                                                         head="""<h1>Aboutme</h1>""")

    start_response(status, response_headers)
    return [template.encode('utf-8')]


class Middleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        top_tag = "<body>"
        bottom_tag = "</body>"
        top_string = "\n<div class='top'>Middleware TOP</div>"
        bottom_string = "<div class='bottom'>Middleware BOTTOM</div>\n"

        string = self.app(environ, start_response)
        if string == ['File not found.']:
            return;
        top_index = string.index(top_tag)
        bottom_index = string.rindex(bottom_tag)

        if bottom_index > -1:
            string = string[:bottom_index - 1] + bottom_string + string[bottom_index:]

        if top_index > -1:
            string = string[:top_index + len(top_tag)] + top_string + string[top_index + len(top_tag):]

        return string


if __name__ == '__main__':
    server = make_server("localhost", 8000, Middleware(app))
    print("Serving localhost on port 8000...")
    server.serve_forever()
