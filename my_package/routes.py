from werkzeug.utils import secure_filename

from my_package import app, db, bcrypt
from flask import render_template, url_for, redirect, request, flash, session, g
from my_package.models import Users, newStudent, Announcement, New_class, New_subject, newTeacher, TimeTable, \
    Assignment, Student_Assignment
from my_package.auth import checkAdmin, checkUser, checkTeacher
import os

# from flask_login import login_user, current_user, logout_user, login_required


# ------------------------------REGISTER---------------------------------------------

app.config['IMAGE_UPLOADS'] = "/PANDORA'S BOX/ON Going Projects/College_project/my_package/static/User_Img"
app.config['ASSIGNMENT_UPLOADS'] = "/PANDORA'S BOX/ON Going Projects/College_project/my_package/static/Assignments"


@app.route('/register', methods=['POST', 'GET'])
def register():
    try:
        if request.method == 'POST':
            uname = request.form.get('userName')
            regId = request.form.get('Reg_id')
            email = request.form.get('email')
            password = request.form.get('password')
            uimg = request.files['photo']
            check_regId = Users.query.filter_by(reg_id=regId).first()

            print(check_regId)
            if check_regId is None:

                file = secure_filename(str(regId) + '.' + uimg.filename.rsplit('.', 1)[1].lower())
                uimg.save(os.path.join(app.config['IMAGE_UPLOADS'], file))
                hashed_pwd = bcrypt.generate_password_hash(password).decode('utf-8')
                obj = Users(name=uname, reg_id=regId, email=email, password=hashed_pwd, img=file)
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


#  ------------------------------home---------------------------------------------

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
            session.clear()
            return render_template('home/login-14.html')
    else:
        return redirect(url_for('login'))


# ------------------------------LOGIN---------------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            remember_me = request.form.get('remember_me')

            user = Users.query.filter_by(email=email).first()

            session["id"] = user.id
            session["userName"] = user.name
            session["userType"] = user.usertype
            session["img"] = user.img

            if user and bcrypt.check_password_hash(user.password, password) and user.usertype == "admin":
                return redirect('admin')
            elif user and bcrypt.check_password_hash(user.password, password) and user.usertype == "teacher":
                return redirect('teacher')
            elif user and bcrypt.check_password_hash(user.password, password) and user.usertype == "user":
                return redirect('student')
            else:
                flash(f' - login failed please try again', 'failed')
                return render_template(url_for('home/login-14.html'))

        elif request.method == 'GET':
            if "id" in session and "userType" in session and "userName" in session:
                if session["userType"] == 'admin':
                    return redirect(url_for('admin'))
                elif session["userType"] == 'user':
                    return redirect(url_for('user'))
                elif session["userType"] == 'teacher':
                    return redirect(url_for('teacher'))
                else:
                    session.clear()
                    print('no user type')
                    return render_template('home/login-14.html')
            else:
                return render_template('home/login-14.html')

    except Exception as e:
        print(e)
        return render_template('home/login-14.html')

# ------------------------------EDIT---------------------------------------------
@app.route('/edit', methods=['POST', 'GET'])
def edit():
    try:
        if request.method == 'POST':
            uname = request.form.get('userName')
            regId = request.form.get('Reg_id')
            email = request.form.get('email')
            password = request.form.get('password')
            uimg = request.files['photo']
            check_regId = Users.query.filter_by(reg_id=regId).first()

            print(check_regId)
            if check_regId is not None:

                file = secure_filename(str(regId) + '.' + uimg.filename.rsplit('.', 1)[1].lower())
                uimg.save(os.path.join(app.config['IMAGE_UPLOADS'], file))
                hashed_pwd = bcrypt.generate_password_hash(password).decode('utf-8')
                obj = Users(name=uname, reg_id=regId, email=email, password=hashed_pwd, img=file)
                db.session.add(obj)
                db.session.commit()
                flash('- Registration Successful', 'Success')
                return render_template('home/edit.html')

        return render_template('home/edit.html')
    except Exception as e:
        print(e)
        flash(' - something went wrong', 'failed')
        return render_template('home/edit.html')


