from flask import Flask , render_template
from flask_cors import CORS

from .extensions import db , jwt

from flask_migrate import Migrate



from datetime import timedelta , datetime , timezone

from .jwtinit import jwtinit

from .auth import auth
from .classmanager import classManager
from .schedulemanager import scheduleManager
from .subjectsmanager import subjectsManager
from .workmanager import workManager
from .baseworkmanager import baseworkManager
from .interface import interface

def create_app():
    app = Flask(__name__, static_folder='static/')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wtfdb.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'eaisjkdaowefsj'
    #app.config['JSON_AS_ASCII'] = False
    #app.config['JSONIFY_MIMETYPE'] = "application/json;charset=utf-8"

    ACCESS_EXPIRES = timedelta(days=30)
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES

    CORS(app)
    db.init_app(app)
    jwt.init_app(app)
    Migrate(app, db)

    
    jwtinit(jwt)
    
    from .models import Classes , BaseWorks , Subjects , Works , Schedule , TokenBlocklist

    

    app.register_blueprint(auth)
    app.register_blueprint(classManager)
    app.register_blueprint(scheduleManager)
    app.register_blueprint(subjectsManager)
    app.register_blueprint(workManager)
    app.register_blueprint(baseworkManager)
    app.register_blueprint(interface)
    app.app_context().push()
    @app.route('/<path:path>')
    def catch_all(path):
        if path.startswith('interface'):
            return render_template("interface.html")
        if not path.startswith('api'):
            return render_template("index.html")
        
    return app