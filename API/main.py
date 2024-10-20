import PIL.Image
from flask import Flask, render_template,make_response
from flask_restful import Api,Resource,fields
from flask_sqlalchemy import SQLAlchemy
import os,random,PIL

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class ImageModel(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    img = db.Column(db.BLOB,primary_key = False)

resource_field = {'img':fields.Raw}
app.app_context().push()
db.create_all()

class Image(Resource):
    def get(self):
        headers = {'Content-Type':'text/html'}
        list_of_dir = os.listdir('.\\static')
        img_name = list_of_dir[random.randint(0,len(list_of_dir)-1)]
        return make_response(render_template('image.html', img = '.\\static\\'+img_name),200,headers)
    def post(self):
        list_of_dir = os.listdir('.\\static')
        i = 0
        for image in list_of_dir:
            img = PIL.Image.open('.\\static\\'+image)
            image = ImageModel(id =i, img=img)
            db.session.add(image)
            db.session.commit()
            return '',201


        


class Images(Resource):
    def get(self):
        headers = {'Content-Type':'text/html'}
        list_of_dir = os.listdir('.\\static')
        for i in range(0,len(list_of_dir)):
            list_of_dir[i] = '.\\static\\'+list_of_dir[i]
        return make_response(render_template('images.html', img = list_of_dir),200,headers)





api.add_resource(Image,"/random_image")
api.add_resource(Images,'/all-images')
if __name__ == "__main__":
    app.run(debug=True)
