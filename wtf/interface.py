from flask import Blueprint , jsonify , render_template
from .models import Classes , Works , Schedule , BaseWorks , Subjects
from datetime import date

interface = Blueprint('interface' , '__name__' , url_prefix='/api/interface')



@interface.route("/<className>/")
def summarize(className):
    the_class = Classes.query.filter_by(ClassName = className).first()
    if not the_class:
        return jsonify({'msg':"class to found"})
    
    schedules = Schedule.query.filter_by(Class_id = the_class.id).all()
    json_schedules = ["" if schedule.Subject.SubjectName == "無科目" else schedule.Subject.SubjectName for schedule in schedules]

    today = date.today()

    works = Works.query.filter(
        Works.Class_id == the_class.id,
        Works.DueTime >= today,
    )\
    .join(Works.BaseWork) \
    .join(BaseWorks.Subject) \
    .order_by(Works.DueTime.asc() , Subjects.id)

    json_works = [{
        "subject":work.BaseWork.Subject.SubjectName,
        "baseWork":work.BaseWork.BaseWorkName,
        "range":work.Range,
        "time_limit":work.DueTime.strftime("%Y-%m-%d"),
        "WorkOrExam":work.WorkOrExam,
    } for work in works]


    body = {
        "username": the_class.ClassName, 
        "remind": the_class.Remind,
        "title": the_class.PageName,
        "url": f"/{the_class.ClassName}/",
        "schedules": json_schedules,
        "works": json_works,
    }

    return jsonify(body)