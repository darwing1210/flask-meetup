# Configuraciones de nuestra aplicación
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    '''Configuración principal.'''
    DEBUG = False
    CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')


class DevConfig(Config):
    '''Configuraciones para desarrollo.'''
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


app_config = {
    'development': DevConfig,
    # 'testing': TestingConfig,
    # 'staging': StagingConfig,
    # 'production': ProductionConfig,
}