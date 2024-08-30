from flask import Flask, render_template, request, flash, redirect, url_for, session, get_flashed_messages
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import distinct
from datetime import datetime, timedelta
from flask_bcrypt import Bcrypt
from random import choice, randint, random
from models import *
app = Flask(__name__)
bcrypt=Bcrypt(app)

app.config['SECRET_KEY']='8a0f946f1471e113e528d927220ad977ed8b2cce63303beff10c8cb4a15e1a99'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///notes.db'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes = 15)
db = SQLAlchemy(app)

def generate_assignments():
    existing_assignments = Assignment.query.filter_by(student_id=session['id']).count()
    if existing_assignments == 0:
        prob = 0.2
        # Generate and add six assignments for the current student
        for i in range(1, 7):
            grade = randint(0, 100)

            if random() < prob:
                grade = None

            assignment = Assignment(
                number=i,
                student_id=session['id'],
                grade=grade,
                regrade_requested=False,
                requested_new_grade=None,
                description= ""
            )
            db.session.add(assignment)
        db.session.commit()
    
def login_user():
    username = request.form['username']
    password = request.form['password']
    person = User.query.filter_by(username=username).first()
    if not person or not bcrypt.check_password_hash(person.password, password):
        flash('❌ Please check your login details and try again.', 'login')
        return render_template('login.html')
    else:
        session['name'] = person.username
        session['type'] = person.type
        session['email'] = person.email
        session['id'] = person.id
        # session['first-name'] = person.first_name
        # session['last-name'] = person.last_name

        instructor_name = (
        db.session.query(distinct(User.username))
        .join(Student, Student.instructor_id == Instructor.id)
        .join(Instructor, Instructor.instructor_id == User.id)
        .filter(Student.student_id == session['id'])
        .scalar()
        )

        if session['type'] == 'student':
            session['instructor'] = instructor_name
        else:
            session['instructor'] = session['name']
        
        session.permanent = True

        generate_assignments()
        return redirect(url_for('index'))

def register_user():
    username = request.form['username']
    email = request.form['email']
    password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
    type = request.form['type']  # Get user type
    # first_name = request.form['first-name']
    # last_name = request.form['last-name']
    existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
    
    if existing_user:
        flash('Username or email already exists. Please choose a different one.', 'register')
        return render_template('login.html')
    
    # If the username and email are unique, create the new user
    new_user = User(username=username, email=email, password=password, type=type)
                    #  first_name=first_name, last_name=last_name)
    db.session.add(new_user)
    db.session.commit()

    # Add the new user to the appropriate table based on user type
    if type == 'student':
        # Randomly select an instructor from existing users
        instructors = User.query.filter_by(type='instructor').all()
        random_instructor = choice(instructors)
        
        new_student = Student(student_id=new_user.id, instructor_id=random_instructor.id)
        db.session.add(new_student)
        db.session.commit()
    elif type == 'instructor':
        new_instructor = Instructor(instructor_id=new_user.id)
        db.session.add(new_instructor)
        db.session.commit()
    
    flash('Registration successful! Please log in.', 'register')
    return render_template('login.html')

def login_status():
    if 'name' not in session:
        return False
    return True

@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'name' in session:
            flash('You are already logged in!')
            return redirect(url_for('index'))
        else:
            return render_template('login.html')
    else: # If it's a POST request
        form_type = request.form.get('form_type')
        if form_type == 'login':
            return login_user()
        elif form_type == 'register':
            return register_user()
        else:
            flash('Invalid form submission.', 'error')
            return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('name', default=None)
    return redirect(url_for('login'))

@app.route('/assignments')
def assignments():
    if not login_status():
        return redirect(url_for('index'))
    return render_template('assignments.html')

