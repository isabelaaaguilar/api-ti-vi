from flask import Flask, Blueprint
from flask_restx import Api
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix

from app.main.pessoa.pessoa_controller import api as home_ns

app = Flask(__name__)
CORS(app)
app.wsgi_app = ProxyFix(app.wsgi_app)
blueprint = Blueprint('api', __name__)
app.register_blueprint(blueprint)

api = Api(app, title='Api Flask Expieriments', version='1.0', description='Api',prefix='/api')
#adicionado namespace pessoa para rotas
api.add_namespace(home_ns, path='/pessoa')