from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login


@login.user_loader
def load_user(id):
    return user.query.get(int(id))

association_table = db.Table('association', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'),index=True),
    db.Column('courses_id', db.Integer, db.ForeignKey('courses.id'),index=True)
)

class user(UserMixin, db.Model):
    __tablename__='user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    user_role=db.Column(db.String(20))
    courses_offered=db.relationship('courses',backref='taught_by',lazy='dynamic')
    has_courses=db.relationship(
        "courses",
        secondary=association_table,
        back_populates="has_students")
    def __repr__(self):
        return '<User {}>'.format(self.username)    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class courses(db.Model):
    __tablename__='courses'
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(64), index=True, unique=True)
    course_code = db.Column(db.String(64), index=True)
    course_description = db.Column(db.String(120))
    course_by_faculty = db.Column(db.Integer, db.ForeignKey('user.id'))
    has_students = db.relationship("user",
                    secondary=association_table,
                    back_populates="has_courses")
    def __repr__(self):
        return '<Course Code {} by {}>'.format(self.course_code,self.taught_by.username)


