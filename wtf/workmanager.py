from flask import Blueprint , jsonify, request
from .models import Works , BaseWorks , Subjects
from .extensions import db
from flask_jwt_extended import jwt_required , get_jwt_identity
from datetime import date , datetime
workManager = Blueprint('workManager' , __name__ , url_prefix='/works')

@workManager.route('/<WorkOrExam>/' , methods=["GET"])
@jwt_required()
def get_work(WorkOrExam):
    
    WorkOrExam = True if WorkOrExam == "work" else False

    all_works = Works.query.filter(
        Works.Class_id == get_jwt_identity(),
        Works.WorkOrExam == WorkOrExam,
        ).order_by(Works.DueTime.desc())


    json_works = [[
        work.id,
        work.BaseWork.Subject.SubjectName,
        work.BaseWork.BaseWorkName,
        work.Range,
        work.DueTime.strftime("%Y-%m-%d"),
        ] for work in all_works]
    return jsonify({'works':json_works})


@workManager.route('/<int:id>/' , methods=['PATCH'])
@jwt_required()
def patch_work(id):

    class_id = get_jwt_identity()
    data = request.get_json()

    the_work = Works.query.filter(
        Works.id == id,
        Works.Class_id == class_id,
    ).first()

    if not the_work:
        return jsonify({"msg":"work not found"}) , 404


    if data.get("subjectName"):
        the_subject = Subjects.query.filter(
            Subjects.Class_id == class_id,
            Subjects.SubjectName == data.get("subjectName"),
        ).first()

        if not the_subject:
            the_subject = Subjects(class_id , data.get("subjectName"))
            db.session.add(the_subject)
            db.session.commit()

        the_baseWork = BaseWorks.query.filter(
            BaseWorks.Class_id == class_id,
            BaseWorks.Subject_id == the_subject.id,
            BaseWorks.BaseWorkName == data["baseWorkName"],
        ).first()

        if not the_baseWork:
            the_baseWork = BaseWorks(class_id , the_subject.id , data["baseWorkName"])
            db.session.add(the_baseWork)
            db.session.commit()

        the_work.BaseWork_id = the_baseWork.id

    if data.get("range"):
        the_work.Range = data.get("range")

    if data.get("DueTime"):
        the_work.DueTime = datetime.strptime(data['DueTime'] , "%Y-%m-%d").date()

    if data.get("WorkOrExam"):
        the_work.WorkOrExam = data.get("WorkOrExam")
    

    db.session.commit()
    
    return jsonify({"msg":"successfully"})


@workManager.route('/<WorkOrExam>/' , methods=['POST'])
@jwt_required()
def add_work(WorkOrExam):

    if WorkOrExam == "work":
        WorkOrExam = True
    else:
        WorkOrExam = False

    data = request.get_json()
    
    class_id = get_jwt_identity()

    the_Subject = Subjects.query.filter(
        Subjects.SubjectName == data["subject"],
        Subjects.Class_id == class_id,
    ).first()

    if not the_Subject:
        the_Subject = Subjects(class_id , data["subject"])
        db.session.add(the_Subject)
        db.session.commit()


    the_BaseWorks = BaseWorks.query.filter(
        BaseWorks.BaseWorkName == data["baseWorkName"],
        BaseWorks.Subject_id == the_Subject.id,
        BaseWorks.Class_id == class_id
    ).first()

    if not the_BaseWorks:
        the_BaseWorks = BaseWorks(class_id , the_Subject.id , data["baseWorkName"])
        db.session.add(the_BaseWorks)
        db.session.commit()
    
    new_work = Works(
        class_id, 
        the_BaseWorks.id, 
        data['range'], 
        datetime.strptime(data['DueTime'] , "%Y-%m-%d").date(),
        WorkOrExam,
    )
    
    db.session.add(new_work)
    db.session.commit()
    return jsonify({'id':new_work.id})


@workManager.route("/<int:id>/" , methods=["DELETE"])
@jwt_required()
def delete_work(id):
    class_id = get_jwt_identity()
    the_work = Works.query.filter(
        Works.id == id,
        Works.Class_id == class_id,
    ).first()

    if not the_work:
        return jsonify({"msg":"work not found"}) , 404

    db.session.delete(the_work)

    db.session.commit()

    return jsonify({"msg":"delete successfully"})