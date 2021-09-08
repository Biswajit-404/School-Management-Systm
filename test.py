from flask import Flask, render_template, url_for, redirect, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from my_package import bcrypt
from my_package.auth import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'afafagqatygava4r36@!#!gsgs'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/pathsala'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/pathsala'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# create models
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    reg_id = db.Column(db.Integer, unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    img = db.Column(db.String(50), nullable=False)
    usertype = db.Column(db.String(120), nullable=False, default='user')


db.create_all()


@app.route('/register', methods=['POST', 'GET'])
def register():
    try:
        if request.method == 'POST':
            uname = request.form.get('userName')
            regId = request.form.get('Reg_id')
            email = request.form.get('email')
            password = request.form.get('password')
            cPassword = request.form.get('confirm_password')
            uimg = request.form.get('photo')
            check_regId = Users.query.filter_by(reg_id=regId).first()
            print(check_regId)
            if check_regId is None:
                hashed_pwd = bcrypt.generate_password_hash(password).decode('utf-8')
                obj = Users(name=uname, reg_id=regId, email=email, password=hashed_pwd, img=uimg)
                db.session.add(obj)
                db.session.commit()
                flash('- Registration Successful', 'Success')
                return render_template('home/register-14.html', )

            else:
                flash(' - duplicate registration no', 'failed')

        return render_template('home/register-14.html')
    except Exception as e:
        print(e)
        flash(' - something went wrong', 'failed')
        return render_template('home/register-14.html')


# LOGIN

@app.route('/', methods=['GET', 'POST'])
def home():
    if "id" in session and "userType" in session and "userName" in session:
        if session["userType"] == 'admin':
            return redirect('admin')
        elif session["userType"] == 'user':
            return render_template(url_for('user'))
        elif session["userType"] == 'teacher':
            return render_template(url_for('teacher'))
        else:
            session.destroy()
            return render_template(url_for('home/login-14.html'))
    else:
        return render_template(url_for('home/login-14.html'))


@app.route('/login', methods=['GET', 'POST'])
def login(curuser=None):
    try:
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            remember_me = request.form.get('remember_me')
            print(remember_me)
            user = Users.query.filter_by(email=email).first()
            print(user)
            session["id"] = user.id
            session["userName"] = user.name
            session["userType"] = user.usertype
            if user and bcrypt.check_password_hash(user.password, password):
                # login_user(user, remember=remember_me)
                return render_template('admin-dashboard.html', user=user)
            else:
                flash(f' - login failed please try again', 'failed')
        elif request.method == 'GET':
            print('inside get')
            if "id" in session and "userType" in session and "userName" in session:
                if session["userType"] == 'admin':
                    return redirect('admin')
                elif session["userType"] == 'user':
                    return render_template(url_for('user'))
                elif session["userType"] == 'teacher':
                    return render_template(url_for('teacher'))
                else:
                    session.destroy()
                    return render_template(url_for('home/login-14.html'))
            else:
                return render_template(url_for('home/login-14.html'))



    except Exception as e:
        print(e)
        return render_template('home/login-14.html')


@app.route('/logout')
def logout():
    session.pop('id', None)
    session.pop('username', None)
    session.pop('userType', None)
    return redirect(url_for('login'))


@app.route('/account')
def account():
    # logout_user()
    return redirect(url_for('login'))


@app.route('/forgot-pass')
def forgot_pass():
    return render_template('home/forgot-pass.html')


@app.route('/otp')
def otp():
    return render_template('home/otp-14.html')


@app.route('/admin/')
def admin():
    if 'id' in session:
        return render_template('admin-dashboard.html')
    else:
        return redirect(url_for('login'))


@app.route('/teacher/')
def teach():
    if 'id' in session:
        return render_template('teacher-dashboard.html')
    else:
        return redirect(url_for('login'))


@app.route('/student/')
def student():
    if 'id' in session:
        return render_template('student-dashboard.html')
    else:
        return render_template('login')


@app.route('/test/')
def test():
    return render_template('test.html')


@app.route('/admin/<value>')
def admin_redi(value):
    return render_template('admin/' + value)


@app.route('/teacher/<value>')
def teacher_redi(value):
    return render_template('teacher/' + value)


@app.route('/student/<value>')
def student_redi(value):
    return render_template('student/' + value)


if __name__ == '__main__':
    app.run(debug=True)
