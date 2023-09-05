from flask import Blueprint , jsonify , request
from .models import Classes
from .extensions import db
from flask_jwt_extended import jwt_required , get_jwt_identity

classManager = Blueprint('classManager' , __name__, url_prefix='/class')

@classManager.route('/' , methods=['GET'])
@jwt_required()
def class_info():
    the_class = Classes.query.filter_by(id = get_jwt_identity()).first()
    send_data = {
        'ClassName':the_class.ClassName,
        'PageName':the_class.PageName,
        'Remind':the_class.Remind,
    }
    return jsonify(send_data) , 200

@classManager.route('/' , methods=['PATCH'])
@jwt_required()
def class_patch():
    data = request.get_json()

    the_class = Classes.query.filter_by(id = get_jwt_identity()).first()

    if data.get('ClassName'):
        the_class.ClassName = data.get('ClassName')
    if data.get('Password'):
        the_class.Password = data.get('Password')
    if data.get('PageName'):
        the_class.PageName = data.get('PageName')
    if data.get('Remind'):
        the_class.Remind = data.get('Remind')
    
    db.session.commit()
    return jsonify({'msg':'change successfully'})