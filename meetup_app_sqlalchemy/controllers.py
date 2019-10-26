from datetime import datetime

from flask import Blueprint, escape, request, render_template, jsonify, abort, g
from dateutil import parser as dateparser

from meetup_app_sqlalchemy import db, auth
from meetup_app_sqlalchemy.models import Usuario, Evento

urls = Blueprint('urls', __name__)

@urls.route('/')
@auth.login_required
def hola():
    nombre = g.user.nombre
    return f'Hola {nombre}!'

@urls.route('/bienvenidos')
def bienvenidos():
    return render_template('bienvenidos.html')

@urls.route('/eventos')
def listar_eventos():
    eventos = Evento.query.all()
    return jsonify([evento.to_dict() for evento in eventos])

@urls.route('/eventos', methods=['POST'])
def crear_evento():
    # Content-Type: application/json
    evento_in = request.json.get('evento', {})
    # evento = Evento(evento_in**)
    evento = Evento()
    evento.nombre = evento_in.get('nombre', 'Evento sin nombre')

    # parseando fecha
    fecha = evento_in.get('fecha', None)
    if fecha is not None:
        fecha = dateparser.parse(fecha)
    evento.fecha = fecha

    evento.descripcion = evento_in.get('descripcion')
    evento.lugar = evento_in.get('lugar')
    db.session.add(evento)
    db.session.commit()

    return jsonify(evento.to_dict())

@urls.route('/eventos/<int:id_evento>', methods=['GET'])
def obtener_evento(id_evento):
    evento = Evento.query.get(id_evento)
    if evento is None:
        return abort(404)
    return jsonify(evento.to_dict())

@urls.route('/eventos/<int:id_evento>', methods=['PUT'])
def actualizar_evento(id_evento):
    evento_in = request.json.get('evento', {})
    evento = Evento.query.get(id_evento)
    if evento is None:
        return abort(404)

    evento.nombre = evento_in.get('nombre', 'Evento sin nombre')

    # parseando fecha
    fecha = evento_in.get('fecha', None)
    if fecha is not None:
        fecha = dateparser.parse(fecha)
    evento.fecha = fecha

    evento.descripcion = evento_in.get('descripcion')
    evento.lugar = evento_in.get('lugar')
    db.session.commit()
    
    return jsonify(evento.to_dict())

@urls.route('/eventos/<int:id_evento>', methods=['DELETE'])
def eliminar_evento(id_evento):
    evento = Evento.query.get(id_evento)

    if evento is None:
        return abort(404)
    
    db.session.delete(evento)
    db.session.commit()
    return {}, 200

##### Usuarios

@urls.route('/usuarios', methods=['POST'])
def crear_usuario():
    email = request.json.get('email')
    password = request.json.get('password')

    if email is None or password is None:
        abort(400, 'falta email o password') # Faltan argumentos
    if Usuario.query.filter_by(email=email).first() is not None:
        abort(400, 'usuario existe') # El usuario existe

    usuario = Usuario(email=email)
    usuario.hash_password(password)

    usuario.nombre = request.json.get('nombre')
    usuario.apellido = request.json.get('apellido')
    usuario.rol = request.json.get('rol')
    usuario.lugar = request.json.get('rol')

    db.session.add(usuario)
    db.session.commit()
    return jsonify({'usuario': usuario.email}), 201

@urls.route('/eventos/<int:id_evento>/registrarse', methods=['POST'])
@auth.login_required
def unirse_a_evento(id_evento):
    evento = Evento.query.get(id_evento)
    if evento is None:
        return abort(404)

    evento.asistentes.append(g.user)
    db.session.commit()

    return {}, 200

@urls.route('/eventos/<int:id_evento>/salirse', methods=['POST'])
@auth.login_required
def salirse_evento(id_evento):
    evento = Evento.query.get(id_evento)
    if evento is None:
        return abort(404)

    evento.asistentes.remove(g.user)
    db.session.commit()

    return {}, 200
