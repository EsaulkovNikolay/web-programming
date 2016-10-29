from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from jinja2 import Environment,FileSystemLoader

environment=Environment(loader=FileSystemLoader('HTML'))

def Index(request):
    return Response(environment.get_template('index.html').render(link='<a href="/about/aboutme.html">About me</a>',
                                                         head='<h1>Index</h1>'))
def AboutMe(request):
    return Response(environment.get_template('about/aboutme.html').render(link='<a href="/index.html">Index</a>',
                                                         head="""<h1>About Me</h1>"""))

if __name__ == "__main__":
    configuration=Configurator()
    configuration.add_view(Index, route_name="home")
    configuration.add_route("home", "/")
    configuration.add_view(Index, route_name="index")
    configuration.add_route("index", "/index.html")
    configuration.add_view(AboutMe, route_name="aboutMe")
    configuration.add_route("aboutMe", "/about/aboutme.html")
    app=configuration.make_wsgi_app()
    server = make_server("localhost", 8080, app)
    print("Serving localhost on port 8080...")
    server.serve_forever()
