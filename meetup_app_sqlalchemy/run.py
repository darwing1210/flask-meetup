import os

from meetup_app_sqlalchemy import crear_app

configuracion = os.getenv('FLASK_ENV') # configuracion = 'development'

app = crear_app(configuracion)

if __name__ == '__main__':
    app.run()