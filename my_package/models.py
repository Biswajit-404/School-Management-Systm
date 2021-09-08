from my_package import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    reg_id = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    img = db.Column(db.String(50), nullable=False)
    usertype = db.Column(db.String(120), nullable=False, default='user')

    def __repr__(self):
        return f"Users('{self.name},'{self.reg_id}','{self.email}','{self.img},'{self.usertype}')"


class newStudent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    dob = db.Column(db.String(60), nullable=False)
    student_phone = db.Column(db.String(60), nullable=False)
    student_email = db.Column(db.String(120), unique=True, nullable=False)
    img = db.Column(db.String(50), nullable=False)
    father = db.Column(db.String(120), nullable=False)
    mother = db.Column(db.String(120), nullable=False)
    parent_phone = db.Column(db.String(60), nullable=False)
    Alternate_phone = db.Column(db.String(60), nullable=False)
    parent_email = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    zipcode = db.Column(db.String(60), nullable=False)
    reg_id = db.Column(db.String(120), unique=True, nullable=False)
    student_class = db.Column(db.String(60), nullable=False)
    student_section = db.Column(db.String(60), nullable=False)
    student_roll_no = db.Column(db.String(60), nullable=False)
    last_college = db.Column(db.String(120), nullable=False)
    last_std = db.Column(db.String(50), nullable=False)
    mark = db.Column(db.String(50), nullable=False)


db.create_all()


class newTeacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    dob = db.Column(db.String(60), nullable=False)
    teacher_phone = db.Column(db.String(60), nullable=False)
    teacher_email = db.Column(db.String(120), unique=True, nullable=False)
    img = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    zipcode = db.Column(db.String(60), nullable=False)
    contact_no = db.Column(db.String(20), nullable=False)
    Alternate_contact_no = db.Column(db.String(20), nullable=False)
    highest_degree = db.Column(db.String(60), nullable=False)
    University_1 = db.Column(db.String(60), nullable=False)
    year_1 = db.Column(db.String(10), nullable=False)
    CGPA_1 = db.Column(db.String(10), nullable=False)
    other_degree = db.Column(db.String(60))
    University_2 = db.Column(db.String(60))
    year_2 = db.Column(db.String(10))
    CGPA_2 = db.Column(db.String(10))


db.create_all()


class Announcement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    announcement_type = db.Column(db.String(20), nullable=False)
    announcement_for = db.Column(db.String(10), nullable=False)
    subject = db.Column(db.String(60), nullable=False)
    description = db.Column(db.Text, nullable=False)
    announced_by = db.Column(db.String(20), nullable=False)


db.create_all()


class New_class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Class_name = db.Column(db.String(20), nullable=False)
    Class_code = db.Column(db.String(10), nullable=False)
    Teacher_name = db.Column(db.String(60), nullable=False)
    Description = db.Column(db.Text, nullable=False)


db.create_all()


class New_subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Subject_name = db.Column(db.String(20), nullable=False)
    Subject_code = db.Column(db.String(10), nullable=False)
    Class_name = db.Column(db.String(10), nullable=False)
    Teacher_name = db.Column(db.String(60), nullable=False)
    Description = db.Column(db.Text, nullable=False)


db.create_all()


class TimeTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Day = db.Column(db.String(10), nullable=False)
    Slot = db.Column(db.String(10), nullable=False)
    Class_name = db.Column(db.String(10), nullable=False)
    Section = db.Column(db.String(10), nullable=False)
    Subject = db.Column(db.String(10), nullable=False)
    Teacher = db.Column(db.String(60), nullable=False)


db.create_all()


class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Class_name = db.Column(db.String(20), nullable=False)
    Section = db.Column(db.String(10), nullable=False)
    Subject = db.Column(db.String(10), nullable=False)
    SubmitBy = db.Column(db.String(20), nullable=False)
    Teacher = db.Column(db.String(60), nullable=False)
    Description = db.Column(db.Text, nullable=False)
    Assignment_file = db.Column(db.String(50), nullable=False)


db.create_all()

class Student_Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Class_name = db.Column(db.String(20), nullable=False)
    Section = db.Column(db.String(10), nullable=False)
    Subject = db.Column(db.String(10), nullable=False)
    Student = db.Column(db.String(60), nullable=False)
    Assignment_file = db.Column(db.String(50), nullable=False)


db.create_all()
