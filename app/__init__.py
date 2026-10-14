import os.path
from flask import Flask, render_template

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY=None)

    app.config['MAX_CONTENT_LENGTH'] = 30 * 1024 * 1024  # 30 MB
    app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif', '.pdf', '.docx', '.xlsx', '.pptx', '.txt', '.zip', '.rar', '.7z', '.mp4', '.mp3', '.wav', '.py', '.java', '.c', '.cpp', '.html', '.css', '.js']
    app.config['MAX_FILES'] = 5
    app.config['MAX_LINKS'] = 10
    app.config['UPLOAD_PATH'] = os.path.join(app.instance_path, 'uploads')
    app.config['MAX_KEY_VALIDITY_DAYS'] = 365
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

    # Error handlers
    @app.errorhandler(413)
    def file_too_large(error):
        return render_template('error.html', code=413, title='File Too Large', message=f'The file you uploaded is too large. The maximum allowed file size is {app.config["MAX_CONTENT_LENGTH"] // (1024 * 1024)} MB.', error=error), 413

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('error.html', code=404, title='Page Not Found', message='The page you are looking for does not exist.', error=error), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template('error.html', code=500, title='Internal Server Error', message='An unexpected error occurred on the server.', error=error), 500
    
    @app.errorhandler(403)
    def forbidden(error):
        return render_template('error.html', code=403, title='Forbidden', message='You do not have the required permissions to access this resource.', error=error), 403

    @app.errorhandler(400)
    def bad_request(error):
        return render_template('error.html', code=400, title='Bad Request', message='The request is malformed and thus could not be understood by the server.', error=error), 400

    @app.errorhandler(405)
    def method_not_allowed(error):
        return render_template('error.html', code=405, title='Method Not Allowed', message='The requested method is not allowed for the requested resource.', error=error), 405

    return app

