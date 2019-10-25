'''
Esta es la aplicación mas sencilla que puedes hacer con Flask 
Tomado y traducido de https://palletsprojects.com/p/flask/
'''

from flask import Flask, escape, request

app = Flask(__name__)

@app.route('/')
def hola():
    nombre = request.args.get('nombre', 'mundo')
    return f'Hola {escape(nombre)}!'