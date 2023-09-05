from flask import Blueprint , request , jsonify
from flask_jwt_extended import jwt_required , get_jwt_identity
from .models import Schedule , Subjects
from .extensions import db
scheduleManager = Blueprint('scheduleManager' , __name__ , url_prefix='/schedule')

@scheduleManager.route('/' , methods=['GET'])
@jwt_required()
def schedule_view():
    users_schedule = Schedule.query.filter_by(Class_id=get_jwt_identity())
    json_schedule = list(map(lambda schedule:schedule.Subject.SubjectName , users_schedule))
    return jsonify({'schedules':json_schedule})


def checkSubjectExist(subject_name):
    the_subject = Subjects.query.filter_by(SubjectName=subject_name).first()
    if the_subject:
        return the_subject.id
    return False

@scheduleManager.route('/' , methods=['PUT'])
@jwt_required()
def schedule_patch():
    data = request.get_json()
    users_schedule = Schedule.query.filter_by(Class_id=get_jwt_identity())

    for i , grid in data.items():
        if grid == '':
            users_schedule[int(i)].Subject_id = Subjects.query.first().id
            print(users_schedule)
            continue

        original_subject = users_schedule[int(i)].Subject
        existing = checkSubjectExist(grid)
        #如果Subject與原本一樣：
        if existing == original_subject.id:
            continue
        #Subject不存在：
        elif existing:
            users_schedule[int(i)].Subject_id = existing
        #不存在：
        else:
            new_subject = Subjects(get_jwt_identity() , grid)
            db.session.add(new_subject)
            db.session.commit()
            users_schedule[int(i)].Subject_id = new_subject.id 
    db.session.commit()
    
    for subject in Subjects.query.filter_by(Class_id = get_jwt_identity())[1:]:
        if not subject.Schedule and not subject.BaseWorks:
            db.session.delete(subject)
    db.session.commit()
    return jsonify({'schedules':'update successfully'})
