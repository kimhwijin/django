from waitress import serve
from stocksite.wsgi import application
## documentation: https://docs.pylonsproject.org/projects/waitress/en/stable/api.html
if __name__ == '__main__':
    #serve(application,host='127.0.0.1',port='8080', listen='*:8080')
    serve(application, listen='*:8080')
    