# ------------------------------LOGOUT---------------------------------------------
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
    return render_template('home/otp-14.html', )


@app.route('/admin/')
@app.route('/admin/admin-dashboard.html')
@checkAdmin
def admin():
    if request.method == 'GET':

        data = Announcement.query.order_by(Announcement.id).all()
        user_count = Users.query.count()
        std_count = Users.query.filter_by(usertype='user').count()
        teach_count = Users.query.filter_by(usertype='teacher').count()

        return render_template('admin/admin-dashboard.html', data=data, user_count=user_count, std_count=std_count,
                               teach_count=teach_count)
    elif request.method == 'POST':
        data = Announcement.query.order_by(Announcement.id).all()
        return render_template('admin/admin-dashboard.html', data=data)


@app.route('/teacher/')
@checkTeacher
def teach():

        if request.method == 'GET':
            assign_count = Assignment.query.count()
            teach_count = Users.query.filter_by(usertype='teacher').count()
            std_count = Users.query.filter_by(usertype='user').count()
            data = Announcement.query.order_by(Announcement.id).all()
            return render_template('teacher/teacher-dashboard.html', data=data, assign_count=assign_count,
                                   teach_count=teach_count, std_count=std_count)
        elif request.method == 'POST':
            data = Announcement.query.order_by(Announcement.id).all()
            return render_template('teacher/teacher-dashboard.html', data=data)


@app.route('/student/')
@app.route('/student/student-dashboard.html')
@checkUser
def student():
        if request.method == 'GET':
            assign_count = Assignment.query.count()
            teach_count = Users.query.filter_by(usertype='teacher').count()
            std_count = Users.query.filter_by(usertype='user').count()
            data = Announcement.query.order_by(Announcement.id).all()
            return render_template('student/student-dashboard.html', data=data, assign_count=assign_count,
                                   teach_count=teach_count, std_count=std_count)
        elif request.method == 'POST':
            data = Announcement.query.order_by(Announcement.id).all()
            return render_template('teacher/teacher-dashboard.html', data=data)


@app.route('/test/')
def test():
    return render_template('test.html')


@app.route('/delete/timetable/<string:tid>')
def deleteTimetable(tid):
    return "<h1>deleted</h1>"
def datetimeformat(value, format='%B'):
    return value.strftime("format", format)


# ------------------------------ADD STUDENT ---------------------------------------------------
@app.route('/admin/admin-add-student.html', methods=['GET', 'POST'])
def admin_add_student():
    try:
        if request.method == 'POST':
            name = request.form.get('name')
            genders = request.form.get('gender')
            dob = request.form.get('dob')
            student_phone = request.form.get('student_phone')
            student_email = request.form.get('student_email')
            img = request.form.get('img')
            father = request.form.get('father')
            mother = request.form.get('mother')
            parent_phone = request.form.get('parent_phone')
            Alternate_phone = request.form.get('alt_contact')
            parent_email = request.form.get('parent_email')
            address = request.form.get('address')
            zipcode = request.form.get('zipcode')
            reg_id = request.form.get('reg_id')
            student_class = request.form.get('class')
            student_section = request.form.get('section')
            student_roll_no = request.form.get('roll_no')
            last_college = request.form.get('last_college')
            last_std = request.form.get('last_std')
            mark = request.form.get('mark')
            check_regId = Users.query.filter_by(reg_id=reg_id).first()
            print(check_regId)
            print(dob)
            if check_regId is None:
                obj = newStudent(name=name, gender=genders, dob=dob, student_phone=student_phone,
                                 student_email=student_email,
                                 img=img, father=father, mother=mother, parent_phone=parent_phone,
                                 Alternate_phone=Alternate_phone, parent_email=parent_email, address=address,
                                 zipcode=zipcode,
                                 reg_id=reg_id,
                                 student_class=student_class, student_section=student_section,
                                 student_roll_no=student_roll_no,
                                 last_college=last_college,
                                 last_std=last_std, mark=mark)
                db.session.add(obj)
                db.session.commit()
                msg = "Registration Successful"
                return render_template('admin/admin-add-student.html', msg=msg, )
        elif request.method == 'GET':
            return render_template('admin/admin-add-student.html')
    except Exception as e:
        print(e)
        msg = f'the student already exists'
        return render_template('admin/admin-add-student.html', msg=msg)


