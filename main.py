from bottle import route, run, template

@route('/hello/<name>/<lastName>')
def index(name, lastName):
    return template('<b>Hello {{name}} {{lastName}}</b>!', name=name,lastName=lastName)

run(host='localhost', port=8080)