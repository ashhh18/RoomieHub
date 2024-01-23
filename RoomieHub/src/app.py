import os
import secrets
from datetime import datetime
from flask import Flask, request, render_template, url_for, flash, redirect, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField, FileField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_wtf.file import FileAllowed
from wtforms.widgets import PasswordInput
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from sqlalchemy import text
import sqlite3


class SignUpForm(FlaskForm):
    name = StringField('Name',
                       validators=[DataRequired(), Length(min=1, max=50)])
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=1, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email(), Length(min=1, max=120)])
    gender = RadioField('Gender',
                        choices=[('M', 'Male'), ('F', 'Female')],
                        validators=[DataRequired()])
    year = RadioField('Batch',
                      choices=[('UG1', 'UG1'), ('UG2', 'UG2'), ('UG3', 'UG3'), ('UG4', 'UG4'), ('PG1', 'PG1'), ('PG2', 'PG2'), ('OTH', 'Others')],
                      validators=[DataRequired()])
    course = RadioField('Course',
                        choices=[('CSE', 'CSE'), ('ECE', 'ECE'), ('CSD', 'CSD'), ('CHD', 'CHD'), ('CLD', 'CLD'), ('CND', 'CND'), ('ECD', 'ECD'), ('OTH', 'Others')],
                        validators=[DataRequired()])
    profile_photo = FileField('Profile Image',
                              validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')])
    
    have_breakfast = RadioField('Do you have breakfast Everyday?',
                                choices=[('y', 'Yes'), ('n', 'No')],
                                validators=[DataRequired()])
    exercise = RadioField('Do you Exercise?',
                                choices=[('y', 'Yes'), ('n', 'No')],
                                validators=[DataRequired()])
    meditate = RadioField('Do you Meditate?',
                                choices=[('y', 'Yes'), ('n', 'No')],
                                validators=[DataRequired()])
    intro_extro = RadioField('Are you an introvert or extrovert?',
                                choices=[('introvert', 'Introvert'), ('extrovert', 'Extrovert')],
                                validators=[DataRequired()])
    smoke = RadioField('Do you Smoke?',
                                choices=[('y', 'Yes'), ('n', 'No')],
                                validators=[DataRequired()])
    drink = RadioField('Do you Drink?',
                                choices=[('y', 'Yes'), ('n', 'No')],
                                validators=[DataRequired()])
    present_hostel = SelectField('Present Hostel',
                                 choices=[('bakul', 'Bakul'), ('obh', 'OBH'), ('nbh', 'NBH'), ('new_parijat', 'New Parijat'), ('old_parijat', 'Old Parijat')],
                                 validators=[DataRequired()])
    preferred_hostel = SelectField('Preferred Hostel',
                                   choices=[('bakul', 'Bakul'), ('obh', 'OBH'), ('nbh', 'NBH'), ('new_parijat', 'New Parijat'), ('old_parijat', 'Old Parijat')],
                                   validators=[DataRequired()])
    content = StringField('About You',
                          validators=[DataRequired(), Length(min=50, max=1200)])
    password = PasswordField('Password',
                             validators=[DataRequired()], widget=PasswordInput(hide_value=False))
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')],
                                     widget=PasswordInput(hide_value=False))
    submit = SubmitField('Sign Up')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already Taken!')
        
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already in use!')
        
    def validate_hostel1(self, present_hostel, gender):
        if gender.data == "M":
            if present_hostel.data in ['old_parijat', 'new_parijat']:
                raise ValidationError('Boys cannot accomodate girls hostel!')
        else:
            if present_hostel.data in ['bakul', 'obh', 'nbh']:
                raise ValidationError('Girls cannot accomodate Boys hostel!')
            
    def validate_hostel2(self, preferred_hostel, gender):
        if gender.data == "M":
            if preferred_hostel.data in ['old_parijat', 'new_parijat']:
                raise ValidationError('Boys cannot accomodate girls hostel!')
        else:
            if preferred_hostel.data in ['bakul', 'obh', 'nbh']:
                raise ValidationError('Girls cannot accomodate Boys hostel!')
    
    
