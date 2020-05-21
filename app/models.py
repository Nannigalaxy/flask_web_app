# app/models.py

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager


class Faculty(UserMixin, db.Model):

    __tablename__ = 'faculty'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    email = db.Column(db.String(60), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    is_classteacher = db.Column(db.Boolean, default=False)

    classes = db.relationship('Classes', backref='faculty',
                              lazy='dynamic')
    class_courses = db.relationship('Class_Courses', backref='faculty', lazy='dynamic')

    @property
    def password(self):

        raise AttributeError('Password is not a readable attribute.')

    @password.setter
    def password(self, password):

        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):

        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '{}'.format(self.id)


@login_manager.user_loader
def load_user(user_id):

    return Faculty.query.get(int(user_id))


class Course(db.Model):

    __tablename__ = 'course'
    __table_args__ = {'extend_existing': True}

    code = db.Column(db.String(20), primary_key=True, autoincrement=False)
    title = db.Column(db.String(60), unique=True)
    credit = db.Column(db.Integer)
    scheme = db.Column(db.Integer)
    course_type = db.Column(db.String(20))
    class_courses = db.relationship('Class_Courses', backref='course', lazy='dynamic')

    def __repr__(self):
        return '{}'.format(self.code)


class Classes(db.Model):

    __tablename__ = 'classes'

    id = db.Column(db.String(10), unique=False, primary_key=True)
    semester = db.Column(db.Integer)
    section = db.Column(db.String(2))

    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id', onupdate="cascade"))

    students = db.relationship('Student', backref='classes',
                               lazy='dynamic')
    class_courses = db.relationship('Class_Courses', backref='classes', lazy='dynamic')

    def __repr__(self):
        return '{}'.format(self.id)


class Class_Courses(db.Model):
    __tablename__ = 'class_courses'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    class_id = db.Column(db.String(10), db.ForeignKey('classes.id', onupdate="cascade"))
    course_code = db.Column(db.String(10), db.ForeignKey('course.code', onupdate="cascade"))
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id', onupdate="cascade"))

    def __repr__(self):
        return '{}'.format(self.id)


class Student(db.Model):

    __tablename__ = 'student'

    usn = db.Column(db.String(20), primary_key=True, index=True, autoincrement=False)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    email = db.Column(db.String(60), index=True, unique=True)
    class_id = db.Column(db.String(10), db.ForeignKey('classes.id', onupdate="cascade"))

    ia_1 = db.relationship('IA_1', cascade='all,delete,delete-orphan', single_parent=True, backref=db.backref('student'),
                           lazy='dynamic')
    ia_2 = db.relationship('IA_2', cascade='all,delete,delete-orphan', single_parent=True, backref=db.backref('student'),
                           lazy='dynamic')
    ia_3 = db.relationship('IA_3', cascade='all,delete,delete-orphan', single_parent=True, backref=db.backref('student'),
                           lazy='dynamic')

    def __repr__(self):
        return '{}'.format(self.usn)


class IA_1(UserMixin, db.Model):
    __tablename__ = 'ia_1'

    usn = db.Column(db.String(10), db.ForeignKey('student.usn', onupdate="cascade"), primary_key=True)
    cs51 = db.Column(db.Integer)
    cs52 = db.Column(db.Integer)
    cs53 = db.Column(db.Integer)
    cs54 = db.Column(db.Integer)
    cs553 = db.Column(db.Integer)
    cs562 = db.Column(db.Integer)


class IA_2(db.Model):
    __tablename__ = 'ia_2'

    usn = db.Column(db.String(10), db.ForeignKey('student.usn', onupdate="cascade"), primary_key=True)
    cs51 = db.Column(db.Integer)
    cs52 = db.Column(db.Integer)
    cs53 = db.Column(db.Integer)
    cs54 = db.Column(db.Integer)
    cs553 = db.Column(db.Integer)
    cs562 = db.Column(db.Integer)


class IA_3(db.Model):
    __tablename__ = 'ia_3'

    usn = db.Column(db.String(10), db.ForeignKey('student.usn', onupdate="cascade"), primary_key=True)
    cs51 = db.Column(db.Integer)
    cs52 = db.Column(db.Integer)
    cs53 = db.Column(db.Integer)
    cs54 = db.Column(db.Integer)
    cs553 = db.Column(db.Integer)
    cs562 = db.Column(db.Integer)
