# Configuraciones de nuestra aplicación
import os

class Config(object):
    '''Configuración principal.'''
    DEBUG = False
    CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')


class DevConfig(Config):
    '''Configuraciones para desarrollo.'''
    DEBUG = True


app_config = {
    'development': DevConfig,
    # 'testing': TestingConfig,
    # 'staging': StagingConfig,
    # 'production': ProductionConfig,
}