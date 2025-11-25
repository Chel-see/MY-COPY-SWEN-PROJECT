from App.models import Shortlist, Position, Staff, Student, Application
from App.database import db


# 1. STAFF SHORTLISTS A STUDENT
def shortlist_student(staff_id, student_id, position_id):

    staff = Staff.query.filter_by(id=staff_id).first()
    student = Student.query.filter_by(id=student_id).first()
    position = Position.query.filter_by(id=position_id).first()

    if not staff or not student or not position:
        return {"error": "Staff, student, or position not found"}, 404

    # Check if application exists
    app = Application.query.filter_by(
        student_id=student_id,
        position_id=position_id
    ).first()

    if not app:
        return {"error": "Student has not applied for this position"}, 400

    # Prevent duplicate shortlisting
    existing = Shortlist.query.filter_by(
        student_id=student_id,
        position_id=position_id
    ).first()

    if existing:
        return {"error": "Student is already shortlisted"}, 400

    # Create shortlist entry
    shortlist = Shortlist(
        student_id=student_id,
        position_id=position_id,
        staff_id=staff_id,
        status="shortlisted"
    )

    db.session.add(shortlist)

    # Update APPLICATION state
    app.setStatus("shortlisted")

    db.session.commit()

    return shortlist.toJSON(), 201

# 2. GET ALL SHORTLISTS FOR A STUDENT
def get_shortlist_by_student(student_id):
    entries = Shortlist.query.filter_by(student_id=student_id).all()
    return [e.toJSON() for e in entries], 200


# 3. GET ALL SHORTLISTS FOR A POSITION
def get_shortlist_by_position(position_id):
    entries = Shortlist.query.filter_by(position_id=position_id).all()
    return [e.toJSON() for e in entries], 200
