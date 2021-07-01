from flask import render_template,redirect,url_for,flash,request
from app.forms import LoginForm
from flask_login import current_user, login_user
from flask_login import logout_user,login_required
from app.models import user,courses
from app import app
from app import db
from app.forms import RegistrationForm

@app.route('/Home')
@app.route('/')
def home():
    return render_template('index.html',title='Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user_ = user.query.filter_by(username=form.username.data).first()
        if user_ is None or not user_.check_password(form.password.data):
            flash('Invalid username or password',category='danger')
            return redirect(url_for('login'))
        login_user(user_, remember=form.remember_me.data)
        return redirect(url_for('home'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user_ = user(username=form.username.data, email=form.email.data,user_role=form.user_role.data)
        user_.set_password(form.password.data)
        db.session.add(user_)
        db.session.commit()
        flash('Congratulations, you are now a registered user!',category='success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/show_dbs')
def ShowDBs():
    u=user.query.all()
    c=courses.query.all()
    return render_template('showdbs.html',users=u,courses=c)


@app.route('/remove_record/<type>/<int:id>',methods=['POST','GET'])
def remove_record(type,id):
    if(type=='course'):
        c=courses.query.filter_by(id=id).first()
        print(c)
        if c is None:
            flash("Sorry some issue in the backend",category='warning')
            return redirect(url_for('ShowDBs'))
        else:
            print('Got Executed Dont Know WHy')
            db.session.delete(c)
            db.session.commit()
            flash('Modified Successfully',category='success')
            u=user.query.all()
            c=courses.query.all()
            return redirect(url_for('ShowDBs',users=u,courses=c))
    if(type=='user'):
        c=user.query.filter_by(id=id).first()
        print(c)
        if c is None:
            flash("Sorry some issue in the backend",category='warning')
            return redirect(url_for('ShowDBs'))
        else:
            db.session.delete(c)
            db.session.commit()
            flash('Modified Successfully',category='success')
            u=user.query.all()
            c=courses.query.all()
            return redirect(url_for('ShowDBs',users=u,courses=c))



@app.route('/edit_record/<type>/<int:id>',methods=['POST','GET'])
def edit_record(type,id):
    if(type=='course'):
        c=courses.query.filter_by(id=id).first()
        print(c)
        if c is None:
            flash("Sorry some issue in the backend",category='warning')
            return redirect(url_for('ShowDBs'))
        else:
            if(request.method=='POST'):
                c.course_name=request.form['coursename']
                c.course_code=request.form['coursecode']
                c.course_description=request.form['coursedescription']
                c.taught_by=user.query.filter_by(username=request.form['teacher']).first()
                db.session.add(c)
                db.session.commit()
                flash('Course Modified Successfully',category='success')
                return redirect(url_for('ShowDBs'))
            return render_template('edit_course.html',users=user.query.filter_by(user_role='Teacher').all(),i=c)
    if(type=='user'):
        c=user.query.filter_by(id=id).first()
        print(c)
        if c is None:
            flash("Sorry some issue in the backend",category='warning')
            return redirect(url_for('ShowDBs'))
        else:
            if(request.method=='POST'):
                c.username=request.form['username']
                c.email=request.form['email']
                db.session.add(c)
                db.session.commit()
                flash('Successfully Modified',category='success')
                return redirect(url_for('ShowDBs',))
            return render_template('edit_user.html',i=c)
    

@app.route('/create_course',methods=['POST','GET'])
def create_course():
    if request.method=='POST':
        coursename=request.form['coursename']
        coursecode=request.form['coursecode']
        coursedescription=request.form['coursedescription']
        teacher=request.form['courseteacher']
        t=user.query.filter_by(username=teacher).first()
        if t is None:
            flash("Account Not Found",category='warning')
            return redirect(url_for('home'))
        c=courses(course_name=coursename,course_code=coursecode,course_description=coursedescription,taught_by=t)
        db.session.add(c)
        db.session.commit()
        flash('Course Created Successfully',category='success')
        return redirect(url_for('ShowDBs'))
    return render_template('new_course.html',users=user.query.filter_by(user_role='Teacher').all())


@app.route('/delete_student/<coursecode>/<username>',methods=['GET','POST'])
def delete_student(username,coursecode):
    use=user.query.filter_by(username=username).first()
    cour=courses.query.filter_by(course_code=coursecode).first()
    cour.has_students.remove(use)
    db.session.add(cour)
    db.session.commit()
    flash('Successfully Deleted Student from Course',category='success')
    return redirect(url_for('ShowDBs'))

@app.route('/enroll_student',methods=['GET','POST'])
def enroll_student():
    u=user.query.filter_by(user_role='Student').all()
    c=courses.query.all()
    if(request.method=='POST'):
        u_=user.query.filter_by(username=request.form['studentname']).first()
        c_=courses.query.filter_by(course_code=request.form['coursecode']).first()
        if(c_ in u_.has_courses):
            flash('Student already enrolled in the given course',category='danger')
        c_.has_students.append(u_)
        db.session.add(u_)
        db.session.commit()
        flash("Enrolled User Successfully",category='success')
        return redirect(url_for('ShowDBs'))
    return render_template('enroll_student.html',users=u,courses=c)