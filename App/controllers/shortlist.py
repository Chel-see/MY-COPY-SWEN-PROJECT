from App.models import Shortlist, Position, Staff, Student, Application
from App.database import db


# 1. GET ELIGIBLE STUDENTS FOR A POSITION
def get_eligible_students(position_id):

    position = Position.query.filter_by(id=position_id).first()
    if not position:
        return None

    gpa_required = position.gpa_requirement

    # All existing Application entries for this position
    applications = Application.query.filter_by(position_id=position_id).all()

    eligible_students = []

    for app in applications:
        student = Student.query.filter_by(id=app.student_id).first()
        if not student:
            continue

        # GPA filter
        if gpa_required is None or student.gpa >= gpa_required:
            eligible_students.append(student)

    return eligible_students


# 2. GET ALL SHORTLISTS FOR A STUDENT
def get_shortlist_by_student(student_id):
    return Shortlist.query.filter_by(student_id=student_id).all()
    


# 3. GET ALL SHORTLISTS FOR A POSITION
def get_shortlist_by_position(position_id):
    return Shortlist.query.filter_by(position_id=position_id).all()
   


# 4. WITHDRAW A SHORTLIST ENTRY
def withdraw_shortlist(shortlist_id):

    shortlist = Shortlist.query.filter_by(id=shortlist_id).first()

    if not shortlist:
        return None

    # Mark as withdrawn
    shortlist.is_withdrawn = True

    # Update application state using parent's state machine
    shortlist.setStatus("withdrawn")

    db.session.commit()
    return shortlist