# --------------------------view student------------------------------------------------

@app.route('/admin/admin-student-list.html', methods=['GET', 'POST'])
def admin_view_student_list():
    if request.method == 'GET':
        data = newStudent.query.order_by(newStudent.id).all()
        return render_template('admin/admin-student-list.html', data=data)


def delete():
    if request.method == 'POST':
        data = newStudent.query.order_by(newStudent.id).all()
        return render_template('admin/admin-student-list.html', data=data)


# ------------------------------ADD TEACHER---------------------------------------------

@app.route('/admin/admin-add-teacher.html', methods=['GET', 'POST'])
def admin_add_teacher():
    try:
        if request.method == 'POST':
            name = request.form.get('name')
            gender = request.form.get('gender')
            dob = request.form.get('dob')
            teacher_phone = request.form.get('teacher_phone')
            teacher_email = request.form.get('teacher_email')
            img = request.form.get('img')
            address = request.form.get('address')
            zipcode = request.form.get('zipcode')
            contact_no = request.form.get('contact_no')
            Alternate_contact_no = request.form.get('alt_contact_no')
            highest_degree = request.form.get('highest_degree')
            University_1 = request.form.get('Uni-1')
            year_1 = request.form.get('year-1')
            CGPA_1 = request.form.get('CGPA-1')
            other_degree = request.form.get('other_degree')
            University_2 = request.form.get('Uni-2')
            year_2 = request.form.get('year-2')
            CGPA_2 = request.form.get('CGPA-2')
            print(dob)
            # check_email = Users.query.filter_by(teacher_email=teacher_email).first()
            # print(check_email)
            obj = newTeacher(name=name, gender=gender, dob=dob, teacher_phone=teacher_phone,
                             teacher_email=teacher_email, img=img,
                             address=address, Alternate_contact_no=Alternate_contact_no,
                             zipcode=zipcode, contact_no=contact_no, highest_degree=highest_degree,
                             University_1=University_1, year_1=year_1, CGPA_1=CGPA_1, other_degree=other_degree,
                             University_2=University_2, year_2=year_2, CGPA_2=CGPA_2)

            db.session.add(obj)
            db.session.commit()
            msg = "Registration Successful"
            return render_template('admin/admin-add-teacher.html', msg=msg)
        elif request.method == 'GET':
            return render_template('admin/admin-add-teacher.html')
    except Exception as e:
        print(e)
        msg = f'the teacher already exists'
        return render_template('admin/admin-add-teacher.html', msg=msg)


# --------------------------view teacher------------------------------------------------

@app.route('/admin/admin-teacher-list.html', methods=['GET', 'POST'])
def admin_view_teacher_list():
    if request.method == 'GET':
        data = newTeacher.query.order_by(newTeacher.id).all()
        return render_template('admin/admin-teacher-list.html', data=data)


def delete():
    if request.method == 'POST':
        data = newTeacher.query.order_by(newTeacher.id).all()
        return render_template('admin/admin-teacher-list.html', data=data)


# ------------------------------ANNOUNCEMENT---------------------------------------------
@app.route('/admin/admin-add-announcement.html', methods=['GET', 'POST'])
def admin_add_announcement():
    try:
        if request.method == 'POST':
            announcement_type = request.form.get('type')
            announcement_for = request.form.get('for')
            subject = request.form.get('ann_subject')
            announced_by = request.form.get('ann_name')
            description = request.form.get('ann_description')
            obj = Announcement(announcement_type=announcement_type, announcement_for=announcement_for, subject=subject,
                               description=description, announced_by=announced_by)
            db.session.add(obj)
            db.session.commit()
            msg = "Announcement added"
            data = Announcement.query.order_by(Announcement.id).all()
            return render_template('admin/admin-add-announcement.html', msg=msg, data=data)
        elif request.method == 'GET':
            data = Announcement.query.order_by(Announcement.id).all()
            return render_template('admin/admin-add-announcement.html', data=data)
    except Exception as e:
        print(e)
        msg = "Error -something went wrong"
        return render_template('admin/admin-add-announcement.html', msg=msg)


