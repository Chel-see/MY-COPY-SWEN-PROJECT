from App.models import Staff, Position, Student, Shortlist, Application
from App.database import db
from App.controllers.shortlist import get_eligible_students


# 1. CREATE STAFF ACCOUNT 
def create_staff(username, password, email, phone_number=None):
    staff = Staff(username, password, email, phone_number)
    db.session.add(staff)
    db.session.commit()
    return staff.get_json(), 201


# 2. GET STAFF BY ID
def get_staff(staff_id):
    staff = Staff.query.filter_by(id=staff_id).first()
    if not staff:
        return {"error": "Staff not found"}, 404
    return staff.get_json(), 200


# 3. LIST ALL STAFF MEMBERS
def get_all_staff():
    staff_list = Staff.query.all()
    return [s.get_json() for s in staff_list], 200


# 4. VIEW ELIGIBLE STUDENTS FOR A POSITION
def staff_view_eligible_students(staff_id, position_id):

    staff = Staff.query.filter_by(id=staff_id).first()
    if not staff:
        return {"error": "Staff not found"}, 404

    return get_eligible_students(position_id)   # returns list + code


# 5. STAFF SHORTLISTS A STUDENT
def staff_shortlist_student(staff_id, student_id, position_id):

    staff = Staff.query.filter_by(id=staff_id).first()
    student = Student.query.filter_by(id=student_id).first()
    position = Position.query.filter_by(id=position_id).first()

    if not staff or not student or not position:
        return {"error": "Staff, student, or position not found"}, 404

    # Student must have an application entry (auto-created by Position controller)
    app = Application.query.filter_by(student_id=student_id, position_id=position_id).first()
    if not app:
        return {"error": "Student is not eligible or never matched to this position"}, 400

    # Check eligibility
    eligible_list, _ = get_eligible_students(position_id)
    eligible_ids = [e["student_id"] for e in eligible_list]

    if student_id not in eligible_ids:
        return {"error": "Student does not meet GPA requirement"}, 400

    # Prevent duplicate shortlist
    existing = Shortlist.query.filter_by(student_id=student_id, position_id=position_id).first()
    if existing:
        return {"error": "Student already shortlisted"}, 400

    # Create shortlist entry
    shortlist = Shortlist(
        student_id=student_id,
        position_id=position_id,
        staff_id=staff_id
    )
    db.session.add(shortlist)

    # Update application table
    app.setStatus("shortlisted")

    db.session.commit()
    return shortlist.toJSON(), 201


# 6. STAFF SHORTLIST HISTORY
def staff_shortlist_history(staff_id):

    staff = Staff.query.filter_by(id=staff_id).first()
    if not staff:
        return {"error": "Staff not found"}, 404

    entries = Shortlist.query.filter_by(staff_id=staff_id).all()
    return [e.toJSON() for e in entries], 200
