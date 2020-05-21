from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from . import admin
from .forms import CourseForm, ClassesForm, StudentForm, Class_CoursesForm, FacultyForm, IAForm, PasswdForm
from .. import db
from ..models import Course, Classes, Faculty, Student, Class_Courses, IA_1, IA_2, IA_3


def check_admin():

    if not current_user.is_admin:
        abort(403)


def check_admin_or_classteacher():

    if not (current_user.is_admin or current_user.is_classteacher):
        abort(403)


# Faculty Views

@admin.route('/faculty', methods=['GET', 'POST'])
@login_required
def list_faculties():

    check_admin()

    faculties = Faculty.query.all()
    classdb = Classes.query.all()

    return render_template('admin/faculty/faculties_list.html',
                           faculties=faculties, classdb=classdb, title="Faculties")


@admin.route('/faculty/add', methods=['GET', 'POST'])
@login_required
def add_faculty():

    check_admin()

    add_faculty = True

    form = FacultyForm()
    if form.validate_on_submit():
        faculty = Faculty(id=form.id.data, first_name=form.first_name.data,
                          last_name=form.last_name.data,
                          email=form.email.data,
                          password=form.first_name.data
                          )
        try:
            # add faculty to the database
            db.session.add(faculty)
            db.session.commit()
            flash('successfully added a new faculty.')
        except:
            # in case faculty name already exists
            flash('Error: faculty name already exists.')

        return redirect(url_for('admin.list_faculties'))

    return render_template('admin/faculty/faculty.html', action="Add",
                           add_faculty=add_faculty, form=form,
                           title="Add faculty")