@app.route('/grades', methods=['GET', 'POST'])
def grades():
    if not login_status():
        return redirect(url_for('index'))
    if session['type'] == 'instructor':
        student_list = Student.query.all()

        all_assignments = Assignment.query.all()
        assignments_by_student = {}

        # Group assignments by student
        for assignment in all_assignments:
            student_id = assignment.student_id
            if student_id not in assignments_by_student:
                assignments_by_student[student_id] = []
            assignments_by_student[student_id].append(assignment)
        # print(assignments_by_student)
        for student in student_list:
            print(student.user)
            print(student.instructor)
            print(student.user.id)
        print(student_list)
        return render_template('grades.html', student_list=student_list, assignments_by_student=assignments_by_student)
    
    assignments = Assignment.query.filter_by(student_id=session['id']).order_by(Assignment.number).all()
    if request.method == 'POST':
        # Process the remark form submission
        assignment_num = request.form['assignmentId']
        requested_grade = request.form['grade']
        description = request.form['description']
        
        # Update assignment in the database
        assignment = assignments[int(assignment_num)-1]
        assignment.regrade_requested = True
        assignment.requested_new_grade = requested_grade
        assignment.description = description
        
        db.session.commit()
        
        # Redirect to avoid form resubmission
        return redirect(url_for('grades'))
    return render_template('grades.html', assignments=assignments)

@app.route('/announcements')
def announcements():
    if not login_status():
        return redirect(url_for('index'))
    return render_template('announcements.html')

@app.route('/courseteam')
def courseteam():
    if not login_status():
        return redirect(url_for('index'))
    instructor_list = db.session.query(User.username)\
                                .join(Instructor)\
                                .with_entities(User.username)\
                                .all()
    instructor_list = [username for username, in instructor_list]
    return render_template('courseteam.html', instructor_list=instructor_list)

@app.route('/modules')
def modules():
    if not login_status():
        return redirect(url_for('index'))
    return render_template('modules.html')

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if not login_status():
        return redirect(url_for('index'))
    if session['type'] == 'instructor':
        
        responses = {'question_1': [], 'question_2': [], 'question_3': [], 'question_4': []}

        # Query the database to get distinct non-empty values for each question
        for question_num in range(1, 5):
            question_attr = getattr(Feedback, f"question_{question_num}")
            distinct_questions = Feedback.query.filter(
                Feedback.instructor_id == session['id'],
                question_attr != ''
            ).with_entities(question_attr).distinct().all()
            for feedback in distinct_questions:
                responses[f'question_{question_num}'].append(feedback[0])

        return render_template('feedback.html', responses=responses)

    instructor_list = db.session.query(User.username)\
                                .join(Instructor)\
                                .with_entities(User.username)\
                                .all()
    instructor_list = [username for username, in instructor_list]

    if request.method == 'POST':
        instruct_id = db.session.query(User.id)\
                .join(Instructor)\
                .filter(User.username == request.form['instructor'])\
                .scalar()
        feedback = Feedback(
            instructor_id=instruct_id,
            question_1=request.form['question1'],
            question_2=request.form['question2'],
            question_3=request.form['question3'],
            question_4=request.form['question4'],
            submitted=True
        )
        db.session.add(feedback)
        db.session.commit()
        session['feedback'] = True
        flash("Thank you for your submission! We value your feedback!")
        flashed_messages = get_flashed_messages()

    return render_template('feedback.html', instructor_list=instructor_list)

@app.route('/grades/<string:username>', methods=['GET', 'POST'])
def student_grades(username):
    if not login_status():
        return redirect(url_for('index'))
    student = Student.query.join(User).filter(User.username == username).first()
    assignments = Assignment.query.filter_by(student_id=student.student_id).all()
    print(assignments)
    names = ['Relational Algebra and SQL', 'HTML/CSS and Flask', 'HTML/CSS, JS, SQL and Flask', 'Labs', 'Midterm', 'Exam']
    
    if request.method == 'POST':
        num = request.form['assignment-number']
        grade = request.form['grade']
        print(num)
        print(grade)
        new_assignment = Assignment.query.filter_by(student_id=student.student_id, number=num).first()
        new_assignment.grade = grade
        new_assignment.description = ""
        new_assignment.regrade_requested = False
        # new_assignment = assignments.filter_by(assignment_number = num)
        # new_assignment.grade = grade
        print(new_assignment)
        db.session.commit()

    return render_template('student-grades.html', student=student, assignments=assignments, names=names)

if __name__ == '__main__':
    app.run(debug=True)
