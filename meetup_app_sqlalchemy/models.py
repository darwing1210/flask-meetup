from werkzeug.security import generate_password_hash, check_password_hash

from meetup_app_sqlalchemy import db


asistentes_evento = db.Table(
    'asistentes_evento',
    db.Column('id_usuario', db.Integer, db.ForeignKey('usuario.id')),
    db.Column('id_evento', db.Integer, db.ForeignKey('evento.id'))
)


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(64))
    apellido = db.Column(db.String(64))
    email = db.Column(db.String(120), index=True, unique=True)
    rol = db.Column(db.String(64))
    lugar = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))

    eventos = db.relationship('Evento', secondary=asistentes_evento)

    def __repr__(self):
        return '<User {} {}>'.format(self.nombre, self.apellido)

    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verificar_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'email': self.email,
            'rol': self.rol,
            'lugar': self.lugar,
        }


class Evento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(64))
    fecha = db.Column(db.DateTime, index=True)
    descripcion = db.Column(db.Text)
    lugar = db.Column(db.String(64))

    asistentes = db.relationship('Usuario', secondary=asistentes_evento)

    def __repr__(self):
        return '<Evento {}>'.format(self.nombre)

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'fecha': self.fecha,
            'descripcion': self.descripcion,
            'lugar': self.lugar,
            'asistentes': [usuario.to_dict() for usuario in self.asistentes]
        }
