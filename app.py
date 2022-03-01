from re import L
from flask import Flask
from flask_restx import Api, Resource
from service import nst_apply
from werkzeug.datastructures import FileStorage


app = Flask(__name__)
api = Api(app)

#swagger에 파일 업로드 하는 부분
upload_parser = api.parser()
upload_parser.add_argument('file', location='files',type=FileStorage, required=True)

@api.route('/hello/<name>&<style>')
@api.expect(upload_parser)
class Hello(Resource):
    def post(self, name, style):
        args = upload_parser.parse_args()
        uploaded_file = args['file']  # This is FileStorage instance
        url = nst_apply(name, uploaded_file, style)
        return {'hello': f'{url}'}







if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')