# --------------------------ADD CLASS------------------------------------------------
@app.route('/admin/admin-add-class.html', methods=['GET', 'POST'])
def admin_add_class():
    try:
        if request.method == 'POST':
            class_name = request.form.get('class_name')
            class_code = request.form.get('class_code')
            Teacher_name = request.form.get('teacher_name')
            description = request.form.get('description')
            obj = New_class(Class_name=class_name, Class_code=class_code, Description=description,
                            Teacher_name=Teacher_name)
            db.session.add(obj)
            db.session.commit()
            msg = "Announcement added"
            data = New_class.query.order_by(New_class.id).all()
            return render_template('admin/admin-add-class.html', data=data)
        elif request.method == 'GET':
            data = New_class.query.order_by(New_class.id).all()
            return render_template('admin/admin-add-class.html', data=data)
    except Exception as e:
        print(e)
        return render_template('admin/admin-add-class.html')


# --------------------------ADD SUBJECTS------------------------------------------------
@app.route('/admin/admin-add-subject.html', methods=['GET', 'POST'])
def admin_add_subject():
    try:
        if request.method == 'POST':
            subject_name = request.form.get('sub_name')
            subject_code = request.form.get('sub_code')
            class_name = request.form.get('cls_name')
            Teach_name = request.form.get('teach_name')
            description = request.form.get('sub_description')
            obj = New_subject(Subject_name=subject_name, Subject_code=subject_code, Class_name=class_name,
                              Description=description,
                              Teacher_name=Teach_name)
            db.session.add(obj)
            db.session.commit()
            msg = "Announcement added"
            data = New_subject.query.all()
            return render_template('admin/admin-add-subject.html', data=data)
        elif request.method == 'GET':
            data = New_subject.query.all()
            return render_template('admin/admin-add-subject.html', data=data)
    except Exception as e:
        print(e)
        return render_template('admin/admin-add-subject.html')


# --------------------------ADD TIMETABLES --------------------------------------------------

@app.route('/admin/admin-create-timetable.html', methods=['GET', 'POST'])
def admin_create_timetable():
    try:
        if request.method == 'POST':
            Day = request.form.get('day')
            Slot = request.form.get('slot')
            Class_name = request.form.get('class_name')
            Section = request.form.get('section_name')
            Subject = request.form.get('subject_name')
            Teacher = request.form.get('teacher_name')

            obj = TimeTable(Day=Day, Slot=Slot, Class_name=Class_name, Section=Section, Subject=Subject,
                            Teacher=Teacher)
            db.session.add(obj)
            db.session.commit()
            msg = "slot added"
            data = TimeTable.query.order_by(TimeTable.id).all()
            return render_template('admin/admin-create-timetable.html', data=data, msg=msg)
        elif request.method == 'GET':
            msg = 'something went wrong'
            data = TimeTable.query.order_by(TimeTable.id).all()
            return render_template('admin/admin-create-timetable.html', data=data, msg=msg)
    except Exception as e:
        print(e)
        return render_template('admin/admin-create-timetable.html')


# --------------------------CREATE ASSIGNMENT------------------------------------------------


