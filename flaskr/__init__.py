"""
The Application Factory
Create flask instance inside a function, called the application factory.
Any configuration, registration, and other setup the application needs will happen
inside the function, then the application will be returned.
"""

import os
from flask import Flask

def create_app(test_config=None):
    # create the Flask instance
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite')
    )

    if test_config is None:
        # when not testing, load the instance config
        app.config.from_pyfile('config.py', silent=True)
    else:
        # or load test config
        app.config.from_mapping(test_config)

    # make sure instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # simple hello world page
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    # register the database commands
    from . import db
    db.init_app(app)

    # register the blueprint
    from . import auth
    app.register_blueprint(auth.bp)

    return app