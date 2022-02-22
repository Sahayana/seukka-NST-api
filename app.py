from re import L
from flask import Flask
from flask_restx import Api, Resource
from service import nst_apply

app = Flask(__name__)
api = Api(app)

@api.route('/hello/<name>')
class Hello(Resource):
    def get(self, name):
        return {'hello': f'HiHi{name}'}








if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')