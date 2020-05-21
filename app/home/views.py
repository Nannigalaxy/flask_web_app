from flask import abort, render_template, request
from flask_login import current_user, login_required
from ..models import Course, Classes, Faculty, Student, Class_Courses, IA_1, IA_2, IA_3
from . import home
from bokeh.palettes import OrRd6
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, FactorRange
from bokeh.palettes import Spectral6
from bokeh.transform import dodge
from bokeh.io import show, output_notebook
import numpy as np


@home.route('/')
def homepage():


    return render_template('home/index.html', title="Welcome")


@home.route('/dashboard')
@login_required
def dashboard():
    """
    Render the dashboard template on the /dashboard route
    """
    features=["Average", "Range"]
    ia_table = [IA_1,IA_2,IA_3]
    course = ["17CS51", "17CS52", "17CS53", "17CS54", "17CS553", "17CS562"]
    mrange = ["0-5", "6-10", "11-15", "16-20", "21-25", "26-30"]

    def get_chart(feature, num):

        ia1=ia2=ia3=False
        ias = ia_table[num-1].query.all()
        if ias and num==1:
            ia1=True
        elif ias and num==2:
            ia2=True
        elif ias and num==3:
            ia3=True
        else:
            pass
        cs51 = []
        cs52 = []
        cs53 = []
        cs54 = []
        cs553 = []
        cs562 = []

        for ia in ias:

            cs51.append(ia.cs51)
            cs52.append(ia.cs52)
            cs53.append(ia.cs53)
            cs54.append(ia.cs54)
            cs553.append(ia.cs553)
            cs562.append(ia.cs562)


        print("\n\n\n", cs51, num)
        if feature == "Average" and (ia1 or ia2 or ia3):
            a_cs51 = int(np.mean(cs51))
            a_cs52 = int(np.mean(cs52))
            a_cs53 = int(np.mean(cs53))
            a_cs54 = int(np.mean(cs54))
            a_cs553 = int(np.mean(cs553))
            a_cs562 = int(np.mean(cs562))

            avg_list = [a_cs51, a_cs52, a_cs53,a_cs54,a_cs553,a_cs562]

            p = figure(x_range=course, plot_height=350, plot_width=900, title="Average Marks")

            # Categorical values can also be used as coordinates
            p.vbar(x=course, top=avg_list , width=0.5)

            # Set some properties to make the plot look better
            p.xgrid.grid_line_color = None
            p.y_range.start = 0
            p.y_range.end = 30

            retvals=[p,ia1,ia2,ia3]

            return retvals

        else:

            def count(listname, s, e):
                c = 0
                for x in listname:
                    if x >= s and x <= e:
                        c += 1
                return c

            colors = ["#d63333","#ff5959","#57f77c","#3af265","#1fe04d","#02c932"]

            # :[count(cs51, 26, 30),count(cs52, 26, 30),count(cs53, 26, 30),count(cs54, 26, 30),count(cs553, 26, 30),count(cs562, 26, 30)]

            data = {"course" : course,
            "0-5":[count(cs51, 0, 5),count(cs52, 0, 5),count(cs53, 0, 5),count(cs54, 0, 5),count(cs553, 0, 5),count(cs562, 0, 5)], "6-10":[count(cs51, 6, 10),count(cs52, 6, 10),count(cs53, 6, 10),count(cs54, 6, 10),count(cs553, 6, 10),count(cs562, 6, 10)],
                      "11-15":[count(cs51, 11, 15),count(cs52, 11, 15),count(cs53, 11, 15),count(cs54, 11, 15),count(cs553, 11, 15),count(cs562, 11, 15)], "16-20":[count(cs51, 16, 20),count(cs52, 16, 20),count(cs53, 16, 20),count(cs54, 16, 20),count(cs553, 16, 20),count(cs562, 16, 20)], "21-25":[count(cs51, 21, 25),count(cs52, 21, 25),count(cs53, 21, 25),count(cs54, 21, 25),count(cs553, 21, 25),count(cs562, 21, 25)], "26-30":[count(cs51, 26, 30),count(cs52, 26, 30),count(cs53, 26, 30),count(cs54, 26, 30),count(cs553, 26, 30),count(cs562, 26, 30)]}



            x = [ (courses, mranges) for courses in course for mranges in mrange ]
            counts = sum(zip(data['0-5'], data['6-10'], data['11-15'], data['16-20'], data['21-25'], data['26-30']), ())

            source = ColumnDataSource(data=dict(x=x, counts=counts))

            p = figure(x_range=FactorRange(*x), plot_height=350, plot_width=900, title="Ranges marks")

            p.vbar(x='x', top='counts', width=0.9, source=source)

            p.y_range.start = 0
            p.x_range.range_padding = 0.1
            p.xaxis.major_label_orientation = 1
            p.xgrid.grid_line_color = None

            # p = figure(y_range=course, plot_height=450,plot_width=850, x_range=(0, 30), title="Internal Assessment {}".format(num))

            # p.hbar_stack(mrange, y='course', height=0.9, color=OrRd6, source=ColumnDataSource(marks),
            #              legend_label=["%s marks" % x for x in mrange])

            # p.y_range.range_padding = 0.1
            # p.ygrid.grid_line_color = None

            retvals=[p,ia1,ia2,ia3]

            return retvals

    current_feature_name = request.args.get("feature_name")
    if current_feature_name == None:
        current_feature_name = "Range"

    plot1 = get_chart(current_feature_name,1)
    script, div = components(plot1[0])

    plot2 = get_chart(current_feature_name,2)
    script2, div2 = components(plot2[0])

    plot3 = get_chart(current_feature_name,3)
    script3, div3 = components(plot3[0])

    return render_template('home/dashboard.html', title="Dashboard", script=script, div=div, script2=script2, div2=div2, script3=script3, div3=div3, ia1=plot1[1], ia2=plot2[2], ia3=plot3[3],feature_names=features,  current_feature_name=current_feature_name)


