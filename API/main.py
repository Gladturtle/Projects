import requests
from flask import Flask, render_template,make_response,send_file,abort,request,redirect
from flask_restful import Api,Resource,fields,reqparse,marshal_with,marshal
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text,engine
from functools import wraps
import datetime
import jwt
import io

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'bacaa3381e4c453088449ccd04f270cf'
db = SQLAlchemy(app)
add = '192.168.15.69'


image_put_img = reqparse.RequestParser()
image_put_img.add_argument('img',type = str,required = True,help = 'Path of the image')

class ImageModel(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    img = db.Column(db.BLOB,primary_key = False)
class UserModel(db.Model):
    usname = db.Column(db.String,primary_key = True)
    password = db.Column(db.String)
    perm = db.Column(db.String)
class LoginAttempts(db.Model):
    usname = db.Column(db.String,primary_key = True)
    attempts = db.Column(db.Integer)
    time = db.Column(db.String)

resource_field_img = {'img':fields.Raw}
resource_field_user = {'usname':fields.String,'password':fields.String,'perm':fields.String}


def token_required(func):
    @wraps(func)
    def decorated(*args,**kwargs):
        resmethods = [Image.delete,Image.put,Signup.get,Signup.post]
        token = request.args.get('token')
        if not token:
            abort(400,'No token found')
        try:
            token = jwt.decode(token,key =app.config['SECRET_KEY'],algorithms=['HS256'])
        except:
            abort(400,'Invalid token')
        print(token['expiration'])
        if datetime.datetime.strptime(token['expiration'], '%Y-%m-%d %H:%M:%S.%f%z') < datetime.datetime.now(datetime.UTC):
            abort(400,'Token Expired. Please log-in again')
        if token['user']['perm'] == "N":
            for method in resmethods:
                if func.__name__ == method.__name__ and func.__module__ == method.__module__:
                    abort(401,'You do not have the authority to do this. This could stem from the fact that your parents abandoned you when you were 3')
        return func(*args,**kwargs)
    return decorated
    


class Image(Resource):
    @token_required
    def get(self,id):
        image = ImageModel.query.get(id)
        image_data = image.img
        return send_file(io.BytesIO(image_data),mimetype='image/jpg',as_attachment=False,download_name='image.jpg')
    @token_required
    @marshal_with(resource_field_img)
    def put(self,id):
        try:
            id = db.session.query(ImageModel.id).order_by(ImageModel.id.desc()).first()[0]+1
        except:
            id = 1
        args = image_put_img.parse_args()
        image = args['img']
        image = open(image, 'rb').read()
        img = ImageModel(id = id, img = image)
        db.session.add(img)
        db.session.commit()
        return '',201
    @token_required
    def delete(self,id):
        img = ImageModel.query.get(id)
        if not img:
            abort(404,'Bruh no index like that')
        db.session.delete(img)
        db.session.commit()
        return '',200
class Images(Resource):
    @token_required
    def get(self):
        headers = {'Content-Type':'text/html'}
        token = request.args.get('token')
        id = db.session.query(ImageModel.id).order_by(ImageModel.id.desc()).first()[0]+1
        list_of_req = []
        for i in range(1,id):
            list_of_req.append('http://'+add+':5000/image/'+str(i)+'/?token='+token)
            requests.get('http://'+add+':5000/image/'+str(i)+'/?token='+token)
        return make_response(render_template('images.html', img = list_of_req),200,headers)




class Login(Resource):
    def get(self):
        headers = {'Content-Type':'text/html'}
        return make_response(render_template('login.html',results = 'login.form'),200,headers)
    def post(self):
        usname = request.form.get('username')
        password = request.form.get('password')
        user = UserModel.query.get(usname)
        if not user:
            abort(400,"No such user")
        if user.usname==usname and user.password==password:
            time = datetime.datetime.now(datetime.UTC)+datetime.timedelta(hours=2)
            login = LoginAttempts.query.get(usname)
            login.attempts = 0
            db.session.commit()
            token = jwt.encode({'user':marshal(user,resource_field_user),
                                'expiration':str(time)},
                                app.config['SECRET_KEY'])
            return {"token":token}
        elif user.usname==usname and user.password!=password:
            user = LoginAttempts.query.get(usname)
            user.attempts +=1
            db.session.commit()
            return redirect('http://'+add+':5000/login',302)

               
class Signup(Resource):
    @token_required
    def get(self):
        token = request.args.get('token')
        headers = {'Content-Type':'text/html'}
        return make_response(render_template('signup.html',results = 'signup.form',token = token),200,headers)
    @token_required
    def post(self):
        usname = request.form.get('username')
        password = request.form.get('password')
        perm = request.form.get('perm')
        if perm not in ['N','A']:
            abort(422,'Not a valid input')
        user = UserModel.query.get(usname)
        if user:
            abort(409,'User already exists')
        user = UserModel(usname = usname,password = password,perm = perm)
        login = LoginAttempts(usname=usname,attempts = 0)
        db.session.add(user)
        db.session.add(login)
        db.session.commit()
        return {'message':'New user has been added'},201
         
        
api.add_resource(Image,"/image/<int:id>/")
api.add_resource(Images,'/all-images/')
api.add_resource(Login,"/login" )
api.add_resource(Signup,"/signup/")

if __name__ == "__main__":
    app.run(debug = True,host= add)
