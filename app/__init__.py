import os.path
from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY=None)

    app.config['MAX_CONTENT_LENGTH'] = 30 * 1024 * 1024  # 30 MB
    app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif', '.pdf', '.docx', '.xlsx', '.pptx', '.txt', '.zip', '.rar', '.7z', '.mp4', '.mp3', '.wav', '.py', '.java', '.c', '.cpp', '.html', '.css', '.js']
    app.config['MAX_FILES'] = 5
    app.config['MAX_LINKS'] = 10
    app.config['UPLOAD_PATH'] = os.path.join(app.instance_path, 'uploads')
    app.config['MAX_KEYS_PER_GENERATION'] = 100


    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=False)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)

    # ensure the uploads folder exists
    os.makedirs(app.config['UPLOAD_PATH'], exist_ok=True)

    from . import database
    database.init_db()

    from jinja2 import StrictUndefined
    app.jinja_env.undefined = StrictUndefined

    from .routes import auth, main, admin, teacher, student, files
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(teacher.bp)
    app.register_blueprint(student.bp)
    app.register_blueprint(files.bp)

    return app

