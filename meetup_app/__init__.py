# Inicializando configuración
from meetup_app.config import app_config
from meetup_app import controllers

from flask import Flask


def crear_app(configuracion):
    app = Flask(__name__)
    app.config.from_object(app_config[configuracion])
    app.register_blueprint(controllers.urls)

    return app