@admin.route('/faculty/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_faculty(id):

    check_admin()

    add_faculty = False

    faculty = Faculty.query.get_or_404(id)
    form = FacultyForm(obj=faculty)
    if form.validate_on_submit():
        try:
            faculty.id = form.id.data,
            faculty.first_name = form.first_name.data,
            faculty.last_name = form.last_name.data,
            faculty.email = form.email.data,
            faculty.password = form.first_name.data
            db.session.commit()
            flash('successfully edited {}.'.format(faculty.id))
        except:
            flash('Error: Faculty ID already exists. ')
            return redirect(url_for('admin.list_faculties'))

        return redirect(url_for('admin.list_faculties'))

    form.id.data = faculty.id
    form.first_name.data = faculty.first_name
    form.last_name.data = faculty.last_name
    form.email.data = faculty.email
    return render_template('admin/faculty/faculty.html', action="Edit",
                           add_faculty=add_faculty, form=form,
                           faculty=faculty, title="Edit faculty")


@admin.route('/faculty/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_faculty(id):

    check_admin()

    faculty = Faculty.query.get_or_404(id)
    name = faculty.first_name + faculty.last_name
    db.session.delete(faculty)
    db.session.commit()
    flash('successfully deleted {}.'.format(name))

    return redirect(url_for('admin.list_faculties'))

    return render_template(title="Delete faculty")


@admin.route('/faculty/change_password/<int:id>', methods=['GET', 'POST'])
@login_required
def passwd_faculty(id):

    faculty = Faculty.query.get_or_404(id)
    form = PasswdForm(obj=faculty)
    if form.validate_on_submit():
        try:
            passwd1 = form.passwd1.data
            passwd2 = form.passwd2.data
            passwd = form.passwd.data
            passwd_hash = generate_password_hash(passwd1)

            if str(passwd1) == str(passwd2):
                faculty.password_hash = passwd_hash
                db.session.commit()
                flash('{} changed password.'.format(faculty.id))
        except:
            flash('Try again.')
            return redirect(url_for('admin.passwd_faculty', id=id))

        return redirect(url_for('admin.passwd_faculty', id=id))

    return render_template('admin/passwd.html', action="passwd", form=form,
                           faculty=faculty, title="Change Password", id=id)


# course Views


@admin.route('/course', methods=['GET', 'POST'])
@login_required
def list_courses():

    check_admin()

    courses = Course.query.all()

    return render_template('admin/course/courses_list.html',
                           courses=courses, title="Courses")


@admin.route('/course/add', methods=['GET', 'POST'])
@login_required
def add_course():

    check_admin()

    add_course = True

    form = CourseForm()
    if form.validate_on_submit():
        course = Course(code=form.code.data,
                        title=form.title.data,
                        credit=form.credit.data,
                        scheme=form.scheme.data,
                        course_type=form.course_type.data
                        )
        try:

            db.session.add(course)
            db.session.commit()
            flash('successfully added a new course.')
        except:

            flash('Error: course name already exists.')

        return redirect(url_for('admin.list_courses'))

    return render_template('admin/course/course.html', action="Add",
                           add_course=add_course, form=form,
                           title="Add Course")


@admin.route('/course/edit/<string:id>', methods=['GET', 'POST'])
@login_required
def edit_course(id):

    check_admin()

    add_course = False

    course = Course.query.get_or_404(id)
    form = CourseForm(obj=course)
    if form.validate_on_submit():
        try:
            course.code = form.code.data,
            course.title = form.title.data,
            course.credit = form.credit.data,
            course.scheme = form.scheme.data,
            course.course_type = form.course_type.data
            db.session.commit()
            flash('successfully edited the course.')
        except:
            flash('Already exists')
            return redirect(url_for('admin.edit_course'))

        return redirect(url_for('admin.list_courses'))

    form.code.data = course.code
    form.title.data = course.title
    form.credit.data = course.credit
    form.scheme.data = course.scheme
    form.course_type.data = course.course_type
    return render_template('admin/course/course.html', action="Edit",
                           add_course=add_course, form=form,
                           course=course, title="Edit course")


@admin.route('/course/delete/<string:id>', methods=['GET', 'POST'])
@login_required
def delete_course(id):

    check_admin()

    course = Course.query.get_or_404(id)
    db.session.delete(course)
    db.session.commit()
    flash('successfully deleted the course.')

    return redirect(url_for('admin.list_courses'))

    return render_template(title="Delete course")


#######################################################
# Classes Views


@admin.route('/classes', methods=['GET', 'POST'])
@login_required
def list_classes():

    check_admin()

    classdb = Classes.query.all()
    for c in classdb:
        if c.faculty_id == c.faculty.id:
            c.faculty.is_classteacher = True
            db.session.commit()

    return render_template('admin/classes/classes_list.html',
                           classdb=classdb, title="Classes")


@admin.route('/classes/add', methods=['GET', 'POST'])
@login_required
def add_classes():

    check_admin()

    add_classes = True

    form = ClassesForm()
    if form.validate_on_submit():
        classes = Classes(id=form.class_id.data,
                          semester=form.semester.data,
                          section=form.section.data,
                          course_code=form.course_code.data,
                          faculty_id=form.faculty_id.data,
                          )
        try:

            db.session.add(classes)
            db.session.commit()
            classes.faculty.is_classteacher = True
            db.session.commit()
            flash('successfully added a new classes.')
        except:

            flash('Error: classes name already exists.')
            return redirect(url_for('admin.add'))

        return redirect(url_for('admin.list_classes'))

    return render_template('admin/classes/classes.html', action="Add",
                           add_classes=add_classes, form=form,
                           title="Add classes")


@admin.route('/classes/edit/<string:id>', methods=['GET', 'POST'])
@login_required
def edit_classes(id):

    check_admin()

    add_classes = False

    classes = Classes.query.get_or_404(id)
    classes.faculty.is_classteacher = False

    form = ClassesForm(obj=classes)
    if form.validate_on_submit():
        try:
            classes.id = form.class_id.data,
            classes.semester = form.semester.data,
            classes.section = form.section.data,
            classes.faculty_id = form.faculty_id.data,
            db.session.commit()
            flash('successfully edited the classes.')

            return redirect(url_for('admin.list_classes'))
        except:
            flash('already exists')
            return redirect(url_for('admin.list_classes'))

    form.class_id.data = classes.id
    form.semester.data = classes.semester
    form.section.data = classes.section
    form.faculty_id.data = classes.faculty_id
    return render_template('admin/classes/classes.html', action="Edit",
                           add_classes=add_classes, form=form,
                           classes=classes, title="Edit classes")


@admin.route('/classes/delete/<string:id>', methods=['GET', 'POST'])
@login_required
def delete_classes(id):

    check_admin()

    classes = Classes.query.get_or_404(id)
    classes.faculty.is_classteacher = False
    db.session.delete(classes)
    db.session.commit()
    flash('successfully deleted the classes.')

    return redirect(url_for('admin.list_classes'))

    return render_template(title="Delete classes")


#######################################################
# Class_Courses Views


@admin.route('/cc', methods=['GET', 'POST'])
@login_required
def list_cc():

    check_admin()

    cc = Class_Courses.query.all()

    return render_template('admin/cc/cc_list.html',
                           cc=cc, title="Class Courses")


@admin.route('/cc/add', methods=['GET', 'POST'])
@login_required
def add_cc():

    check_admin()

    add_cc = True

    form = Class_CoursesForm()
    if form.validate_on_submit():
        cc = Class_Courses(class_id=form.class_id.data,
                           course_code=form.course_code.data,
                           faculty_id=form.faculty_id.data,

                           )
        present = Class_Courses.query.filter_by(class_id=str(form.class_id.data), course_code=str(form.course_code.data)).first()

        try:

            if not present:

                db.session.add(cc)
                db.session.commit()
                flash('successfully added a new classes.')
            else:
                # in case classes name already exists
                flash('Error: course in class already exists.')
                return redirect(url_for('admin.add_cc'))
        except:
            # in case classes name already exists
            flash('Error: classes name already exists.')
            return redirect(url_for('admin.add_cc'))

        return redirect(url_for('admin.list_cc'))

    return render_template('admin/cc/cc.html', action="Add",
                           add_cc=add_cc, form=form,
                           title="Add class courses")


@admin.route('/cc/edit/<string:id>', methods=['GET', 'POST'])
@login_required
def edit_cc(id):

    check_admin()

    add_cc = False

    cc = Class_Courses.query.get_or_404(id)
    form = Class_CoursesForm(obj=cc)
    if form.validate_on_submit():
        try:
            cc.id = form.class_id.data,
            cc.course_code = form.course_code.data,
            cc.faculty_id = form.faculty_id.data,
            db.session.commit()
            flash('successfully edited the classes.')

            return redirect(url_for('admin.list_cc'))
        except:
            flash('already exists')
            return redirect(url_for('admin.list_cc'))

    form.class_id.data = cc.id
    form.faculty_id.data = cc.faculty_id
    form.course_code.data = cc.course_code
    return render_template('admin/cc/cc.html', action="Edit",
                           add_classes=add_cc, form=form,
                           classes=cc, title="Edit class courses")


@admin.route('/cc/delete/<string:id>', methods=['GET', 'POST'])
@login_required
def delete_cc(id):

    check_admin()

    cc = Class_Courses.query.get_or_404(id)
    db.session.delete(cc)
    db.session.commit()
    flash('successfully deleted the classes.')

    return redirect(url_for('admin.list_cc'))

    return render_template(title="Delete classes")


#*****************
# Student Views


@admin.route('/student', methods=['GET', 'POST'])
@login_required
def list_students():
    isct = current_user.is_classteacher

    check_admin_or_classteacher()

    students = Student.query.all()

    return render_template('admin/student/students_list.html',
                           students=students, isct=isct, title="students")


@admin.route('/student/add', methods=['GET', 'POST'])
@login_required
def add_student():

    check_admin_or_classteacher()

    add_student = True

    form = StudentForm()
    if form.validate_on_submit():
        student = Student(usn=form.usn.data,
                          first_name=form.first_name.data,
                          last_name=form.last_name.data,
                          email=form.email.data,
                          class_id=form.class_id.data
                          )
        try:

            db.session.add(student)
            db.session.commit()
            flash('{} {} is successfully added.'.format(student.first_name, student.last_name))
        except:

            flash('Error: student name already exists.')

        return redirect(url_for('admin.list_students'))

    return render_template('admin/student/student.html', action="Add",
                           add_student=add_student, form=form,
                           title="Add student")


@admin.route('/student/edit/<string:id>', methods=['GET', 'POST'])
@login_required
def edit_student(id):

    check_admin_or_classteacher()

    add_student = False

    student = Student.query.get_or_404(id)
    form = StudentForm(obj=student)
    if form.validate_on_submit():
        student.usn = form.usn.data,
        student.first_name = form.first_name.data,
        student.last_name = form.last_name.data,
        student.email = form.email.data,
        student.class_id = form.class_id.data
        db.session.commit()
        flash('{} {} is successfully edited.'.format(student.first_name, student.last_name))

        return redirect(url_for('admin.list_students'))

    form.usn.data = student.usn
    form.first_name.data = student.first_name
    form.last_name.data = student.last_name
    form.email.data = student.email
    form.class_id.data = student.class_id
    return render_template('admin/student/student.html', action="Edit",
                           add_student=add_student, form=form,
                           student=student, title="Edit student")


@admin.route('/student/delete/<string:id>', methods=['GET', 'POST'])
@login_required
def delete_student(id):

    check_admin_or_classteacher()

    student = Student.query.filter_by(usn=id).first()
    stu = student
    db.session.delete(student)
    db.session.commit()
    flash('{} {} is successfully deleted.'.format(stu.first_name, stu.last_name))

    return redirect(url_for('admin.list_students'))

    return render_template(title="Delete student")

#*****************
# IA Views


@admin.route('/ia', methods=['GET', 'POST'])
@login_required
def disp_ias():

    return render_template('home/ia/ia.html',
                           title="Internal Assessment")


@admin.route('/ia1', methods=['GET', 'POST'])
@login_required
def list_ias1():
    isadmin = current_user.is_admin
    isct = current_user.is_classteacher

    check_admin_or_classteacher()

    ias = IA_1.query.all()

    return render_template('home/ia/ia1.html',
                           ias=ias, isadmin=isadmin, isct=isct, title="IA 1")


@admin.route('/ia1/add', methods=['GET', 'POST'])
@login_required
def add_ia1():

    check_admin_or_classteacher()

    add_ia = True

    form = IAForm()
    if form.validate_on_submit():
        ia = IA_1(usn=form.usn.data,
                  cs51=form.cs51.data,
                  cs52=form.cs52.data,
                  cs53=form.cs53.data,
                  cs54=form.cs54.data,
                  cs553=form.cs553.data,
                  cs562=form.cs562.data
                  )
        try:

            db.session.add(ia)
            db.session.commit()
            flash('successfully added a new ia.')
        except:

            flash('Error: USN already exists or Invalid input')

        return redirect(url_for('admin.list_ias1'))

    return render_template('home/ia/ia_edit.html', action="Add",
                           add_ia=add_ia, form=form, admin=admin,
                           title="Add IA 1")


@admin.route('/ia1/edit/<string:id>', methods=['GET', 'POST'])
@login_required
def edit_ia1(id):

    check_admin_or_classteacher()

    add_ia = False

    ia = IA_1.query.get_or_404(id)
    form = IAForm(obj=ia)
    if form.validate_on_submit():
        try:
            ia.usn = form.usn.data,
            ia.cs51 = form.cs51.data,
            ia.cs52 = form.cs51.data,
            ia.cs53 = form.cs51.data,
            ia.cs54 = form.cs51.data,
            ia.cs553 = form.cs51.data,
            ia.cs562 = form.cs51.data,
            db.session.commit()

            flash('{} successfully edited.'.format(ia.usn))

        except:
            flash('Error: USN already exists or Invalid input')
            return redirect(url_for('admin.list_ias1'))

        return redirect(url_for('admin.list_ias1'))

    form.usn.data = ia.usn
    form.cs51.data = ia.cs51
    form.cs52.data = ia.cs52
    form.cs53.data = ia.cs53
    form.cs54.data = ia.cs54
    form.cs553.data = ia.cs553
    form.cs562.data = ia.cs562
    return render_template('home/ia/ia_edit.html', action="Edit",
                           add_ia=add_ia, form=form,
                           ia=ia, title="Edit IA 1")


@admin.route('/ia1/delete/<string:id>', methods=['GET', 'POST'])
@login_required
def delete_ia1(id):

    check_admin_or_classteacher()

    ia = IA_1.query.get_or_404(id)
    usn = ia.usn
    db.session.delete(ia)
    db.session.commit()
    flash('Successfully deleted {} marks.'.format(usn))

    return redirect(url_for('admin.list_ias1'))

    return render_template(title="Delete IA 1")


#*****************
# IA2 Views


@admin.route('/ia2', methods=['GET', 'POST'])
@login_required
def list_ias2():
    isadmin = current_user.is_admin
    isct = current_user.is_classteacher

    check_admin_or_classteacher()

    ias = IA_2.query.all()

    return render_template('home/ia/ia2.html',
                           ias=ias, isadmin=isadmin, isct=isct, title="IA 2")


@admin.route('/ia2/add', methods=['GET', 'POST'])
@login_required
def add_ia2():

    check_admin_or_classteacher()

    add_ia = True

    form = IAForm()
    if form.validate_on_submit():
        ia = IA_2(usn=form.usn.data,
                  cs51=form.cs51.data,
                  cs52=form.cs52.data,
                  cs53=form.cs53.data,
                  cs54=form.cs54.data,
                  cs553=form.cs553.data,
                  cs562=form.cs562.data
                  )
        try:

            db.session.add(ia)
            db.session.commit()
            flash('{} successfully added'.format(ia.usn))
        except:
            # in case ia name already exists
            flash('Error: USN already exists')

        return redirect(url_for('admin.list_ias2'))

    # load ia template
    return render_template('home/ia/ia_edit.html', action="Add",
                           add_ia=add_ia, form=form, admin=admin,
                           title="Add IA 2")


@admin.route('/ia2/edit/<string:id>', methods=['GET', 'POST'])
@login_required
def edit_ia2(id):

    check_admin_or_classteacher()

    add_ia = False

    ia = IA_2.query.get_or_404(id)
    form = IAForm(obj=ia)
    if form.validate_on_submit():
        try:
            ia.usn = form.usn.data,
            ia.cs51 = form.cs51.data,
            ia.cs52 = form.cs51.data,
            ia.cs53 = form.cs51.data,
            ia.cs54 = form.cs51.data,
            ia.cs553 = form.cs51.data,
            ia.cs562 = form.cs51.data,
            db.session.commit()
            flash('{} successfully edited.'.format(ia.usn))
            return redirect(url_for('admin.list_ias2'))

        except:
            flash('Error: USN already exists or Invalid input')
            return redirect(url_for('admin.list_ias2'))

        return redirect(url_for('admin.list_ias2'))

    form.usn.data = ia.usn
    form.cs51.data = ia.cs51
    form.cs52.data = ia.cs52
    form.cs53.data = ia.cs53
    form.cs54.data = ia.cs54
    form.cs553.data = ia.cs553
    form.cs562.data = ia.cs562
    return render_template('home/ia/ia_edit.html', action="Edit",
                           add_ia=add_ia, form=form,
                           ia=ia, title="Edit IA 2")


@admin.route('/ia2/delete/<string:id>', methods=['GET', 'POST'])
@login_required
def delete_ia2(id):

    check_admin_or_classteacher()

    ia = IA_2.query.get_or_404(id)
    usn = ia.usn
    db.session.delete(ia)
    db.session.commit()
    flash('Successfully deleted {} marks.'.format(usn))

    # redirect to the departments page
    return redirect(url_for('admin.list_ias2'))

    return render_template(title="Delete IA 2")


#*****************
# IA 3 Views


@admin.route('/ia3', methods=['GET', 'POST'])
@login_required
def list_ias3():
    isadmin = current_user.is_admin
    isct = current_user.is_classteacher

    check_admin_or_classteacher()

    ias = IA_3.query.all()

    return render_template('home/ia/ia3.html',
                           ias=ias, isadmin=isadmin, isct=isct, title="IA 3")


@admin.route('/ia3/add', methods=['GET', 'POST'])
@login_required
def add_ia3():

    check_admin_or_classteacher()

    add_ia = True

    form = IAForm()
    if form.validate_on_submit():
        ia = IA_3(usn=form.usn.data,
                  cs51=form.cs51.data,
                  cs52=form.cs52.data,
                  cs53=form.cs53.data,
                  cs54=form.cs54.data,
                  cs553=form.cs553.data,
                  cs562=form.cs562.data
                  )
        try:
            # add ia to the database
            db.session.add(ia)
            db.session.commit()
            flash('{} successfully added'.format(ia.usn))
        except:
            # in case ia name already exists
            flash('Error: USN already exists or Invalid input')

        return redirect(url_for('admin.list_ias3'))

    # load ia template
    return render_template('home/ia/ia_edit.html', action="Add",
                           add_ia=add_ia, form=form, admin=admin,
                           title="Add IA 3")


@admin.route('/ia3/edit/<string:id>', methods=['GET', 'POST'])
@login_required
def edit_ia3(id):

    check_admin_or_classteacher()

    add_ia = False

    ia = IA_3.query.get_or_404(id)
    form = IAForm(obj=ia)
    if form.validate_on_submit():
        try:
            ia.usn = form.usn.data,
            ia.cs51 = form.cs51.data,
            ia.cs52 = form.cs51.data,
            ia.cs53 = form.cs51.data,
            ia.cs54 = form.cs51.data,
            ia.cs553 = form.cs51.data,
            ia.cs562 = form.cs51.data,
            db.session.commit()
            flash('{} successfully edited.'.format(ia.usn))
            return redirect(url_for('admin.list_ias3'))

        except:
            flash('Error: USN already exists or Invalid input')
            return redirect(url_for('admin.list_ias3'))

        return redirect(url_for('admin.list_ias3'))

    form.usn.data = ia.usn
    form.cs51.data = ia.cs51
    form.cs52.data = ia.cs52
    form.cs53.data = ia.cs53
    form.cs54.data = ia.cs54
    form.cs553.data = ia.cs553
    form.cs562.data = ia.cs562
    return render_template('home/ia/ia_edit.html', action="Edit",
                           add_ia=add_ia, form=form,
                           ia=ia, title="Edit IA 3")


@admin.route('/ia3/delete/<string:id>', methods=['GET', 'POST'])
@login_required
def delete_ia3(id):

    check_admin_or_classteacher()

    ia = IA_3.query.get_or_404(id)
    usn = ia.usn
    db.session.delete(ia)
    db.session.commit()
    flash('Successfully deleted {} marks.'.format(usn))

    return redirect(url_for('admin.list_ias3'))

    return render_template(title="Delete IA 3")
