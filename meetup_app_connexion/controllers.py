from datetime import datetime

from flask import current_app as app
from flask import Blueprint, escape, request, render_template, jsonify, abort, g
from dateutil import parser as dateparser

from meetup_app_connexion import db, auth
from meetup_app_connexion.models import Usuario, Evento

urls = Blueprint('urls', __name__)

@urls.route('/')
@auth.login_required
def hola():
    nombre = g.user.nombre
    return f'Hola {nombre}!'

@urls.route('/bienvenidos')
def bienvenidos():
    return render_template('bienvenidos.html')


def listar_eventos():
    eventos = Evento.query.all()
    return jsonify([evento.to_dict() for evento in eventos])


def crear_evento(evento_in):
    # Content-Type: application/json
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


def obtener_evento(id_evento):
    evento = Evento.query.get(id_evento)
    if evento is None:
        return abort(404)
    return jsonify(evento.to_dict())


def actualizar_evento(id_evento, evento_in):
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


def eliminar_evento(id_evento):
    evento = Evento.query.get(id_evento)

    if evento is None:
        return abort(404)
    
    db.session.delete(evento)
    db.session.commit()
    return {}, 200

##### Usuarios

def crear_usuario(usuario_in):
    email = usuario_in.get('email')
    password = usuario_in.get('password')

    if email is None or password is None:
        abort(400, 'falta email o password') # Faltan argumentos
    if Usuario.query.filter_by(email=email).first() is not None:
        abort(400, 'usuario existe') # El usuario existe

    usuario = Usuario(email=email)
    usuario.hash_password(password)

    usuario.nombre = usuario_in.get('nombre')
    usuario.apellido = usuario_in.get('apellido')
    usuario.rol = usuario_in.get('rol')
    usuario.lugar = usuario_in.get('rol')

    db.session.add(usuario)
    db.session.commit()
    return jsonify(usuario.to_dict()), 201

@auth.login_required
def unirse_a_evento(id_evento):
    evento = Evento.query.get(id_evento)
    if evento is None:
        return abort(404)

    evento.asistentes.append(g.user)
    db.session.commit()

    return {}, 200

@auth.login_required
def salirse_evento(id_evento):
    evento = Evento.query.get(id_evento)
    if evento is None:
        return abort(404)

    evento.asistentes.remove(g.user)
    db.session.commit()

    return {}, 200
