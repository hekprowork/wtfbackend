from flask import Blueprint , jsonify , request
from flask_jwt_extended import jwt_required , get_jwt_identity
from .models import BaseWorks , Subjects
from .extensions import db
baseworkManager = Blueprint('baseworkManager' , __name__ , url_prefix='/basework')

@baseworkManager.route('/' , methods=['GET'])
@jwt_required()
def get_basework():
    all_baseworks = BaseWorks.query.filter(
        BaseWorks.Class_id == get_jwt_identity(),
        BaseWorks.Suggest == True,
    )
    json_baseworks = [[basework.id , basework.Subject.SubjectName , basework.BaseWorkName] for basework in all_baseworks]
    return jsonify({'msg':json_baseworks})

@baseworkManager.route('/' , methods=['POST'])
@jwt_required()
def put_basework():
    data = request.get_json()
    class_id = get_jwt_identity()

    if BaseWorks.query.filter_by(SubjectName = data["subjectName"]):
        return jsonify({'msg':'basework already exist'})
    
    the_subject = Subjects.query.filter(
        Subjects.Class_id == class_id,
        Subjects.SubjectName == data["subjectName"]
        ).first()
    
    if not the_subject:
        the_subject = Subjects(class_id , data["subjectName"])
        db.session.add(the_subject)
        db.session.commit()

    new_basework = BaseWorks(class_id , the_subject.id , data["baseworkName"])
    db.session.add(new_basework)
    db.session.commit()
    return jsonify({"id":new_basework.id})

@baseworkManager.route('/<int:basework_id>/' , methods=["DELETE"])
@jwt_required()
def delete_basework(basework_id):

    class_id = get_jwt_identity()
    data = request.get_json()

    the_basework = BaseWorks.query.filter(
        BaseWorks.id == basework_id,
        BaseWorks.Class_id == class_id
    ).first()

    if not the_basework:
        return jsonify({"msg":"the basework not found"})

    the_basework.Suggest = False
    db.session.commit()
    return jsonify({'msg':"change successfully"})


@baseworkManager.route('/<int:basework_id>/' , methods=["PATCH"])
@jwt_required()
def patch_basework(basework_id):
    class_id = get_jwt_identity()
    data = request.get_json()

    the_basework = BaseWorks.query.filter(
        BaseWorks.id == basework_id,
        BaseWorks.Class_id == class_id
    ).first()

    if not the_basework:
        return jsonify({"msg":"the basework not found"})

    if data.get('subjectName') and the_basework.Subject.SubjectName != data.get("subjectName"):
        the_subject = Subjects.query.filter(
        Subjects.Class_id == class_id,
        Subjects.SubjectName == data["subjectName"]
        ).first()

        if not the_subject:
            return jsonify({'msg':"subject not found"}) , 406

        the_basework.Subject_id = the_subject.id

    if data.get("basework_name") and data.get("basework_name") != the_basework.BaseWorkName:
        the_basework.BaseWorkName = data.get("basework_name")

    db.session.commit()
    return jsonify({'msg':"change successfully"})


    
    

    