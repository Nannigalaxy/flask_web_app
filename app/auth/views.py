from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user, current_user

from . import auth
from .forms import LoginForm, RegistrationForm
from .. import db
from ..models import Faculty


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle requests to the /register route
    Add an faculty to the database through the registration form
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        faculty = Faculty(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            password=form.first_name.data)

        # add faculty to the database
        db.session.add(faculty)
        db.session.commit()
        flash('You have asuccessfully registered! You may now login. First name is password')

        # redirect to the login page
        return redirect(url_for('auth.login'))

    # load registration template
    return render_template('auth/register.html', form=form, title='Register')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle requests to the /login route
    Log an faculty in through the login form
    """
    if current_user.is_authenticated:
        return redirect(url_for('home.dashboard'))

    form = LoginForm()
    if form.validate_on_submit():

        # check whether faculty exists in the database and whether
        # the password entered matches the password in the database
        faculty = Faculty.query.filter_by(email=form.email.data).first()
        if faculty is not None and faculty.verify_password(
                form.password.data):
            # log faculty in
            login_user(faculty)

            # redirect to the dashboard page after login
            if faculty.is_admin:
                return redirect(url_for('home.admin_dashboard'))
            else:
                return redirect(url_for('home.dashboard'))

        # when login details are incorrect
        else:
            flash('Invalid email or password.')

    # load login template
    return render_template('auth/login.html', form=form, title='Login')


@auth.route('/logout')
@login_required
def logout():
    """
    Handle requests to the /logout route
    Log an faculty out through the logout link
    """
    logout_user()
    flash('You have successfully been logged out.')

    # redirect to the login page
    return redirect(url_for('auth.login'))
