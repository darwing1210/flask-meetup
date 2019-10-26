import connexion

from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_httpauth import HTTPBasicAuth


# Extensiones
db = SQLAlchemy()
migrate = Migrate()
auth = HTTPBasicAuth()

# Inicializando configuración
from meetup_app_connexion.config import app_config
from meetup_app_connexion import controllers

# Esto es requerido para que alembic reconozca los modelos
from meetup_app_connexion import models

def crear_app(configuracion):
    cxapp = connexion.App(__name__, specification_dir='./')
    cxapp.add_api('swagger.yml')
    cxapp.app.config.from_object(app_config[configuracion])
    cxapp.app.register_blueprint(controllers.urls)

    # inicializando db
    db.init_app(cxapp.app)
    migrate.init_app(cxapp.app, db)

    return cxapp.app


@auth.verify_password
def verify_password(username, password):
    usuario = models.Usuario.query.filter_by(email=username).first()
    if usuario is None or not usuario.verificar_password(password):
        return False
    # explicar que significa g
    g.user = usuario
    return True
