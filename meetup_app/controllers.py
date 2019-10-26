from datetime import datetime

from flask import Blueprint, escape, request, render_template, jsonify, abort

urls = Blueprint('urls', __name__)

eventos = [{
    'id': 1,
    'nombre': 'Python Day 7',
    'fecha': datetime.now(),
    'descripcion': 'Taller: Flask, Construyendo REST API.',
    'lugar': 'NicaSource',
    'asistentes': [{
        'id': 1,
        'nombre': 'Juan Perez',
        'rol': 'miembro',
        'lugar': 'Managua',
    }]
}]


@urls.route('/')
def hola():
    nombre = request.args.get('nombre', 'mundo')
    return f'Hola {escape(nombre)}!'

@urls.route('/bienvenidos')
def bienvenidos():
    return render_template('bienvenidos.html')

@urls.route('/eventos')
def listar_eventos():
    return jsonify(eventos)

@urls.route('/eventos', methods=['POST'])
def crear_evento():
    # Content-Type: application/json
    evento = request.json.get('evento', {})
    eventos.append(evento)

    return jsonify(evento)

@urls.route('/eventos/<int:id_evento>', methods=['GET'])
def obtener_evento(id_evento):
    evento = next(
        (evento for evento in eventos if evento["id"] == id_evento), None
    )
    if evento is None:
        return abort(404)
    return jsonify(evento)

@urls.route('/eventos/<int:id_evento>', methods=['PUT'])
def actualizar_evento(id_evento):
    indice = next(
        (indice for indice, evento in enumerate(eventos)
            if evento["id"] == id_evento),
        None)

    if indice is None:
        return abort(404)
    
    eventos[indice] = request.json.get('evento', {})
    return jsonify(eventos[indice])

@urls.route('/eventos/<int:id_evento>', methods=['DELETE'])
def eliminar_evento(id_evento):
    indice = next(
        (indice for indice, evento in enumerate(eventos)
            if evento["id"] == id_evento),
        None)

    if indice is None:
        return abort(404)
    
    del(eventos[indice])
    return {}, 200