class SignInFormEmail(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
    
    
class SignInFormUsername(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=1, max=20)])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class UpdateForm(FlaskForm):
    name = StringField('Name',
                       validators=[DataRequired(), Length(min=1, max=50)])
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=1, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email(), Length(min=1, max=120)])
    year = RadioField('Batch',
                      choices=[('UG1', 'UG1'), ('UG2', 'UG2'), ('UG3', 'UG3'), ('UG4', 'UG4'), ('PG1', 'PG1'), ('PG2', 'PG2'), ('OTH', 'Others')],
                      validators=[DataRequired()])
    course = RadioField('Course',
                        choices=[('CSE', 'CSE'), ('ECE', 'ECE'), ('CSD', 'CSD'), ('CHD', 'CHD'), ('CLD', 'CLD'), ('CND', 'CND'), ('ECD', 'ECD'), ('OTH', 'Others')],
                        validators=[DataRequired()])
    profile_photo = FileField('Profile Image',
                              validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')])
    
    have_breakfast = RadioField('Do you have breakfast Everyday?',
                                choices=[('y', 'Yes'), ('n', 'No')],
                                validators=[DataRequired()])
    exercise = RadioField('Do you Exercise?',
                                choices=[('y', 'Yes'), ('n', 'No')],
                                validators=[DataRequired()])
    meditate = RadioField('Do you Meditate?',
                                choices=[('y', 'Yes'), ('n', 'No')],
                                validators=[DataRequired()])
    intro_extro = RadioField('Are you an introvert or extrovert?',
                                choices=[('introvert', 'Introvert'), ('extrovert', 'Extrovert')],
                                validators=[DataRequired()])
    smoke = RadioField('Do you Smoke?',
                                choices=[('y', 'Yes'), ('n', 'No')],
                                validators=[DataRequired()])
    drink = RadioField('Do you Drink?',
                                choices=[('y', 'Yes'), ('n', 'No')],
                                validators=[DataRequired()])
    present_hostel = SelectField('Present Hostel',
                                 choices=[('bakul', 'Bakul'), ('obh', 'OBH'), ('nbh', 'NBH'), ('new_parijat', 'New Parijat'), ('old_parijat', 'Old Parijat')],
                                 validators=[DataRequired()])
    preferred_hostel = SelectField('Preferred Hostel',
                                   choices=[('bakul', 'Bakul'), ('obh', 'OBH'), ('nbh', 'NBH'), ('new_parijat', 'New Parijat'), ('old_parijat', 'Old Parijat')],
                                   validators=[DataRequired()])
    content = StringField('About You',
                          validators=[DataRequired(), Length(min=50, max=1200)])
    submit = SubmitField('Update')
    
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username already Taken!')
        
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email already in use!')
            
    def validate_hostel(self, present_hostel, gender):
        if gender.data == "M":
            if present_hostel.data in ['old_parijat', 'new_parijat']:
                raise ValidationError('Boys cannot accomodate girls hostel!')
        else:
            if present_hostel.data in ['bakul', 'obh', 'nbh']:
                raise ValidationError('Girls cannot accomodate Boys hostel!')
            
    def validate_hostel(self, preferred_hostel, gender):
        if gender.data == "M":
            if preferred_hostel.data in ['old_parijat', 'new_parijat']:
                raise ValidationError('Boys cannot accomodate girls hostel!')
        else:
            if preferred_hostel.data in ['bakul', 'obh', 'nbh']:
                raise ValidationError('Girls cannot accomodate Boys hostel!')
    

class SearchForm(FlaskForm):
    username = StringField('Username')
    gender = RadioField('Your Gender:',
                                choices=[('M', 'Male'), ('F', 'Female')],
                                validators=[DataRequired()])
    preferred_hostel = RadioField('Preferred Hostel:',
                                choices=[('bakul', 'Bakul'), ('obh', 'OBH'), ('nbh', 'NBH'), ('new_parijat', 'New Parijat'), ('old_parijat', 'Old Parijat')])
    year = RadioField('Batch',
                      choices=[('UG1', 'UG1'), ('UG2', 'UG2'), ('UG3', 'UG3'), ('UG4', 'UG4'), ('PG1', 'PG1'), ('PG2', 'PG2'), ('OTH', 'Others')])
    course = RadioField('Course',
                        choices=[('CSE', 'CSE'), ('ECE', 'ECE'), ('CSD', 'CSD'), ('CHD', 'CHD'), ('CLD', 'CLD'), ('CND', 'CND'), ('ECD', 'ECD'), ('OTH', 'Others')])
    submit = SubmitField('Search')
    
    def validate_hostel(self, present_hostel, gender):
        if gender.data == "M":
            if present_hostel.data in ['old_parijat', 'new_parijat']:
                raise ValidationError('Boys cannot accomodate girls hostel!')
        else:
            if present_hostel.data in ['bakul', 'obh', 'nbh']:
                raise ValidationError('Girls cannot accomodate Boys hostel!')
            
    def validate_hostel(self, preferred_hostel, gender):
        if gender.data == "M":
            if preferred_hostel.data in ['old_parijat', 'new_parijat']:
                raise ValidationError('Boys cannot accomodate girls hostel!')
        else:
            if preferred_hostel.data in ['bakul', 'obh', 'nbh']:
                raise ValidationError('Girls cannot accomodate Boys hostel!')
    
    
# Setup for flask app and database
app = Flask(__name__)
app.config['SECRET_KEY'] = '1974bf4e181357512bf418984285ad45'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'signInEmail'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    year = db.Column(db.String(3), nullable=False)
    course = db.Column(db.String(3), nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    profile_photo = db.Column(db.String(20), nullable=False, default='default.jpg')
    have_breakfast = db.Column(db.String(1), nullable=False)
    exercise = db.Column(db.String(1), nullable=False)
    meditate = db.Column(db.String(1), nullable=False)
    intro_extro = db.Column(db.String(9), nullable=False)
    smoke = db.Column(db.String(1), nullable=False)
    drink = db.Column(db.String(1), nullable=False)
    present_hostel = db.Column(db.String(5), nullable=False)
    preferred_hostel = db.Column(db.String(5), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    date_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    roommate_pref1 = db.Column(db.Integer, nullable=False, default=-1)
    roommate_pref2 = db.Column(db.Integer, nullable=False, default=-1)
    roommate_pref3 = db.Column(db.Integer, nullable=False, default=-1)
    
    def __repr__(self):
        # We are not printing content as it can be very long and the data may look messy
        return f"User('{self.id}', '{self.name}', '{self.username}', '{self.email}', '{self.year}', '{self.course}', '{self.gender}', '{self.profile_photo}', '{self.have_breakfast}', '{self.exercise}', '{self.meditate}', '{self.intro_extro}', '{self.smoke}', '{self.drink}', '{self.present_hostel}', '{self.preferred_hostel}', '{self.password}', '{self.roommate_pref1}', '{self.roommate_pref2}', '{self.roommate_pref3}')"

# This function takes argument as a string form of query to be executed > executes the query and returns the result obtained
# example:
# query_db("""CREATE TABLE IF NOT EXISTS songs (id, name, img, artist, album, duration, UNIQUE(id));""")

def query_db(*args, **kw_args):
    db_path = os.path.join(os.path.dirname(__file__), 'instance', 'database.db')
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    result = cur.execute(*args, **kw_args).fetchall()
    con.commit()
    cur.close()
    con.close()
    return result

@app.route('/home', methods=['GET', 'POST'])
def home():
    if current_user.is_authenticated:
        next_page = request.args.get('next')
        users = query_db("SELECT * FROM User;")[-3::]
        return redirect(next_page) if next_page else render_template('Main-Pages/index.html', users=users)
    else:
        flash('You need to first login to access that page', 'danger')
        return redirect(url_for('signInEmail'))


def save_profile_picture(form_picture):
    random_text = secrets.token_hex(8)
    _, file_extension = os.path.splitext(form_picture.filename)
    picture_filename = random_text + file_extension
    picture_path = os.path.join(app.root_path, 'static/Media/profile_pictures', picture_filename)
    form_picture.save(picture_path)
    return picture_filename


@app.route('/signUp', methods=['GET', 'POST'])
def signUp():
    form = SignUpForm()
    if form.validate_on_submit():
        picture_filename = 'default.jpg'
        if form.profile_photo.data:
            temp_picture_filename = save_profile_picture(form.profile_photo.data)
            picture_filename = temp_picture_filename
            
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data,
                    username=form.username.data,
                    email=form.email.data,
                    year=form.year.data,
                    course=form.course.data,
                    gender=form.gender.data,
                    profile_photo=picture_filename,
                    have_breakfast=form.have_breakfast.data,
                    exercise=form.exercise.data,
                    meditate=form.meditate.data,
                    intro_extro=form.intro_extro.data,
                    smoke=form.smoke.data,
                    drink=form.drink.data,
                    present_hostel=form.present_hostel.data,
                    preferred_hostel=form.preferred_hostel.data,
                    password=hashed_password,
                    content=form.content.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created Successfully {form.username.data}! Now you can Log In!', 'success')
        return redirect(url_for('signInEmail'))
    return render_template('Forms/signUp.html', form=form)


@app.route('/', methods=['GET', 'POST'])
@app.route('/signInEmail', methods=['GET', 'POST'])
def signInEmail():
    form = SignInFormEmail()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            users = query_db("SELECT * FROM User;")[-3::]
            return redirect(next_page) if next_page else render_template('Main-Pages/index.html', users=users)
        else:
            flash('Login unsucessful! Please check your credentials!', 'danger')
    return render_template('Forms/signInEmail.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('signInEmail'))

@app.route('/user-info', methods=['GET', 'POST'])
def user_info():
    if current_user.is_authenticated:
        pref1 = User.query.filter_by(username=current_user.username).first().roommate_pref1
        pref2 = User.query.filter_by(username=current_user.username).first().roommate_pref2
        pref3 = User.query.filter_by(username=current_user.username).first().roommate_pref3
        lst = []
        if pref1 != -1:
            p1 = User.query.filter_by(id=pref1).first()
            lst.append(p1)
        if pref2 != -1:
            p2 = User.query.filter_by(id=pref2).first()
            lst.append(p2)
        if pref3 != -1:
            p3 = User.query.filter_by(id=pref3).first()
            lst.append(p3)
        return render_template('Main-Pages/UserInfo.html', user=current_user, preffs=lst)
    else:
        flash('You need to first login to access that page', 'danger')
        return redirect(url_for('signInEmail'))


@app.route('/update', methods=['GET', 'POST'])
def update():
    if current_user.is_authenticated:
        form = UpdateForm()
        if form.validate_on_submit():
            if form.profile_photo.data:
                picture_file = save_profile_picture(form.profile_photo.data)
                current_user.profile_photo = picture_file
                
            current_user.name = form.name.data
            current_user.username = form.username.data
            current_user.email = form.email.data
            current_user.year = form.year.data
            current_user.course = form.course.data
            current_user.have_breakfast = form.have_breakfast.data
            current_user.exercise = form.exercise.data
            current_user.meditate = form.meditate.data
            current_user.intro_extro = form.intro_extro.data
            current_user.smoke = form.smoke.data
            current_user.drink = form.drink.data
            current_user.present_hostel = form.present_hostel.data
            current_user.preferred_hotel = form.preferred_hostel.data
            current_user.content = form.content.data
            
            db.session.commit()
            flash('Account Info successfully updated!', 'success')
            return redirect(url_for('user_info'))
        elif request.method == 'GET':
            form.name.data = current_user.name
            form.username.data = current_user.username
            form.email.data = current_user.email
            form.year.data = current_user.year
            form.course.data = current_user.course
            form.have_breakfast.data = current_user.have_breakfast
            form.exercise.data = current_user.exercise
            form.meditate.data = current_user.meditate
            form.intro_extro.data = current_user.intro_extro
            form.smoke.data = current_user.smoke
            form.drink.data = current_user.drink
            form.present_hostel.data = current_user.present_hostel
            form.preferred_hostel.data = current_user.preferred_hostel
            form.content.data = current_user.content
            
        image_file = current_user.profile_photo
        print(form.errors)
        return render_template('Forms/update.html', form=form, image_file=image_file)
    else:
        flash('You need to first login to access that page', 'danger')
        return redirect(url_for('signInEmail'))
    

@app.route('/search', methods=['GET', 'POST'])
def search():
    if current_user.is_authenticated:
        form = SearchForm()
        if form.validate_on_submit():
            username=form.username.data
            year=form.year.data
            preferred_hostel = form.preferred_hostel.data
            course = form.course.data
            gender = form.gender.data
            query_str = f"SELECT * FROM User WHERE gender='{gender}'"
            if username:
                query_str += f" AND username='{username}'"
            if preferred_hostel:
                query_str += f" AND preferred_hostel='{preferred_hostel}'"
            if year:
                query_str += f" AND year='{year}'"
            if course:
                query_str += f" AND course='{course}'"
            query_str += ';'
            ans = query_db(query_str)
            return render_template('Main-Pages/search-page.html', form=form, display='t', users=ans)
        return render_template('Main-Pages/search-page.html', form=form, display='f')
    else:
        flash('You need to first login to access that page', 'danger')
        return redirect(url_for('signInEmail'))
    

@app.route('/show-all-users', methods=['GET', 'POST'])
def show_all_users():
    if current_user.is_authenticated:
        list_of_users = User.query.all()
        return render_template('Main-Pages/all-users.html', users=list_of_users)
    else:
        flash('You need to first login to access that page', 'danger')
        return redirect(url_for('signInEmail'))
    

@app.route('/open_user_profile/<string:username>', methods=['GET', 'POST'])
def open_user_profile(username):
    if current_user.is_authenticated:
        user=User.query.filter_by(username=username).first()
        return render_template('Main-Pages/other-user.html', user=user)
    else:
        flash('You need to first login to access that page', 'danger')
        return redirect(url_for('signInEmail'))
    

@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('Main-Pages/about.html')

@app.route('/discover', methods=['GET', 'POST'])
def discover():
    if current_user.is_authenticated:
        users = query_db("SELECT * FROM User;")
        final_users = []
        for user in users:
            if user[2] == current_user.username:
                continue
            else:
                final_users.append(user)
        return render_template('Main-Pages/discover.html', users=final_users)
    else:
        flash('You need to first login to access that page', 'danger')
        return redirect(url_for('signInEmail'))
    

@app.route('/add_to_following/<string:username>', methods=['GET', 'POST'])
def add_to_following(username):
    user = User.query.filter_by(username=username).first()
    pref1 = current_user.roommate_pref1
    pref2 = current_user.roommate_pref2
    pref3 = current_user.roommate_pref3
    if pref1 != -1 and pref2 != -1 and pref3 != -1:
        flash('More than 3 people cannot be added!', 'danger')
        return redirect(url_for('user_info'))
    elif pref1 == user.id or pref2 == user.id or pref3 == user.id:
        flash("Person already added!", 'info')
        return redirect(url_for('user_info')) 
    else:
        if pref1 == -1:
            current_user.roommate_pref1 = user.id
        elif pref2 == -1:
            current_user.roommate_pref2 = user.id
        else:
            current_user.roommate_pref3 = user.id
        db.session.commit()
        flash('Person added successfully!', 'success')
        return redirect(url_for('user_info'))
        

@app.route('/remove/<string:username>', methods=['GET', 'POST'])
def remove(username):
    user = User.query.filter_by(username=username).first()
    user_id = user.id
    if current_user.roommate_pref1 == user_id:
        current_user.roommate_pref1 = -1
    elif current_user.roommate_pref2 == user_id:
        current_user.roommate_pref2 = -1
    elif current_user.roommate_pref3 == user_id:
        current_user.roommate_pref3 = -1
    db.session.commit()
    flash('Person removed successfully!', 'success')
    return redirect(url_for('user_info'))



@app.route('/followers', methods=['GET', 'POST'])
def followers():
    if current_user.is_authenticated:
        list_of_followers = []
        users = User.query.all()
        for user in users:
            if current_user.id in [user.roommate_pref1, user.roommate_pref2, user.roommate_pref3]:
                list_of_followers.append(user)
        return render_template('Main-Pages/followers.html', followers = list_of_followers)
    else:
        flash('You need to first login to access that page', 'danger')
        return redirect(url_for('signInEmail'))
    
    
if __name__ == '__main__':
    app.run(debug=True)