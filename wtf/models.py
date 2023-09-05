from .extensions import db
class Classes(db.Model):
    __tablename__ = 'Classes'
    id = db.Column(db.Integer , primary_key=True)
    ClassName = db.Column(db.String(20) , unique=True)
    Password = db.Column(db.String(255))
    PageName = db.Column(db.String(20))
    Remind = db.Column(db.String(255) , default='')
    admin = db.Column(db.Boolean , default=False)
    subject = db.relationship('Subjects' , backref = 'Class' , cascade='all , delete-orphan')
    basework = db.relationship('BaseWorks' , backref = 'Class' , cascade='all , delete-orphan')
    work = db.relationship('Works' , backref = 'Class' , cascade='all , delete-orphan')
    schedule = db.relationship('Schedule' , backref = 'Class' , cascade='all , delete-orphan')
    def __init__(self , ClassName , Password , PageName):
        self.ClassName = ClassName
        self.Password = Password
        self.PageName = PageName
class Subjects(db.Model):
    __tablename__ = 'Subjects'
    id = db.Column(db.Integer , primary_key=True)
    Class_id = db.Column(db.ForeignKey('Classes.id'))
    SubjectName = db.Column(db.String(20))
    Suggest = db.Column(db.Boolean)
    Schedule = db.relationship('Schedule' , backref = 'Subject')
    BaseWorks = db.relationship('BaseWorks' , backref = 'Subject')
    def __init__(self , Class_id , SubjectName):
        self.Class_id = Class_id
        self.SubjectName = SubjectName
        self.Suggest = True
 
class BaseWorks(db.Model):
    __tablename__ = 'BaseWorks'
    id = db.Column(db.Integer , primary_key=True)
    Class_id = db.Column(db.ForeignKey('Classes.id'))
    Subject_id = db.Column(db.ForeignKey('Subjects.id'))
    BaseWorkName = db.Column(db.String(20))
    Suggest = db.Column(db.Boolean)
    
    def __init__(self , Class_id , Subject_id , BaseWorkName):
        self.Class_id = Class_id
        self.Subject_id = Subject_id
        self.BaseWorkName = BaseWorkName
        self.Suggest = True

class Works(db.Model):
    __tablename__ = 'Works'
    id = db.Column(db.Integer , primary_key=True)
    Class_id = db.Column(db.ForeignKey('Classes.id'))
    BaseWork_id = db.Column(db.ForeignKey('BaseWorks.id'))
    Range = db.Column(db.String(20))
    DueTime = db.Column(db.Date)
    WorkOrExam = db.Column(db.Boolean)
    BaseWork = db.relationship('BaseWorks' , backref = 'Work')
    def __init__(self , Class_id , BaseWork_id , Range , DueTime , WorkOrExam):
        self.Class_id = Class_id
        self.BaseWork_id = BaseWork_id
        self.Range = Range
        self.DueTime = DueTime
        self.WorkOrExam = WorkOrExam


class Schedule(db.Model):
    __tablename__ = 'Schedule'
    id = db.Column(db.Integer , primary_key=True)
    Class_id = db.Column(db.ForeignKey('Classes.id'))
    Subject_id = db.Column(db.ForeignKey('Subjects.id'))
    
    def __init__(self , Class_id , Subject_id):
        self.Class_id = Class_id
        self.Subject_id = Subject_id

class TokenBlocklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, index=True)
    created_at = db.Column(db.DateTime, nullable=False)