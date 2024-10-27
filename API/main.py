import requests
from flask import Flask, render_template,make_response,send_file,abort
from flask_restful import Api,Resource,fields,reqparse,marshal_with
from flask_sqlalchemy import SQLAlchemy
import random
import io

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

image_put_img = reqparse.RequestParser()
image_put_img.add_argument('img',type = str,required = True,help = 'Path of the image')

class ImageModel(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    img = db.Column(db.BLOB,primary_key = False)

resource_field = {'img':fields.Raw}
app.app_context().push()
db.create_all()

class Image(Resource):
    def get(self,id):
        image = ImageModel.query.get(id)
        image_data = image.img
        return send_file(io.BytesIO(image_data),mimetype='image/jpg',as_attachment=False,download_name='image.jpg')
    @marshal_with(resource_field)
    def put(self,id):
        try:
            id = db.session.query(ImageModel.id).order_by(ImageModel.id.desc()).first()[0]+1
        except:
            id = 0
        args = image_put_img.parse_args()
        image = args['img']
        image = open(image, 'rb').read()
        img = ImageModel(id = id, img = image)
        db.session.add(img)
        db.session.commit()
        return '',201
    def delete(self,id):
        img = ImageModel.query.get(id)
        if not img:
            abort(404,'Bruh no index like that')
        db.session.delete(img)
        db.session.commit()
        return '',200


        


class Images(Resource):
    def get(self):
        headers = {'Content-Type':'text/html'}
        id = db.session.query(ImageModel.id).order_by(ImageModel.id.desc()).first()[0]+1
        list_of_req = []
        for i in range(0,id):
            list_of_req.append('http://127.0.0.1:5000/image/'+str(i))
            requests.get('http://127.0.0.1:5000/image/'+str(i))
        print(list_of_req)
        return make_response(render_template('images.html', img = list_of_req),200,headers)




api.add_resource(Image,"/image/<int:id>")
api.add_resource(Images,'/all-images')
if __name__ == "__main__":
    app.run(debug=True)
