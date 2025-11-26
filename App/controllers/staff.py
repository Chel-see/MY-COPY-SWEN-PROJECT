from App.models import Staff, Position, Student, Shortlist, Application
from App.database import db
from App.controllers.shortlist import get_eligible_students


# 1. CREATE STAFF ACCOUNT 
def create_staff(username, password, email, phone_number=None):
    staff = Staff(username, password, email, phone_number)
    db.session.add(staff)
    db.session.commit()
    return staff


# 2. GET STAFF BY ID
def get_staff(staff_id):
    staff = Staff.query.filter_by(id=staff_id).first()
    if not staff:
        return None
    return staff


# 3. LIST ALL STAFF MEMBERS
def get_all_staff():
    return Staff.query.all()


# 4. VIEW ELIGIBLE STUDENTS FOR A POSITION
def staff_view_eligible_students(staff_id, position_id):

    staff = Staff.query.filter_by(id=staff_id).first()
    if not staff:
        return None

    return get_eligible_students(position_id) 


# 5. STAFF SHORTLISTS A STUDENT
def staff_shortlist_student(staff_id, student_id, position_id):

    staff = Staff.query.get(staff_id)
    student = Student.query.get(student_id)
    position = Position.query.get(position_id)

    if not staff or not student or not position:
        return None

    # Student must have an application entry (auto-created by Position controller)
    app = Application.query.filter_by(student_id=student_id, position_id=position_id).first()
    if not app:
        return None
    
    # Must be eligible
    eligible_students = get_eligible_students(position_id)
    eligible_ids = [s.id for s in eligible_students]

    if student_id not in eligible_ids:
        return None

    # Prevent duplicate shortlist
    existing = Shortlist.query.filter_by(student_id=student_id, position_id=position_id).first()
    if existing:
        return None

    # Create shortlist entry
    shortlist = Shortlist(
        student_id=student_id,
        position_id=position_id,
        staff_id=staff_id
    )
    db.session.add(shortlist)

    # Update application table
    shortlist.setStatus("shortlisted")

    db.session.commit()
    return shortlist


# 6. STAFF SHORTLIST HISTORY
def staff_shortlist_history(staff_id):

    staff = Staff.query.get(staff_id)
    if not staff:
        return None

    return Shortlist.query.filter_by(staff_id=staff_id).all()
