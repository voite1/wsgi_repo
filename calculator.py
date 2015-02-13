import re

def add (left, right):
    return str(int(left) + int(right))

def subtract (left, right):
    return str(int(left) - int(right))

def multiply (left, right):
    return str(int(left) * int(right))   

def divide (left, right):
    return str(int(left) / int(right))

def home():
    body = ['<h2>Usage</h2>']
    body.append('<ul>')
    body.append('<li>/add/&lt;integer&gt;/&lt;integer&gt;</li>')
    body.append('<li>/subtract/&lt;integer&gt;/&lt;integer&gt;</li>')
    body.append('<li>/multiply/&lt;integer&gt;/&lt;integer&gt;</li>')
    body.append('<li>/divide/&lt;integer&gt;/&lt;integer&gt;</li>')
    body.append('</ul>')
    return "\n".join(body)

def resolve_path(path):
    methods = { 'add':add, 'subtract':subtract, 'multiply':multiply, 'divide':divide }
    # isolate path and arguments
    p = re.compile(r'/')
    lst = p.split(path)
    # redirect to home page
    if len(lst[1]) == 0:
        return (home, ())
    # dispatch requests
    if len(lst) == 4:
        if lst[1] in methods.keys():
            return methods[lst[1].strip()], (lst[2].strip(), lst[3].strip())
        else:
            # invalid method/page name
            raise NameError
    else:
        # invalid number of arguments
        raise ValueError

def application(environ, start_response):
    headers = [("Content-type", "text/html")]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except ValueError:
        status = "406 Not Acceptable"
        body = "<h1>406 Not Acceptable<h1>"
    except ZeroDivisionError:
        status = "406 Not Acceptable"
        body = "<h1>Integer Division or Modulo by Zero</h1>"
    except Exception, e:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
        print str(e)
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body]

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
