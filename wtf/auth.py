from flask import Blueprint , request , jsonify
from .models import Classes , TokenBlocklist , Schedule , Subjects
from flask_jwt_extended import create_access_token , get_jwt , jwt_required , get_jwt_identity
from datetime import datetime , timezone

from .extensions import db

auth = Blueprint('auth' , __name__)

@auth.route('/login' , methods = ['POST'])
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
            return jsonify({'access_token':access_token , "username":the_class.ClassName})
        else:
            return jsonify({'msg':'帳號或密碼錯誤'}) , 401
          
    else:
        return jsonify({'msg':'帳號或密碼錯誤'}) , 401

@auth.route('/logout' , methods=['DELETE'])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    now = datetime.now(timezone.utc)
    db.session.add(TokenBlocklist(jti=jti, created_at=now))
    db.session.commit()
    return jsonify(msg="You have logout")
 
@auth.route("/checklogin", methods=["GET"])
@jwt_required()
def protected():
    username = Classes.query.filter_by(id = get_jwt_identity()).first().ClassName
    return jsonify({'username':username})


@auth.route('/signup' , methods=['POST'])
def signup():
    data = request.get_json()

    new_class = Classes(data['username'] , data['password'] , data['pagename'])
    db.session.add(new_class)
    db.session.commit()
    
    meta_subject = Subjects(new_class.id , '無科目')
    db.session.add(meta_subject)
    db.session.commit()

    for i in range(45):
        db.session.add(Schedule(new_class.id , meta_subject.id))
    db.session.commit()
    
    access_token = create_access_token(identity=new_class.id)
    return jsonify({'access_token':access_token , 'msg':'login successfully'}) 
