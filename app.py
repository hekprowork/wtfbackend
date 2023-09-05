from flask import Blueprint , Flask , request , jsonify
from .extensions import db


from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

from flask_jwt_extended import create_access_token ,  get_jwt , jwt_required , JWTManager , current_user
from datetime import timedelta , datetime , timezone


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wtfdb.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'eaisjkdaowefsj'
jwt = JWTManager(app)
ACCESS_EXPIRES = timedelta(days=30)
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES


migrate = Migrate(app, db)


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
    jti = jwt_payload["jti"]
    token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()

    return token is not None




@app.route('/login' , methods = ['POST'])
def login():
    data = request.get_json()
    class_name = data.get('username' , None)
    password = data.get('password' , None)
    #檢查帳號密碼
    the_class = Classes.query.filter_by(ClassName=class_name).first()
    if the_class:
        correct_password = the_class.Password == password
        if correct_password:
            access_token = create_access_token(identity=the_class.id)
            return jsonify({'access_token':access_token}) , 200
        else:
             return jsonify({'msg':'密碼錯誤'}) , 401
          
    else:
        return jsonify({'msg':'無此帳號'}) , 401

@app.route('/logout' , methods=['DELETE'])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    now = datetime.now(timezone.utc)
    db.session.add(TokenBlocklist(jti=jti, created_at=now))
    db.session.commit()
    return jsonify(msg="You have logout")
 
@app.route("/checklogin", methods=["GET"])
@jwt_required()
def protected():
    return jsonify({'msg':'you are logged in'})



def get_user_name_password(this_class):
    return [this_class.ClassName , this_class.Password]

@app.route('/get_users' , methods = ['GET'])
def get_users():
    
    users = list(map(get_user_name_password , Classes.query.all()))
    return jsonify({'all_user':users})

@app.route('/signup' , methods=['POST'])
def signup():
    data = request.get_json()
    new_class = Classes(data['username'] , data['password'] , data['pagename'])
    db.session.add(new_class)
    db.session.commit()
    access_token = create_access_token(identity=new_class.id)
    return jsonify({'access_token':access_token , 'msg':'login successfully'}) 


app.app_context().push()
db.create_all()

if __name__=='__main__':
    app.run(debug=True , port='5000')