@home.route('/query', methods=['GET', 'POST'])
@login_required
def list_query():

    ia1 = IA_1.query.all()
    ia2 = IA_2.query.all()
    ia3 = IA_3.query.all()

    return render_template('home/query.html',
                           ia1=ia1,ia2=ia2,ia3=ia3, title="Query")







@home.route('/admin/dashboard')
@login_required
def admin_dashboard():
    # prevent non-admins from accessing the page
    if not current_user.is_admin:
        abort(403)

    return render_template('home/admin_dashboard.html', title="Admin Dashboard")


# Faculty Views

@home.route('/faculty', methods=['GET', 'POST'])
@login_required
def list_faculties():


    faculties = Faculty.query.all()
    classdb = Classes.query.all()

    return render_template('home/faculty/faculties_list.html',
                           faculties=faculties, classdb=classdb, title="Faculties")


@home.route('/course', methods=['GET', 'POST'])
@login_required
def list_courses():

    courses = Course.query.all()

    return render_template('home/course/courses_list.html',
                           courses=courses, title="Courses")

# Classes Views


@home.route('/classes', methods=['GET', 'POST'])
@login_required
def list_classes():


    classdb = Classes.query.all()

    return render_template('home/classes/classes_list.html',
                           classdb=classdb, title="Classes")


@home.route('/cc', methods=['GET', 'POST'])
@login_required
def list_cc():

    isclassteacher = current_user.is_classteacher
    cc = Class_Courses.query.all()

    return render_template('home/cc/cc_list.html',
                           cc=cc, title="Class Courses")


@home.route('/student', methods=['GET', 'POST'])
@login_required
def list_students():

    isclassteacher = current_user.is_classteacher

    students = Student.query.all()

    return render_template('home/student/students_list.html',
                           students=students, isct=isclassteacher, title="students")


@home.route('/ia', methods=['GET', 'POST'])
@login_required
def list_ias():

    isclassteacher = current_user.is_classteacher
    # print("*******************\n\n\n{}\n\n\n********************\n\n".format(admin))

    ia1 = IA_1.query.all()
    ia2 = IA_2.query.all()
    ia3 = IA_3.query.all()

    return render_template('home/ia/ia_list.html',
                           ia1=ia1, ia2=ia2, ia3=ia3, isct=isclassteacher, title="Internal Assessment")


@home.route('/student_ia', methods=['GET', 'POST'])
@login_required
def student_ia():


    return render_template('home/student/students_ia.html', title="Student Dashboard")
