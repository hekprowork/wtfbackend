from flask import Blueprint , jsonify
from .models import Subjects
from .extensions import db
from flask_jwt_extended import jwt_required , get_jwt_identity
subjectsManager = Blueprint('subjectsManager' , __name__ , url_prefix='/subjects')

@subjectsManager.route('/' , methods=['GET'])
@jwt_required()
def get_subjects():
    all_subjects = Subjects.query.filter(
        Subjects.Class_id == get_jwt_identity(),
        Subjects.Suggest == True,
    ).all()
    json_subjects = [[subject.id , subject.SubjectName] for subject in all_subjects[1:]]
    print(json_subjects)
    return jsonify({'msg':json_subjects})

@subjectsManager.route('/<int:id>/' , methods=['DELETE'])
@jwt_required()
def delete_subject(id):
    the_subject = Subjects.query.filter(
        Subjects.id == id,
        Subjects.Class_id == get_jwt_identity()
    ).first()
    if not the_subject:
        return jsonify({'msg':'Subject Not Found'}) , 404
    
    the_subject.Suggest = False
    
    db.session.commit()

    return jsonify({'msg':'turn off auto suggest'})
    