@app.route('/teacher/teacher-create-assignment.html', methods=['GET', 'POST'])
def teacher_create_assignment():
    try:
        if request.method == 'POST':
            Class_name = request.form.get('class_name')
            Section = request.form.get('section_name')
            Subject = request.form.get('subject_name')
            SubmitBy = request.form.get('Time_limit')
            Teacher = request.form.get('teacher_name')
            Description = request.form.get('description')
            file = request.files['assignment_File']
            file.save(os.path.join(app.config['ASSIGNMENT_UPLOADS'], file.filename))

            obj = Assignment(Class_name=Class_name, Section=Section, Subject=Subject,
                             SubmitBy=SubmitBy, Teacher=Teacher, Description=Description, Assignment_file=file.filename)
            db.session.add(obj)
            db.session.commit()
            msg = "Assignment added"
            return render_template('/teacher/teacher-create-assignment.html', msg=msg)
        elif request.method == 'GET':
            msg = 'something went wrong'
            return render_template('/teacher/teacher-create-assignment.html', msg=msg)
    except Exception as e:
        print(e)
        return render_template('/teacher/teacher-create-assignment.html')


# --------------------------DOWNLOAD ASSIGNMENT------------------------------------------------


@app.route('/teacher/teacher-assignment-download.html', methods=['GET', 'POST'])
def teacher_download_assignment():
    data = Student_Assignment.query.order_by(Student_Assignment.id).all()
    try:
        if request.method == 'GET':
            print('in get')
            print(data)
            return render_template('/teacher/teacher-assignment-download.html', data=data)
        if request.method == 'POST':
            return render_template('/teacher/teacher-assignment-download.html', data=data)

    except Exception as e:
        print(e)
        return render_template('/teacher/assignment-download.html', data=data)


# --------------------------DOWNLOAD ASSIGNMENT------------------------------------------------

@app.route('/student/student-assignment-download.html', methods=['GET', 'POST'])
def student_download_assignment():
    data = Assignment.query.order_by(Assignment.id).all()
    try:
        if request.method == 'GET':
            print('in get')
            print(data)
            return render_template('/student/student-assignment-download.html', data=data)
        if request.method == 'POST':
            return render_template('/student/student-assignment-download.html', data=data)

    except Exception as e:
        print(e)
        return render_template('/student/student-assignment-download.html', data=data)

    # --------------------------UPLOAD ASSIGNMENT------------------------------------------------


@app.route('/student/student-assignment-upload.html', methods=['GET', 'POST'])
def student_upload_assignment():
    try:
        if request.method == 'POST':
            Class_name = request.form.get('class_name')
            Section = request.form.get('section_name')
            Subject = request.form.get('subject_name')
            Student = request.form.get('student_name')
            file = request.files['assignment_File']
            file.save(os.path.join(app.config['ASSIGNMENT_UPLOADS'], file.filename))

            obj = Student_Assignment(Class_name=Class_name, Section=Section, Subject=Subject,
                                     Student=Student, Assignment_file=file.filename)
            db.session.add(obj)
            db.session.commit()
            msg = "Assignment added"
            return render_template('/student/student-assignment-upload.html', msg=msg)
        elif request.method == 'GET':
            msg = 'something went wrong'
            return render_template('/student/student-assignment-upload.html', msg=msg)
    except Exception as e:
        print(e)
        return render_template('/student/student-assignment-upload.html')


# --------------------------STUDENT TABLE-----------------------------------------------

@app.route('/student/student-timetable.html', methods=['GET', 'POST'])
def student_timetable():
    data = TimeTable.query.order_by(TimeTable.id).all()
    try:
        if request.method == 'GET':
            return render_template('student/student-timetable.html', data=data)
    except Exception as e:
        print(e)
        return render_template('student/student-timetable.html', data=data)


# --------------------------teacher TABLE-----------------------------------------------

@app.route('/teacher/teacher-timetable.html', methods=['GET', 'POST'])
def teacher_timetable():
    data = TimeTable.query.order_by(TimeTable.id).all()
    try:
        if request.method == 'GET':
            return render_template('teacher/teacher-timetable.html', data=data)
    except Exception as e:
        print(e)
        return render_template('teacher/teacher-timetable.html', data=data)


@app.route('/admin/<value>', methods=['GET', 'POST'])
def admin_redi(value):
    return render_template('admin/' + value)


@app.route('/teacher/<value>')
def teacher_redi(value):
    return render_template('teacher/' + value)


@app.route('/student/<value>')
def student_redi(value):
    return render_template('student/' + value)
