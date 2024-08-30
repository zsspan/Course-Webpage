from app import db

class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    type = db.Column(db.String(20), nullable=False)
    # first_name = db.Column(db.String(30))
    # last_name = db.Column(db.String(30))

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Student(db.Model):
    __tablename__ = 'Student'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    instructor_id = db.Column(db.Integer, db.ForeignKey('Instructor.id'), nullable=False)

    user = db.relationship('User', backref=db.backref('student', uselist=False))
    instructor = db.relationship('Instructor', backref=db.backref('students', lazy=True))

    def __repr__(self):
        return f"Student('{self.user.id}', '{self.user.username}')"

class Instructor(db.Model):
    __tablename__ = 'Instructor'
    id = db.Column(db.Integer, primary_key=True)
    instructor_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)

    user = db.relationship('User', backref=db.backref('instructor', uselist=False))

    def __repr__(self):
        return f"Instructor('{self.user.username}')"

class Assignment(db.Model):
    __tablename__ = 'Assignment'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('Student.id'), nullable=False)
    grade = db.Column(db.Integer)
    regrade_requested = db.Column(db.Boolean, default=False)
    requested_new_grade = db.Column(db.Integer)
    description = db.Column(db.Text)

    student = db.relationship('Student', backref=db.backref('assignments', lazy=True))

    def __repr__(self):
        return f"Assignment(id={self.id}, number={self.number}, student_id={self.student_id}, regrade_requested={self.regrade_requested}, description={self.description}, reqested_new_grade={self.requested_new_grade})"


class Feedback(db.Model):
    __tablename__ = 'Feedback'
    id = db.Column(db.Integer, primary_key=True)
    instructor_id = db.Column(db.Integer, db.ForeignKey('Instructor.id'), nullable=False)
    question_1 = db.Column(db.Text)
    question_2 = db.Column(db.Text)
    question_3 = db.Column(db.Text)
    question_4 = db.Column(db.Text)
    submitted = db.Column(db.Boolean, default=False)  # boolean

    instructor = db.relationship('Instructor', backref=db.backref('feedback_received', uselist=False))

    def __repr__(self):
        return f"Feedback(id={self.id}, instructor_id={self.instructor_id}, " \
               f"question_1='{self.question_1}', question_2='{self.question_2}', " \
               f"question_3='{self.question_3}', question_4='{self.question_4}', " \
               f"submitted={self.submitted})"