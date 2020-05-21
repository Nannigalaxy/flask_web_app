from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, validators, PasswordField, ValidationError
from wtforms.validators import DataRequired, Email
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from ..models import Course, Classes, Faculty, Class_Courses, Student
import re


class FacultyForm(FlaskForm):
    id = IntegerField('Faculty ID', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])

    def validate_first_name(form, field):
        if re.search("[0-9][0-9]*", field.data):
            raise ValidationError("Numbers and Special character not allowed")
    last_name = StringField('Last Name')

    def validate_last_name(form, field):
        if re.search("[0-9][0-9]*", field.data):
            raise ValidationError("Numbers and Special character not allowed")
    email = StringField('Email', validators=[DataRequired(), Email()])

    submit = SubmitField('Submit')


class CourseForm(FlaskForm):
    """
    Form for admin to add or edit a department
    """

    code = StringField('Code', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    credit = IntegerField('Credit', [validators.NumberRange(min=2, max=4)])
    scheme = IntegerField('Scheme', validators=[DataRequired()])
    course_type = StringField('Course Type', validators=[DataRequired()])
    submit = SubmitField('Submit')


class ClassesForm(FlaskForm):
    """
    Form for admin to add or edit a department
    """
    class_id = IntegerField('Class ID', validators=[DataRequired()])
    semester = IntegerField('Semester', validators=[DataRequired()])
    section = StringField('Section', validators=[DataRequired()])
    faculty_id = QuerySelectField('Faculty', query_factory=lambda: Faculty.query.all(),
                                  )
    submit = SubmitField('Submit')


class Class_CoursesForm(FlaskForm):
    """
    Form for admin to add or edit a department
    """
    class_id = QuerySelectField('Class ID', query_factory=lambda: Classes.query.all())
    course_code = QuerySelectField('Course code', query_factory=lambda: Course.query.all(), get_label='code')
    faculty_id = QuerySelectField('Faculty ID', query_factory=lambda: Faculty.query.all())
    submit = SubmitField('Submit')


class StudentForm(FlaskForm):
    """
    Form for admin to add or edit a department
    """
    usn = StringField('USN', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])

    def validate_first_name(form, field):
        if re.search("[0-9][0-9]*", field.data):
            raise ValidationError("Numbers and Special character not allowed")

    last_name = StringField('Last Name')

    def validate_last_name(form, field):
        if re.search("[0-9][0-9]*", field.data):
            raise ValidationError("Numbers and Special character not allowed")

    email = StringField('Email', validators=[DataRequired(), Email()])
    class_id = QuerySelectField(query_factory=lambda: Classes.query.all(),
                                get_label="id")

    submit = SubmitField('Submit')


class IAForm(FlaskForm):
    """
    Form for admin to add or edit a department
    """
    min = 0
    max = 30
    usn = QuerySelectField('USN', query_factory=lambda: Student.query.all(),
                           get_label="usn")
    cs51 = IntegerField('17CS51', validators=[DataRequired()])
    cs52 = IntegerField('17CS52', [validators.NumberRange(min=min, max=max)])
    cs53 = IntegerField('17CS53', [validators.NumberRange(min=min, max=max)])
    cs54 = IntegerField('17CS54', [validators.NumberRange(min=min, max=max)])
    cs553 = IntegerField('17CS553', [validators.NumberRange(min=min, max=max)])
    cs562 = IntegerField('17CS562', [validators.NumberRange(min=min, max=max)])

    submit = SubmitField('Submit')


class PasswdForm(FlaskForm):
    passwd = StringField('Current password', validators=[DataRequired()])
    passwd1 = StringField('New password', validators=[DataRequired()])
    passwd2 = StringField('New password again', validators=[DataRequired()])

    def validate_passwd2(form, field):
        if re.search(passwd1, field.data):
            raise ValidationError("Numbers and Special character not allowed")
    submit = SubmitField('Submit')
