import os
import sys

from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.wsgi import wsgiapp
 
top = "<div class='top'>Middleware TOP</div>"
bottom =  "<div class='botton'>Middleware BOTTOM</div>"

class MiddleWareWork(object):
    def __init__(self, app):
        self.app = app
        
    def __call__(self, environ, start_response):
        
        page = self.app(environ, start_response)[0]
        if page.find('<body>') >-1:
            header,body = page.split('<body>')
            data,htmlend = body.split('</body>')
            data = '<body>'+ top + data + bottom+'</body>'
            yield header + data + htmlend
        else:
            yield top + page + bottom
    

@wsgiapp
def index(environ, start_response):
    
    path = environ['PATH_INFO']
    filePath = '.' + path  
    if not os.path.isfile(filePath):
        filePath ='./index.html' 

    file = open(filePath,'r')
    fileContent = file.read()
    file.close()

    start_response('200 OK', [('Content-Type', 'text/html')])
    return [fileContent]

@wsgiapp
def aboutme(environ, start_response):
    
    path = environ['PATH_INFO']
    filePath = '.' + path  
    if not os.path.isfile(filePath):
        filePath ='./aboutme.html' 

    file = open(filePath,'r')
    fileContent = file.read()
    file.close()

    start_response('200 OK', [('Content-Type', 'text/html')])
    return [fileContent]


if __name__ == '__main__':
        config = Configurator()
    
        config.add_route('index', '/index.html')
        config.add_route('aboutme', '/about/aboutme.html')

        config.add_view(app, route_name='index')
        config.add_view(app, route_name='aboutme')

        pyramid_app = config.make_wsgi_app()
        result = MiddleWareWork(pyramid_app)

        server = make_server('0.0.0.0', 8000, answer)
        server.serve_forever()